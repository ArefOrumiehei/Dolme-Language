def colorize(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'orange': '\033[33m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    return f"{colors.get(color, colors['white'])}{text}{colors['reset']}"
