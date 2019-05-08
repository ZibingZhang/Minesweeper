import tkinter as tk
from minesweeper import Minesweeper
from itertools import product


class Solver(Minesweeper):
    """ A solver for the minesweeper game.

    A solver that will assist in solving the minesweeper game using logical deduction.

    Attributes:
        root: The root window.
        active_cells: An ordered list of the cells that we are currently interested in,
            i.e. uncovered and not fully flagged.

    Overwritten Methods:
        bind_shortcuts: Binds the appropriate keyboard shortcuts.
        resize: Resize the board.
        generate_bombs: Randomly generates the bombs and updates the 2D cell array accordingly.
        new: Resets the game.
        uncover_neighbors: Uncovers neighboring cells.

    New Methods:
        flag_appropriate_cells: Flags cells which should obviously be flagged.
        neighboring_uncovered: Counts the number of neighboring uncovered cells.
    """
    def __init__(self, root):
        """ Initializes the object.

        Initializes the instance attributes as described above.

        Args:
            root: The root window.
        """
        super().__init__(root)

        # The current cells that we are interested in.
        self.active_cells = []

    def bind_shortcuts(self):
        """ Binds the appropriate keyboard shortcuts.

        Adds new key bindings which assist in solving the game.

        <Number-1> : Flags cells which should obviously be flagged.
        """
        super().bind_shortcuts()
        self.root.bind("1", lambda event: self.flag_appropriate_cells())

    def resize(self, rows, columns, bombs):
        """ Resize the board.

        Adds a message printed to console indicating the new number of rows, columns, and bombs.

        Args:
            rows: The new number of rows.
            columns: The new number of columns.
            bombs: The new number of bombs.
        """
        super().resize(rows, columns, bombs)
        print(f"NEW SIZE | Rows: {self.rows}, Columns: {self.columns}, Bombs: {self.bombs}")

    def new(self):
        """ Resets the game.

        Resets the active cells attribute.
        """
        super().new()
        self.active_cells = []

    def generate_bombs(self, initial_row, initial_column):
        """ Randomly generates the bombs.

        Adds a message to indicate that a new set of bombs has been generated.

        Args:
            initial_row: The row of the cell that should not border a bomb.
            initial_column: The column of the cell that should not border a bomb.
        """
        super().generate_bombs(initial_row, initial_column)
        print("BOMBS GENERATED")

    def uncover_neighbors(self, row, column):
        """ Uncovers neighboring cells.

        Adds the newly uncovered cells to the list of active cells if
            the number of neighboring bombs is greater than the number of neighboring flags, and
            the cell is not already in the list of active cells.

        Args:
            row: The row of the cell whose neighbors are being uncovered.
            column: The column of the cell whose neighbors are being uncovered.
        """
        super().uncover_neighbors(row, column)

        # We have a separate array that we will then merge with the already
        # active cells so we can deal with the logic of merging separately.
        new_active_cells = []

        for row_offset, column_offset in product((-1, 0, 1), (-1, 0, 1)):
            try:
                if self.cells[row + row_offset][column + column_offset].state == "uncovered" and \
                        row + row_offset >= 0 and column + column_offset >= 0 and \
                        self.neighboring_bombs(row + row_offset, column + column_offset) - \
                        self.neighboring_flags(row + row_offset, column + column_offset) > 0 and \
                        not self.cells[row + row_offset][column + column_offset] in new_active_cells and \
                        not self.cells[row + row_offset][column + column_offset] in self.active_cells:
                    new_active_cells.append(self.cells[row + row_offset][column + column_offset])
            except (TypeError, IndexError):
                pass

        # Merge the two arrays.
        if len(self.active_cells) == 0:
            self.active_cells = new_active_cells
        else:
            for new_cell in new_active_cells:
                for index, cell in enumerate(self.active_cells):
                    if new_cell.row < cell.row:
                        self.active_cells.insert(index, new_cell)
                        break
                    elif new_cell.row == cell.row and new_cell.column < cell.column:
                        self.active_cells.insert(index, new_cell)
                        break
                else:
                    self.active_cells.append(new_cell)

    def flag_appropriate_cells(self):
        """ Flags cells which should obviously be flagged.

        Cells where the number of neighboring bombs equals the number of neighboring uncovered cells
        plus the number of neighboring flags have only one option for where the remaining flags should go.
        """
        # If the game is over, do nothing.
        if self.game_over:
            return

        # Flag the appropriate cells and note their index.
        index_flagged = []
        for index, cell in enumerate(self.active_cells):
            if self.neighboring_bombs(cell.row, cell.column) == \
                    self.neighboring_flags(cell.row, cell.column) + self.neighboring_uncovered(cell.row, cell.column):
                index_flagged.append(index)
                for row_offset, column_offset in product((0, -1, 1), (0, -1, 1)):
                    try:
                        if not (row_offset == 0 and column_offset == 0) and \
                                cell.row + row_offset >= 0 and cell.column + column_offset >= 0 and \
                                self.cells[cell.row + row_offset][cell.column + column_offset].state == "covered":
                            self.cells[cell.row + row_offset][cell.column + column_offset].right_click()
                    except IndexError:
                        pass

        # Removes the fully flagged cells from the list of active cells.
        for index in reversed(index_flagged):
            del self.active_cells[index]

    def neighboring_uncovered(self, row, column):
        """ Counts the number of neighboring uncovered cells.

        Args:
            row: The row of the cell whose neighboring uncovered cells are being counted.
            column: The column of the cell whose neighboring uncovered cells are being counted.

        Returns:
             int: The number of neighboring uncovered cells.
        """
        empty = 0
        for row_offset, column_offset in product((0, -1, 1), (0, -1, 1)):
            try:
                if not (row_offset == 0 and column_offset == 0) and \
                        row + row_offset >= 0 and column + column_offset >= 0 and \
                        self.cells[row + row_offset][column+column_offset].state == "covered":
                    empty += 1
            except IndexError:
                pass
        return empty


root = tk.Tk()
solver = Solver(root)
root.mainloop()
