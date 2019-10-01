def check(sudoku,i,j,n):
    if n in sudoku[i]:
        return False
    elif n in column(sudoku,j):
        return False
    elif n in box(sudoku,i,j):
        return False
    else: return True

def column(sudoku,c):
    return [sudoku[i][c] for i in range(9)]

def box(sudoku,i,j):
    i1=i//3
    j1=j//3
    i2=i1*3
    j2=j1*3
    return [sudoku[x][y] for x in range(i2,i2+3) for y in range(j2,j2+3)]

def empty(sudoku):
    for x in range(9):
        for y in range(9):
            if (sudoku[x][y]==0):
                return [x,y]
    return False  

def solver(sudoku):
    if empty(sudoku):
        l=empty(sudoku)
        x=l[0]
        y=l[1]
        for n in range(1,10):
            if not(check(sudoku,x,y,n)): continue
            else:
                sudoku[x][y]=n
                if not(solver(sudoku)): 
                    sudoku[x][y]=0
                    continue
                else: return True
        else: return False
    else: 
        print(sudoku)
        return True

sudoku19=[[0, 0, 3, 0, 5, 0, 0, 0, 9],
         [0, 0, 6, 0, 8, 0, 1, 0, 3], 
         [0, 8, 9, 1, 2, 0, 0, 5, 6],
         [0, 3, 4, 0, 6, 7, 8, 9, 0],
         [5, 0, 7, 8, 0, 0, 0, 3, 4], 
         [8, 9, 0, 2, 3, 0, 5, 6, 0],
         [0, 0, 2, 0, 4, 5, 6, 0, 8],
         [6, 7, 8, 0, 1, 2, 3, 4, 5], 
         [3, 4, 5, 6, 7, 8, 9, 0, 2]]

sudoku20=[[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]

sudoku24=[[0,0,0,0,0,0,0,0,0],   ###not solvable
          [2,0,0,0,0,3,0,8,5],
          [0,0,1,0,2,0,0,0,0],
          [0,0,0,5,0,7,0,0,0],
          [0,0,4,0,0,0,1,0,0],
          [0,9,0,0,0,0,0,0,0],
          [5,0,0,0,0,0,0,7,3],
          [0,0,2,0,1,0,0,0,0],
          [0,0,0,0,4,0,0,0,9]]

sudoku25=[[0,0,0,3,7,0,0,2,0],
          [0,9,0,0,8,5,7,0,0],
          [3,0,0,9,0,0,0,0,5],
          [1,0,0,0,0,0,0,8,0],
          [0,0,0,0,0,0,3,0,0],
          [0,0,0,0,9,0,0,0,7],
          [2,0,0,6,0,0,0,0,1],
          [0,4,8,0,0,0,6,0,0],
          [0,3,1,0,0,0,0,4,0]]

