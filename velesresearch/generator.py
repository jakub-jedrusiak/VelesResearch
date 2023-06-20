"Functions for generating survey package."
from __future__ import annotations
import os
from importlib.metadata import version
from json import dump
from pathlib import Path
from pynpm import NPMPackage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .structure import Survey


def install_npm_deps(path: str | Path = os.getcwd()) -> None:
    """Install npm dependencies for VelesResearch."""

    npm_dependencies = {
        "name": "veles-survey",
        "private": True,
        "version": version("velesresearch"),
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "tsc && vite build",
            "lint": "eslint src --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
            "preview": "vite preview",
        },
        "dependencies": {
            "@json2csv/plainjs": "^7.0.1",
            "file-saver": "^2.0.5",
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "survey-react-ui": "^1.9.92",
        },
        "devDependencies": {
            "@types/file-saver": "^2.0.5",
            "@types/react": "^18.0.37",
            "@types/react-dom": "^18.0.11",
            "@typescript-eslint/eslint-plugin": "^5.59.0",
            "@typescript-eslint/parser": "^5.59.0",
            "@vitejs/plugin-react": "^4.0.0",
            "eslint": "^8.38.0",
            "eslint-plugin-react-hooks": "^4.6.0",
            "eslint-plugin-react-refresh": "^0.3.4",
            "typescript": "^5.0.2",
            "vite": "^4.3.9",
        },
    }

    if isinstance(path, str):
        path = Path(path)
    path = path / "package.json"
    with open(path, "w", encoding="utf-8") as package_json:
        dump(npm_dependencies, package_json)

    NPMPackage(path).install()


def generate_survey(Survey_object: "Survey", path: str | Path = os.getcwd()) -> None:
    "Saves survey to survey.js file"

    if isinstance(path, str):
        path = Path(path)

    # package.json
    os.makedirs(path / "src", exist_ok=True)
    os.makedirs(path / "public", exist_ok=True)

    # App.tsx
    with open(path / "src" / "App.tsx", "w", encoding="utf-8") as app_tsx_file:
        App_tsx = """import SurveyComponent from "./SurveyComponent";

function App() {
  return <SurveyComponent />
}

export default App;"""
        app_tsx_file.write(App_tsx)

    # index.css
    with open(path / "src" / "index.css", "w", encoding="utf-8") as index_css_file:
        index_css = ""
        index_css_file.write(index_css)

    # main.tsx
    with open(path / "src" / "main.tsx", "w", encoding="utf-8") as main_tsx_file:
        main_tsx = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""
        main_tsx_file.write(main_tsx)

    # survey.ts
    with open(path / "src" / "survey.ts", "w", encoding="utf-8") as survey_js:
        survey_js.write("export const json = ")

    with open(path / "src" / "survey.ts", "a", encoding="utf-8") as survey_js:
        from .structure import SurveyEncoder

        dump(Survey_object, survey_js, cls=SurveyEncoder)

    # SurveyComponent.tsx
    with open(
        path / "src" / "SurveyComponent.tsx", "w", encoding="utf-8"
    ) as survey_component_file:
        SurveyComponent = """import { Model } from "survey-core";
import { Survey } from "survey-react-ui";
import "survey-core/defaultV2.min.css";
import "./index.css";
import { json } from "./survey.ts";
import { Parser } from '@json2csv/plainjs';
import { saveAs } from "file-saver";

function MakeID(length: number) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
}

function SurveyComponent() {
    const survey = new Model(json);
    survey.onComplete.add((sender) => {
        const result = Object.assign({ id: MakeID(8) }, sender.data);
        console.log(result)
        const parser = new Parser({ delimiter: ';' });
        const csvData = parser.parse(result);
        const blob = new Blob([csvData], { type: "text/csv;charset=utf-8;" });
        saveAs(blob, "data.csv");
    });
    return (<Survey model={survey} />);
}

export default SurveyComponent;"""
        survey_component_file.write(SurveyComponent)

    # vite-env.d.ts
    with open(path / "src" / "vite-env.d.ts", "w", encoding="utf-8") as vite_env_file:
        vite_env_d_ts = '/// <reference types="vite/client" />\n'
        vite_env_file.write(vite_env_d_ts)

    # index.html
    with open(path / "index.html", "w", encoding="utf-8") as index_html_file:
        index_html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{Survey_object.label}</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>"""
        index_html_file.write(index_html)

    # .eslintrc.cjs
    with open(path / ".eslintrc.cjs", "w", encoding="utf-8") as eslintrc_cjs_file:
        eslintrc_cjs = """module.exports = {
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: { ecmaVersion: 'latest', sourceType: 'module' },
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': 'warn',
  },
}"""
        eslintrc_cjs_file.write(eslintrc_cjs)

    # .gitignore
    with open(path / ".gitignore", "w", encoding="utf-8") as gitignore_file:
        gitignore = """# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

node_modules
dist
dist-ssr
*.local

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?
"""

        gitignore_file.write(gitignore)

    # tsconfig.json
    with open(path / "tsconfig.json", "w", encoding="utf-8") as tsconfig_json_file:
        tsconfig_json = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
"""
        tsconfig_json_file.write(tsconfig_json)

    # tsconfig.node.json
    with open(
        path / "tsconfig.node.json", "w", encoding="utf-8"
    ) as tsconfig_node_json_file:
        tsconfig_node_json = """{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
"""
        tsconfig_node_json_file.write(tsconfig_node_json)

    # vite.config.ts
    with open(path / "vite.config.ts", "w", encoding="utf-8") as vite_config_ts_file:
        vite_config_ts = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})
"""
        vite_config_ts_file.write(vite_config_ts)


def build_survey(path: str | Path = os.getcwd()) -> None:
    """Builds survey package."""

    if isinstance(path, str):
        path = Path(path)

    NPMPackage(path).run_script("build")
