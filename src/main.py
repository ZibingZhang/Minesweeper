import tkinter as tk
from random import randint
from itertools import product


class Cell(object):
    """ A cell on the minesweeper board

    A cell on the minesweeper board. It includes the widget that is displayed and various
    other information regarding the cell.

    Attributes:
        row (int): The row of the cell
        column (int): The column of the cell
        text (StringVar): The text displayed on the cell
        button (Button): A button widget representing the cell
        bomb (bool): Is the cell a bomb?
        flagged (bool): Is the cell flagged?
        covered (bool): Is the cell hidden?
        neighboring_bombs (int): The number of neighboring bombs
        neighboring_flags (int): The number of neighboring flags
        minesweeper (Minesweeper): The minesweeper game object
        background_color (str): The default background color

    Methods:
        left_cell_press: Called when a cell is left clicked
        right_cell_press: Called when a cell is right clicked
        double_left_cell_press: Called when a cell is double left clicked
        hold_down: Keeps the button pressed on left mouse click
        show_text: Shows the text of the cell
        uncover: Uncovers the cell and the surrounding cells
        flag: Alters the flagged state of the cell
        show: Uncovers just this cell
    """

    def __init__(self, minesweeper, parent, row, column):
        """ Initializes the object

        :param minesweeper: The Minesweeper object
        :param parent: The parent widget
        :param row: The row number
        :param column: The column number
        """

        self.row = row
        self.column = column
        self.text = tk.StringVar()
        self.bomb = False
        self.flagged = False
        self.covered = True
        self.neighboring_bombs = 0
        self.neighboring_flags = 0
        self.minesweeper = minesweeper

        self.button = tk.Button(parent, width=2, textvariable=self.text,
                                command=lambda: self.hold_down())
        self.button.bind("<Button-1>", lambda event: self.left_cell_press())
        self.button.bind("<Button-3>", lambda event: self.right_cell_press())
        self.button.bind("<Double-Button-1>", lambda event: self.double_left_cell_press())
        self.button.grid(row=row, column=column)

        self.background_color = self.button.cget("background")

    def left_cell_press(self):
        """ Left click event handler

        If the cell is uncovered, not flagged, and a bomb, then the game should end.
        Otherwise the cell should be uncovered.
        """
        if self.covered and not self.flagged:
            if self.bomb:
                self.minesweeper.end_game()
            else:
                self.uncover()

    def right_cell_press(self):
        """ Right click event handler

        If the cell is covered, it should be flagged
        """
        if self.covered:
            self.flag()

    def double_left_cell_press(self):
        """ Double left click event handler

        If the number of neighboring cells equals then number of neighboring bombs,
        uncover the neighboring cells.
        """
        if self.neighboring_flags == self.neighboring_bombs:
            self.minesweeper.uncover_neighbors(self.row, self.column)

    def hold_down(self):
        """ Ensures that the cell stays pressed when clicked

        """
        if not self.flagged:
            self.button.config(relief=tk.SUNKEN)

    def show_text(self):
        """ Displays the text of the cell

        The text displayed varies on whether or not the cell is a bomb and
        the number of neighboring cells.
        """
        if self.bomb:
            self.text.set("*")
        elif self.neighboring_bombs == 0:
            self.text.set("")
        else:
            self.text.set(int(self.neighboring_bombs))

    def uncover(self):
        """ Uncovers the cell

        Uncovers the cell if it is not flagged. Will end the game if the cell is a bomb.
        Also uncovers the neighbors of the cell if the cell is empty.
        """
        if not self.flagged:
            if self.bomb:
                self.minesweeper.end_game()
            else:
                self.covered = False
                self.hold_down()
                self.show_text()
                if self.neighboring_bombs == 0:
                    self.minesweeper.uncover_neighbors(self.row, self.column)

    def flag(self):
        """ Changes the flagged state of the cell

        Reverses whether the cell is flagged or not, updates the cell background color accordingly.
        Also updates the number of bombs left on the bottom of the screen.
        """
        if not self.flagged:
            self.flagged = True
            self.button.config(background="red")
            self.minesweeper.flag_neighbors(self.row, self.column)
            self.minesweeper.alter_counter(-1)
        else:
            self.flagged = False
            self.button.config(background=self.background_color)
            self.minesweeper.unflag_neighbors(self.row, self.column)
            self.minesweeper.alter_counter(1)

    def show(self):
        """ Shows the cell

        Unflags the cell, presses it down, and displays its contents. Meant for when the game
        has been lost.
        """
        if self.flagged:
            self.flag()
        self.covered = False
        self.hold_down()
        self.show_text()


class Minesweeper(object):
    """ The minesweeper game.

    The minesweeper game. It includes all the widgets for the GUI.

    Class Attributes:
        PAD_X (int): The amount of horizontal padding for the top and bottom half frames
        PAD_Y (int): The amount of vertical padding for the top and bottom half frames
        WIDTH (int): The number of cells, horizontally, for the minesweeper game
        HEIGHT (int): The number of cells, vertically, for the minesweeper game
        BOMBS (int): The number of bombs on the board

    Instance Attributes:
        root (Tk): The root window
        top (Frame): The top half of the window, the part where the game is played
        bottom (Frame): The bottom half of the window, the part where information is displayed
        bombs_left (StringVar): The number of bombs left
        bombs_left_label (Label): The widget where the number of bombs left is displayed
        cells (List-of (List-of Cell)): 2D array of all the Cell objects

    Methods:
        init_cells: Initializes the 2D array of cells
        generate_board: Randomly generates the bombs and updates the 2D cell array accordingly
        uncover_neighbors: Uncovers neighboring cells
        flag_neighbors: Adds one to neighboring cells flag counters
        unflag_neighbors: Removes one from neighboring cells flag counters
        end_game: Ends the game
        alter_counter: Updates the counter
    """

    PAD_X = 10
    PAD_Y = 10
    WIDTH = 9
    HEIGHT = 9
    BOMBS = 16

    def __init__(self, root):
        """ Initializes the object

        :param root: The root window
        """
        # Two halves of the screen
        self.root = root
        self.root.resizable(False, False)
        self.top = tk.Frame(root, padx=self.PAD_X, pady=self.PAD_Y)
        self.top.pack(side=tk.TOP)
        self.bottom = tk.Frame(root, padx=self.PAD_X, pady=self.PAD_Y)
        self.bottom.pack(side=tk.BOTTOM)

        # Footer
        self.bombs_left = tk.StringVar()
        self.bombs_left_label = tk.Label(self.bottom, textvariable=self.bombs_left)
        self.bombs_left.set("16")
        self.bombs_left_label.pack()

        # Tkinter Board
        self.cells = []
        self.init_cells()

        self.generate_board()

    def init_cells(self):
        """ Initializes the cells

        Initializes the cells into a 2D array. Each cell is a button, geometrically displayed
        as a grid.
        """
        for row in range(self.WIDTH):
            self.cells.append([])
            for column in range(self.HEIGHT):
                button = Cell(self, self.top, row, column)
                self.cells[row].append(button)

    def generate_board(self):
        """ Generates a board

        Generates the bombs randomly and the numbers for each cell
        """
        bombs = self.BOMBS

        while bombs > 0:
            row = randint(0, self.WIDTH-1)
            column = randint(0, self.HEIGHT-1)

            if not self.cells[row][column].bomb:
                self.cells[row][column].bomb = True
                for i, j in product((-1, 1, 0), (-1, 1, 0)):
                    try:
                        if row + i >= 0 and column + j >= 0:
                            self.cells[row + i][column + j].neighboring_bombs += 1
                    except (TypeError, IndexError):
                        pass
                bombs -= 1

    def uncover_neighbors(self, row, column):
        """ Uncovers the cells neighbors

        Uncovers the neighbors of the cell at the position given by row and column.

        :param row: The row of the cell
        :param column: The column of the cell
        """
        for i, j in product((-1, 0, 1), (-1, 0, 1)):
            try:
                if self.cells[row + i][column + j].covered and \
                        row + i >= 0 and column + j >= 0:
                    self.cells[row + i][column + j].uncover()
            except (TypeError, IndexError):
                pass

    def flag_neighbors(self, row, column):
        """ Adds one to the flag counter of the cells neighbors

        Adds one to the flag counter of the neighbors of the cell at
        the position given by row and column.

        :param row: The row of the cell
        :param column: The column of the cell
        """
        for i, j in product((-1, 0, 1), (-1, 0, 1)):
            try:
                if row + i >= 0 and column + j >= 0:
                    self.cells[row + i][column + j].neighboring_flags += 1
            except (TypeError, IndexError):
                pass

    def unflag_neighbors(self, row, column):
        """ Subtracts one from the flag counter of the cells neighbors

        Subtracts one from the flag counter of the neighbors of the cell at
        the position given by row and column.

        :param row: The row of the cell
        :param column: The column of the cell
        """
        for i, j in product((-1, 0, 1), (-1, 0, 1)):
            try:
                if row + i >= 0 and column + j >= 0:
                    self.cells[row + i][column + j].neighboring_flags -= 1
            except (TypeError, IndexError):
                pass

    def end_game(self):
        """ Ends the game

        Removes all flags, presses all cells down, and displays all the cells.
        """
        for row in range(self.WIDTH):
            for column in range(self.HEIGHT):
                self.cells[row][column].show()

    def alter_counter(self, increment):
        """ Changes the counter indicating the number of bombs remaining

        :param increment: The change to the counter
        """
        self.bombs_left.set(str(int(self.bombs_left.get()) + increment))


root = tk.Tk()
minesweeper = Minesweeper(root)
root.mainloop()
