DEBUG = False


class PuzzleSolver(object):
    WORDS = ['OX', 'CAT', 'TOY', 'AT', 'DOG',  'CATAPULT', 'T']

    def is_word(self, word):
        """
        Returns true of word is in the dictionary, false otherwise.
        """
        return word in self.WORDS

    def log(self, message):
        """
        Show message on console if global DEBUG==True
        :param message:
        """
        if DEBUG:
            print(message)

    def get_matrix_resolution(self, matrix):
        """
        Check the matrix and return resolution
        :param matrix:
        :return: (height,widht) or Exception
        """
        width = 0
        height = 0
        for row in matrix:
            if not isinstance(row,str):      # check the matrix consist of strings
                raise Exception
            if height == 0:
                width = len(row)         # remember length of the first line...
            else:
                if width != len(row):    # ...and compare with others
                    raise Exception
            height += 1

        if width == 0 or height == 0:
            raise Exception

        return height, width

    def check_word_on_direction(self, matrix, wordlen, y, x, v, h):
        """
        Check word of puzzle in given direction
        :param matrix: puzzle
        :param wordlen: length of the word
        :param y: start row
        :param x: start column
        :param v: vertical direction (North,South)
        :param h: horizontal direction (West,East)
        :return: True if word in self.WORDS
        """
        word = ""
        for i in range(wordlen):
            if (y < 0 or y >= len(matrix) or
                x < 0 or x >= len(matrix[0])):  # make sure word inside the matrix
                return False
            word += matrix[y][x]
            y += v
            x += h
        if self.is_word(word):
            self.log(word)
            return True
        return False

    def find_words(self, puzzle):
        """
        Return the number of all non-distinct  occurrences
        of the words found in puzzle, horizontally, vertically
        or diagonally,  and also the reverse in each direction.
        The input to find_words (i.e. puzzle ) is a rectangular
        matrix of characters (list of strings).
        :param puzzle: Matrix of chars
        :return (width,height) or Exception:
        """
        height, width = self.get_matrix_resolution(puzzle)
        count = 0

        # Check for single symbols (have no directions)
        self.log("Check for 1 symbol word")
        for y in range(height):
            for x in range(width):
                char = puzzle[y][x]
                if self.is_word(char):
                    count += 1
                    self.log(char)

        # Check for words in directions N,NE,E,SE,S,SW,W,NS
        for wordlen in range(2,max(width,height)+1):
            self.log("Check for %i symbols word" % wordlen)
            for y in range(height):
                for x in range(width):
                    if self.check_word_on_direction(puzzle, wordlen, y, x, -1,  0):    # North
                        count += 1
                    if self.check_word_on_direction(puzzle, wordlen, y, x, -1,  1):    # North-East
                        count += 1
                    if self.check_word_on_direction(puzzle, wordlen, y, x,  0,  1):    # East
                        count += 1
                    if self.check_word_on_direction(puzzle, wordlen, y, x,  1,  1):    # South-East
                        count += 1
                    if self.check_word_on_direction(puzzle, wordlen, y, x,  1,  0):    # South
                        count += 1
                    if self.check_word_on_direction(puzzle, wordlen, y, x,  1, -1):    # South-West
                        count += 1
                    if self.check_word_on_direction(puzzle, wordlen, y, x,  0, -1):    # West
                        count += 1
                    if self.check_word_on_direction(puzzle, wordlen, y, x, -1, -1):    # North-West
                        count += 1

        return count

if __name__ == '__main__':
    DEBUG = True

    puzzle_solver = PuzzleSolver()

    puzzle = [
        "CAT",
        "XZT",
        "YOT"
    ]
    print(puzzle_solver.find_words(puzzle))

    puzzle = [
        "CATAPULT",
        "XZTTOYOO",
        "YOTOXTXX"
    ]
    print(puzzle_solver.find_words(puzzle))
