# Release notes

## future release

* Added a functional `index.css` file.
* Matrix questions work as expected. Added the `matrixDropdown` question type.

## 0.2.0

* `yarn` is now called directly through `subprocess.run()`. This should resolve some problems in Windows. `pynpm` dependency has been removed.
* Added `customCode` and `customFunctions` arguments for direct javascript use. Also added `getJS()` helper to get the code from a file.
* Now markdown and html in question titles are honored by default.
* Added reCAPTCHA v3 protection by default.
* Added `monitorInput` property allowing for couting the number of key presses and time elapsed on textual questions. Can be used to check if the answer was pasted.
