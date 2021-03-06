import os
from exactcover import createnodematrix, exactcover
from typing import List, Optional, Tuple
from timeit import default_timer as timer
import warnings
import csv


class SudokuSolver:
    @classmethod
    def readtxt(cls, fp: str) -> List[List[int]]:
        '''
        Reads a text file containing a puzzle and returns it as a 2D matrix of int | None. Text
        files should represent puzzles as space-separated integers. '0's should be used to
        represent empty squares.
        '''
        puzzle = []
        with open(fp) as file:
            for line in map(str.strip, file.readlines()):
                row = list(map(int, line.split(' ')))
                puzzle.append(row)
        if len(puzzle) != 9 or not all([len(row) == 9 for row in puzzle]):
            warnings.warn('Malformed puzzle read!')
        return puzzle


    def __init__(self, puzzle: List[List[Optional[int]]]) -> None:
        self.puzzle = puzzle


    def solve(self) -> Tuple[List[List[int]], bool]:
        '''
        Attempts to solve the current puzzle state. Returns the final puzzle state and a bool value
        indicating if a solution was found.
        '''
        # create exact cover matrix from puzzle
        matrix, row_map = self.creatematrix()
        node_matrix = createnodematrix(matrix, len(matrix), 324)

        # run exact cover
        ans = []
        exactcover(node_matrix, all_solutions=ans)

        # translate exact cover solution to puzzle solution, takes only the first solution found
        if len(ans) > 0:
            for row, col, digit in map(lambda a: row_map[a.row], ans[0]):
                self.puzzle[row][col] = digit
            return self.puzzle, True
        return self.puzzle, False


    def creatematrix(self) -> Tuple[List[List[int]], List[Tuple[int, int, int]]]:
        '''
        Creates a compressed version of the exact cover matrix from current puzzle state. Refer to 
        ./examples/*_puzzle_matrix.txt for an example or
        https://www.stolaf.edu/people/hansonr/sudoku/exactcovermatrix.htm for more info.
        '''
        mat = []
        row_map = []
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[i])):
                if self.puzzle[i][j] != 0:
                    row_map.append((i, j, self.puzzle[i][j]))
                    mat.append(self.generatematrow(i, j, self.puzzle[i][j] - 1))
                else:
                    row_map += [(i, j, digit) for digit in range(1, 10)]
                    mat += self.creatematslice(i, j)
        return mat, row_map


    def generatematrow(self, row: int, col: int, digit: int) -> List[int]:
        '''
        Generates a row of the exact cover matrix corresponding to the given row, column, and
        digit. Digit given should be from 0-8 inclusive.
        '''
        offset = 81
        ret = [0] * 324
        row_col_const_idx = row * 9 + col
        row_num_const_idx = row * 9 + digit + offset
        col_num_const_idx = col * 9 + digit + (offset * 2)
        box_num_const_idx = (row // 3) * (9 * 3) + (col // 3) * 9 + digit + (offset * 3)
        return [row_col_const_idx, row_num_const_idx, col_num_const_idx, box_num_const_idx]


    def creatematslice(self, row: int, col: int) -> List[List[int]]:
        '''
        Creates a slice of the exact cover matrix corresponding to the given row and column.
        '''
        return [self.generatematrow(row, col, digit) for digit in range(9)]


    def dumpmatrix(self, m: List[List[int]], row_map: List[Tuple[int, int, int]]) -> None:
        '''
        Dumps the given exact cover matrix to a file named 'matrix_dump.txt'.
        '''
        with open('matrix_dump.txt', 'w+') as file:
            lines = ['       ' + (''.join(str(i) for i in range(9)) * 9 * 4) + '\n']  # initialize with header
            for i, r in enumerate(m):
                res = f'r{row_map[i][0]}c{row_map[i][1]}#{row_map[i][2]} ' +\
                        ''.join(map(lambda c: str(c) if c != 0 else ' ', r)) + '\n'
                lines.append(res)
            file.writelines(lines)


    def __str__(self) -> str:
        res = ''
        for row in self.puzzle:
            res += ' '.join(map(str, row)) + '\n'
        return res


def readpuzzles(fp: str, limit=100):
    '''
    Reads puzzles from a csv file with the following format:
    puzzles, solution
    100000090208970605000532000006050400700806002083700010604080120890600050015040007,157468293238971645469532781926153478741896532583724916674385129892617354315249867
    205040003001009000046001587004607090802000056090020340170008200000500800500903001,285746913731859624946231587354687192812394756697125348179468235463512879528973461
    .
    .
    .
    '''
    puzzles = []
    with open(fp) as csv_file:
        count = 0
        limit = 500
        for row in csv.reader(csv_file, delimiter=','):
            if count > 0:
                puzzle, solution = row
                puzzle = [[int(puzzle[i + j]) for i in range(0, 81, 9)] for j in range(9)]
                solution = [[int(solution[i + j]) for i in range(0, 81, 9)] for j in range(9)]
                puzzles.append((puzzle, solution))
            if count >= limit:
                break
            count += 1
    return puzzles


def verifysolution(solution: List[List[int]]):
    '''
    Verifies the given Sudoku solution.
    '''
    # check each row
    for row in solution:
        row_set = set(row)
        if not all([n in row_set for n in range(1, 10)]):
            return False
    
    # check each column
    for i in range(len(solution)):
        col_set = set([row[i] for row in solution])
        if not all([n in col_set for n in range(1, 10)]):
            return False

    # check each box
    for i in range(0, len(solution), 3):
        for j in range(0, len(solution), 3):
            box_set = set([n for sub in [row[i: i + 3] for row in solution[j: j + 3]] for n in sub])
            if not all([n in box_set for n in range(1, 10)]):
                return False
    return True


if __name__ == '__main__':
    times = []
    for puzzle, s in readpuzzles('./puzzles/sudoku.csv', limit=10000):
        puzzle = SudokuSolver(puzzle)
        time_taken = timer()
        solution, solved = puzzle.solve()
        time_taken = timer() - time_taken
        correct = verifysolution(solution)
        if not correct:
            print('Incorrect solution found!')
            break
        print('Time taken:', time_taken)
        times.append(time_taken)

    times.sort()
    len_times = len(times)
    print('Mean:', sum(times) / len_times)
    print(
        'Median:',
        times[len_times // 2]
        if len_times % 2 == 0 else
        (times[len_times // 2] + times[len_times // 2 + 1]) / 2
    )
    print('Max:', max(times))
    print('Min:', min(times))
