class _Getch:

    def __init__(self):
        self.impl = _GetchWindows()

    def __call__(self): return self.impl()

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()