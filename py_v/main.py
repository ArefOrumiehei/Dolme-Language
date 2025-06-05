from compiler.lexer import tokenize
from compiler.parser import Parser
from helpers.colorize import colorize

with open("./py_v/input.txt", "r") as f:
    code = f.read()

print(colorize("----------------------------Lexer--------------------------------", "lightblue"))
tokens = tokenize(code)
print(colorize("----------------------------Parser--------------------------------", "lightgreen"))
parser = Parser(tokens)
parser.parse()
parser.codegen.save("./py_v/output.txt")

