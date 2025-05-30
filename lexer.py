import re

# تعریف الگوها برای توکن‌ها
token_specs = [
    ('NUMBER',    r'\d+(\.\d+)?([eE][+-]?\d+)?'),  # عدد صحیح یا اعشاری یا علمی
    ('ID',        r'[a-zA-Z_][a-zA-Z0-9_]*'),      # شناسه
    ('EQ',        r'=='),                         # ==
    ('NE',        r'!='),                         # !=
    ('LE',        r'<='),                         # <=
    ('GE',        r'>='),                         # >=
    ('ASSIGN',    r'='),                          # =
    ('LT',        r'<'),                          # <
    ('GT',        r'>'),                          # >
    ('PLUS',      r'\+'),                         # +
    ('MINUS',     r'-'),                          # -
    ('MULT',      r'\*'),                         # *
    ('DIV',       r'/'),                          # /
    ('LPAREN',    r'\('),                         # (
    ('RPAREN',    r'\)'),                         # )
    ('LBRACE',    r'\{'),                         # {
    ('RBRACE',    r'\}'),                         # }
    ('SEMI',      r';'),                          # ;
    ('SKIP',      r'[ \t\n]+'),                   # فاصله و newline
    ('MISMATCH',  r'.'),                          # هرچیز نامعتبر
]

# لیست کلمات کلیدی
keywords = {'let', 'if', 'else', 'while', 'print', 'true', 'false', 'not', 'and', 'or'}

# کامپایل regex کلی
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specs)
get_token = re.compile(tok_regex).match

def tokenize(code):
    tokens = []
    pos = 0
    while pos < len(code):
        match = get_token(code, pos)
        if not match:
            raise SyntaxError(f'Unexpected character: {code[pos]}')
        kind = match.lastgroup
        value = match.group()

        if kind == 'SKIP':
            pass
        elif kind == 'ID' and value in keywords:
            tokens.append(('KEYWORD', value))
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Illegal token: {value}')
        else:
            tokens.append((kind, value))
        pos = match.end()
    return tokens

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        code = f.read()
    tokens = tokenize(code)
    for token in tokens:
        print(token)
