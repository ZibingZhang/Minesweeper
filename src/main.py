from tkinter import *
from random import randint
from itertools import product


class Cell(object):
    """ A cell on the minesweeper board

    A cell on the minesweeper board. It includes the widget that is displayed and various
    other information regarding the cell.

    Attributes:
        text (StringVar): The text displayed on the cell
        button (Button): A button widget representing the cell
        bomb (bool): Is the cell a bomb?
        flag (bool): Is the cell flagged?
        hidden (bool): Is the cell hidden?
        neighboring_bombs (int): The number of neighboring bombs
        neighboring_flags (int): The number of neighboring flags
        minesweeper (Minesweeper): The minesweeper game object

    Methods:
        hold_down: Keeps the button pressed on left mouse click
        show_text: Shows the text of the cell
        uncover: Uncovers the cell
    """
    def __init__(self, minesweeper, parent, row, column):
        self.text = StringVar()
        self.bomb = False
        self.flag = False
        self.hidden = True
        self.neighboring_bombs = 0
        self.neighboring_flags = 0
        self.minesweeper = minesweeper

        self.button = Button(parent, width=2, textvariable=self.text,
                             command=lambda: self.hold_down())
        self.button.bind("<Button-1>",
                         lambda event, row=row, column=column: self.minesweeper.left_cell_press(row, column))
        self.button.bind("<Button-3>",
                         lambda event, row=row, column=column: self.minesweeper.right_cell_press(row, column))
        self.button.grid(row=row, column=column)

    def hold_down(self):
        self.button.config(relief=SUNKEN)

    def show_text(self):
        if self.bomb:
            self.text.set("*")
        else:
            self.text.set(int(self.neighboring_bombs))

    def uncover(self):
        self.show_text()


class Minesweeper(object):

    PAD_X = 10
    PAD_Y = 10
    WIDTH = 9
    HEIGHT = 9
    BOMBS = 16

    def __init__(self, root):

        # Two halves of the screen
        self.root = root
        self.root.resizable(False, False)
        self.top = Frame(root, padx=self.PAD_X, pady=self.PAD_Y)
        self.top.pack(side=TOP)
        self.bottom = Frame(root, padx=self.PAD_X, pady=self.PAD_Y)
        self.bottom.pack(side=BOTTOM)

        # Footer
        self.bombs_left = StringVar()
        self.score = Label(self.bottom, textvariable=self.bombs_left)
        self.bombs_left.set("16")
        self.score.pack()

        # Tkinter Board
        self.cells = []
        self.init_cells()

        self.generate_board()
        self.display_board()

    def init_cells(self):
        for row in range(self.WIDTH):
            self.cells.append([])

            for column in range(self.HEIGHT):

                button = Cell(self, self.top, row, column)
                self.cells[row].append(button)

    def left_cell_press(self, row, column):
        self.cells[row][column].uncover()
        print("left", row, column)

    def right_cell_press(self, row, column):
        print("right", row, column)

    def generate_board(self):
        bombs = self.BOMBS

        while bombs > 0:
            row = randint(0, self.WIDTH-1)
            column = randint(0, self.HEIGHT-1)

            if not self.cells[row][column].bomb:
                self.cells[row][column].bomb = True
                for i, j in product((-1, 1, 0), (-1, 1, 0)):
                    self.add_count(row, column, i, j)
                bombs -= 1

    def add_count(self, row, column, i, j):
        try:
            if row+i >= 0 and column+j >= 0:
                self.cells[row+i][column+j].neighboring_bombs += 1
        except (TypeError, IndexError):
            pass

    def display_board(self):
        for row in range(self.WIDTH):
            for column in range(self.HEIGHT):
                self.cells[row][column].show_text()





root = Tk()
minesweeper = Minesweeper(root)
root.mainloop()
