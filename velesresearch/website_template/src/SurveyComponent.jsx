import { Model } from "survey-core";
import { Survey } from "survey-react-ui";
import "survey-core/survey.i18n";
import "survey-core/survey-core.min.css";
import { json } from "./survey.js";
import * as SurveyCore from "survey-core";
import { nouislider } from "surveyjs-widgets";
import "nouislider/distribute/nouislider.css";
import { Converter } from "showdown";
import CSRFToken from "./csrf.ts";
import registerCustomFunctions from "./customExpressionFunctions.js";
import * as theme from "./theme.json";

nouislider(SurveyCore);

function MakeID(length) {
  let result = "";
  const characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  const charactersLength = characters.length;
  let counter = 0;
  while (counter < length) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
    counter += 1;
  }
  return result;
}

function groupNumber(max) {
  return Math.floor(Math.random() * max + 1);
}

function createResults(survey) {
  if (!survey.getVariable("date_completed")) {
    const dateCompleted = new Date();
    survey.setVariable("date_completed", dateCompleted.toISOString());
  }

  const variables = {};
  for (const variable of survey.getVariableNames()) {
    if (
      survey?.calculatedValues.some(
        // Skip calculatedValues that are not included into results
        (dict) =>
          (dict.name === variable || dict.name?.toLowerCase() === variable) &&
          dict.includeIntoResult === false,
      )
    )
      continue;
    variables[variable] = survey.getVariable(variable);
  }

  const standard = [
    "id",
    "date_started",
    "date_completed",
    "g_recaptcha_score",
    "group",
  ];
  const questionNames = survey
    .getAllQuestions(false, false, true)
    .map((question) => question?.name)
    .filter((name) => name);

  const result = { id: survey.participantID };
  ["date_started", "date_completed", "group"].forEach((name) => {
    const value = survey.getVariable(name);
    if (value !== undefined) result[name] = value;
  });
  Object.assign(result, variables, survey.data);
  result._labelStructure = {
    standard,
    variables: Object.keys(variables).filter(
      (name) => !standard.includes(name),
    ),
    questions: questionNames,
  };
  return result;
}

async function handleResults(survey) {
  const result = createResults(survey);

  // Add scores to results
  if (survey.addScoreToResults === undefined || survey.addScoreToResults) {
    for (const question of survey.getAllQuestions()) {
      if (question.correctAnswer && question.selectedItem) {
        const scoreName = question.name + (survey.scoresSuffix || "_score");
        result[scoreName] =
          question.selectedItem.value === question.correctAnswer ? 1 : 0;
        if (!result._labelStructure.questions.includes(scoreName))
          result._labelStructure.questions.push(scoreName);
      }
    }
  }

  // reCAPTCHA is optional: never block or reject an otherwise valid response.
  const recaptchaScript = document.getElementById("recaptchaScript");
  const siteKey = recaptchaScript
    ? new URL(recaptchaScript.src).searchParams.get("render")
    : null;
  if (siteKey && window.grecaptcha) {
    try {
      const recaptchaToken = await Promise.race([
        (async () => {
          await new Promise((resolve) => window.grecaptcha.ready(resolve));
          return window.grecaptcha.execute(siteKey, { action: "submit" });
        })(),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error("reCAPTCHA timed out")), 5000),
        ),
      ]);
      Object.assign(result, { "g-recaptcha-token": recaptchaToken });
    } catch (error) {
      console.warn("reCAPTCHA failed; submitting without a token", error);
    }
  }

  // send data to Django backend
  const requestHeaders = {
    method: "POST",
    headers: Object.assign(
      {
        "Content-Type": "application/json",
      },
      CSRFToken(),
    ),
    body: JSON.stringify(result),
  };
  const url = window.location.pathname + "submit/";
  const response = await fetch(url, requestHeaders);
  const responseData = await response.json().catch(() => null);

  // Only redirect after the server explicitly confirms a committed save.
  return response.ok && responseData?.saved === true;
}

// Input monitoring function
function setupTracking(survey, questionName) {
  const textboxId = survey.getQuestionByName(questionName).id + "i";
  const setupTextboxEvents = () => {
    const textbox = document.getElementById(textboxId);

    if (!textbox) return; // Return if the textbox is not yet available in the DOM

    // Retrieve previously stored values
    let totalFocusedTime =
      parseInt(survey.getVariable(`${questionName}_time`), 10) || 0;
    let keystrokeCount =
      parseInt(survey.getVariable(`${questionName}_keystrokes`), 10) || 0;
    let timerInterval = null;
    let startTime = 0; // Start time when focused

    // Start the timer
    const startTimer = () => {
      if (!timerInterval) {
        startTime = Date.now(); // Record the time when focus starts
        timerInterval = setInterval(() => {
          const elapsedTime = Math.floor((Date.now() - startTime) / 1000);
          survey.setVariable(
            `${questionName}_time`,
            totalFocusedTime + elapsedTime,
          );
        }, 1000); // Update every second
      }
    };

    // Stop the timer and update the total time
    const stopTimer = () => {
      if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
        totalFocusedTime += Math.floor((Date.now() - startTime) / 1000); // Add elapsed time to total
        survey.setVariable(`${questionName}_time`, totalFocusedTime);
      }
    };

    // Count keystrokes only when focused
    const countKeystrokes = (event) => {
      if (event.isTrusted && textbox === document.activeElement) {
        // Ensure the event is a valid user input
        keystrokeCount++;
        survey.setVariable(`${questionName}_keystrokes`, keystrokeCount);
      }
    };

    // Add event listeners for focus, blur, and keystrokes
    textbox.addEventListener("focus", startTimer);
    textbox.addEventListener("blur", stopTimer);
    textbox.addEventListener("keydown", countKeystrokes);
  };

  // Watch for the textbox being added back to the DOM
  const observeDOMChanges = () => {
    const container = document.getElementById("root");

    // MutationObserver to detect when the textbox is added back to the DOM
    const observer = new MutationObserver(() => {
      const textbox = document.getElementById(textboxId);
      if (textbox) {
        setupTextboxEvents(); // Reattach the event listeners once the textbox exists
      }
    });

    // Start observing for DOM changes
    observer.observe(container, { childList: true, subtree: true });

    // Initial setup if the textbox is already in the DOM
    setupTextboxEvents();
  };

  observeDOMChanges(); // Begin observing and setup tracking
}

function formatTime(timeInSeconds) {
  const minutes = Math.floor(timeInSeconds / 60);
  const seconds = timeInSeconds % 60;
  return `${minutes}:${seconds.toString().padStart(2, "0")}`;
}

function timerSubtraction(timerString) {
  const [minutes, seconds] = timerString.split(":").map(Number);

  const remainingSecondsTotal = minutes * 60 + seconds - 1;
  if (remainingSecondsTotal <= 0) {
    return "0:00";
  }
  return formatTime(remainingSecondsTotal);
}

// {% customFunctions %}

// placeholder

// {% end customFunctions %}

registerCustomFunctions();

function SurveyComponent() {
  SurveyCore.Serializer.addProperty("question", {
    name: "monitorInput",
    type: "boolean",
  });
  SurveyCore.Serializer.addProperty("survey", {
    name: "numberOfGroups",
    type: "number",
    default: 1,
  });
  SurveyCore.Serializer.addProperty("survey", {
    name: "urlParameters",
  });
  SurveyCore.Serializer.addProperty("survey", {
    name: "showTimerOnlyWhenLimit:boolean",
    default: false,
  });
  SurveyCore.Serializer.addProperty("page", {
    name: "timeMinimum:number",
    default: 0,
  });

  const survey = new Model(json);
  survey.participantID = MakeID(8);
  const dateStarted = new Date();

  survey.applyTheme(theme);

  document.documentElement.lang = survey.locale;

  if (survey.numberOfGroups > 1) {
    survey.setVariable("group", groupNumber(survey.numberOfGroups));
  }
  survey.setVariable("date_started", dateStarted.toISOString());

  const URLparams = new URLSearchParams(window.location.search);
  if (survey.urlParameters) {
    survey.urlParameters.forEach((param) => {
      const value = URLparams.get(param);
      if (value !== null) {
        survey.setVariable(param, value);
      }
    });
  }

  survey.onAfterRenderSurvey.add((sender, options) => {
    const backgroundColor = document
      .getElementsByClassName("sd-root-modern")[0]
      .style.getPropertyValue("--sjs-general-backcolor-dim");
    document.body.style.setProperty(
      "--sjs-general-backcolor-dim",
      backgroundColor,
    );
    document
      .querySelector("footer")
      .style.setProperty("--sjs-general-backcolor-dim", backgroundColor);
  });

  // Markdown formatting
  const converter = new Converter();
  survey.onTextMarkdown.add(function (survey, options) {
    // Convert Markdown to HTML
    let str = converter.makeHtml(options.text);
    // Remove root paragraphs <p></p>
    str = str.substring(3);
    str = str.substring(0, str.length - 4);
    // Set HTML markup to render
    options.html = str;
  });

  // Timer only on pages with the time limit
  if (survey.showTimerOnlyWhenLimit) {
    survey.onCurrentPageChanging.add((sender, options) => {
      if (options.newCurrentPage.timeLimit) {
        survey.setPropertyValue("showTimer", true);
        survey.startTimer();
      } else {
        survey.setPropertyValue("showTimer", false);
        survey.stopTimer();
      }
    });
  }

  // Input monitoring setup
  survey.onAfterRenderQuestion.add((sender, options) => {
    if (options.question.getPropertyValue("monitorInput", false))
      setupTracking(sender, options.question.name);
  });

  // Time minimum setup
  // survey-core 3.x renders nav button labels from locTitle (bound to pageNextText/completeText),
  // not from Action.title - setting .title directly is silently ignored by the UI
  let originalNextButtonText = null;
  survey.onCurrentPageChanging.add(function (sender, options) {
    if (options.newCurrentPage.timeMinimum) {
      const isLastPage =
        options.newCurrentPage.name === survey.pages.at(-1).name;
      const nextButton = isLastPage
        ? survey.navigationBar.getActionById("sv-nav-complete")
        : survey.navigationBar.getActionById("sv-nav-next");
      nextButton.innerCss += " override-opacity-for-time-minimum";
      originalNextButtonText = isLastPage
        ? survey.completeText
        : survey.pageNextText;
      nextButton.enabled = false;
      const countdownText = formatTime(options.newCurrentPage.timeMinimum);
      if (isLastPage) survey.completeText = countdownText;
      else survey.pageNextText = countdownText;
      survey.startTimer();
    }
  });

  survey.onTimerTick.add(() => {
    if (!survey.currentPage?.timeMinimum || originalNextButtonText === null)
      return;
    const isLastPage = survey.isLastPage;
    const nextButton = isLastPage
      ? survey.navigationBar.getActionById("sv-nav-complete")
      : survey.navigationBar.getActionById("sv-nav-next");
    const currentText = isLastPage ? survey.completeText : survey.pageNextText;
    if (currentText === originalNextButtonText) return;
    const updatedText = timerSubtraction(currentText);
    if (isLastPage) survey.completeText = updatedText;
    else survey.pageNextText = updatedText;
    if (updatedText === "0:00") {
      if (isLastPage) survey.completeText = originalNextButtonText;
      else survey.pageNextText = originalNextButtonText;
      nextButton.innerCss = nextButton.innerCss.replace(
        " override-opacity-for-time-minimum",
        "",
      );
      nextButton.enabled = true;
      originalNextButtonText = null;
    }
  });

  // {% customCode %}

  // placeholder

  // {% end customCode %}

  survey.onComplete.add(async (sender, options) => {
    options.showSaveInProgress();
    try {
      const responseOK = await handleResults(sender);
      responseOK ? options.showSaveSuccess() : options.showSaveError();
    } catch (error) {
      console.error("Could not save survey response", error);
      options.showSaveError();
    }
  });
  return <Survey model={survey} />;
}

export default SurveyComponent;
