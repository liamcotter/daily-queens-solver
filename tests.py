import solve
import unittest

class TestBoard(unittest.TestCase):
    """Simple unit tests."""
    def test_board(self):
        board = solve.Board(3, [1, 1, 2, 1, 3, 2, 3, 3, 2])
        self.assertEqual(str(board), 'a a b\na c b\nc c b')
    

if __name__ == '__main__':
    unittest.main()