from compiler.codegen import  CodeGenerator
from utils.colorize import colorize, log_parse
from helpers.validation import is_number, validate_braces, is_valid_var_name

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None
        self.prev_token = None
        self.symbol_table = {}
        self.codegen = CodeGenerator()

    def eat(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            print(f"{colorize('[match]', 'lightyellow')} {self.current_token}")
            self.prev_token = self.current_token
            self.pos += 1
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        else:
            if self.current_token is None:
                line = self.prev_token[2] if self.prev_token else '?'
                col = self.prev_token[3] if self.prev_token else '?'
                expected = ";" if token_type == "SEMI" else token_type
                raise SyntaxError(f"{colorize('[Syntax Error]', 'lightred')} unexpected end of input, expected {expected} at line {line} col {col}")
            else:
                if token_type in {"RPAREN", "LPAREN"}:
                    missing_typo = "(  or  )"
                elif token_type in {"RBRACE", "LBRACE"}:
                    missing_typo = "{  or  }"

                raise SyntaxError(
                    f"{colorize('[Syntax Error]', 'lightred')} expected {token_type} "
                    f"but got '{self.current_token[1]}' at line {self.current_token[2]} col {self.current_token[3]}. "
                    f"Perhaps a {missing_typo} is missing?"
                )

                # raise Exception(f"{colorize('[error]', 'lightred')} Syntax error: expected {token_type} but got {self.current_token[1]} at line {self.current_token[2]} col {self.current_token[3]}")

    def peek_token(self):
        return self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else (None, None)


    def parse(self):
        validate_braces(tokens=self.tokens)
        self.program()

    def program(self):
        log_parse("Program")
        self.stmt_list()

    def stmt_list(self):
        log_parse("StmtList")
        while self.current_token and self.current_token[0] in ('KEYWORD', 'ID'):
            self.stmt()
        if self.current_token != None:
            if self.current_token[0] in ('SEMI'):
                raise SyntaxError(f"{colorize('[Syntax Error]', 'lightred')} unexpected {self.current_token[1]} at line {self.current_token[2]} col {self.current_token[3]}")
            else:
                while self.current_token and self.current_token[0] in ('KEYWORD', 'ID'):
                    self.stmt()


    def stmt(self):
        log_parse("Stmt")
        if self.current_token[1] == 'let':
            self.decl()
        elif self.current_token[0] == 'ID' and self.peek_token()[0] == 'ASSIGN':
            self.assign()
        elif self.current_token[1] == 'if':
            self.if_stmt()
        elif self.current_token[1] == 'while':
            self.while_stmt()
        elif self.current_token[1] == 'print':
            self.print_stmt()
        else:
            raise SyntaxError(f"{colorize('[Syntax Error]', 'lightred')} unexpected statement start: {self.current_token[1]} at line {self.current_token[2]} col {self.current_token[3]}")


    def decl(self):
        log_parse("Decl")
        self.eat('KEYWORD')
        var_name = self.current_token[1]

        if not is_valid_var_name(var_name):
            raise SyntaxError(f"{colorize('[Syntax Error]', 'lightred')} invalid variable name '{var_name}'")

        self.eat('ID')
        if var_name in self.symbol_table:
            raise Exception(f"{colorize('[Semantic Error]', 'lightred')} variable '{var_name}' already defined")
            
        self.eat('ASSIGN')
        val = self.expr()

        self.symbol_table[var_name] = val
        
        self.codegen.emit(f"{var_name} = {val}")
        self.eat('SEMI')

    def assign(self):
        log_parse("Assign")
        var_name = self.current_token[1]

        if var_name not in self.symbol_table:
            raise Exception(f"{colorize('[Semantic Error]', 'lightred')} variable '{var_name}' used before declaration.")

        self.eat('ID')
        self.eat('ASSIGN')
        val = self.expr()
        self.codegen.emit(f"{var_name} = {val}")
        self.eat('SEMI')


    def if_stmt(self):
        log_parse("IfStmt")
        self.eat('KEYWORD')

        if not self.current_token or self.current_token[0] != 'LPAREN':
            line = self.current_token[2] if self.current_token else '?'
            col = self.current_token[3] if self.current_token else '?'
            raise SyntaxError(f"{colorize('[Syntax Error]', 'lightred')} missing condition for 'if' at line {line} col {col}")

        self.eat('LPAREN')
        cond_var = self.cond()
        self.eat('RPAREN')

        label_else = self.codegen.new_label()
        label_end = self.codegen.new_label()

        self.codegen.emit(f"if_false {cond_var} goto {label_else}")

        self.eat('LBRACE')
        self.stmt_list()
        self.eat('RBRACE')

        self.codegen.emit(f"goto {label_end}")
        self.codegen.emit(f"{label_else}:")

        if self.current_token and self.current_token[1] == 'else':
            self.eat('KEYWORD')

            self.eat('LBRACE')
            self.stmt_list()
            self.eat('RBRACE')

        self.codegen.emit(f"{label_end}:")


    def while_stmt(self):
        log_parse("WhileStmt")
        self.eat('KEYWORD')

        label_start = self.codegen.new_label()
        label_end = self.codegen.new_label()

        self.codegen.emit(f"{label_start}:")

        self.eat('LPAREN')
        cond_var = self.cond()
        self.eat('RPAREN')

        self.codegen.emit(f"if_false {cond_var} goto {label_end}")

        self.eat('LBRACE')
        self.stmt_list()
        self.eat('RBRACE')

        self.codegen.emit(f"goto {label_start}")
        self.codegen.emit(f"{label_end}:")

    def print_stmt(self):
        log_parse("PrintStmt")
        self.eat('KEYWORD')

        if self.current_token is None or self.current_token[0] != 'LPAREN':
            line = self.prev_token[2] if self.prev_token else '?'
            col = self.prev_token[3] if self.prev_token else '?'
            raise SyntaxError(f"{colorize('[Syntax Error]', 'lightred')} expected '(' after 'print' at line {line} col {col}")

        self.eat('LPAREN')

        var_name = self.current_token[1]

        expr_val = self.expr()

        if not is_number(expr_val) and expr_val not in self.symbol_table and not expr_val.startswith("t"):
            raise Exception(f"{colorize('[Semantic Error]', 'lightred')} variable '{var_name}' used before declaration")

        if self.current_token is None or self.current_token[0] != 'RPAREN':
            line = self.prev_token[2] if self.prev_token else '?'
            col = self.prev_token[3] if self.prev_token else '?'
            raise SyntaxError(f"{colorize('[Syntax Error]', 'lightred')} expected ')' after variable name at line {line} col {col}")

        self.eat('RPAREN')

        if self.current_token is None or self.current_token[0] != 'SEMI':
            line = self.prev_token[2] if self.prev_token else '?'
            col = self.prev_token[3] if self.prev_token else '?'
            raise SyntaxError(f"{colorize('[Syntax error]', 'lightred')} expected ';' after print statement at line {line} col {col}")

        self.eat('SEMI')
        self.codegen.emit(f"print({expr_val})")


    def expr(self):
        log_parse("Expr")
        left = self.term()
        return self.expr_prime(left)

    def expr_prime(self, inherited):
        while self.current_token and self.current_token[0] in ('PLUS', 'MINUS'):
            op = self.current_token[1]
            self.eat(self.current_token[0])
            right = self.term()
            temp = self.codegen.new_temp()
            self.codegen.emit(f"{temp} = {inherited} {op} {right}")
            inherited = temp
        return inherited

    def term(self):
        log_parse("Term")
        left = self.factor()
        return self.term_prime(left)

    def term_prime(self, inherited):
        while self.current_token and self.current_token[0] in ('MULT', 'DIV'):
            op = self.current_token[1]
            self.eat(self.current_token[0])
            right = self.factor()
            temp = self.codegen.new_temp()
            self.codegen.emit(f"{temp} = {inherited} {op} {right}")
            inherited = temp
        return inherited

    def factor(self):
        log_parse("Factor")
        
        if self.current_token[0] == 'MINUS':
            self.eat('MINUS')
            val = self.factor()
            temp = self.codegen.new_temp()
            self.codegen.emit(f"{temp} = -{val}")
            return temp
        elif self.current_token[0] == 'ID':
            token_type, val_name, line, col = self.current_token
            if val_name not in self.symbol_table:
                raise Exception(f"{colorize('[Semantic Error]', 'lightred')} variable '{val_name}' used before declaration at line {line} col {col}")
            self.eat('ID')
            return val_name
        elif self.current_token[0] == 'NUMBER':
            val = self.current_token[1]
            self.eat('NUMBER')
            return val
        elif self.current_token[0] == 'LPAREN':
            self.eat('LPAREN')
            val = self.expr()
            self.eat('RPAREN')
            return val
        else:
            raise SyntaxError(f"{colorize('[Syntax Error]', 'lightred')} unexpected factor: {self.current_token}")


    def cond(self):
        log_parse("Cond")
        if self.current_token[0] == 'RPAREN':
            raise SyntaxError(f"{colorize('[Syntax Error]', 'lightred')} empty condition in if/while at line {self.current_token[2]}")
        return self.or_expr()

    def or_expr(self):
        log_parse("OrExpr")
        left = self.and_expr()
        return self.or_expr_prime(left)
    
    def or_expr_prime(self, inherited):
        while self.current_token and self.current_token[1] == 'or':
            self.eat('KEYWORD')
            right = self.and_expr()
            temp = self.codegen.new_temp()
            self.codegen.emit(f"{temp} = {inherited} or {right}")
            inherited = temp
        return inherited


    def and_expr(self):
        log_parse("AndExpr")
        left = self.not_expr()
        return self.and_expr_prime(left)
    
    def and_expr_prime(self, inherited):
        while self.current_token and self.current_token[1] == 'and':
            self.eat('KEYWORD')
            right = self.not_expr()
            temp = self.codegen.new_temp()
            self.codegen.emit(f"{temp} = {inherited} and {right}")
            inherited = temp
        return inherited


    def not_expr(self):
        log_parse("NotExpr")
        if self.current_token and self.current_token[1] == 'not':
            self.eat('KEYWORD')
            val = self.not_expr()
            temp = self.codegen.new_temp()
            self.codegen.emit(f"{temp} = not {val}")
            return temp
        else:
            return self.rel_expr()


    def rel_expr(self):
        log_parse("RelExpr")
        left = self.bool_primary()
        return self.rel_expr_prime(left)
        
    def rel_expr_prime(self, inherited):
        if self.current_token and self.current_token[0] in ('EQ', 'NE', 'LE', 'GE', 'LT', 'GT'):
            op = self.current_token[1]
            self.eat(self.current_token[0])
            right = self.bool_primary()
            temp = self.codegen.new_temp()
            self.codegen.emit(f"{temp} = {inherited} {op} {right}")
            return temp
        else:
            return inherited


    def bool_primary(self):
        log_parse("BoolPrimary")
        if self.current_token[1] in ('true', 'false'):
            val = self.current_token[1]
            self.eat('KEYWORD')
            return val
        elif self.current_token[0] == 'LPAREN':
            self.eat('LPAREN')
            val = self.cond()
            self.eat('RPAREN')
            return val
        else:
            return self.expr()
