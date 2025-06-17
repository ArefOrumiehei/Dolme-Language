from utils.colorize import colorize
from helpers.validation import is_valid_var_name

class ThreeAddressInterpreter:
    def __init__(self, code_lines):
        self.code = code_lines
        self.variables = {}
        self.symbol_table = {}
        self.instruction_pointer = 0

    def get_value(self, operand):
        if operand == '_':
            return None
        if operand in ("true", "false"):
            return 1 if operand == "true" else 0
        if operand.startswith('"') and operand.endswith('"'):
            return operand[1:-1]
        if operand.startswith("'") and operand.endswith("'"):
            return operand[1:-1]
        if operand.startswith("#"):
            operand = operand[1:]
        
        if str(operand) in self.variables:
            val = self.variables[operand]
            while isinstance(val, str) and val in self.variables:
                val = self.variables[val]
            return val
            

        if isinstance(operand, int) or isinstance(operand, float):
            return operand

        try:
            return int(operand)
        except (ValueError, TypeError):
            try:
                return float(operand)
            except (ValueError, TypeError):
                if operand in self.symbol_table:
                    addr = self.symbol_table[operand]
                    val = self.variables.get(addr, 0)
                    while isinstance(val, str) and val in self.variables:
                        val = self.variables[val]
                    return val
                else:
                    raise RuntimeError(f"{colorize('[Runtime Error]', 'lightred')} Unknown variable or temp: {operand}")
                
    def eval_expr(self, left, op, right):
        lval = self.get_value(left)
        rval = self.get_value(right)
        if op == '+': return lval + rval
        if op == '-': return lval - rval
        if op == '*': return lval * rval
        if op == '/': return lval / rval
        if op == '%': return lval % rval
        if op == '>': return int(lval > rval)
        if op == '<': return int(lval < rval)
        if op == '>=': return int(lval >= rval)
        if op == '<=': return int(lval <= rval)
        if op == '==': return int(lval == rval)
        if op == '!=': return int(lval != rval)
        if op == 'and': return int(bool(lval) and bool(rval))
        if op == 'or': return int(bool(lval) or bool(rval))
        raise RuntimeError(f"{colorize('[Runtime Error]', 'lightred')} Unknown operator: {op}")

    def parse_line(self, line):
        if not (line.startswith("(") and line.endswith(")")):
            raise RuntimeError(f"{colorize('[Runtime Error]', 'lightred')} Invalid line format: {line}")
        content = line[1:-1]
        parts = [p.strip() for p in content.split(",")]
        if len(parts) != 4:
            raise RuntimeError(f"{colorize('[Runtime Error]', 'lightred')} Malformed line: {line}")
        return parts  # op, arg1, arg2, result

    def preprocess_symbol_table(self):
        next_address = 400
        for line in self.code:
            op, arg1, arg2, result = self.parse_line(line.strip())
            for token in (arg1, arg2, result):
                if is_valid_var_name(token) and token not in self.symbol_table and token not in {'let', 'if', 'else', 'while', 'print', 'true', 'false', 'not', 'and', 'or',}:
                    self.symbol_table[token] = str(next_address)
                    next_address += 1

    def run(self):
        self.preprocess_symbol_table()
        previous_ip = -1

        while self.instruction_pointer < len(self.code):
            line = self.code[self.instruction_pointer].strip()
            if not line:
                if self.instruction_pointer == previous_ip:
                    raise RuntimeError(f"{colorize('[Infinite Loop]', 'yellow')} IP didn't change in last step!")
                previous_ip = self.instruction_pointer
                self.instruction_pointer += 1
                continue

            op, arg1, arg2, result = self.parse_line(line)

            ip_info = colorize(f"[IP={self.instruction_pointer + 1}]", 'lightblue')
            print(f"\n{ip_info} {colorize(line, 'lightwhite')}")
            print(f"{colorize('[symbol_table]', 'magenta')} {self.symbol_table}")
            print(f"{colorize('[variables]', 'lightyellow')} {self.variables}")

            if op == '=':
                if is_valid_var_name(arg1) and arg1 in self.symbol_table:
                    val = self.get_value(arg2)
                else:
                    val = self.get_value(arg1)
                self.variables[result] = val

            elif op in ('+', '-', '*', '/', '%', '>', '<', '>=', '<=', '==', '!=', 'and', 'or'):
                self.variables[result] = self.eval_expr(arg1, op, arg2)

            elif op == 'not':
                self.variables[result] = int(not self.get_value(arg1))

            elif op == 'uminus':
                self.variables[result] = -self.get_value(arg1)

            elif op == 'jmp':
                target = int(result)
                if target == self.instruction_pointer:
                    raise RuntimeError(f"{colorize('[Infinite Loop]', 'yellow')} jmp to same line {target}")
                self.instruction_pointer = target - 1
                continue

            elif op == 'jmpf':
                cond = self.get_value(arg1)
                print(f"{colorize('Condition Result:', 'lightcyan')}", cond)
                target = int(result)
                if not cond:
                    if target == self.instruction_pointer:
                        raise RuntimeError(f"{colorize('[Infinite Loop]', 'yellow')} jmpf to same line {target}")
                    self.instruction_pointer = target - 1
                    continue

            elif op == 'print':
                print(f"{colorize('Output:', 'lightgreen')} {self.get_value(arg1)}")

            else:
                raise RuntimeError(f"{colorize('[Runtime Error]', 'lightred')} Unknown operation: {op}")

            self.instruction_pointer += 1
