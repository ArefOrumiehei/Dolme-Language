from compiler.codegen import  CodeGenerator
from py_v.helpers.colorize import colorize

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None
        self.codegen = CodeGenerator()

    def eat(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            print(f"[eat] Consuming {self.current_token}")
            self.pos += 1
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        else:
            raise Exception(f"Syntax error: expected {token_type} but got {self.current_token}")

    def parse(self):
        self.program()

    def program(self):
        print("[parse] Program")
        self.stmt_list()

    def stmt_list(self):
        print("[parse] StmtList")
        while self.current_token and self.current_token[0] in ('KEYWORD', 'ID'):
            self.stmt()

    def stmt(self):
        print("[parse] Stmt")
        if self.current_token[1] == 'let':
            self.decl()
        elif self.current_token[0] == 'ID':
            self.assign()
        elif self.current_token[1] == 'print':
            self.print_stmt()
        elif self.current_token[1] == 'if':
            self.if_stmt()
        elif self.current_token[1] == 'while':
            self.while_stmt()
        else:
            raise Exception(f"Unexpected statement start: {self.current_token}")

    def if_stmt(self):
        print("[parse] IfStmt")
        self.eat('KEYWORD')  # if
        self.eat('LPAREN')
        cond_var = self.cond()  # باید شرط رو اصلاح کنیم تا مقدار برگردونه
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
            self.eat('KEYWORD')  # else
            self.eat('LBRACE')
            self.stmt_list()
            self.eat('RBRACE')

        self.codegen.emit(f"{label_end}:")


    def while_stmt(self):
        print("[parse] WhileStmt")
        self.eat('KEYWORD')  # while

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



    def decl(self):
        print("[parse] Decl")
        self.eat('KEYWORD')  # let
        var_name = self.current_token[1]
        self.eat('ID')
        self.eat('ASSIGN')
        val = self.expr()
        self.codegen.emit(f"{var_name} = {val}")
        self.eat('SEMI')

    def assign(self):
        print("[parse] Assign")
        var_name = self.current_token[1]
        self.eat('ID')
        self.eat('ASSIGN')
        val = self.expr()
        self.codegen.emit(f"{var_name} = {val}")
        self.eat('SEMI')


    def print_stmt(self):
        print("[parse] PrintStmt")
        self.eat('KEYWORD')  # print
        self.eat('LPAREN')
        self.eat('ID')
        self.eat('RPAREN')
        self.eat('SEMI')

    def expr(self):
        print("[parse] Expr")
        left = self.term()
        return self.expr_prime(left)

    def expr_prime(self, inherited):
        while self.current_token and self.current_token[0] in ('PLUS', 'MINUS'):
            op = self.current_token[1]
            self.eat(self.current_token[0])  # eat 'PLUS' or 'MINUS'
            right = self.term()
            temp = self.codegen.new_temp()
            self.codegen.emit(f"{temp} = {inherited} {op} {right}")
            inherited = temp
        return inherited

    def term(self):
        print("[parse] Term")
        left = self.factor()
        return self.term_prime(left)

    def term_prime(self, inherited):
        while self.current_token and self.current_token[0] in ('MULT', 'DIV'):
            op = self.current_token[1]
            self.eat(self.current_token[0])  # eat 'MUL' or 'DIV'
            right = self.factor()
            temp = self.codegen.new_temp()
            self.codegen.emit(f"{temp} = {inherited} {op} {right}")
            inherited = temp
        return inherited


    def factor(self):
        print("[parse] Factor")
        if self.current_token[0] == 'ID':
            val = self.current_token[1]
            self.eat('ID')
            return val
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
            raise Exception(f"Unexpected factor: {self.current_token}")


    def cond(self):
        print("[parse] Cond")
        return self.or_expr()

    def or_expr(self):
        print("[parse] OrExpr")
        left = self.and_expr()
        while self.current_token and self.current_token[1] == 'or':
            self.eat('KEYWORD')  # 'or'
            right = self.and_expr()
            temp = self.codegen.new_temp()
            self.codegen.emit(f"{temp} = {left} or {right}")
            left = temp
        return left


    def and_expr(self):
        print("[parse] AndExpr")
        left = self.not_expr()
        while self.current_token and self.current_token[1] == 'and':
            self.eat('KEYWORD')  # 'and'
            right = self.not_expr()
            temp = self.codegen.new_temp()
            self.codegen.emit(f"{temp} = {left} and {right}")
            left = temp
        return left


    def not_expr(self):
        print("[parse] NotExpr")
        if self.current_token and self.current_token[1] == 'not':
            self.eat('KEYWORD')
            val = self.not_expr()
            temp = self.codegen.new_temp()
            self.codegen.emit(f"{temp} = not {val}")
            return temp
        else:
            return self.rel_expr()


    def rel_expr(self):
        print("[parse] RelExpr")
        left = self.bool_primary()
        if self.current_token and self.current_token[0] in ('EQ', 'NE', 'LE', 'GE', 'LT', 'GT'):
            op = self.current_token[1]
            self.eat(self.current_token[0])
            right = self.bool_primary()
            temp = self.codegen.new_temp()
            self.codegen.emit(f"{temp} = {left} {op} {right}")
            return temp
        else:
            return left


    def bool_primary(self):
        print("[parse] BoolPrimary")
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


