from minesweeper import Minesweeper
from itertools import product
from math import sqrt


class Solver(Minesweeper):
    """ A solver for the minesweeper game.

    A solver that will assist in solving the minesweeper game using logical deduction.

    Attributes:
        root: The root window.
        active_cells: An ordered list of the cells that we are currently interested in,
            i.e. uncovered and not fully flagged,
            organized in a 2D array.
        updated: When solving, has the board made any progress?
        bombs_left: The number of bombs remaining.

    Overwritten Methods:
        bind_shortcuts: Binds the appropriate keyboard shortcuts.
        new: Resets the game.
        uncover_neighbors: Uncovers neighboring cells.
        alter_counter: Changes the counter by the increment to indicate the number of bombs remaining.

    New Methods:
        insert_active_cell: Inserts the cell into the 2D array of active cells.
        remove_active_cell: Removes the cell from the 2D array of active cells.
        list_active_cells: Returns a 1D array of all the active cells ordered by row then column.
        solve: Solves the minesweeper board as far as possible.
        flag_obvious_cells: Flags cells which should obviously be flagged.
        neighboring_uncovered: Counts the number of neighboring uncovered cells.
        left_click_obvious_cells: Left clicks cells which should obviously be uncovered.
        find_last_bomb: Attempts to find the location of the last bomb.
        are_adjacent: Are the two cells adjacent?
    """
    def __init__(self, root):
        """ Initializes the object.

        Initializes the instance attributes as described above.

        Args:
            root: The root window.
        """
        super().__init__(root)

        # The current cells that we are interested in organized in a 2D array.
        self.active_cells = [[None]*self.columns for row in range(self.rows)]
        self.updated = False
        self.bombs_left = self.bombs

    def bind_shortcuts(self):
        """ Binds the appropriate keyboard shortcuts.

        Adds new key bindings which assist in solving the game.

           <s>     : Solves the minesweeper board as far as possible.
        <Number-1> : Flags cells which should obviously be flagged.
        <Number-2> : Uncovers cells which should obviously be uncovered.
        """
        super().bind_shortcuts()
        self.root.bind("<s>", lambda event: self.solve())
        self.root.bind("1", lambda event: self.flag_obvious_cells())
        self.root.bind("2", lambda event: self.double_left_click_obvious_cells())
        self.root.bind("3", lambda event: self.find_last_bomb())

    def new(self):
        """ Resets the game.

        Resets the active cells attribute.
        """
        super().new()
        self.active_cells = [[None]*self.columns for row in range(self.rows)]
        self.bombs_left = self.bombs
        print("---------- New Round ----------")

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

        for row_offset, column_offset in product((-1, 0, 1), (-1, 0, 1)):
            try:
                if self.cells[row + row_offset][column + column_offset].state == "uncovered" and \
                        row + row_offset >= 0 and column + column_offset >= 0 and \
                        self.neighboring_bombs(row + row_offset, column + column_offset) - \
                        self.neighboring_flags(row + row_offset, column + column_offset) >= 0 and \
                        self.neighboring_uncovered(row + row_offset, column + column_offset) > 0 and \
                        not self.cells[row + row_offset][column + column_offset] in self.list_active_cells():
                    self.insert_active_cell(self.cells[row + row_offset][column + column_offset])
            except (TypeError, IndexError):
                pass

    def alter_counter(self, increment):
        """ Changes the counter by the increment to indicate the number of bombs remaining.

        Keeps track of the number of bombs remaining.

        Args:
            increment: The change to the counter.
        """
        super().alter_counter(increment)
        self.bombs_left += increment

    def insert_active_cell(self, insert_cell):
        """ Inserts the cell into the 2D array of active cells.

        Args:
            insert_cell: The new cell being inserted into the 2D array of active cells.
        """
        self.active_cells[insert_cell.row][insert_cell.column] = insert_cell

    def remove_active_cell(self, remove_cell):
        """ Removes the cell from the 2D array of active cells.

        Args:
            remove_cell: The cell to be removed from the 2D array of active cells.
        """
        self.active_cells[remove_cell.row][remove_cell.column] = None

    def list_active_cells(self):
        """ Returns a 1D array of all the active cells ordered by row then column.

        Returns:
             (List-of Cell): A 1D array of all the active cells ordered by row then column.
        """
        list_active_cells = []
        for row in self.active_cells:
            for cell in row:
                if cell is not None:
                    list_active_cells.append(cell)
        return list_active_cells

    def solve(self):
        """ Solves the minesweeper board as far as possible. """
        self.updated = True
        while self.updated and not self.game_over:
            self.updated = False
            self.flag_obvious_cells()
            self.double_left_click_obvious_cells()

            # if self.bombs_left == 1:
            #     self.find_last_bomb()

        message = self.message.get()
        if message == "You Win":
            print("You Win")
        elif message == "You Lose":
            print("You Lose")
        elif self.bombs_left > 0:
            print(f"Bombs Left: {self.bombs_left}")
        else:
            raise Exception("Impossible Game State")

    def flag_obvious_cells(self):
        """ Flags cells which should obviously be flagged.

        Cells where the number of neighboring bombs equals the number of neighboring uncovered cells
        plus the number of neighboring flags have only one option for where the remaining flags should go.
        """
        # If the game is over, do nothing.
        if self.game_over:
            return

        # Flag the appropriate cells and removes the appropriate cell (not the cell flagged)
        # off the list of active cells.
        for cell in self.list_active_cells():
            if self.neighboring_bombs(cell.row, cell.column) == \
                    self.neighboring_flags(cell.row, cell.column) + self.neighboring_uncovered(cell.row, cell.column):
                for row_offset, column_offset in product((0, -1, 1), (0, -1, 1)):
                    try:
                        current_cell = self.cells[cell.row + row_offset][cell.column + column_offset]
                        if not (row_offset == 0 and column_offset == 0) and \
                                cell.row + row_offset >= 0 and cell.column + column_offset >= 0 and \
                                current_cell.state == "covered":
                            current_cell.right_click()
                    except IndexError:
                        pass
                self.remove_active_cell(cell)
                self.updated = True

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
                        self.cells[row + row_offset][column + column_offset].state == "covered":
                    empty += 1
            except IndexError:
                pass
        return empty

    def double_left_click_obvious_cells(self):
        """ Left clicks cells which should obviously be uncovered.

        Covered cells around cells where the number of surrounding bombs equals
        the number of surrounding flags should be uncovered.
        """
        for cell in self.list_active_cells():
            if self.neighboring_flags(cell.row, cell.column) == self.neighboring_bombs(cell.row, cell.column):
                cell.double_left_click()
                self.remove_active_cell(cell)
                self.updated = True

    def find_last_bomb(self):
        """ Attempts to find the location of the last bomb.

        First make a list of covered cells.
        One by one, assume that each of the remaining covered cells is a bomb.
        If all the remaining active cells border this cell, then it might be the bomb.
            Note the combinations of "bomb" and "not bomb" which make this solution possible.
        Check all the possible combinations of "bomb" and "not bomb" and see if any cell
        is always not a bomb.
            Click said cells and add them to the list of active bombs.
        Solve the rest of the board.
        """
        # If there is not one bomb left, stop.
        if self.bombs_left != 1:
            return

        # The list of cells that might be the last bomb.
        covered_cells = []  # 1D array

        # A list of valid configurations for where the last bomb might be.
        # Each configuration is in the form of a 1D array, e.g. [0, 1, 0, 0],
        # where the 1 represents where the last bomb might be.
        valid_configuration = []  # 2D array

        # Find all the covered cells (not necessarily adjacent to active cells).
        for row in range(self.rows):
            for column in range(self.columns):
                if self.cells[row][column].state == "covered":
                    covered_cells.append(self.cells[row][column])

        # Check to see if each of the remaining covered cells could be the last bomb.
        for index, assume_cell in enumerate(covered_cells):
            for active_cell in self.list_active_cells():
                # If the cell we assume to be the bomb does not border any of the active
                # cells it must not be the last bomb. This is true since there is only one
                # bomb left, it must border all of the remaining active cells.
                if not self.are_adjacent(assume_cell, active_cell):
                    break
            else:
                # If the cell we assume to be the bomb borders all of the current active
                # cells, then the configuration of the cell to be a bomb and the remaining
                # covered cells to not be a bomb is a valid configuration.
                configuration = [True if cell == assume_cell else False for cell in covered_cells]
                valid_configuration.append(configuration)

        # If any of the cells, for all of the possible configurations, is not a bomb,
        # then it must not be a bomb and should be left clicked and added.
        # I.e, if any of the columns are all false, then it must not be a bomb.
        for index, cell in enumerate(covered_cells):
            if not any([valid_configuration[row][index] for row in range(len(valid_configuration))]):
                cell.left_click()
                self.insert_active_cell(cell)
                self.updated = True

        # Attempt to solve the rest of the board with the (hopefully) new information.
        self.solve()

    @staticmethod
    def are_adjacent(cell_1, cell_2):
        """ Are the two cells adjacent?

        Args:
            cell_1:
            cell_2:
        Returns:
            bool: Are the two cells adjacent?
        """
        return sqrt((cell_1.row - cell_2.row)**2 + (cell_1.column - cell_2.column)**2) < 1.5
