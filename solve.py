class Board:
    def __init__(self, size: int, board: list):
        """Each board is size x size, with size different regions. Size must be a natural number."""
        assert 1 <= size <= 20
        assert size*size == len(board)
        self.size = size
        self.board = [board[size*i:size*(i+1)] for i in range(size)]
        print(self.board)
        self.colours = ['r', 'g', 'b']
        self.subBoards = []
        for n in self.colours:
            self.subBoards.append(subBoard(size, self, n))
        
    def __str__(self):
        return '\n'.join([' '.join([str(cell) for cell in row]) for row in self.board])
            

class subBoard(Board):
    def __init__(self, size: int, parent_board: Board, colour: str):
        self.board = [[None for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                self.board[i][j] = colour if parent_board.board[i][j] == colour else 'x'
        
            

    
    def solve(self):
        ...
    
    def pattern_match(self):
        ...
