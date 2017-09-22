#Coding Puzzle

Author: Alexei Bushuev

Email: alexeib.2017@gmail.com

Language: python3 (python2 will not be accepted). Please submit .py file(s).

Given the following:

class  PuzzleSolver(object):
    WORDS = ['OX', 'CAT', 'TOY', 'AT', 'DOG',  'CATAPULT', 'T']
    
    def is_word(self, word):
	""" 
	Returns true of word is in the dictionary, false otherwise.
	"""
	return word in self.WORDS
	
    def find_words(self, puzzle):
	"""
	Should return the number of all non-distinct  occurrences
	of the words found in puzzle, horizontally, vertically 
	or diagonally,  and also the reverse in each direction. 
	The input to find_words (i.e. puzzle ) is a rectangular 
	matrix of characters (list of strings).
	"""
	pass

Implement the function find_words(self, puzzle)

Example Input 1:

[
    "CAT",

    "XZT",

    "YOT"
]

Example Output 1:

8

This 8 words are:

(AT, AT, CAT, OX, TOY, T, T, T)

Example Input 2:

[
    "CATAPULT",
    "XZTTOYOO",
    "YOTOXTXX"
]

Example Output 2:

22

Notes:

We are trying to see the quality of the code you write (hint: unit tests, comments, pep8). You will be mainly
evaluated on how well you break down the problem and how well you test your code. Don’t worry too much about
performance and efficiency but your program should work correctly. It should also be capable of scaling to
puzzles with dimensions such as 4x4, 6x9, 9x9.
