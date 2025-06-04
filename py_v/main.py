from compiler.lexer import tokenize
from compiler.parser import Parser

with open("./py_v/input.txt", "r") as f:
    code = f.read()

tokens = tokenize(code)
parser = Parser(tokens)
parser.parse()
parser.codegen.save("./py_v/output.txt")

