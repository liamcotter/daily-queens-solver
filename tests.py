import solve
import unittest
from testcase_import import testcase_import

class TestBoard(unittest.TestCase):
    """Simple unit tests."""
    def test_board(self):
        board = solve.ParentBoard(4, [5, 5, 5, 5, 5, 3, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4])
        board.place_queen((1, 1))
        self.assertEqual(str(board), 'd X d d\nX Q X X\nb X b b\nc X c c\n')

        b1 = solve.ParentBoard(*testcase_import())
        b1.solve()
        self.assertEqual(str(b1), 'X X X X X Q X\nX X X Q X X X\nX X X X X X Q\nX Q X X X X X\nX X X X Q X X\nX X Q X X X X\nQ X X X X X X\n')

if __name__ == '__main__':
    unittest.main()