def colorize(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'orange': '\033[33m',
        'white': '\033[97m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'gray': '\033[90m',
        'orange': '\033[33m',
        'lightblue': '\033[94m',
        'lightgreen': '\033[92m',
        'lightcyan': '\033[96m',
        'lightred': '\033[91m',
        'lightmagenta': '\033[95m',
        'reset': '\033[0m'
    }
    return f"{colors.get(color, colors['white'])}{text}{colors['reset']}"
