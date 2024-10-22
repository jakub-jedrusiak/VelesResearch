# Release notes

## future release

* Hot reloading now only reloads the survey, not the whole page.

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
