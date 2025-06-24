from utils.colorize import colorize

def show_error (type, src, msg):
  colored_msg = colorize(msg, 'lightwhite')
  if type == "syntax":
    raise SyntaxError(f"{colorize('[Syntax Error]', 'lightred')} {colored_msg}")
  elif type == "semantic" and src == "parser":
    raise Exception(f"{colorize('[Semantic Error]', 'lightred')} {colored_msg}")
  elif type == "semantic" and src == "interpreter":
    raise RuntimeError(f"{colorize('[Semantic Error]', 'lightred')} {colored_msg}")
  elif type == "runtime":
    raise RuntimeError(f"{colorize('[Runtime Error]', 'lightred')} {colored_msg}")
  elif type == "divbyzero":
    raise ZeroDivisionError(f"{colorize('[Semantic Error]', 'lightred')} {colored_msg}")

def show_warning(type, src, msg):
  colored_msg = colorize(msg, 'lightwhite')

  if type == "infiniteloop":
    raise RuntimeWarning(f"{colorize('[Infinite Loop]', 'yellow')} {colored_msg}")
