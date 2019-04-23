import tkinter as tk
from minesweeper import Minesweeper
from itertools import product


class Solver(object):

    def __init__(self, minesweeper):
        self.minesweeper = minesweeper
        self.root = minesweeper.root

        self.bind_shortcuts()
        self.action = True  # For the solve method, while an action is being taken

        self.completed = []  # Have all the surrounding cells been revealed?
        for row in range(minesweeper.ROWS):
            self.completed.append([])
            for column in range(minesweeper.COLUMNS):
                self.completed[row].append(False)

    def bind_shortcuts(self):
        self.root.bind("<Key-1>", lambda event: self.double_click_complete())
        self.root.bind("<Key-2>", lambda event: self.flag_complete())
        self.root.bind("<s>", lambda event: self.solve())
        self.root.bind("<r>", lambda event: self.reset())

    def reset(self):
        self.minesweeper.reset()  # this is what <Control-r> does
        for row in range(minesweeper.ROWS):
            for column in range(minesweeper.COLUMNS):
                self.completed[row][column] = False

    def solve(self):
        self.action = True
        while self.action:
            self.action = False
            self.flag_complete()
            self.double_click_complete()

    def double_click_complete(self):
        """ Repeatedly double clicks the "completed" cells, the cells which are fully flagged

        """
        done = False

        while not done and not self.minesweeper.game_over:
            done = True
            row = 0
            column = 0

            while not self.minesweeper.game_over and column < self.minesweeper.COLUMNS:
                current_cell = self.minesweeper.cells[row][column]
                if not current_cell.covered and current_cell.neighboring_bombs == 0:
                    self.completed[row][column] = True
                elif not self.completed[row][column] and not current_cell.covered and \
                        current_cell.neighboring_bombs == current_cell.neighboring_flags:
                    current_cell.double_left_click()
                    self.completed[row][column] = True
                    done = False
                    self.action = True

                row += 1
                if row >= self.minesweeper.ROWS:
                    row = 0
                    column += 1

    def flag_complete(self):
        """ Flags the cells which have no other options

        """
        for row in range(self.minesweeper.ROWS):
            for column in range(self.minesweeper.COLUMNS):
                current_cell = self.minesweeper.cells[row][column]
                if current_cell.covered or current_cell.neighboring_bombs == 0:
                    continue
                neighboring_covered_cells = []
                neighboring_flagged_cells = []
                for i, j in product((0, 1, -1), (0, 1, -1)):
                    if row+i >= 0 and column+j >= 0 and not (row == 0 and column == 0):
                        try:
                            current_bordering_cell = self.minesweeper.cells[row+i][column+j]
                            if current_bordering_cell.flagged:
                                neighboring_flagged_cells.append(current_bordering_cell)
                            elif current_bordering_cell.covered:
                                neighboring_covered_cells.append(current_bordering_cell)
                        except IndexError:
                            pass
                if len(neighboring_flagged_cells) + len(neighboring_covered_cells) == current_cell.neighboring_bombs:
                    for cell in neighboring_covered_cells:
                        cell.flag()
                        self.action = True


root = tk.Tk()
minesweeper = Minesweeper(root)
solver = Solver(minesweeper)
root.mainloop()
