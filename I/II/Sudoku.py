import time
from threading import Thread

from Box import *


class Sudoku:

    def __init__(self, parent, posx, posy):
        self.parent = parent
        self.posx = posx
        self.posy = posy
        self.boxes = []
        for _ in range(9):
            self.boxes.append(Box())
        self.solved = [False]
        self.graphic_data = [0 for _ in range(81)]

    def solve(self, sudokuid, solve_pieced=False):
        start_time = time.time()
        if solve_pieced:
            if len(self.solved) < 2:
                self.solved.append(False)
            t1 = Thread(target=self.backtracking_from_end, args=(sudokuid, 0))
            t2 = Thread(target=self.backtracking_from_start, args=(sudokuid, 1))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        else:
            self.backtracking_from_end(sudokuid, 0)
            self.backtracking_from_start(sudokuid, 0)

        print(self.solved, sudokuid, time.time() - start_time)

    def backtracking_from_start(self, sudokuid, solved_id):
        if self.solved[solved_id]:
            return
        for boxid, box in enumerate(self.boxes):
            for cellid, cell in enumerate(box.cells):
                if cell.value == -1:
                    for value in range(1, 10):
                        if self.parent.isvalid(sudokuid, boxid, cellid, value):
                            self.set_cell(boxid, cellid, value)
                            self.graphic_data[boxid * 9 + cellid] = time.time()
                            self.backtracking_from_start(sudokuid, solved_id)
                            if self.solved[solved_id]:
                                self.parent.output_file.write(
                                    "sudokuid: " + str(sudokuid) + ", boxid: " + str(boxid) + ", cellid: " + str(
                                        cellid) + ", value:" + str(value) + "\n")
                                time.sleep(0.001)
                                return
                            self.set_cell(boxid, cellid, -1)
                    return

        self.solved[solved_id] = True

    def backtracking_from_end(self, sudokuid, solved_id):
        if self.solved[solved_id]:
            return
        for boxid in range(8, -1, -1):
            box = self.boxes[boxid]
            for cellid in range(8, -1, -1):
                cell = box.cells[cellid]
                if cell.value == -1:
                    for value in range(1, 10):
                        if self.parent.isvalid(sudokuid, boxid, cellid, value):
                            self.set_cell(boxid, cellid, value)
                            self.graphic_data[boxid * 9 + cellid] = time.time()
                            self.backtracking_from_end(sudokuid, solved_id)
                            if self.solved[solved_id]:
                                self.parent.output_file.write(
                                    "sudokuid: " + str(sudokuid) + ", boxid: " + str(boxid) + ", cellid: " + str(
                                        cellid) + ", value:" + str(value) + "\n")
                                time.sleep(0.001)
                                return
                            self.set_cell(boxid, cellid, -1)
                    return

        self.solved[solved_id] = True

    def draw_sudoku(self):
        self.parent.canvas.create_rectangle(self.posx, self.posy,
                                            self.posx + self.parent.cellSize * 9 + self.parent.cellSpace * 16,
                                            self.posy + self.parent.cellSize * 9 + self.parent.cellSpace * 16,
                                            fill="#346699",
                                            outline="")
        for boxID, box in enumerate(self.boxes):
            for cellID, cell in enumerate(box.cells):
                self.draw_cell(boxID, cellID)

    def set_cell(self, boxID, cellID, value, update=False):
        self.boxes[boxID].cells[cellID].value = value
        if update:
            self.draw_cell(boxID, cellID)

    def draw_cell(self, boxID, cellID):
        x = self.posx + self.parent.cellSize * (boxID % 3 * 3 + cellID % 3) \
            + self.parent.cellSpace * (3 + boxID % 3 * 4 + cellID % 3)
        y = self.posy + self.parent.cellSize * (boxID // 3 * 3 + cellID // 3) \
            + self.parent.cellSpace * (3 + boxID // 3 * 4 + cellID // 3)

        fill = "#BFBFBF" if (boxID + cellID) % 2 else "#E8E8E8"

        self.parent.canvas.create_rectangle(
            x, y, x + self.parent.cellSize, y + self.parent.cellSize,
            fill=fill,
            outline=""
        )
        if self.boxes[boxID].cells[cellID].value != -1:
            self.parent.canvas.create_text(
                x + self.parent.cellSize // 2,
                y + self.parent.cellSize // 2,
                font=f"Arial {self.parent.cellSize // 2} bold",
                text=self.boxes[boxID].cells[cellID].value)
