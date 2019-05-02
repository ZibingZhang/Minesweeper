import tkinter as tk
from minesweeper import Minesweeper
from itertools import product


class Solver(object):

    def __init__(self, minesweeper):
        self.minesweeper = minesweeper
        self.root = minesweeper.root
        self.size = (minesweeper.rows, minesweeper.columns)

        self.bind_shortcuts()
        self.action = True  # For the solve method, while an action is being taken

        self.completed = []  # Have all the surrounding cells been revealed?
        for row in range(minesweeper.rows):
            self.completed.append([])
            for column in range(minesweeper.columns):
                self.completed[row].append(False)

    def bind_shortcuts(self):
        self.root.bind("<Key-1>", lambda event: self.double_click_complete())
        self.root.bind("<Key-2>", lambda event: self.flag_complete())
        self.root.bind("<Key-3>", lambda event: self.flag_patterns())
        self.root.bind("<s>", lambda event: self.solve())

        self.root.bind("<t>", lambda event: self.test_1())

        self.root.bind("<r>", lambda event: self.reset())
        self.root.bind("<q>", lambda event: self.root.destroy())

    def reset(self):
        self.minesweeper.reset()  # this is what <Control-r> does
        for row in range(minesweeper.rows):
            for column in range(minesweeper.columns):
                self.completed[row][column] = False

    def reset_completed(self):
        self.completed = []  # Have all the surrounding cells been revealed?
        for row in range(minesweeper.rows):
            self.completed.append([])
            for column in range(minesweeper.columns):
                self.completed[row].append(False)

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
        if self.size != (minesweeper.rows, minesweeper.columns):
            self.size = (minesweeper.rows, minesweeper.columns)
            self.reset_completed()

        while not done and not self.minesweeper.game_over:
            done = True
            row = 0
            column = 0

            while not self.minesweeper.game_over and column < self.minesweeper.columns:
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
                if row >= self.minesweeper.rows:
                    row = 0
                    column += 1

    def flag_complete(self):
        """ Flags the cells which have no other options

        """
        for row in range(self.minesweeper.rows):
            for column in range(self.minesweeper.columns):
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

    def flag_patterns(self):
        """
        Flag basic patterns, such as the "1-2-1" pattern.
        """
        pass

    def test_1(self):
        """
        We test how far into the game we can get by only flagging around cells with no other
        options and revealing cells which have already been completely flagged.
        """

        center_x = self.minesweeper.rows//2
        center_y = self.minesweeper.columns//2

        for trial in range(5):
            self.minesweeper.cells[center_x][center_y].left_click()
            self.solve()
            if self.minesweeper.bombs_left.get() == "You Win":
                bombs_left = 0
            else:
                bombs_left = self.minesweeper.bombs_left.get()
            print(trial, bombs_left, end="\t,")
            self.reset()
        print("")


root = tk.Tk()
minesweeper = Minesweeper(root)
solver = Solver(minesweeper)
root.mainloop()
