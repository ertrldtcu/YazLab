from Cell import *


class Box:

    def __init__(self):
        self.cells = []
        for _ in range(9):
            self.cells.append(Cell())
