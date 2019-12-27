import sys


class Log:
    # TODO maybe the right way to do this is to use something like colorama?
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    MAGENTA = '\033[35m'
    RESET = '\033[0m'
    BLUE = '\033[36m'

    level = 0
    @staticmethod
    def _format(s):
        return s

    @staticmethod
    def _print(s, color=None, format=True):
        s = str(s)
        if color and sys.stdout.isatty() and sys.platform != 'win32':
            print(color + s + Log.RESET)
        else:
            print(s)

    @staticmethod
    def d(s, format=True):
        if Log.level <= 0:
            Log._print(s, Log.MAGENTA)

    @staticmethod
    def i(s, format=True):
        if Log.level <= 0:
            Log._print(s, Log.GREEN)

    @staticmethod
    def w(s, format=True):
        if Log.level <= 1:
            Log._print(s, Log.YELLOW)

    @staticmethod
    def e(s, format=True):
        if Log.level <= 2:
            Log._print(s, Log.RED)

    @staticmethod
    def t(s, format=True):
        if Log.level <= 1:
            Log._print("------------------------------------------", Log.BLUE)
            Log._print(s, Log.BLUE)
            Log._print("------------------------------------------", Log.BLUE)
