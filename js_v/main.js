import { Parser } from "./compiler/parser.js";
import { tokenize } from "./compiler/lexer.js";

document.getElementById("compileBtn").addEventListener("click", compileCode);
const codeInput = document.getElementById("codeInput");
const outputElement = document.getElementById("output");
outputElement.style.display = "none";


function compileCode() {
  if (!codeInput || !outputElement) {
    console.error("Input or output element not found in DOM.");
    return;
  }

  const code = codeInput.value.trim();
  if (code === "") {
    outputElement.style.display = "none";
    outputElement.textContent = "There is no code detected.";
    return;
  } else {
    outputElement.style.display = "block";
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
