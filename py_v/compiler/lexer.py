import re
from utils.colorize import colorize
from utils.show_msg import show_error

token_specs = [
    ('COMMENT_BLOCK', r'/\*[\s\S]*?\*/'),
    ('COMMENT',   r'//[^\n]*'),
    ('NUMBER',    r'\d+(\.\d+)?([eE][+-]?\d+)?'),
    ('STRING', r'"(\\.|[^"\\\n])*"|\'(\\.|[^\'\\\n])*\''),
    ('ID',        r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('LE',        r'<='),
    ('GE',        r'>='),
    ('EQ',        r'=='),
    ('NE',        r'!='),
    # ('AND',       r'&&'),
    # ('OR',        r'\|\|'),
    # ('NOT',       r'!'),
    ('LT',        r'<'),
    ('GT',        r'>'),
    ('ASSIGN',    r'='),
    ('PLUS',      r'\+'),
    ('MINUS',     r'-'),
    ('MULT',      r'\*'),
    ('DIV',       r'/'),
    ('MOD',       r'%'),
    ('LPAREN',    r'\('),
    ('RPAREN',    r'\)'),
    ('LBRACE',    r'\{'),
    ('RBRACE',    r'\}'),
    ('SEMI',      r';'),
    ('SKIP',      r'[ \t\n]+'),                   # space and newline
    ('MISMATCH',  r'.'),                          # anything not valid
]

keywords = {
    'let', 
    'if', 
    'else', 
    'while', 
    'print', 
    'true', 
    'false', 
    'not', 
    'and', 
    'or', 
    'break',
    'continue'
}

tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specs)
get_token = re.compile(tok_regex).match


def tokenize(code):
    tokens = []
    pos = 0
    line = 1
    col = 1
    while pos < len(code):
        match = get_token(code, pos)
        if not match:
            show_error("syntax", "lexer", f"Unexpected character at line {line} col {col}: {code[pos]}")
        type = match.lastgroup
        value = match.group()
        print(colorize(f"value: {value}", "yellow"))
        print(colorize(f"type: {type}", "cyan"))
        print(colorize(f"................", "red"))

        if type in {"SKIP", "COMMENT_BLOCK", "COMMENT"}:
            lines = value.count('\n')
            if lines > 0:
                line += lines
                col = 1 + len(value) - value.rfind('\n')
            else:
                col += len(value)
        elif type == 'ID' and value in keywords:
            tokens.append(('KEYWORD', value, line, col))
            col += len(value)
        elif type == 'MISMATCH':
            show_error("syntax", "lexer", f"Illegal token at line {line} col {col}: {value}")
        else:
            tokens.append((type, value, line, col))
            col += len(value)

        pos = match.end()
    print(colorize("________________________________Tokens________________________________", "magenta"))
    print(tokens)
    return tokens