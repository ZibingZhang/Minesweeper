import tkinter as tk
from random import randint
from itertools import product
from cell import Cell


class Minesweeper(object):
    """ The minesweeper game.

    The minesweeper game. It includes all the widgets for the GUI.

    Class Attributes:
        PAD_X (int): The amount of horizontal padding for the top and bottom half frames.
        PAD_Y (int): The amount of vertical padding for the top and bottom half frames.

    Instance Attributes:
        rows (int): The number of cells, vertically, for the minesweeper game.
        columns (int): The number of cells, horizontally, for the minesweeper game.
        bombs (int): The number of bombs on the board.
        root (Tk): The root window.
        top (Frame): The top half of the window, the part where the game is played.
        bottom (Frame): The bottom half of the window, the part where information is displayed.
        menu_bar (Menu): The menu bar.
        bombs_left (StringVar): The number of bombs left.
        bombs_left_label (Label): The widget where the number of bombs left is displayed.
        cells (List-of (List-of Cell)): 2D array of all the Cell objects.
        generated_board (bool): Has the board been generated yet?
        game_over (bool): Is the game over?

    Methods:
        bind_shortcuts: Binds the appropriate keyboard shortcuts.

        !!! to be redesigned and rewritten !!!
        size_small
        size_medium
        size_large

        generate_cells: Generates the 2D array of cells.
        create_menu_bar: Creates the menu bar.
        new: Resets the game.
        generate_board: Randomly generates the bombs and updates the 2D cell array accordingly.
        uncover_neighbors: Uncovers neighboring cells.
        neighboring_bombs: Counts the number of neighboring bombs.
        neighboring_flags: Counts the number of neighboring flags.
        lose_game: Lose the game.
        win_game: Win the game.
        has_won: Has the user won the game?
        alter_counter: Updates the counter.
    """

    PAD_X = 10
    PAD_Y = 10

    def __init__(self, root):
        """ Initializes the object

        Args:
            root: The root window
        """

        # Board size
        self.rows = 9
        self.columns = 9
        self.bombs = 10

        # Two halves of the screen
        self.root = root
        self.root.title("Minesweeper")
        self.root.resizable(False, False)
        self.top = tk.Frame(root, padx=self.PAD_X, pady=self.PAD_Y)
        self.top.pack(side=tk.TOP)
        self.bottom = tk.Frame(root, padx=self.PAD_X, pady=self.PAD_Y)
        self.bottom.pack(side=tk.BOTTOM)

        # Menu Bar
        self.menu_bar = tk.Menu(self.root)
        self.create_menu_bar()
        self.root.config(menu=self.menu_bar)

        # Footer
        self.bombs_left = tk.StringVar()
        self.bombs_left_label = tk.Label(self.bottom, textvariable=self.bombs_left)
        self.bombs_left.set(str(self.bombs))
        self.bombs_left_label.pack()

        # Tkinter Board
        self.cells = []
        self.generate_cells()

        self.generated_board = False
        self.game_over = False

        # Keyboard Shortcuts
        self.bind_shortcuts()

    def bind_shortcuts(self):
        """ Binds the appropriate keyboard shortcuts.

        Ctrl-q exits the game.
        Ctrl-n or F2 starts a new game.
        Ctrl-z starts a new game with a small sized board.
        Ctrl-x starts a new game with a medium sized board.
        Ctrl-c starts a new game with a large sized board.
        """

        self.root.bind("<Control-q>", lambda event: self.root.destroy())
        self.root.bind("<Control-n>", lambda event: self.new())
        self.root.bind("<F2>", lambda event: self.new())
        self.root.bind("<Control-z>", lambda event: self.size_small())
        self.root.bind("<Control-x>", lambda event: self.size_medium())
        self.root.bind("<Control-c>", lambda event: self.size_large())

    def size_small(self):
        self.rows = 9
        self.columns = 9
        self.bombs = 10
        self.generate_cells()
        self.bombs_left.set(self.bombs)
        self.new()

    def size_medium(self):
        self.rows = 16
        self.columns = 16
        self.bombs = 40
        self.generate_cells()
        self.bombs_left.set(self.bombs)
        self.new()

    def size_large(self):
        self.rows = 16
        self.columns = 30
        self.bombs = 99
        self.generate_cells()
        self.bombs_left.set(self.bombs)
        self.new()

    def generate_cells(self):
        """ Generates the 2D array of cells.

        Destroys the old cells and creates a new 2D array of cells.
        """

        for row in self.cells:
            for cell in row:
                cell.button.destroy()

        self.cells = []
        for row in range(self.rows):
            self.cells.append([])
            for column in range(self.columns):
                button = Cell(self, self.top, row, column)
                self.cells[row].append(button)

    def create_menu_bar(self):
        """ Creates the menu bar. """

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new)

        # create more pull down menus
        size_menu = tk.Menu(file_menu, tearoff=0)
        size_menu.add_command(label="Small", command=self.size_small)
        size_menu.add_command(label="Medium", command=self.size_medium)
        size_menu.add_command(label="Large", command=self.size_large)
        file_menu.add_cascade(label="Size", menu=size_menu)

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def new(self):
        """ Resets the game. """

        for row in range(self.rows):
            for column in range(self.columns):
                self.cells[row][column].reset()

        self.generated_board = False
        self.game_over = False
        self.bombs_left.set(self.bombs)

    def generate_board(self, initial_row, initial_column):
        """ Randomly generates the bombs and updates the 2D cell array accordingly.

        Generates the bombs such that they do not they do not border the first cell clicked.

        Args:
            initial_row: The row of the cell that should not border a bomb.
            initial_column: The column of the cell that should not border a bomb.
        """

        self.generated_board = True

        bombs = self.bombs

        while bombs > 0:
            row = randint(0, self.rows-1)
            column = randint(0, self.columns-1)

            if not self.cells[row][column].is_bomb and \
                    ((row-initial_row)**2 + (column-initial_column)**2)**0.5 > 1.5:
                self.cells[row][column].is_bomb = True
                bombs -= 1

    def uncover_neighbors(self, row, column):
        """ Uncovers neighboring cells.

        Uncovers the neighbors of the cell at the position given by row and column.

        Args:
            row: The row of the cell whose neighbors are being uncovered.
            column: The column of the cell whose neighbors are being uncovered.
        """

        for row_offset, column_offset in product((-1, 0, 1), (-1, 0, 1)):
            try:
                if self.cells[row + row_offset][column + column_offset].state == "covered" and \
                        row + row_offset >= 0 and column + column_offset >= 0:
                    self.cells[row + row_offset][column + column_offset].left_click()
            except (TypeError, IndexError):
                pass

    def neighboring_bombs(self, row, column):
        """ Counts the number of neighboring bombs.

        Args:
            row: The row of the cell whose neighboring bombs are being counted.
            column: The column of the cell whose neighboring bombs are being counted.

        Returns:
            int: The number of neighboring bombs.
        """

        bombs = 0
        for row_offset, column_offset in product((0, -1, 1), (0, -1, 1)):
            try:
                if not (row_offset == 0 and column_offset == 0) and \
                        row + row_offset >= 0 and column + column_offset >= 0 and \
                        self.cells[row + row_offset][column+column_offset].is_bomb:
                    bombs += 1
            except IndexError:
                pass
        return bombs

    def neighboring_flags(self, row, column):
        """ Counts the number of neighboring flags.

        Args:
            row: The row of the cell whose neighboring flags are being counted.
            column: The column of the cell whose neighboring flags are being counted.

        Returns:
            int: The number of neighboring flags.
        """

        flags = 0
        for row_offset, column_offset in product((0, -1, 1), (0, -1, 1)):
            try:
                if not (row_offset == 0 and column_offset == 0) and \
                        row + row_offset >= 0 and column + column_offset >= 0 and \
                        self.cells[row + row_offset][column + column_offset].state == "flagged":
                    flags += 1
            except IndexError:
                pass
        return flags

    def lose_game(self):
        """ Lose the game.

        Removes all flags, presses all cells down, and displays all the cells.
        """

        for row in range(self.rows):
            for column in range(self.columns):
                self.cells[row][column].show_text()
                self.cells[row][column].remove_flag()

        self.game_over = True
        self.bombs_left.set("You Lose")

    def alter_counter(self, increment):
        """ Changes the counter by the increment to indicate the number of bombs remaining.

        Args:
            increment: The change to the counter.
        """

        self.bombs_left.set(str(int(self.bombs_left.get()) + increment))

    def has_won(self):
        """ Has the user won the game?

        Is the total number of uncovered cells plus the number of cells that are bombs
        equal to the total number of cells?

        Returns:
            bool: Has the user won the game?
        """

        total = self.rows*self.columns

        for row in range(self.rows):
            for column in range(self.columns):
                if self.cells[row][column].is_bomb:
                    total -= 1
                elif not self.cells[row][column].state == "covered":
                    total -= 1

        return total == 0

    def win_game(self):
        """ Win the game.

        Flags the remaining bombs that have not yet been flagged
        """
        for row in range(self.rows):
            for column in range(self.columns):
                if self.cells[row][column].is_bomb and not self.cells[row][column].state == "flagged":
                    self.cells[row][column].flag()

        self.bombs_left.set("You Win")
