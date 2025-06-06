from utils.colorize import colorize

class ThreeAddressInterpreter:
    def __init__(self, code_lines):
        self.code = code_lines
        self.variables = {}
        self.labels = {}
        self.instruction_pointer = 0

        for idx, line in enumerate(self.code):
            line = line.strip()
            if line.endswith(':'):
                label = line[:-1].strip()
                self.labels[label] = idx

    def get_value(self, operand):
        if operand in ("true", "false"):
            return 1 if operand == "true" else 0
        try:
            return int(operand)
        except ValueError:
            try:
                return float(operand)
            except ValueError:
                return self.variables.get(operand, 0)


    def eval_expr(self, left, op, right):
        lval = self.get_value(left)
        rval = self.get_value(right)
        if op == '+': return lval + rval
        if op == '-': return lval - rval
        if op == '*': return lval * rval
        if op == '/': return lval / rval
        if op == '>': return int(lval > rval)
        if op == '<': return int(lval < rval)
        if op == '>=': return int(lval >= rval)
        if op == '<=': return int(lval <= rval)
        if op == '==': return int(lval == rval)
        if op == '!=': return int(lval != rval)
        if op == 'and': return int(bool(lval) and bool(rval))
        if op == 'or': return int(bool(lval) or bool(rval))
        raise Exception(f"Unknown operator: {op}")

    def run(self):
        while self.instruction_pointer < len(self.code):
            line = self.code[self.instruction_pointer].strip()

            if not line or line.endswith(':'):
                self.instruction_pointer += 1
                continue

            if line.startswith("print("):
                var = line[6:-1].strip()
                print(self.get_value(var))

            elif line.startswith("goto"):
                label = line.split()[1]
                if label not in self.labels:
                    raise RuntimeError(f"{colorize('[Runtime Error]', 'lightred')} undefined label: {label}")
                self.instruction_pointer = self.labels[label]
                continue


            elif line.startswith("if_false"):
                _, cond_var, _, label = line.split()
                condition = self.get_value(cond_var)
                if not condition:
                    if label not in self.labels:
                        raise RuntimeError(f"{colorize('[Runtime Error]', 'lightred')} undefined label: {label}")
                    self.instruction_pointer = self.labels[label]
                    continue


            elif line.startswith("if_true"):
                _, cond_var, _, label = line.split()
                condition = self.get_value(cond_var)
                if condition:
                    if label not in self.labels:
                        raise RuntimeError(f"{colorize('[Runtime Error]', 'lightred')} undefined label: {label}")
                    self.instruction_pointer = self.labels[label]
                    continue


            elif '=' in line:
                if '=' in line and not line.strip().startswith(('print', 'if', 'goto', 'label')):
                    target, expr = map(str.strip, line.split('=', 1))

                tokens = expr.split()

                if len(tokens) == 1:
                    if tokens[0] == 'not':
                        raise Exception(f"{colorize('[Semantic Error]', 'lightred')} invalid use of 'not' without operand.")
                    elif tokens[0].startswith("not"):
                        val = tokens[0][3:]
                        self.variables[target] = int(not self.get_value(val))
                    else:
                        self.variables[target] = self.get_value(tokens[0])

                elif len(tokens) == 2 and tokens[0] == 'not':
                    self.variables[target] = int(not self.get_value(tokens[1]))

                elif len(tokens) == 3:
                    left, op, right = tokens
                    self.variables[target] = self.eval_expr(left, op, right)

            else:
                raise RuntimeError(f"{colorize('[Runtime Error]', 'lightred')} invalid instruction: {line}")

            self.instruction_pointer += 1
