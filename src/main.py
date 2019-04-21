from tkinter import *
from random import randint


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
        self.button_labels = []

        # Actual Board
        self.board = []

        self.init_board()

        self.generate_board()
        self.display_board()

    def init_board(self):
        for row in range(self.WIDTH):
            self.cells.append([])
            self.button_labels.append([])
            self.board.append([])

            for column in range(self.HEIGHT):
                self.button_labels[row].append(StringVar())

                button = Button(self.top, width=2, textvariable=self.button_labels[row][column],
                                command=lambda row=row, column=column: self.cell_press(row, column))
                button.bind("<Button-1>", lambda event, row=row, column=column: self.left_cell_press(row, column))
                button.bind("<Button-3>", lambda event, row=row, column=column: self.right_cell_press(row, column))
                button.grid(row=row, column=column)
                self.cells[row].append(button)

                self.board[row].append(0)

    def cell_press(self, row, column):
        self.cells[row][column].config(relief=SUNKEN)

    def left_cell_press(self, row, column):
        print("left", row, column)

    def right_cell_press(self, row, column):
        print("right", row, column)

    def generate_board(self):
        bombs = self.BOMBS

        while bombs > 0:
            row = randint(0, self.WIDTH-1)
            column = randint(0, self.HEIGHT-1)

            if self.board[row][column] != "bomb":
                self.board[row][column] = "bomb"
                bombs -= 1

    def display_board(self):
        for row in range(self.WIDTH):
            for column in range(self.HEIGHT):
                if self.board[row][column] == "bomb":
                    print("Asdf")
                    self.button_labels[row][column].set("*")




root = Tk()
minesweeper = Minesweeper(root)
root.mainloop()
