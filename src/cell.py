import tkinter as tk


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
        text_color (str): The default text color
        disabled (bool): Is the cell disabled?

    Methods:
        left_click: Called when a cell is left clicked
        right_click: Called when a cell is right clicked
        double_left_click: Called when a cell is double left clicked
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
        self.button.bind("<Button-1>", lambda event: self.left_click())
        self.button.bind("<Button-3>", lambda event: self.right_click())
        self.button.bind("<Double-Button-1>", lambda event: self.double_left_click())
        self.button.grid(row=row, column=column)
        self.background_color = self.button.cget("background")
        self.text_color = self.button.cget("foreground")

    def left_click(self):
        """ Left click event handler

        If the cell is uncovered, not flagged, and a bomb, then the game should end.
        Otherwise the cell should be uncovered.
        """

        if not self.disabled and not self.flagged and self.covered:
            if not self.minesweeper.generated_board:
                self.minesweeper.generate_board(self.row, self.column)
                self.uncover()
            elif self.bomb:
                self.minesweeper.end_game()
            else:
                self.uncover()
                self.minesweeper.has_won()

    def right_click(self):
        """ Right click event handler

        If the cell is covered, it should be flagged
        """
        if not self.disabled and self.covered:
            self.flag()

    def double_left_click(self):
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
            self.button.config(foreground=self.text_color)
            self.text.set("*")
        elif self.neighboring_bombs == 0:
            self.text.set("")
        else:
            if self.neighboring_bombs == 1:
                self.button.config(foreground="blue")
            elif self.neighboring_bombs == 2:
                self.button.config(foreground="green")
            elif self.neighboring_bombs == 3:
                self.button.config(foreground="red")
            elif self.neighboring_bombs == 4:
                self.button.config(foreground="#800080")  # purple
            elif self.neighboring_bombs == 5:
                self.button.config(foreground="black")
            elif self.neighboring_bombs == 6:
                self.button.config(foreground="#800000")  # maroon
            elif self.neighboring_bombs == 7:
                self.button.config(foreground="#808080")  # gray
            elif self.neighboring_bombs == 8:
                self.button.config(foreground="#40E0D0")  # turquoise
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
