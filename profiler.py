import cProfile
from sudokusolver import SudokuSolver
from copy import deepcopy


puzzle = [
    [0,4,0,0,5,0,1,0,3],
    [0,0,3,0,0,9,5,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,5,0,0,7,0,0,0,0],
    [0,0,0,0,0,8,7,0,9],
    [0,7,0,9,0,1,3,0,8],
    [7,0,0,6,0,0,0,3,5],
    [0,0,0,0,4,7,0,0,0],
    [0,0,9,0,8,5,2,7,0]
]


if __name__ == '__main__':
    solver = SudokuSolver(deepcopy(puzzle))
    cProfile.run('solver.solve()')
