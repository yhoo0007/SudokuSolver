import os
from exactcover import createdancinglinks, exactcover
from typing import List, Optional, Tuple
from timeit import default_timer as timer
import warnings


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


    def solve(self) -> List[List[int]]:
        '''
        Attempts to solve the current puzzle state.
        '''
        # create matrix from puzzle
        matrix, row_map = self.creatematrix()

        # run exact cover
        dl = createdancinglinks(matrix)
        ans = exactcover(dl, partial_solution=[])

        # translate exact cover result to puzzle
        for row, col, digit in map(lambda a: row_map[a.row], ans):
            self.puzzle[row][col] = digit

        return self.puzzle


    def creatematrix(self) -> Tuple[List[List[int]], List[Tuple[int, int, int]]]:
        '''
        Create matrix from current puzzle state.
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
        Generates the matrix row. Digit given should be from 0-8 inclusive.
        '''
        ret = [0] * 324
        row_col_const_idx = row * 9 + col
        row_num_const_idx = row * 9 + digit + (9 * 9)
        col_num_const_idx = col * 9 + digit + (9 * 9 * 2)
        box_num_const_idx = (row // 3) * (9 * 3) + (col // 3) * 9 + digit + (9 * 9 * 3)
        ret[row_col_const_idx] = 1
        ret[row_num_const_idx] = 1
        ret[col_num_const_idx] = 1
        ret[box_num_const_idx] = 1
        return ret


    def creatematslice(self, row: int, col: int) -> List[List[int]]:
        '''
        Creates a slice of the matrix.
        '''
        return [self.generatematrow(row, col, digit) for digit in range(9)]


    def dumpmatrix(m, row_map: List[Tuple[int, int, int]]) -> None:
        with open('matrix_dump.txt', 'w+') as file:
            lines = ['       ' + (''.join(str(i) for i in range(9)) * 9 * 4) + '\n']
            for i, r in enumerate(m):
                res = f'r{row_map[i][0]}c{row_map[i][1]}#{row_map[i][2]} '
                for c in r:
                    res += str(c) if c != 0 else ' '
                res += '\n'
                lines.append(res)
            file.writelines(lines)


    def __str__(self) -> str:
        res = ''
        for row in self.puzzle:
            res += ' '.join(map(str, row)) + '\n'
        return res


if __name__ == '__main__':
    times = []
    for dir, _, files in os.walk('./puzzles'):
        for i, file in enumerate(files):
            puzzle = SudokuSolver(SudokuSolver.readtxt(f'{dir}/{file}'))
            print(i, file)
            time_taken = timer()
            puzzle.solve()
            time_taken = timer() - time_taken
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
