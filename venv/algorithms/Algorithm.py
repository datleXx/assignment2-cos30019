import sys

sys.setrecursionlimit(100000)


class Algorithm :
    def __init__(self) -> None:
        self.output = "NO"

    def getOutput(self):
        return self.output

    def infer(self, kb, query):
        raise NotImplementedError("infer method must be implemented in subclasses")