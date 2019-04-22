from random import randint
from itertools import product
from cell import Cell
import tkinter as tk


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
        generated_board (bool): Has the board been generated yet?
        menu_bar (Menu): The menu bar
        game_over (bool): Is the game over?

    Methods:
        init_cells: Initializes the 2D array of cells
        init_menu_bar: Initializes the menu bar
        reset: Resets the game
        generate_board: Randomly generates the bombs and updates the 2D cell array accordingly
        uncover_neighbors: Uncovers neighboring cells
        flag_neighbors: Adds one to neighboring cells flag counters
        unflag_neighbors: Removes one from neighboring cells flag counters
        end_game: Ends the game
        alter_counter: Updates the counter
    """

    PAD_X = 10
    PAD_Y = 10
    # ROWS = 9
    # COLUMNS = 9
    # BOMBS = 10
    ROWS = 16
    COLUMNS = 30
    BOMBS = 99

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
        self.bombs_left.set(str(self.BOMBS))
        self.bombs_left_label.pack()

        # Tkinter Board
        self.cells = []
        self.init_cells()

        # Menu Bar
        self.menu_bar = tk.Menu(self.root)
        self.init_menu_bar()
        self.root.config(menu=self.menu_bar)

        self.generated_board = False
        self.game_over = False

        # Bing Keyboard Shortcuts
        self.bind_shortcuts()

    def bind_shortcuts(self):
        self.root.bind("<Control-q>", lambda event: self.root.quit())
        self.root.bind("<Control-r>", lambda event: self.reset())

    def init_cells(self):
        """ Initializes the cells

        Initializes the cells into a 2D array. Each cell is a button, geometrically displayed
        as a grid.
        """
        for row in range(self.ROWS):
            self.cells.append([])
            for column in range(self.COLUMNS):
                button = Cell(self, self.top, row, column)
                self.cells[row].append(button)

    def init_menu_bar(self):
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.reset)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def reset(self):
        for row in range(self.ROWS):
            for column in range(self.COLUMNS):
                self.cells[row][column].reset()

        self.generated_board = False
        self.game_over = False

    def generate_board(self, r, c):
        """ Generates a board

        Generates the bombs randomly and the numbers for each cell

        :param r: The row of the cell that should not border a bomb
        :param c: The column of the cell that should not border a bomb
        """
        self.generated_board = True

        bombs = self.BOMBS

        while bombs > 0:
            row = randint(0, self.ROWS-1)
            column = randint(0, self.COLUMNS-1)

            if not self.cells[row][column].bomb and \
                    ((row-r)**2 + (column-c)**2)**0.5 > 1.5:
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
        """ Ends the game when the user has lost

        Removes all flags, presses all cells down, and displays all the cells.
        """
        for row in range(self.ROWS):
            for column in range(self.COLUMNS):
                self.cells[row][column].show()

        self.game_over = True
        self.bombs_left.set("You Lose")

    def alter_counter(self, increment):
        """ Changes the counter indicating the number of bombs remaining

        :param increment: The change to the counter
        """
        self.bombs_left.set(str(int(self.bombs_left.get()) + increment))

    def has_won(self):
        """ Ends the game when the user has won

        """
        total = self.ROWS*self.COLUMNS

        for row in range(self.ROWS):
            for column in range(self.COLUMNS):
                if self.cells[row][column].bomb:
                    total -= 1
                elif not self.cells[row][column].covered:
                    total -= 1

        if total == 0:
            for row in range(self.ROWS):
                for column in range(self.COLUMNS):
                    if self.cells[row][column].bomb and not self.cells[row][column].flagged:
                        self.cells[row][column].flag()

                    self.cells[row][column].button.config(state=tk.DISABLED)
                    self.cells[row][column].disabled = True

            self.bombs_left.set("You Win")
