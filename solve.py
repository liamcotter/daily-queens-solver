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
        self.board = [board[size*i:size*(i+1)] for i in range(size)]
        self.subBoards = []
        for col in range(2, self.size+2):
            self.subBoards.append(subBoard(size, self, col))
        
    def place_queen(self, tile: tuple[int, int]):
        """Places a queen on the board and nullifies the incompatible tiles."""
        self.eliminate_row(tile[0])
        self.eliminate_col(tile[1])
        self.board[tile[0]][tile[1]] = self.QUEEN
    
    def eliminate_row(self, row: int):
        ...
    
    def eliminate_col(self, col: int):
        ...
    
    def eliminate_tile(self, tile: tuple[int, int]):
        ...

class subBoard(Board):
    """A board for each individual colour."""
    def __init__(self, size: int, parent_board: ParentBoard, colour: int):
        """Creates a subboard for a specific colour based off of the parent board."""
        super().__init__()

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
                if self.board[i][j]:
                    available.append((i, j))
                    if self.count == len(available): return available
        return available   

    
    def solve(self):
        ...
    
    def pattern_match(self):
        """Identifies a pattern and acts accordingly."""
        if self.count == 1:
            tile = self.get_available_tiles()[0]
            self.place_queen(tile)


b = ParentBoard(4, [5, 5, 5, 5, 5, 3, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4])
print(b)
for sb in b.subBoards:
    print(sb)