from utils.colorize import colorize

_error_map = {
    ("syntax", None): SyntaxError,
    ("semantic", "parser"): Exception,
    ("semantic", "interpreter"): RuntimeError,
    ("runtime", None): RuntimeError,
    ("divbyzero", None): ZeroDivisionError,
}

_warning_map = {
    "infiniteloop": RuntimeWarning,
}

def show_error(err_type, src=None, msg=""):
    colored_msg = colorize(msg, 'lightwhite')
    exc_class = _error_map.get((err_type, src)) or _error_map.get((err_type, None))
    if exc_class is None:
        raise Exception(f"Unknown error type: {err_type} - {msg}")
    prefix = {
        "syntax": "[Syntax Error]",
        "semantic": "[Semantic Error]",
        "runtime": "[Runtime Error]",
        "divbyzero": "[Semantic Error]",
    }.get(err_type, "[Error]")
    raise exc_class(f"{colorize(prefix, 'lightred')} {colored_msg}")

def show_warning(warn_type, src=None, msg=""):
    colored_msg = colorize(msg, 'lightwhite')
    warn_class = _warning_map.get(warn_type)
    if warn_class:
        raise warn_class(f"{colorize('[Infinite Loop]', 'yellow')} {colored_msg}")
    else:
        print(f"{colorize('[Warning]', 'yellow')} {colored_msg}")
