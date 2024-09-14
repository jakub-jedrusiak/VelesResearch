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

function SurveyComponent() {
  const survey = new Model(json);
  const date_started = new Date();

  document.documentElement.lang = survey.locale;
  const completedHtml = survey.completedHtml.valueOf();
  survey.completedHtml = '<div style="text-align: center; padding-bottom: 2em"><div class="lds-dual-ring"></div></div>';

  survey.setVariable("group", groupNumber(config.numberOfGroups));
  survey.setVariable("date_started", date_started.toISOString());

  survey.onComplete.add((sender) => {
    const date_completed = new Date();
    survey.setVariable("date_completed", date_completed.toISOString());

    const variables = {};
    for (const variable in survey.getVariableNames()) {
      variables[variable] = survey.getVariable(variable);
    }

    const URLparams = Object.fromEntries(new URLSearchParams(window.location.search));

    const result = Object.assign(
      {
        id: MakeID(8)
      },
      sender.data,
      URLparams,
      variables
    );

    // send data to Django backend
    const postData = {
      method: "POST",
      headers: Object.assign(
        {
          "Content-Type": "application/json",
        },
        CSRFToken()
      ),
      body: JSON.stringify(result),
    }
    fetch(window.location.pathname + "submit/", postData)
      .then(response => {
        if (response.ok) {
          document.getElementsByClassName("sd-completedpage")[0].innerHTML = completedHtml;
        } else {
          fetch(window.location.pathname + "submit/", postData)
            .then(response => {
              if (response.ok) {
                document.getElementsByClassName("sd-completedpage")[0].innerHTML = completedHtml;
              } else {
                document.getElementsByClassName("sd-completedpage")[0].innerHTML = `<div style="text-align: center">Results not saved</div><br><div style="text-align: center; font-size: 3em; color: #CC0000; font-weight: bold">Error ${response.status}</div><br><div style="text-align: center; padding-bottom: 2em; fint-size: 2em">${response.statusText}</div>`;
              }
            });
        }
      })
  });
  return <Survey model={survey} />;
}

export default SurveyComponent;
