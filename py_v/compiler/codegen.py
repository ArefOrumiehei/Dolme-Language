class CodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 600
        self.var_address = 400
        self.current_line = 0
        self.var_table = {}
        self.break_stack = []
        self.continue_stack = []

    def new_temp(self):
        temp_var = self.temp_count
        self.temp_count += 1
        return f"{temp_var}"
    
    def new_var_address(self, var_name):
        var_adr = self.var_address
        self.var_address += 1
        self.var_table[var_name] = var_adr
        return var_adr
    
    def get_var_address(self, var_name):
        return self.var_table.get(var_name, None)

    def emit(self, op, arg1='_', arg2='_', result='_'):
        line = f"({op}, {arg1}, {arg2}, {result})"
        self.code.append(line)
        self.current_line += 1
    
    def save(self, filename="output.txt"):
        with open(filename, "w") as f:
            for line in self.code:
                f.write(line + "\n")
