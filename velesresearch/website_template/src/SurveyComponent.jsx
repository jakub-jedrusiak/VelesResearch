import { Model } from "survey-core";
import { Survey } from "survey-react-ui";
import "survey-core/survey.i18n";
import "survey-core/defaultV2.min.css";
import { json } from "./survey.js";
import * as SurveyCore from "survey-core";
import { nouislider } from "surveyjs-widgets";
import "nouislider/distribute/nouislider.css";
import { Converter } from "showdown";
import * as config from "./config.js";
import CSRFToken from "./csrf.js";
import registerCustomFunctions from "./customExpressionFunctions.js";

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
  if (!survey.getVariable("dateCompleted")) {
    const dateCompleted = new Date();
    survey.setVariable("dateCompleted", dateCompleted.toISOString());
  }

  const variables = {};
  for (const variable of survey.getVariableNames()) {
    if (survey?.calculatedValues.some( // Skip calculatedValues that are not included into results
      dict => (dict.name === variable || dict.name?.toLowerCase() === variable) && dict.includeIntoResult === false
    )) continue;
    variables[variable] = survey.getVariable(variable);
  }

  const URLparams = Object.fromEntries(new URLSearchParams(window.location.search));

  return Object.assign(
    {
      id: survey.participantID
    },
    survey.data,
    URLparams,
    variables
  );
}

async function handleResults(survey, completedHtml) {
  const result = createResults(survey);

  // Add scores to results
  if (survey.addScoreToResults === undefined || survey.addScoreToResults) {
    for (const question of survey.getAllQuestions()) {
      if (question.correctAnswer && question.selectedItem) {
        result[question.name + (survey.scoresSuffix || "_score")] = question.selectedItem.value === question.correctAnswer ? 1 : 0;
      }
    }
  }

  // Wait for reCAPTCHA to be ready and get token
  let siteKey = new URL(document.getElementById("recaptchaScript").src).searchParams.get("render");
  await new Promise(resolve => window.grecaptcha.ready(resolve));
  const token = await window.grecaptcha.execute(siteKey, { action: 'submit' });
  Object.assign(result, { "g-recaptcha-token": token });

  // send data to Django backend
  const requestHeaders = {
    method: "POST",
    headers: Object.assign(
      {
        "Content-Type": "application/json",
      },
      CSRFToken()
    ),
    body: JSON.stringify(result),
  };
  const url = window.location.pathname + "submit/";
  const response = await fetch(url, requestHeaders);

  if (response.ok) {
    document.getElementsByClassName("sd-completedpage")[0].innerHTML = completedHtml;
    document.getElementById("tryAgainDiv").style.display = "none";
    document.getElementById("tryAgainButton").disabled = true;
    return "OK";
  } else {
    document.getElementsByClassName("sd-completedpage")[0].innerHTML = `
        <div style="text-align: center">${SurveyCore.surveyLocalization.getString("savingDataError", survey.locale)}</div>
        <br>
        <div style="text-align: center; font-size: 3em; color: #CC0000; font-weight: bold">Error ${response.status}</div>
        <br>
        <div style="text-align: center; padding-bottom: 2em; font-size: 2em">${response.statusText}</div>
      `;
    document.getElementById("tryAgainDiv").style.display = "block";
    document.getElementById("tryAgainButton").disabled = false;
    return "Error";
  }
}

// {% customFunctions %}

// placeholder

// {% end customFunctions %}

registerCustomFunctions();

function SurveyComponent() {
  const survey = new Model(json);
  survey.participantID = MakeID(8);
  const dateStarted = new Date();

  document.documentElement.lang = survey.locale;
  const completedHtml = survey.completedHtml + "<br>";
  survey.completedHtml = '<div style="text-align: center; padding-bottom: 2em;"><div class="lds-dual-ring"></div></div>';
  document.getElementById("tryAgainButton").innerHTML = SurveyCore.surveyLocalization.getString("saveAgainButton", survey.locale);

  survey.setVariable("group", groupNumber(config.numberOfGroups));
  survey.setVariable("dateStarted", dateStarted.toISOString());

  document.getElementById("tryAgainButton").addEventListener("click", () => {
    if (survey.isCompleted) {
      document.getElementsByClassName("sd-completedpage")[0].innerHTML = '<div style="text-align: center; padding-bottom: 2em;"><div class="lds-dual-ring"></div></div>';
      document.getElementById("tryAgainDiv").style.display = "none";
      document.getElementById("tryAgainButton").disabled = true;
      handleResults(survey, completedHtml)
    }
  });

  survey.onAfterRenderSurvey.add((sender, options) => {
    document.body.style.setProperty("--sjs-general-backcolor-dim", document.getElementsByClassName("sd-root-modern")[0].style.getPropertyValue("--sjs-general-backcolor-dim"));
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

  // {% customCode %}

  // placeholder

  // {% end customCode %}

  survey.onComplete.add(sender => handleResults(sender, completedHtml));
  return <Survey model={survey} />;
}

export default SurveyComponent;
