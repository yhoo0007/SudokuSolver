# Python Sudoku Solver
A Sudoku solver written in Python. This solver works by transforming the Sudoku puzzle to an exact cover problem, and then using Knuth's Algorithm X to find a solution which is transformed back to the final completed puzzle.

### Explanation
The exact cover problem is to find a subset of rows of a binary matrix such that when combined, each column of the subset contains a single '1'. I.e. the rows combined **exactly** cover all the columns. For example given the following matrix:
|   | A | B | C |
| - | - | - | - |
| 1 | 0 | 1 | 0 |
| 2 | 1 | 0 | 1 |
| 3 | 0 | 1 | 1 |

The solution to the exact cover problem is rows {1, 2}. This is because {0, 1, 0} combined with {1, 0, 1} = {1, 1, 1}: there is one and only one '1' in each column.

A Sudoku puzzle can be modelled using such a matrix where each row represents the option of placing a particular digit in a particular square and the columns represent the constraints of the puzzle:
 - There can only be one number in each square
 - Each row must contain each number exactly once
 - Each column must contain each number exactly once
 - Each box must contain each number exactly once

The solution to the puzzle can then be found by solving the exact cover problem on the matrix.

### Example
The complete matrix representing an empty Sudoku puzzle can be found [here][blank-puzzle-matrix] or [here][exact-cover-full-matrix] (external link with some additional explanation).
This solver works by going through these steps: reading the puzzle, converting it to its matrix representation, solving the exact cover problem on the matrix, converting the answer to a solution for the puzzle. An example of a Sudoku puzzle going through these steps can be found here:
 - [Example Sudoku puzzle][example-puzzle]
 - [Unsolved matrix representation][example-puzzle-matrix]
 - [Solved/Solution matrix representation][solved-puzzle-matrix]
 - [Example Sudoku puzzle solved][solved-puzzle]

Hopefully this explanation + the examples are sufficient! If not, a more in-depth explanation can be found [here][exact-cover-wiki] (Wikipedia).

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

[exact-cover-wiki]: <https://en.wikipedia.org/wiki/Sudoku_solving_algorithms#Exact_cover>
[exact-cover-full-matrix]: <https://www.stolaf.edu/people/hansonr/sudoku/exactcovermatrix.htm>
[blank-puzzle-matrix]: <https://github.com/yhoo0007/SudokuSolver/blob/master/examples/blank_puzzle_matrix.txt>
[example-puzzle]: <https://github.com/yhoo0007/SudokuSolver/blob/master/examples/example_puzzle.txt>
[example-puzzle-matrix]: <https://github.com/yhoo0007/SudokuSolver/blob/master/examples/example_puzzle_matrix.txt>
[solved-puzzle-matrix]: <https://github.com/yhoo0007/SudokuSolver/blob/master/examples/solved_puzzle_matrix.txt>
[solved-puzzle]: <https://github.com/yhoo0007/SudokuSolver/blob/master/examples/example_puzzle_solved.txt>
