import re
from utils.colorize import colorize

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    

def validate_braces(tokens):
    stack = []
    for token_type, token_value, line, col in tokens:
        if token_type == 'LBRACE':
            stack.append('{')
        elif token_type == 'RBRACE':
            if not stack or stack[-1] != '{':
                raise SyntaxError(f"{colorize('[Syntax Error]', 'lightred')} unmatched '}}' found at line {line} col {col}")
            stack.pop()
        elif token_type == 'LPAREN':
            stack.append('(')
        elif token_type == 'RPAREN':
            if not stack or stack[-1] != '(':
                raise SyntaxError(f"{colorize('[Syntax Error]', 'lightred')} unmatched ')' found at line {line} col {col}")
            stack.pop()

    if stack:
        raise SyntaxError(f"{colorize('[Syntax Error]', 'lightred')} unclosed brace/paren found")

def is_valid_var_name(name):
    pattern = r'^[A-Za-z][A-Za-z0-9_]*$'
    return bool(re.match(pattern, name))