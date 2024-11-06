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



class subBoard(Board):
    """A board for each individual colour."""
    def __init__(self, size: int, parent_board: ParentBoard, colour: int):
        """Creates a subboard for a specific colour based off of the parent board."""
        super().__init__()

        self.parent_board = parent_board
        self.colour = colour
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.count = 0
        for i in range(size):
            for j in range(size):
                self.board[i][j] = colour if parent_board.board[i][j] == colour else self.NULL
                if self.board[i][j] == colour:
                    self.count += 1
        
    def get_available_tiles(self) -> list[tuple[int, int]]:
        """Fetches the coordinates of all tiles that can have a queen."""
        available = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != self.NULL:
                    available.append((i, j))
                    if self.count == len(available): return available
        return available
    
    def eliminate_row_sub(self, row: int):
        """Eliminates a row from the subboard."""
        for ind, cell in enumerate(self.board[row]):
            if cell != self.NULL:
                self.count -= 1
                self.board[row][ind] = self.NULL
        
    def elimiate_col_sub(self, col: int):
        """Eliminates a column from the subboard."""
        for ind, row in enumerate(self.board):
            if row[col] != self.NULL:
                self.count -= 1
                self.board[ind][col] = self.NULL
    
    def eliminate_tile_sub(self, row: int, col: int):
        """Eliminates a tile from the subboard."""
        if self.board[row][col] != self.NULL:
            self.count -= 1
            self.board[row][col] = self.NULL

    def pattern_match(self) -> bool:
        """Identifies a pattern and acts accordingly. Returns True if any tiles are eliminated, allowing for another iteration."""
        if self.count == 1:
            [tile] = self.get_available_tiles()
            self.parent_board.place_queen(tile)
            return True
        return False

# Temporary test code
if __name__ == "__main__":
    b = ParentBoard(4, [5, 2, 5, 5, 5, 5, 5, 3, 4, 5, 5, 5, 5, 5, 5, 5])
    #b.place_queen((0, 1))
    print(b)
    for sb in b.subBoards:
        print(sb)
    b.solve()
    print(b)