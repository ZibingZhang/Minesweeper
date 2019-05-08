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
        message (StringVar): The message being displayed at the bottom.
        message_label (Label): The widget where the number of bombs left is displayed.
        cells (List-of (List-of Cell)): 2D array of all the Cell objects.
        generated_bombs (bool): Has the bombs been generated yet?
        game_over (bool): Is the game over?

    Methods:
        bind_shortcuts: Binds the appropriate keyboard shortcuts.
        resize: Resize the board.
        create_menu_bar: Creates the menu bar.
        new: Resets the game.
        generate_bombs: Randomly generates the bombs and updates the 2D cell array accordingly.
        uncover_neighbors: Uncovers neighboring cells.
        neighboring_bombs: Counts the number of neighboring bombs.
        neighboring_flags: Counts the number of neighboring flags.
        alter_counter: Updates the counter.
        has_won: Has the user won the game?
        win_game: Win the game.
        lose_game: Lose the game.
    """
    PAD_X = 10
    PAD_Y = 10

    def __init__(self, root):
        """ Initializes the object.

        Initializes the instance attributes as described above.
        Generates the GUI components for the game, namely the two halves and the menu bar.
            The top half includes the 2D array of buttons that represents the cells.
            The bottom half includes the display message which indicates how many bombs are left or if the game is over.
            The menu bar has options to restart, change the size, and exit.
        Binds shortcuts to various key combinations as described below.

        Args:
            root: The root window.
        """
        self.root = root

        # Board size
        self.rows = 9
        self.columns = 9
        self.bombs = 10

        # Window Settings
        self.root.title("Minesweeper")
        self.root.resizable(False, False)

        # Two halves of the screen
        self.top = tk.Frame(root, padx=self.PAD_X, pady=self.PAD_Y)
        self.top.pack(side=tk.TOP)
        self.bottom = tk.Frame(root, padx=self.PAD_X, pady=self.PAD_Y)
        self.bottom.pack(side=tk.BOTTOM)

        # Menu Bar
        self.menu_bar = tk.Menu(self.root)
        self.create_menu_bar()
        self.root.config(menu=self.menu_bar)

        # Footer
        self.message = tk.StringVar()
        self.message_label = tk.Label(self.bottom, textvariable=self.message)
        self.message.set(str(self.bombs))
        self.message_label.pack()

        # Tkinter Board
        self.cells = []
        for row in range(self.rows):
            self.cells.append([])
            for column in range(self.columns):
                button = Cell(self, self.top, row, column)
                self.cells[row].append(button)

        self.generated_bombs = False
        self.game_over = False

        # Keyboard Shortcuts
        self.bind_shortcuts()

    def bind_shortcuts(self):
        """ Binds the appropriate keyboard shortcuts.

        <Ctrl-q> : exits the game.
        <Ctrl-n> : or F2 starts a new game.
        <Ctrl-z> : starts a new game with a small sized board.
        <Ctrl-x> : starts a new game with a medium sized board.
        <Ctrl-c> : starts a new game with a large sized board.
        """
        self.root.bind("<Control-q>", lambda event: self.root.destroy())
        self.root.bind("<Control-n>", lambda event: self.new())
        self.root.bind("<F2>", lambda event: self.new())
        self.root.bind("<Control-z>", lambda event: self.resize(9, 9, 10))
        self.root.bind("<Control-x>", lambda event: self.resize(16, 16, 40))
        self.root.bind("<Control-c>", lambda event: self.resize(16, 30, 99))

    def create_menu_bar(self):
        """ Creates the menu bar. """
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new)

        # create more pull down menus
        size_menu = tk.Menu(file_menu, tearoff=0)
        size_menu.add_command(label="Small", command=lambda: self.resize(9, 9, 10))
        size_menu.add_command(label="Medium", command=lambda: self.resize(16, 16, 40))
        size_menu.add_command(label="Large", command=lambda: self.resize(16, 30, 99))
        file_menu.add_cascade(label="Size", menu=size_menu)

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def resize(self, rows, columns, bombs):
        """ Resize the board.

        Args:
            rows: The new number of rows.
            columns: The new number of columns.
            bombs: The new number of bombs.
        """
        for row in range(self.rows):
            for column in range(self.columns):
                self.cells[row][column].button.destroy()

        self.cells = []
        self.rows = rows
        self.columns = columns
        self.bombs = bombs
        self.message.set(self.bombs)

        for row in range(self.rows):
            self.cells.append([])
            for column in range(self.columns):
                self.cells[row].append(Cell(self, self.top, row, column))

        self.new()

    def new(self):
        """ Resets the game. """
        for row in range(self.rows):
            for column in range(self.columns):
                self.cells[row][column].reset()

        self.generated_bombs = False
        self.game_over = False
        self.message.set(self.bombs)

    def generate_bombs(self, initial_row, initial_column):
        """ Randomly generates the bombs and updates the 2D cell array accordingly.

        Generates the bombs such that they do not they do not border the first cell clicked.

        Args:
            initial_row: The row of the cell that should not border a bomb.
            initial_column: The column of the cell that should not border a bomb.
        """
        # self.generated_bombs = True
        # bombs = self.bombs
        #
        # while bombs > 0:
        #     row = randint(0, self.rows-1)
        #     column = randint(0, self.columns-1)
        #
        #     if not self.cells[row][column].is_bomb and \
        #             ((row-initial_row)**2 + (column-initial_column)**2)**0.5 > 1.5:
        #         self.cells[row][column].is_bomb = True
        #         bombs -= 1

        # Test Case - 3 bombs left
        # -------------------------------
        self.generated_bombs = True
        self.cells[2][4].is_bomb = True
        self.cells[3][0].is_bomb = True
        self.cells[4][1].is_bomb = True
        self.cells[5][2].is_bomb = True
        self.cells[5][4].is_bomb = True
        self.cells[5][8].is_bomb = True
        self.cells[6][0].is_bomb = True
        self.cells[7][0].is_bomb = True
        self.cells[7][1].is_bomb = True
        self.cells[7][7].is_bomb = True

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
        # Unable to see the number of the cell unless it is uncovered.
        assert self.cells[row][column].state == "uncovered"
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

    def alter_counter(self, increment):
        """ Changes the counter by the increment to indicate the number of bombs remaining.

        Args:
            increment: The change to the counter.
        """
        try:
            self.message.set(int(self.message.get()) + increment)
        except ValueError:
            # Not sure why it sometimes throws errors...
            pass

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

        self.game_over = True
        self.message.set("You Win")

    def lose_game(self):
        """ Lose the game.

        Removes all flags, presses all cells down, and displays all the cells.
        """
        for row in range(self.rows):
            for column in range(self.columns):
                self.cells[row][column].state = "uncovered"
                self.cells[row][column].show_text()
                self.cells[row][column].remove_flag()

        self.game_over = True
        self.message.set("You Lose")
