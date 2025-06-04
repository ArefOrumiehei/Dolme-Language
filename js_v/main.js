import { Parser } from "./compiler/parser.js";
import { tokenize } from "./compiler/lexer.js";

document.getElementById("compileBtn").addEventListener("click", compileCode);

function compileCode() {
  const codeInput = document.getElementById("codeInput");
  const outputElement = document.getElementById("output");

  if (!codeInput || !outputElement) {
    console.error("Input or output element not found in DOM.");
    return;
  }

  const code = codeInput.value.trim();
  if (code === "") {
    outputElement.textContent = "There is no code detected.";
    return;
  }

  try {
    const tokens = tokenize(code);
    const parser = new Parser(tokens);
    const result = parser.parse();
    outputElement.textContent = result.join("\n");
  } catch (err) {
    outputElement.textContent = `Error: ${err.message}`;
  }
}
