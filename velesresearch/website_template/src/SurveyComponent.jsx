import { Model } from "survey-core";
import { Survey } from "survey-react-ui";
import "survey-core/survey.i18n";
import "survey-core/defaultV2.min.css";
import { json } from "./survey.js";
import * as SurveyCore from "survey-core";
import { nouislider } from "surveyjs-widgets";
import "nouislider/distribute/nouislider.css";
import * as config from "./config.js";
import CSRFToken from "./csrf.js";

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
  for (const variable in survey.getVariableNames()) {
    variables[variable] = survey.getVariable(variable);
  }

  const URLparams = Object.fromEntries(new URLSearchParams(window.location.search));

  return Object.assign(
    {
      id: MakeID(8)
    },
    survey.data,
    URLparams,
    variables
  );
}

async function handleResults(survey, completedHtml) {
  const result = createResults(survey);
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

  let response = await fetch(url, requestHeaders);
  if (response.ok) {
    document.getElementsByClassName("sd-completedpage")[0].innerHTML = completedHtml
    document.getElementById("tryAgainDiv").style.display = "none";
    document.getElementById("tryAgainButton").disabled = true;
    return "OK";
  } else {
    document.getElementsByClassName("sd-completedpage")[0].innerHTML = `<div style="text-align: center">${SurveyCore.surveyLocalization.getString("savingDataError", survey.locale)}</div><br><div style="text-align: center; font-size: 3em; color: #CC0000; font-weight: bold">Error ${response.status}</div><br><div style="text-align: center; padding-bottom: 2em; fint-size: 2em">${response.statusText}</div>`;
    document.getElementById("tryAgainDiv").style.display = "block";
    document.getElementById("tryAgainButton").disabled = false;
    return "Error";
  }
}

function SurveyComponent() {
  const survey = new Model(json);
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

  survey.onComplete.add(sender => handleResults(sender, completedHtml));
  return <Survey model={survey} />;
}

export default SurveyComponent;
