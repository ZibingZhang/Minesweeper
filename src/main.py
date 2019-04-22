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
        disabled (bool): Is the cell disabled?

    Methods:
        left_cell_press: Called when a cell is left clicked
        right_cell_press: Called when a cell is right clicked
        double_left_cell_press: Called when a cell is double left clicked
        hold_down: Keeps the button pressed on left mouse click
        show_text: Shows the text of the cell
        uncover: Uncovers the cell and the surrounding cells
        flag: Alters the flagged state of the cell
        show: Uncovers just this cell
        reset: Resets the cell
    """

    def __init__(self, minesweeper, parent, row, column):
        """ Initializes the object

        :param minesweeper: The Minesweeper object
        :param parent: The parent widget
        :param row: The row number
        :param column: The column number
        """

        self.minesweeper = minesweeper
        self.row = row
        self.column = column

        self.covered = True
        self.bomb = False
        self.flagged = False
        self.disabled = False

        self.neighboring_bombs = 0
        self.neighboring_flags = 0

        self.text = tk.StringVar()
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

        if not self.disabled and not self.flagged:
            if not self.minesweeper.generated_board:
                self.minesweeper.generate_board(self.row, self.column)
                self.uncover()
            elif self.bomb:
                self.minesweeper.end_game()
            elif self.covered:
                self.uncover()
                self.minesweeper.has_won()

    def right_cell_press(self):
        """ Right click event handler

        If the cell is covered, it should be flagged
        """
        if not self.disabled and self.covered:
            self.flag()

    def double_left_cell_press(self):
        """ Double left click event handler

        If the number of neighboring cells equals then number of neighboring bombs,
        uncover the neighboring cells.
        """
        if not self.disabled and not self.covered and \
                self.neighboring_flags == self.neighboring_bombs:
            self.minesweeper.uncover_neighbors(self.row, self.column)

        if not self.minesweeper.game_over:
            self.minesweeper.has_won()

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
            self.text.set(self.neighboring_bombs)

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
        if self.flagged:
            self.flagged = False
            self.button.config(background=self.background_color, state=tk.NORMAL)
            self.minesweeper.unflag_neighbors(self.row, self.column)
            self.minesweeper.alter_counter(1)
        else:
            self.flagged = True
            self.button.config(background="red", state=tk.DISABLED)
            self.minesweeper.flag_neighbors(self.row, self.column)
            self.minesweeper.alter_counter(-1)

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
        self.disabled = True

    def reset(self):
        self.text.set("")
        self.bomb = False
        self.flagged = False
        self.covered = True
        self.disabled = False
        self.neighboring_bombs = 0
        self.neighboring_flags = 0

        self.button.config(relief=tk.RAISED, background=self.background_color, state=tk.NORMAL)
        self.minesweeper.bombs_left.set(self.minesweeper.BOMBS)


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
    WIDTH = 9
    HEIGHT = 9
    BOMBS = 10

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
        for row in range(self.WIDTH):
            self.cells.append([])
            for column in range(self.HEIGHT):
                button = Cell(self, self.top, row, column)
                self.cells[row].append(button)

    def init_menu_bar(self):
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.reset)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def reset(self):
        for row in range(self.WIDTH):
            for column in range(self.HEIGHT):
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
            row = randint(0, self.WIDTH-1)
            column = randint(0, self.HEIGHT-1)

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
        for row in range(self.WIDTH):
            for column in range(self.HEIGHT):
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
        total = self.WIDTH*self.HEIGHT

        for row in range(self.WIDTH):
            for column in range(self.HEIGHT):
                if self.cells[row][column].bomb:
                    total -= 1
                elif not self.cells[row][column].covered:
                    total -= 1

        if total == 0:
            for row in range(self.WIDTH):
                for column in range(self.HEIGHT):
                    if self.cells[row][column].bomb and not self.cells[row][column].flagged:
                        self.cells[row][column].flag()

                    self.cells[row][column].button.config(state=tk.DISABLED)
                    self.cells[row][column].disabled = True

            self.bombs_left.set("You Win")


root = tk.Tk()
minesweeper = Minesweeper(root)
root.mainloop()
