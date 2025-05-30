# main.py

from lexer import tokenize
from parser import Parser

with open("input.txt", "r") as f:
    code = f.read()

tokens = tokenize(code)
parser = Parser(tokens)
parser.parse()
parser.codegen.save("output.txt")

