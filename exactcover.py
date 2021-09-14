# Wikipedia example:
#   1 2 3 4 5 6 7
# A 1 0 0 1 0 0 1
# B 1 0 0 1 0 0 0
# C 0 0 0 1 1 0 1
# D 0 0 1 0 1 1 0
# E 0 1 1 0 0 1 1
# F 0 1 0 0 0 0 1

# Choose column with lowest number of 1s (column 1)
# Select row A, remove it and all rows and columns where there is a 1 in the same position as row A:
#   2 3 5 6
# D 0 1 1 1
# Lowest number of 1s is column 2, but it is 0, thus this branch terminates unsuccessfully

# Select row B:
#   2 3 5 6 7
# D 0 1 1 1 0
# E 1 1 0 1 1
# F 1 0 0 0 1

# Lowest number of 1s is column 5
# Select row D:
#   2 7
# F 1 1

# Select row F:
# Matrix is empty, hence this branch terminates successfully. Rows B, D, and F are returned as the solution.

from typing import List, Optional, Tuple


class Node:
    def __init__(
        self,
        val,
        row: int,
        col: int,
        left: Optional['Node']=None,
        right: Optional['Node']=None,
        up: Optional['Node']=None,
        down: Optional['Node']=None
    ) -> None:
        self.val = val
        self.row = row
        self.col = col
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.removed = False


    def __repr__(self) -> str:
        return f'{self.val} ({self.row}, {self.col})'


def printnodematrix(node_matrix: Node, n_rows: int, n_cols: int) -> None:
    '''
    Prints the node matrix.
    '''
    res = [['+' for _ in range(n_cols)] for _ in range(n_rows)]
    
    # traverse node_matrix column by column
    current_col = node_matrix.right
    while current_col != node_matrix:
        current_node = current_col.down
        while current_node != current_col:
            res[current_node.row][current_node.col] = '1'
            current_node = current_node.down
        current_col = current_col.right

    print(' '.join(map(str, range(n_cols))) + '\n' + '\n'.join([' '.join(map(str, row)) for row in res]))


def createnodematrix(mat: List[List[int]], num_rows: int, num_cols: int) -> Node:
    '''
    Creates a node representation of the given matrix. Every node is connected to the 4 adjacent
    nodes. The connections are circular. Returns the head node.
    '''
    heads = [None] * num_cols  # stores the column header nodes
    tails = [None] * num_cols  # stores the column tail nodes
    head = Node('h', 0, 0)
    prev = head

    # create column header nodes
    for col in range(num_cols):
        node = Node(val=None, row=-1, col=col)
        heads[col] = node
        tails[col] = node
        node.left = prev
        prev.right = node
        prev = node
    head.left = prev
    prev.right = head

    # create matrix of nodes row by row
    for row in range(num_rows):
        first = None
        prev = None
        for col in range(num_cols):
            if mat[row][col] == 1:  # only create nodes for '1's
                node = Node(val=1, row=row, col=col)

                # link new node to its column
                node.up = tails[col]
                tails[col].down = node
                tails[col] = node

                if first is None:  # track first node created
                    first = node
                if prev:  # link new node to the previous node created
                    node.left = prev
                    prev.right = node
                prev = node

        # wrap the list around if > 0 nodes were created
        if first is not None:
            first.left = prev
            prev.right = first

    # wrap the tails of each column back to their heads
    for col in range(num_cols):
        tails[col].down = heads[col]
        heads[col].up = tails[col]

    return head


def exactcover(node_matrix: Node, partial_solution: List[Node]=[]) -> Optional[List[Node]]:
    '''
    Finds a subset of rows from the node matrix which solves the exact cover problem or None if no
    solution is found.
    '''
    selected_col, selected_count = selectcol(node_matrix)
    if selected_col == node_matrix:  # empty matrix, partial solution is a complete solution
        return partial_solution
    
    # if the column has no '1's, an exact cover is impossible
    if selected_count == 0:
        return None
    
    # iterate through the rows which are '1's
    current_row = selected_col.down
    while current_row != selected_col:  # current_row guaranteed != header node

        # include current row in partial solution
        partial_solution.append(current_row)

        # iterate each column in current row
        deleted_nodes = []
        deleting_col = current_row
        while True:
            # iterate each row in that column
            deleting_row = deleting_col
            while True:
                if deleting_row.row != -1: # skip header row
                    deleted_nodes += removerow(deleting_row)

                if deleting_row.down == deleting_row:
                    break
                deleting_row = deleting_row.down

            deleted_nodes += removecolumn(deleting_col)

            if deleting_col.right == deleting_col:
                break
            deleting_col = deleting_col.right

        # recurse with the reduced dancing links
        ret = exactcover(node_matrix, partial_solution)
        if ret is not None:
            return ret

        # restore state
        partial_solution.pop()
        for node in deleted_nodes:
            restorenode(node)

        current_row = current_row.down
    
    # no solution was found
    return None


def selectcol(node_matrix: Node) -> Tuple[Node, int]:
    '''
    Selects the column with the fewest number of nodes.
    '''
    # count the number of nodes in each column and return the column with the fewest
    current = node_matrix.right
    selected_col = node_matrix.right
    selected_count = None
    while current != node_matrix:
        current_row = current
        count = 0
        while current_row.down != current:
            current_row = current_row.down
            count += 1
        if selected_count is None or count < selected_count:
            selected_count = count
            selected_col = current
            if selected_count == 0:  # terminate early if an empty column is found
                return selected_col, selected_count
        current = current.right
    return selected_col, selected_count


def removecolumn(node_in_column: Node) -> List[Node]:
    '''Removes a column of nodes and returns them in order of their removal'''
    current = node_in_column
    removed_nodes = []
    while True:
        if not current.removed:
            removed_nodes.append(removenode(current))
        if current.down == current:  # linking to itself, means entire column is removed
            return removed_nodes
        current = current.down


def removerow(node_in_row: Node) -> List[Node]:
    '''Removes a row of nodes and returns them in order of their removal'''
    current = node_in_row
    removed_nodes = []
    while True:
        if not current.removed:
            removed_nodes.append(removenode(current))
        if current.right == current:  # linking to itself, means entire row is removed
            return removed_nodes
        current = current.right


def removenode(node: Node) -> Node:
    '''Idempotently remove node'''
    if node.removed:
        return node
    node.left.right = node.right
    node.right.left = node.left
    node.up.down = node.down
    node.down.up = node.up
    node.removed = True
    return node


def restorenode(node: Node) -> Node:
    '''Idempotently restore node'''
    if not node.removed:
        return node
    node.left.right = node
    node.right.left = node
    node.up.down = node
    node.down.up = node
    node.removed = False
    return node


if __name__ == '__main__':
    mat = [
        [1,0,0,1,0,0,1],
        [1,0,0,1,0,0,0],
        [0,0,0,1,1,0,1],
        [0,0,1,0,1,1,0],
        [0,1,1,0,0,1,1],
        [0,1,0,0,0,0,1]
    ]

    node_matrix = createnodematrix(mat, len(mat), len(mat[0]))
    printnodematrix(node_matrix, n_rows=len(mat), n_cols=len(mat[0]))

    ret = exactcover(node_matrix)
    print(ret)
