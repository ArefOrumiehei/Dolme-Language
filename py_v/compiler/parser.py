from compiler.codegen import  CodeGenerator
from utils.colorize import colorize, log_parse
from utils.show_msg import show_error
from helpers.validation import is_number, validate_braces, is_valid_var_name
from helpers.formatting import format_number

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
            print(f"{colorize('[match]', 'lightyellow')} {colorize(self.current_token, 'lightwhite')}")
            self.prev_token = self.current_token
            self.pos += 1
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        else:
            if self.current_token is None:
                line = self.prev_token[2] if self.prev_token else '?'
                col = self.prev_token[3] if self.prev_token else '?'
                expected = ";" if token_type == "SEMI" else token_type
                show_error("syntax", "parser", f"Unexpected end of input, expected {expected} at line {line} col {col}")
            else:
                if token_type in {"RPAREN", "LPAREN"}:
                    show_error(
                        "syntax", 
                        "parser",
                        f"Expected {token_type} but got '{self.current_token[1]}' at line {self.current_token[2]} col {self.current_token[3]}. Perhaps a ( or ) is missing?"
                    )
                elif token_type in {"RBRACE", "LBRACE"}:
                    show_error(
                        "syntax", 
                        "parser",
                        f"Expected {token_type} but got '{self.current_token[1]}' at line {self.current_token[2]} col {self.current_token[3]}. Perhaps a '{{' or '}}' is missing?"
                    )

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
                show_error("syntax", "parser", f"Unexpected {self.current_token[1]} at line {self.current_token[2]} col {self.current_token[3]}")
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
        elif self.current_token[1] == 'break':
            self.break_stmt()
        elif self.current_token[1] == 'continue':
            self.continue_stmt()
        else:
            show_error("syntax", "parser", f"Unexpected statement start: {self.current_token[1]} at line {self.current_token[2]} col {self.current_token[3]}")


    def decl(self):
        log_parse("Decl")
        self.eat('KEYWORD')
        var_name = self.current_token[1]

        if not is_valid_var_name(var_name):
            show_error("syntax", "parser", f"Invalid variable name '{var_name}' at line {self.current_token[2]} col {self.current_token[3]}")

        self.eat('ID')
        if var_name in self.symbol_table:
            show_error("semantic", "parser", f"Variable '{var_name}' already defined at line {self.current_token[2]} col {self.current_token[3]}")
            
        self.eat('ASSIGN')
        val = self.expr()

        self.symbol_table[var_name] = val
        var_adr = self.codegen.new_var_address(var_name)

        if isinstance(val, int) or (isinstance(val, str) and val.isdigit()):
            val = format_number(val)
        elif isinstance(val, str) and val in self.symbol_table:
            val = self.codegen.get_var_address(val)
        
        self.codegen.emit("=", var_name, val, var_adr)

        if not self.current_token or self.current_token[0] != 'SEMI':
            line = self.prev_token[2] if self.prev_token else '?'
            col = self.prev_token[3] if self.prev_token else '?'
            show_error("syntax", "parser", f"Missing ';' at line {line} col {col}")

        self.eat('SEMI')

    def assign(self):
        log_parse("Assign")
        var_name = self.current_token[1]

        if var_name not in self.symbol_table:
            show_error("semantic", "parser", f"Variable '{var_name}' used before declaration at line {self.current_token[2]} col {self.current_token[3]}")

        self.eat('ID')
        self.eat('ASSIGN')
        val = self.expr()
        var_adr = self.codegen.get_var_address(var_name)

        if isinstance(val, int) or (isinstance(val, str) and val.isdigit()):
            val_formatted = format_number(val)
            self.codegen.emit("=", val_formatted, "_", var_adr)
        else:
            if isinstance(val, str) and val in self.symbol_table:
                val_addr = self.codegen.get_var_address(val)
            else:
                val_addr = val
            self.codegen.emit("=", val_addr, "_", var_adr)

        if not self.current_token or self.current_token[0] != 'SEMI':
            line = self.prev_token[2] if self.prev_token else '?'
            col = self.prev_token[3] if self.prev_token else '?'
            show_error("syntax", "parser", f"Missing ';' at line {line} col {col}")

        self.eat('SEMI')


    def if_stmt(self):
        log_parse("IfStmt")
        self.eat('KEYWORD')

        if not self.current_token or self.current_token[0] != 'LPAREN':
            line = self.current_token[2] if self.current_token else '?'
            col = self.current_token[3] if self.current_token else '?'
            show_error("syntax", "parser", f"Missing condition for 'if' at line {line} col {col}")

        self.eat('LPAREN')
        cond_var = self.cond()
        self.eat('RPAREN')

        jmpf_index = self.codegen.current_line
        cond_addr = self.codegen.get_var_address(cond_var)
        cond = cond_var if cond_var.startswith("6") else cond_addr
        self.codegen.emit('jmpf', cond, '_', '___')

        self.eat('LBRACE')
        self.stmt_list()
        self.eat('RBRACE')

        has_else = self.current_token and self.current_token[1] == 'else'

        if has_else:
            jmp_index = self.codegen.current_line
            self.codegen.emit('jmp', '_', '_', '___')

            else_line = self.codegen.current_line
            self.codegen.code[jmpf_index] = f"(jmpf, {cond}, _, {else_line + 1})"

            self.eat('KEYWORD')
            self.eat('LBRACE')
            self.stmt_list()
            self.eat('RBRACE')

            end_line = self.codegen.current_line
            self.codegen.code[jmp_index] = f"(jmp, _, _, {end_line + 1})"
        else:
            end_line = self.codegen.current_line
            self.codegen.code[jmpf_index] = f"(jmpf, {cond}, _, {end_line + 1})"
        

    def while_stmt(self):
        log_parse("WhileStmt")
        self.eat('KEYWORD')

        start_line = self.codegen.current_line
        self.codegen.continue_stack.append(start_line + 1)

        self.eat('LPAREN')
        cond_var = self.cond()
        self.eat('RPAREN')

        jmpf_index = self.codegen.current_line
        cond_addr = self.codegen.get_var_address(cond_var)
        cond = cond_var if cond_var.startswith("6") else cond_addr
        self.codegen.emit('jmpf', cond, '_', '___')

        self.eat('LBRACE')

        break_indices = []
        self.codegen.break_stack.append(break_indices)

        self.stmt_list()
        self.eat('RBRACE')

        self.codegen.emit("jmp", "_", "_", start_line + 1)

        end_line = self.codegen.current_line
        self.codegen.code[jmpf_index] = f"(jmpf, {cond}, _, {end_line + 1})"

        for idx in break_indices:
            self.codegen.code[idx] = f"(jmp, _, _, {end_line + 1})"

        self.codegen.break_stack.pop()
        self.codegen.continue_stack.pop()

    def print_stmt(self):
        log_parse("PrintStmt")
        self.eat('KEYWORD')

        if self.current_token is None or self.current_token[0] != 'LPAREN':
            line = self.prev_token[2] if self.prev_token else '?'
            col = self.prev_token[3] if self.prev_token else '?'
            show_error("syntax", "parser", f"Expected '(' after 'print' at line {line} col {col}")

        self.eat('LPAREN')

        var_name = self.current_token[1]

        expr_val = self.expr()

        if not is_number(expr_val) and not (isinstance(expr_val, str) and (
                    expr_val.startswith('"') and expr_val.endswith('"') or
                    expr_val.startswith("'") and expr_val.endswith("'") or
                    expr_val in self.symbol_table or
                    expr_val.startswith("t"))):
                show_error("semantic", "parser", f"Variable '{var_name}' used before declaration at line {self.current_token[2]} col {self.current_token[3]}")


        if self.current_token is None or self.current_token[0] != 'RPAREN':
            line = self.prev_token[2] if self.prev_token else '?'
            col = self.prev_token[3] if self.prev_token else '?'
            show_error("syntax", "parser", f"Expected ')' after variable name at line {line} col {col}")

        self.eat('RPAREN')

        if self.current_token is None or self.current_token[0] != 'SEMI':
            line = self.prev_token[2] if self.prev_token else '?'
            col = self.prev_token[3] if self.prev_token else '?'
            show_error("syntax", "parser", f"Expected ';' after print statement at line {line} col {col}")

        self.eat('SEMI')

        if is_number(expr_val):
            val = format_number(expr_val)
        elif isinstance(expr_val, str) and expr_val in self.symbol_table:
            val = self.codegen.get_var_address(expr_val)
        else:
            val = expr_val
        self.codegen.emit("print", val, "_", "_")


    def break_stmt(self):
        log_parse("BreakStmt")
        self.eat('KEYWORD')
        if self.current_token is None or self.current_token[0] != 'SEMI':
            show_error("syntax", "parser", f"Expected ';' after 'break' at line {self.prev_token[2]} col {self.prev_token[3]}")
        self.eat('SEMI')

        if not self.codegen.break_stack:
            show_error("syntax", "parser", f"'break' used outside loop at line {self.prev_token[2]} col {self.prev_token[3]}")

        self.codegen.emit('jmp', '_', '_', '___')
        self.codegen.break_stack[-1].append(self.codegen.current_line - 1)


    def continue_stmt(self):
        log_parse("ContinueStmt")
        self.eat('KEYWORD')
        if self.current_token is None or self.current_token[0] != 'SEMI':
            show_error("syntax", "parser", f"Expected ';' after 'continue' at line {self.prev_token[2]} col {self.prev_token[3]}")
        self.eat('SEMI')

        if not self.codegen.continue_stack:
            show_error("syntax", "parser", f"'continue' used outside loop at line {self.prev_token[2]} col {self.prev_token[3]}")

        self.codegen.emit('jmp', '_', '_', str(self.codegen.continue_stack[-1]))



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

            left_operand = self.codegen.get_var_address(inherited) if inherited in self.symbol_table else format_number(inherited)
            right_operand = self.codegen.get_var_address(right) if right in self.symbol_table else format_number(right)

            self.codegen.emit(op, left_operand, right_operand, temp)
            inherited = temp
        return inherited

    def term(self):
        log_parse("Term")
        left = self.factor()
        return self.term_prime(left)

    def term_prime(self, inherited):
        while self.current_token and self.current_token[0] in ('MULT', 'DIV', 'MOD'):
            op = self.current_token[1]
            self.eat(self.current_token[0])
            right = self.factor()
            temp = self.codegen.new_temp()

            left_operand = self.codegen.get_var_address(inherited) if inherited in self.symbol_table else format_number(inherited)
            right_operand = self.codegen.get_var_address(right) if right in self.symbol_table else format_number(right)

            self.codegen.emit(op, left_operand, right_operand, temp)
            inherited = temp
        return inherited

    def factor(self):
        log_parse("Factor")
        
        if self.current_token[0] == 'MINUS':
            self.eat('MINUS')
            val = self.factor()
            temp = self.codegen.new_temp()
            val = self.codegen.get_var_address(val) if val in self.symbol_table else format_number(val)
            self.codegen.emit("uminus", val, "_", temp)
            return temp
        elif self.current_token[0] == 'ID':
            token_type, val_name, line, col = self.current_token
            if val_name not in self.symbol_table:
                show_error("semantic", "parser", f"Variable '{val_name}' used before declaration at line {line} col {col}")
            self.eat('ID')
            return val_name
        elif self.current_token[0] == 'NUMBER':
            val = self.current_token[1]
            self.eat('NUMBER')
            return val
        elif self.current_token[0] == 'KEYWORD' and self.current_token[1] in ('true', 'false'):
            val = self.current_token[1]
            self.eat('KEYWORD')
            return val
        elif self.current_token[0] == 'STRING':
            val = self.current_token[1]
            self.eat('STRING')
            return val
        elif self.current_token[0] == 'LPAREN':
            self.eat('LPAREN')
            val = self.expr()
            self.eat('RPAREN')
            return val
        else:
            show_error("syntax", "parser", f"Unexpected factor: {self.current_token}")


    def cond(self):
        log_parse("Cond")
        if self.current_token[0] == 'RPAREN':
            show_error("syntax", "parser", f"Empty condition in if/while at line {self.current_token[2]}")
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

            self.codegen.emit('or', inherited, right, temp)
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

            self.codegen.emit('and', inherited, right, temp)
            inherited = temp
        return inherited


    def not_expr(self):
        log_parse("NotExpr")
        if self.current_token and self.current_token[1] == 'not':
            self.eat('KEYWORD')
            var = self.not_expr()
            temp = self.codegen.new_temp()

            var_addr = self.codegen.get_var_address(var)
            val = var if var.startswith("6") else var_addr

            self.codegen.emit('not', val, '_', temp)
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
            left_operand = self.codegen.get_var_address(inherited) if inherited in self.symbol_table else format_number(inherited)
            right_operand = self.codegen.get_var_address(right) if right in self.symbol_table else format_number(right)

            self.codegen.emit(op, left_operand, right_operand, temp)
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
