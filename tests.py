import solve
import unittest

class TestBoard(unittest.TestCase):
    """Simple unit tests."""
    def test_board(self):
        board = solve.ParentBoard(4, [5, 5, 5, 5, 5, 3, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4])
        board.place_queen((1, 1))
        self.assertEqual(str(board), 'd X d d\nX Q X X\nb X b b\nc X c c\n')
    

if __name__ == '__main__':
    unittest.main()