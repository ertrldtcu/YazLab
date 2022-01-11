from Sudoku import *
from threading import Thread
from random import random, shuffle
from tkinter import *
import sys

sys.setrecursionlimit(10000)
margin = 25


class SamuraiSudoku:

    def __init__(self, canvas, graph_canvas, source_file, x=0, y=0, cellSize=28, cellSpace=1):
        self.canvas = canvas
        self.graph = graph_canvas
        self.x = x
        self.y = y
        self.cellSize = cellSize
        self.cellSpace = cellSpace
        self.control_timer = 0
        self.sudokus = []
        self.empty_cell_count = 369
        self.source_file = source_file
        self.load_sudoku()
        self.output_file = -1

    def load_sudoku(self):
        self.sudokus = []
        self.empty_cell_count = 369
        self.sudokus.append(Sudoku(self,
                                   margin,
                                   margin))
        self.sudokus.append(Sudoku(self,
                                   self.cellSize * 12 + self.cellSpace * 18 + margin,
                                   margin))
        self.sudokus.append(Sudoku(self,
                                   self.cellSize * 6 + self.cellSpace * 9 + margin,
                                   self.cellSize * 6 + self.cellSpace * 9 + margin))
        self.sudokus.append(Sudoku(self,
                                   margin,
                                   self.cellSize * 12 + self.cellSpace * 18 + margin))
        self.sudokus.append(Sudoku(self,
                                   self.cellSize * 12 + self.cellSpace * 18 + margin,
                                   self.cellSize * 12 + self.cellSpace * 18 + margin))

        self.sudokus[2].boxes[0] = self.sudokus[0].boxes[8]
        self.sudokus[2].boxes[2] = self.sudokus[1].boxes[6]
        self.sudokus[2].boxes[6] = self.sudokus[3].boxes[2]
        self.sudokus[2].boxes[8] = self.sudokus[4].boxes[0]
        if self.source_file is not None:
            file = open(self.source_file, "r")
            for row, line in enumerate(file):
                for column, character in enumerate(line):
                    if character == "\n" or character == "*":
                        continue
                    self.empty_cell_count -= 1
                    character = int(character)
                    rowForBox = row
                    colForBox = column
                    sudokuIndex = 0
                    if row < 6 and column > 8:
                        sudokuIndex = 1
                        colForBox = column - 9
                    elif row < 9 and column > 11:
                        sudokuIndex = 1
                        colForBox = column - 12
                    if 8 < column < 12 and (5 < row < 9 or 11 < row < 15):
                        sudokuIndex = 2
                        rowForBox = row - 6
                        colForBox = column - 6
                    elif 8 < row < 12:
                        sudokuIndex = 2
                        rowForBox = row - 6
                    elif row > 11 and column < 9:
                        sudokuIndex = 3
                        rowForBox = row - 12
                    elif 11 < row < 15 and column > 11:
                        sudokuIndex = 4
                        rowForBox = row - 12
                        colForBox = column - 12
                    elif row > 14 and column > 8:
                        sudokuIndex = 4
                        rowForBox = row - 12
                        colForBox = column - 9
                    boxID = rowForBox // 3 * 3 + colForBox // 3
                    cellID = (row % 3) * 3 + (column - 9) % 3
                    self.sudokus[sudokuIndex].set_cell(boxID, cellID, character)

        for sudokuid in [0, 1, 3, 4, 2]:
            self.sudokus[sudokuid].draw_sudoku()

    def isvalid(self, sudokuid, boxid, cellid, value, check_intersection=True):

        sudoku = self.sudokus[sudokuid]

        # check box
        box = sudoku.boxes[boxid]
        for cell in box.cells:
            if cell.value == value:
                return False

        # check row
        row = cellid // 3
        for brid in range(boxid // 3 * 3, boxid // 3 * 3 + 3):  # brid: box row id
            for crid, cell in enumerate(sudoku.boxes[brid].cells):  # crid: cell row id
                if crid // 3 == row and cell.value == value:
                    return False

        # check col
        col = cellid % 3
        for bcid in range(boxid % 3, boxid % 3 + 7, 3):  # bcid: box col id
            for ccid, cell in enumerate(sudoku.boxes[bcid].cells):  # ccid: cell col id
                if ccid % 3 == col and cell.value == value:
                    return False

        # check for central sudoku intersection boxes
        if check_intersection:
            if sudokuid != 2 and boxid == 8 - sudokuid * 2:
                if not self.isvalid(2, sudokuid * 2, cellid, value, False):
                    return False
            elif sudokuid == 2:
                if boxid != 4 and boxid % 2 == 0:
                    if not self.isvalid(boxid // 2, 8 - boxid, cellid, value, False):
                        return False

        return True

    def get_graphic_data(self, interval=0.001):
        # toplam boş hücre sayısı 248
        parsed_data = []
        counter = 0
        while True:
            for sudoku in self.sudokus:
                for solved_time in sudoku.graphic_data:
                    dif = solved_time - self.control_timer
                    if 0 <= dif < interval:
                        counter += 1
            parsed_data.append(counter)
            self.control_timer += interval
            if counter >= self.empty_cell_count:
                break
        return parsed_data

    def solve(self, solve_pieced=False):

        while True:

            self.control_timer = time.time()

            self.output_file = open("solution.txt", "w", encoding="utf-8")
            threads = []

            sudokus = [0, 1, 2, 3, 4]
            shuffle(sudokus)
            for sudokuid in sudokus:
                threads.append(Thread(target=self.sudokus[sudokuid].solve, args=(sudokuid, solve_pieced)))

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            solved_counter = 0
            for sudoku in self.sudokus:
                s = False
                for solved in sudoku.solved:
                    s = s or solved
                if s:
                    solved_counter += 1
            if solved_counter == 5:
                break
            else:
                self.load_sudoku()

            self.output_file.close()

        for sudokuid in [0, 1, 3, 4, 2]:
            self.sudokus[sudokuid].draw_sudoku()

        interval = 0.02
        graphicdata = self.get_graphic_data(interval)
        k = 16

        height = self.graph.winfo_height()

        rhex = "#{:02x}{:02x}{:02x}".format(int(random() * 125)+55, int(random() * 125)+55, int(random() * 125)+55)
        old_count2 = 0
        old_count = 0
        for i, count in enumerate(graphicdata):

            if old_count != count or old_count2 != count:
                self.graph.create_line(15 + i * k, height - 17, 15 + i * k, height - old_count - 15,
                                       fill="#B1B1B1", dash=(3, 3))
                self.graph.create_text(15 + i * k, height - 15, font=f"Arial 5", text="%1.2f" % (i * interval),
                                       fill="black", anchor=N)
            if old_count != count and old_count2 != count:
                self.graph.create_line(15 + (i + 1) * k, height - 17, 15 + (i + 1) * k, height - count - 15,
                                       fill="#B1B1B1", dash=(3, 3))
                self.graph.create_line(15, height - count - 15, 15 + (i + 1) * k, height - count - 15,
                                       fill="#B1B1B1", dash=(3, 3))
                self.graph.create_text(15 + (i + 1) * k, height - 15, font=f"Arial 5",
                                       text="%1.2f" % ((i + 1) * interval), fill="black", anchor=N)
                self.graph.create_text(13, height - count - 15, font=f"Arial 5", text=str(count),
                                       fill="black", anchor=E)

            self.graph.create_line(15 + i * k, height - old_count - 15, 15 + (i + 1) * k, height - count - 15,
                                   fill=rhex)
            old_count2 = old_count
            old_count = count
