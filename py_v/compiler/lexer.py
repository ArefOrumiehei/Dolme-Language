import re

token_specs = [
    ('NUMBER',    r'\d+(\.\d+)?([eE][+-]?\d+)?'),
    ('ID',        r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('EQ',        r'=='),
    ('NE',        r'!='),
    ('LE',        r'<='),
    ('GE',        r'>='),
    ('LT',        r'<'),
    ('GT',        r'>'),
    ('ASSIGN',    r'='),
    ('PLUS',      r'\+'),
    ('MINUS',     r'-'),
    ('MULT',      r'\*'),
    ('DIV',       r'/'),
    ('LPAREN',    r'\('),
    ('RPAREN',    r'\)'),
    ('LBRACE',    r'\{'),
    ('RBRACE',    r'\}'),
    ('SEMI',      r';'),
    ('SKIP',      r'[ \t\n]+'),                   # space and newline
    ('MISMATCH',  r'.'),                          # anything not valid
]

keywords = {'let', 'if', 'else', 'while', 'print', 'true', 'false', 'not', 'and', 'or'}

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
            raise SyntaxError(f'Unexpected character at line {line} col {col}: {code[pos]}')
        kind = match.lastgroup
        value = match.group()

        if kind == 'SKIP':
            lines = value.count('\n')
            if lines > 0:
                line += lines
                col = 1 + len(value) - value.rfind('\n')
            else:
                col += len(value)
        elif kind == 'ID' and value in keywords:
            tokens.append(('KEYWORD', value, line, col))
            col += len(value)
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Illegal token at line {line} col {col}: {value}')
        else:
            tokens.append((kind, value, line, col))
            col += len(value)

        pos = match.end()
    return tokens