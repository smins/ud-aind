###
# Udacity AI Nanodegree
# Sudoku Solver
# Stu Minshull 5.4.2017
###

### Functions

# Returns all combinations of the contents of lists a & b
def cross(a, b):
    return [s+t for s in a for t in b]




### Script Below ###

rows = 'ABCDEFGHI'
cols = '123456789'

# All boxes on the board
boxes = cross(rows, cols)
print(boxes)

# Unit sets as lists
row_units = [cross(row, cols) for row in rows]
col_units = [cross(col, rows) for col in cols]

# Hardcode the square units
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

# Concat all the unit sets into a master set
unitlist = row_units + col_units + square_units
print(unitlist)
