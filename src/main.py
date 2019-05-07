import tkinter as tk
from minesweeper import Minesweeper
from itertools import product


class Solver(Minesweeper):

    def __init__(self, root):

        super().__init__(root)
        self.active_cells = []  # The current cells that we are interested in

    def generate_bombs(self, initial_row, initial_column):
        super().generate_bombs(initial_row, initial_column)
        # This causes some when the initial click is not empty, only happens during testing
        # since the first click should always be empty.
        super().uncover_neighbors(initial_row, initial_column)
        print("BOMBS GENERATED")
        for row in range(self.rows):
            for column in range(self.columns):
                if self.cells[row][column].state == "uncovered" and self.neighboring_bombs(row, column) > 0:
                    self.active_cells.append(self.cells[row][column])

    def resize(self, rows, columns, bombs):
        super().resize(rows, columns, bombs)
        print(f"NEW SIZE | Rows: {self.rows}, Columns: {self.columns}, Bombs: {self.bombs}")

    def bind_shortcuts(self):
        super().bind_shortcuts()
        self.root.bind("1", lambda event: self.flag_appropriate_cells())

    def flag_appropriate_cells(self):
        if self.game_over:
            return None

        index_flagged = []
        for index, cell in enumerate(self.active_cells):
            if self.neighboring_bombs(cell.row, cell.column) == \
                    self.neighboring_flags(cell.row, cell.column) + self.neighboring_empties(cell.row, cell.column):
                index_flagged.append(index)
                for row_offset, column_offset in product((0, -1, 1), (0, -1, 1)):
                    try:
                        if not (row_offset == 0 and column_offset == 0) and \
                                cell.row + row_offset >= 0 and cell.column + column_offset >= 0 and \
                                self.cells[cell.row + row_offset][cell.column + column_offset].state == "covered":
                            self.cells[cell.row + row_offset][cell.column + column_offset].right_click()
                    except IndexError:
                        pass

        for index in reversed(index_flagged):
            del self.active_cells[index]

    def neighboring_empties(self, row, column):
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

    def uncover_neighbors(self, row, column):
        super().uncover_neighbors(row, column)
        for row_offset, column_offset in product((-1, 0, 1), (-1, 0, 1)):
            try:
                if self.cells[row + row_offset][column + column_offset].state == "uncovered" and \
                        row + row_offset >= 0 and column + column_offset >= 0 and \
                        self.neighboring_bombs(row + row_offset, column + column_offset) > 0:
                    # Should be inserted, not just appended
                    self.active_cells.append(self.cells[row + row_offset][column + column_offset])
            except (TypeError, IndexError):
                pass


root = tk.Tk()
solver = Solver(root)
root.mainloop()
