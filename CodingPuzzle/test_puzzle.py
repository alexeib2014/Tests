import unittest
from puzzle import PuzzleSolver


class ResultsTests(unittest.TestCase):
    """
    Tests of PuzzleSolver HR tasks
    """
    def test_3x3(self):
        """
        Task test puzzle 3x3
        """
        puzzle_solver = PuzzleSolver()
        puzzle = [
            "CAT",
            "XZT",
            "YOT"
        ]
        assert puzzle_solver.find_words(puzzle) == 8

    def test_3x8(self):
        """
        Task test puzzle 3x8
        """
        puzzle_solver = PuzzleSolver()
        puzzle = [
            "CATAPULT",
            "XZTTOYOO",
            "YOTOXTXX"
        ]
        assert puzzle_solver.find_words(puzzle) == 22


class ParametersTests(unittest.TestCase):
    """
    Tests of input parameters
    """
    def test_matrix_ok(self):
        """
        Test good matrix
        """
        puzzle_solver = PuzzleSolver()
        puzzle = [
            "CATAPULT",
            "XZTTOYOO",
            "YOTOXTXX"
        ]
        height, width = puzzle_solver.get_matrix_resolution(puzzle)
        assert height == 3
        assert width == 8

    def test_matrix_norect(self):
        """
        Test not rectangular matrix
        """
        puzzle_solver = PuzzleSolver()
        puzzle = [
            "CATAPULT",
            "XZTTOYO",
            "YOTOXTXX"
        ]
        with self.assertRaises(Exception):
            puzzle_solver.find_words(puzzle)

    def test_matrix_nostr(self):
        """
        Test matrics consist of no string values
        """
        puzzle_solver = PuzzleSolver()
        puzzle = [
            "CAT",
            [0,1,2],
            "YOT"
        ]
        with self.assertRaises(Exception):
            puzzle_solver.find_words(puzzle)


if __name__ == '__main__':
    unittest.main(exit=False)
