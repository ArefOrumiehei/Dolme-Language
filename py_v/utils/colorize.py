def colorize(text, color):
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'gray': '\033[90m',
        'lightred': '\033[91m',
        'lightgreen': '\033[92m',
        'lightyellow': '\033[93m',
        'lightblue': '\033[94m',
        'lightmagenta': '\033[95m',
        'lightcyan': '\033[96m',
        'lightwhite': '\033[97m',
        'reset': '\033[0m'
    }
    return f"{colors.get(color, colors['white'])}{text}{colors['reset']}"

def log_parse(msg):
    print(f"{colorize('[parse]', 'lightblue')} {msg}")