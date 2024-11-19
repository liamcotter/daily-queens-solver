from itertools import batched

class Board:
    def __init__(self):
        self.QUEEN = 0 # index
        self.NULL = 1 # index
        
    def __str__(self):
        """Printable representation of the board. Numbers are converted to letters for better readability."""
        colours = ['Q', 'X', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        return '\n'.join([' '.join([colours[cell] for cell in row]) for row in self.board]) + "\n"

       
class ParentBoard(Board):
    def __init__(self, size: int, board: list):
        """Each board is size x size, with size different regions. Size must be a natural number."""
        assert 4 <= size <= 10, f"Size is {size}"
        assert size*size == len(board), f"Board is {len(board)} elements long, but should be {size*size}"
        super().__init__()

        self.size = size
        self.queen_count = 0
        self.board = [board[size*i:size*(i+1)] for i in range(size)]
        self.subBoards = []
        for col in range(2, self.size+2):
            self.subBoards.append(subBoard(size, self, col))
        
        self.pattern_board = {}

    def eliminated_tile_count(self) -> int:
        """Returns the number of eliminated tiles to check for differences."""
        eliminated_tile_count = 0
        for row in self.board:
            for tile in row:
                if tile == 1:
                    eliminated_tile_count += 1
        return eliminated_tile_count
    
    def replace_tile(self, tile: tuple[int, int], colour: int):
        """Replaces a tile, for use after clearing the rest of the row."""
        self.board[tile[0]][tile[1]] = colour
    
    def place_queen(self, tile: tuple[int, int]):
        """Places a queen on the board and nullifies the incompatible tiles."""
        self.eliminate_row(tile[0])
        self.eliminate_col(tile[1])
        self.eliminate_tile(tile[0]-1, tile[1]-1) # corners
        self.eliminate_tile(tile[0]-1, tile[1]+1)
        self.eliminate_tile(tile[0]+1, tile[1]-1)
        self.eliminate_tile(tile[0]+1, tile[1]+1)

        self.board[tile[0]][tile[1]] = self.QUEEN
        self.queen_count += 1
    
    def eliminate_row(self, row: int):
        """Eliminates a row from all boards."""
        self.board[row] = [self.NULL for _ in range(self.size)]
        for subBoard in self.subBoards:
            subBoard.eliminate_row_sub(row)
    
    def eliminate_col(self, col: int):
        """Eliminates a column from all boards."""
        for row in self.board:
            row[col] = self.NULL
        for subBoard in self.subBoards:
            subBoard.elimiate_col_sub(col)
    
    def eliminate_tile(self, row: int, col: int):
        """Eliminates one specified tile on all boards."""
        if 0 <= row < self.size and 0 <= col < self.size:
            self.board[row][col] = self.NULL
            for subBoard in self.subBoards:
                subBoard.eliminate_tile_sub(row, col)
    
    def solve(self):
        """Initiates the solve."""
        while self.queen_count < self.size:
            for subBoard in self.subBoards:
                if subBoard.pattern_match():
                    break   # restart the loop after an update
            # also check for solid rows/columns?
            print(self)
            print(self.queen_count, self.size)
    
    def add_PatternBoard(self, pattern: 'PatternBoard'):
        """Adds a pattern to the board."""
        self.pattern_board[pattern.custom_hash()] = pattern.custom_sol()


class subBoard(Board):
    """A board for each individual colour."""
    def __init__(self, size: int, parent_board: ParentBoard, colour: int):
        """Creates a subboard for a specific colour based off of the parent board."""
        super().__init__()

        self.parent_board = parent_board
        self.colour = colour
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.tiles_left = 0
        for i in range(size):
            for j in range(size):
                self.board[i][j] = colour if parent_board.board[i][j] == colour else self.NULL
                if self.board[i][j] == colour:
                    self.tiles_left += 1
        
    def get_available_tiles(self) -> list[tuple[int, int]]:
        """Fetches the coordinates of all tiles that can have a queen."""
        available = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != self.NULL:
                    available.append((i, j))
                    if self.tiles_left == len(available): return available
        return available
    
    def eliminate_row_sub(self, row: int):
        """Eliminates a row from the subboard."""
        for ind, cell in enumerate(self.board[row]):
            if cell != self.NULL:
                self.tiles_left -= 1
                self.board[row][ind] = self.NULL
        
    def elimiate_col_sub(self, col: int):
        """Eliminates a column from the subboard."""
        for ind, row in enumerate(self.board):
            if row[col] != self.NULL:
                self.tiles_left -= 1
                self.board[ind][col] = self.NULL
    
    def eliminate_tile_sub(self, row: int, col: int):
        """Eliminates a tile from the subboard."""
        if self.board[row][col] != self.NULL:
            self.tiles_left -= 1
            self.board[row][col] = self.NULL

    def pattern_match(self) -> bool:
        """Identifies a pattern and acts accordingly. Returns True if any tiles are eliminated, allowing for another iteration."""
        if self.tiles_left == 0:
            return False
        elif self.tiles_left == 1:
            [tile] = self.get_available_tiles()
            self.parent_board.place_queen(tile)
            return True
        # elif self.tiles_left == 2:
        #     ... # weird pattern matching stuff here
        # elif self.count == self.size:
        else:
            tiles = self.get_available_tiles()
            if all([x[0] == tiles[0][0] for x in tiles]):
                row = tiles[0][0]
                pre_elim_count = self.parent_board.eliminated_tile_count()
                self.parent_board.eliminate_row(row)
                for tile in tiles:
                    self.parent_board.replace_tile(tile, self.colour)
                    self.board[tile[0]][tile[1]] = self.colour
                    self.tiles_left += 1
                print(self.parent_board.eliminated_tile_count(), pre_elim_count)
                if self.parent_board.eliminated_tile_count() == pre_elim_count:
                    return False # No change
                return True
            
            elif all([x[1] == tiles[0][1] for x in tiles]):
                col = tiles[0][1]
                pre_elim_count = self.parent_board.eliminated_tile_count()
                self.parent_board.eliminate_col(col)
                for tile in tiles:
                    self.parent_board.replace_tile(tile, self.colour)
                    self.board[tile[0]][tile[1]] = self.colour
                    self.tiles_left += 1
                if self.parent_board.eliminated_tile_count() == pre_elim_count:
                    return False # No change
                return True
            return False    # No match
        # else:
        #     return False

class PatternBoard(Board):
    def __init__(self, board: list, width: int, clear_line: str):
        """Variable size board that also shows the eliminated tiles.
            Board is the full solution board.
            Width is for the shape of the board
            clear_line denotes when a full line is cleared (only applies to where the solution is on one line), offset included"""
        super().__init__()
        self.open_board = [t if t == 0 else None for t in board]
        self.w_offset = 0
        self.h_offset = 0
        self.clear_line = clear_line
        height = int(len(self.open_board)/width)

        # Crop board
        while self.open_board[0:width] == [0]*width:
            self.open_board = self.open_board[width:]
            height -= 1
            self.h_offset += 1
        while self.open_board[-width:] == [0]*width:
            self.open_board = self.open_board[:-width]
            height -= 1
            self.h_offset += 1
        # sides
        self.open_board = self.rotate_clockwise(self.open_board, width)
        while self.open_board[0:height] == [0]*height:
            self.open_board = self.open_board[height:]
            width -= 1
            self.w_offset += 1
        while self.open_board[-height:] == [0]*height:
            self.open_board = self.open_board[:-height]
            width -= 1
            self.w_offset += 1
        self.open_board = self.rotate_counter_clockwise(self.open_board, height)

        self.marked_board = [t if t in [0, 1] else None for t in board]
        self.input_board = board
        self.width = width
    
    def rotate_clockwise(self, board: list, size: int):
        """Rotates a board 90 degrees clockwise."""
        return list(zip(*batched(board, size)[::-1]))
    
    def rotate_counter_clockwise(self, board: list, size: int):
        """Rotates a board 90 degrees counter-clockwise."""
        return list(zip(*batched(board, size)))[::-1]
    
    def custom_hash(self) -> int:
        """Creates a hash for the board."""
        return hash(tuple(self.open_board + [self.width]))
    
    def custom_sol(self) -> tuple:
        """Returns the solution board and offset."""
        return self.open_board, (self.w_offset, self.h_offset), self.clear_line


# Temporary test code
if __name__ == "__main__":
    b = ParentBoard(4, [5, 2, 5, 5, 5, 5, 5, 3, 4, 5, 5, 5, 5, 5, 5, 5])
    #b.place_queen((0, 1))
    print(b)
    for sb in b.subBoards:
        print(sb)
    b.solve()
    print(b)

"""
For pattern matching:
Get original shape: store minimum, hash (board+size), store in dict with solution as val
solution is board + offset because of new outer border + clear_lines
For pattern: Record top left of pattern. crop, rotate/flip and record actions. Update size each time (swaps from L(n), b to L(n), L(n)/b and back)
                check if hash exists. If so, get solution and reverse actions. Update offset too.
                Needs 4 rotations and a flip, so 8 combinations. Cancel duplicates.
Adjust top left point by offset. Mask new solution to eliminate tiles. Ignore OOB.
"""