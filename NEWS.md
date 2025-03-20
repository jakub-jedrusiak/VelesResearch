# Release notes

## future release

* Fixed a bug where nested objects were not included in the result.
* Fixed a bug causing `urlParameters` were not saved correctly.

## 0.5.0

* Added `imagePicker()` question type.
* `getJS()` now does not crash when it encounters regex escape sequences (e.g. `\d`).
* Veles now uses the default `completedHTML` setup, as the previous one had some problems with dynamic values.
* Changed the result structure, so the order of the answers is preserved.
* Additional changes to the website template to change the structure of the files.
* URL parameters added to the survey `UrlParameters` argument are now saved as variables before the survey is rendered.
* Adapted Veles to work with SurveyJS 2.0.0:
  * Technical changes
  * Question numbers are now hidden by default. They can be shown again using the `showQuestionNumbers` option.
  * Logo size is now `auto`x40px (instead of 300x200px) by default.
  * Images in `imagePicker()` now have max width and height of 3000px (instead of 400x266px) by default.
  * Renamed a series of arguments (see <https://surveyjs.io/stay-updated/release-notes/v2.0.0#obsolete-form-library-api>). Mainly:
    * `firstPageIsStarted` -> `firstPageIsStartPage`
    * `maxTimeToFinish` -> `timeLimit`
    * `maxTimeToFinishPage` -> `timeLimitPerPage`
    * `questionsOrder` -> `questionOrder`
    * `showTimerPanel` -> split into `showTimer` and `timerLocation`
    * `showTimerPanelMode` -> `timerInfoMode`
    * `hideNumber` -> `showNumber` (but note that now they are hidden by default)
    * `size` -> `inputSize`
    * `isAllRowRequired` -> `eachRowRequired`
    * `rowsOrder` -> `rowOrder`
    * `UrlParameters` -> `urlParameters`
* All the docs are now sorted properly.
* Added `showTimerOnlyWhenLimit` to automatically hide the timer on pages that do not have a time limit.
* Added `timeMinimum` for pages to allow for minimum time the user has to spend.

## 0.4.1

* Updated the `rowTitleWidth` documentation to point out that you need to also set `columnMinWidth` to change the relative width of the title column.
* Hotfix: Fixed a bug where `navigateToUrl` would fire even if the results were not saved. Now Veles uses SurveyJS's native Try Again button.

## 0.4.0

* Hot reloading now only reloads the survey, not the whole page.
* Added `UrlParameters` argument to the `Survey` class to specify what parameters should be saved in the database.
* Added `pauseBuild` arg to `SurveyModel.build()` to prevent the survey from being built when created.
* Added `surveyFromJson()` function to create a survey from a json file made with the visual creator.
* Themes have been implemented. See `themeFile` argument in the `SurveyModel` class.
* Imports in __init__.py are now explicit.
* Fixed the `monitorInput` property so it now works as expected.
* Added `botSalt()` function that can be put inside a question's title. It will generate a non-visible string that can still be copied and pasted. This can be used to detect GPT usage.

## 0.3.2

* Moved building code to a .ts file.
* Extensively changed the development server so building now happens only when invoked by the user and the window reloads automatically when the survey is updated.
* The node_modules folder is not copied even if it exists in the website_template folder for any reason.

## 0.3.0

* Added a functional `index.css` file.
* Matrix questions work as expected. Added the `matrixDropdown` question type.
* Surveys, pages and panels are now iterable so they can be unpacked with the `*` operator.
* Moved from yarn and webpack to bun, esbuild and hono which makes everything much faster.
* Repleced the `createStructure` and `buildForProduction` args and methods (`survey()`) with a single `build()` as building is now quick enough to be done on the fly.

## 0.2.0

* `yarn` is now called directly through `subprocess.run()`. This should resolve some problems in Windows. `pynpm` dependency has been removed.
* Added `customCode` and `customFunctions` arguments for direct javascript use. Also added `getJS()` helper to get the code from a file.
* Now markdown and html in question titles are honored by default.
* Added reCAPTCHA v3 protection by default.
* Added `monitorInput` property allowing for couting the number of key presses and time elapsed on textual questions. Can be used to check if the answer was pasted.
