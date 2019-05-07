import tkinter as tk


class Cell(object):
    """ A cell on the minesweeper board

    A cell on the minesweeper board. It includes the widget that is displayed and various
    other information regarding the cell.

    Attributes:
        minesweeper (Minesweeper): The minesweeper game object.
        row (int): The row of the cell.
        column (int): The column of the cell.
        state (string): The state of the string, one of: "covered", "uncovered", "flagged".
        is_bomb (bool): Is the cell a bomb?
        text (StringVar): The text displayed on the cell.
        button (Button): A button widget representing the cell.

    Methods:
        left_click: Left click event handler.
        right_click: Right click event handler.
        double_left_click: Double left click event handler.
        show_text: Displays the appropriate text for the cell.
        number_color: Returns the color of the given number.
        flag: Flags the cell.
        remove_flag: Removes the flag.
        reset: Resets the cell.
    """

    def __init__(self, minesweeper, parent, row, column):
        """ Initializes the object.

        Args:
            minesweeper: The Minesweeper object.
            parent: The parent widget.
            row: The row number.
            column: The column number.
        """
        self.minesweeper = minesweeper
        self.row = row
        self.column = column
        self.state = "covered"
        self.is_bomb = False
        self.text = tk.StringVar()

        self.button = tk.Button(parent, width=2, textvariable=self.text,
                                command=lambda: self.button.config(relief=tk.SUNKEN))
        self.button.grid(row=row, column=column)
        self.button.bind("<Button-1>", lambda event: self.left_click())
        self.button.bind("<Button-3>", lambda event: self.right_click())
        self.button.bind("<Double-Button-1>", lambda event: self.double_left_click())

    def left_click(self):
        """ Left click event handler.

        If the mines have not been generated, generate them.
        If the cell is flagged or uncovered, do nothing.
        If the cell is a bomb, end the game appropriately.
        If the cell is covered, uncover the cell.
            If the cell is "blank", uncover the surrounding cells.
            If the game is won, end the game appropriately.
        """
        if not self.minesweeper.generated_bombs:
            self.minesweeper.generate_bombs(self.row, self.column)

        if self.state == "flagged" or self.state == "uncovered":
            pass
        elif self.is_bomb:
            self.minesweeper.lose_game()
        elif self.state == "covered":
            self.state = "uncovered"
            self.show_text()

            if self.minesweeper.neighboring_bombs(self.row, self.column) == 0:
                self.minesweeper.uncover_neighbors(self.row, self.column)

            if self.minesweeper.has_won():
                self.minesweeper.win_game()

    def right_click(self):
        """ Right click event handler.

        If the cell is uncovered, do nothing.
        If the cell is covered, flag the cell.
        If the cell is flagged, remove the flag.
        """
        if self.state == "uncovered":
            pass
        elif self.state == "covered":
            self.flag()
        elif self.state == "flagged":
            self.remove_flag()

    def double_left_click(self):
        """ Double left click event handler.

        If the cell is flagged or covered, do nothing.
        If the cell is uncovered, and
            if the number of neighboring cells equals then number of neighboring bombs,
            uncover the neighboring cells.
        """
        if self.state == "covered" or self.state == "flagged":
            pass
        elif self.state == "uncovered":
            neighboring_flags = self.minesweeper.neighboring_flags(self.row, self.column)
            neighboring_bombs = self.minesweeper.neighboring_bombs(self.row, self.column)
            if neighboring_bombs == neighboring_flags:
                self.minesweeper.uncover_neighbors(self.row, self.column)

    def show_text(self):
        """ Displays the appropriate text for the cell.

        The text displayed varies on whether or not the cell is a bomb and
        the number of neighboring cells.
        """
        neighboring_bombs = self.minesweeper.neighboring_bombs(self.row, self.column)
        self.button.config(relief=tk.SUNKEN)

        if self.is_bomb:
            self.button.config(foreground="black")
            self.text.set("*")
        elif neighboring_bombs == 0:
            self.text.set("")
        else:
            self.button.config(foreground=self.number_color(neighboring_bombs))
            self.text.set(neighboring_bombs)

    @staticmethod
    def number_color(number):
        """ Returns the color of the given number.

        Args:
            number: The number of surrounding bombs.

        Returns:
            str: The color associated with the given number.
        """
        return {1: "blue",             # blue
                2: "green",            # green
                3: "red",              # red
                4: "#800080",          # purple
                5: "black",            # black
                6: "#800000",          # maroon
                7: "#808080",          # gray
                8: "#40E0D0"}[number]  # turquoise

    def flag(self):
        """ Flags the cell. """
        self.state = "flagged"
        self.button.config(background="red", state=tk.DISABLED)
        self.minesweeper.alter_counter(-1)

    def remove_flag(self):
        """ Removes the flag. """
        self.state = "covered"
        self.button.config(background="SystemButtonFace", state=tk.NORMAL)
        self.minesweeper.alter_counter(1)

    def reset(self):
        """ Resets the cell. """
        self.text.set("")
        self.state = "covered"
        self.is_bomb = False
        self.button.config(background="SystemButtonFace", relief=tk.RAISED, state=tk.NORMAL)
