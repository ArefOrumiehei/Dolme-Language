class CodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"
    
    def new_label(self):
        self.label_count += 1
        return f'L{self.label_count}'

    def emit(self, line):
        self.code.append(line)
    
    def save(self, filename="output.txt"):
        with open(filename, "w") as f:
            for line in self.code:
                f.write(line + "\n")
