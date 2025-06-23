from utils.colorize import colorize

def show_error (type, msg):
  if type == "syntax":
    raise SyntaxError(f"{colorize("[Syntax Error]", "lightred")} {msg}")
  elif type == "semantic":
    print("S")
  