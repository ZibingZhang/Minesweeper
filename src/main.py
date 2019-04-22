import tkinter as tk
from minesweeper import Minesweeper


class Solver(object):

    def __init__(self, minesweeper):
        self.minesweeper = minesweeper
        self.root = minesweeper.root

        self.bind_shortcuts()

        self.completed = []  # Have all the surrounding cells been revealed?
        for row in range(minesweeper.ROWS):
            self.completed.append([])
            for column in range(minesweeper.COLUMNS):
                self.completed[row].append(False)

    def bind_shortcuts(self):
        self.root.bind("<Key-1>", lambda event: self.double_click_complete())

    def reset_completed(self):
        for row in range(minesweeper.ROWS):
            for column in range(minesweeper.COLUMNS):
                self.completed[row][column] = False

    def double_click_complete(self):
        """ Repeatedly double clicks the "completed" cells, the cells which are fully flagged

        """
        self.reset_completed()
        done = False

        while not done and not self.minesweeper.game_over:
            done = True
            row = 0
            column = 0

            while not self.minesweeper.game_over and column < self.minesweeper.COLUMNS:
                current_cell = self.minesweeper.cells[row][column]
                if current_cell.neighboring_bombs == 0:
                    self.completed[row][column] = True
                elif not self.completed[row][column] and not current_cell.covered and \
                        current_cell.neighboring_bombs == current_cell.neighboring_flags:
                    current_cell.double_left_click()
                    self.completed[row][column] = True
                    done = False

                row += 1
                if row >= self.minesweeper.ROWS:
                    row = 0
                    column += 1


root = tk.Tk()
minesweeper = Minesweeper(root)
solver = Solver(minesweeper)
root.mainloop()
