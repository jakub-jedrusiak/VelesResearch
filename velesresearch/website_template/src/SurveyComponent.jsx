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
  // Create results object
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
          dict.includeIntoResult === false
      )
    )
      continue;
    variables[variable] = survey.getVariable(variable);
  }

  return Object.assign(
    {
      id: survey.participantID,
    },
    survey.data,
    variables
  );
}

async function handleResults(survey) {
  const result = createResults(survey);

  // Add scores to results
  if (survey.addScoreToResults === undefined || survey.addScoreToResults) {
    for (const question of survey.getAllQuestions()) {
      if (question.correctAnswer && question.selectedItem) {
        result[question.name + (survey.scoresSuffix || "_score")] =
          question.selectedItem.value === question.correctAnswer ? 1 : 0;
      }
    }
  }

  // Wait for reCAPTCHA to be ready and get token
  let siteKey = new URL(
    document.getElementById("recaptchaScript").src
  ).searchParams.get("render");
  let recaptchaToken;
  if (siteKey) {
    await new Promise((resolve) => window.grecaptcha.ready(resolve));
    recaptchaToken = await window.grecaptcha.execute(siteKey, {
      action: "submit",
    });
  } else {
    recaptchaToken = NaN;
  }
  Object.assign(result, { "g-recaptcha-token": recaptchaToken });

  // Gather keys for ordering
  const firstColumns = ["id", "date_started", "date_completed", "group"];

  const questionNames = survey
    .getAllQuestions(false, false, true)
    .map((x) => x?.name || null)
    .filter((x) => x !== null);

  const varNames = survey
    .getVariableNames()
    .filter((x) => !firstColumns.includes(x));

  const orderKeys = [...firstColumns, ...questionNames, ...varNames];

  const remainingKeys = Object.keys(result)
    .filter((x) => !orderKeys.includes(x))
    .sort((a, b) =>
      a.localeCompare(b, undefined, { numeric: true, sensitivity: "base" })
    );

  // send data to Django backend
  const requestHeaders = {
    method: "POST",
    headers: Object.assign(
      {
        "Content-Type": "application/json",
      },
      CSRFToken()
    ),
    body: JSON.stringify(result, [...orderKeys, ...remainingKeys]),
  };
  const url = window.location.pathname + "submit/";
  const response = await fetch(url, requestHeaders);

  return response.ok;
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
            totalFocusedTime + elapsedTime
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
    name: "UrlParameters",
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
  if (survey.UrlParameters) {
    survey.UrlParameters.forEach((param) => {
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
      backgroundColor
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

  // Input monitoring setup
  survey.onAfterRenderQuestion.add((sender, options) => {
    if (options.question.getPropertyValue("monitorInput", false))
      setupTracking(sender, options.question.name);
  });

  // {% customCode %}

  // placeholder

  // {% end customCode %}

  survey.onComplete.add(async (sender, options) => {
    options.showSaveInProgress();
    const responseOK = await handleResults(sender);
    responseOK ? options.showSaveSuccess() : options.showSaveError();
  });
  return <Survey model={survey} />;
}

export default SurveyComponent;
