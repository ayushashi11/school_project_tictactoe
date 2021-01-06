from numpy import array
#from pprint import pprint
from random import randint, choice
ln=3
board=array([[0 for i in range(ln)] for i in range(ln)])
values=array([[0 for i in range(ln)] for i in range(ln)],dtype="float64")
vbuf=[]
tolerance=0
player_goes_first = False
def win(_board,ln=ln):
    d1,d2=0,0
    for i in range(ln):
        s=sum(_board[:,i])
        if abs(s)==ln:return s//ln
        s=sum(_board[i,:])
        if abs(s)==ln:return s//ln
        d1+=_board[i,i]
        d2+=_board[ln-i-1,i]
    else:
        if abs(d1)==ln:return d1//ln
        if abs(d2)==ln:return d2//ln
        return 0
def movesleft(_board):
    return 0 in board.reshape(-1)
def printb(_board,v=[" ","O","X"]):
    for i in range(ln):
        line=v[_board[i][0]]
        for j in range(1,ln):
            line+="|"+v[_board[i][j]]
        print(line)
        print("-"*(2*ln-1)) if i<ln-1 else 0
def set(x,y,p,ln=ln):
    board[x][y]=p
    s=tolerance if p==-1 else 1
    values[x][y]=0
    iv=values.copy()
    for j in range(ln):
        if (not j==y) and board[x][j]==0:
            values[x][j]+=s#s*(abs(y-j)+1)
    for i in range(ln):
        if (not i==x) and board[i][y]==0:
            values[i][y]+=s#s*(abs(x-i)+1)
    if x==y:
        for i in range(ln):
            if (not x==i) and board[i][i]==0:
                values[i][i]+=s#s*(abs(x+y-i-j)+1)
    if x+y==ln-1:
        for i in range(ln):
            if (not y==i) and board[ln-i-1][i]==0:
                values[ln-i-1][i]+=s#s*(abs(x-y-i+j)+1)
    vbuf.append(values.copy()-iv)
    print(vbuf[-1])
def findbest_old(_values,ln=ln):
    best,bi,bj=-float('inf'),-1,-1
    if sum(sum(values))==0:
        return randint(0,ln-1),randint(0,ln-1)
    for i in range(ln):
        for j in range(ln):
            if board[i][j]==0:
                if _values[i][j]>=best:
                    best,bi,bj=_values[i][j],i,j
    print(_values == _values.max())
    return bi,bj

def findbest(_values,ln=ln):
    #best,bi,bj=-float('inf'),-1,-1
    if sum(sum(values))==0:
        return randint(0,ln-1),randint(0,ln-1)
    mask = _values == _values.max()
    coords = []
    for i in range(ln):
        for j in range(ln):
            if mask[i][j]:
                coords.append((i,j))
    print(mask)
    return choice(coords)

def main():
    moves = 0
    if player_goes_first:
        x,y=map(int,input(">> ").split())
        set(x,y,1)
        moves += 1
    while movesleft(board):
        i,j=findbest(values)
        print(i,j)
        set(i,j,-1)
        if win(board,ln):
            printb(board)
            print("i win")
            return -1, moves
        printb(board)
        x,y=map(int,input(">> ").split())
        if board[x][y]==0:
            set(x,y,1)
            moves += 1
        else:
            print("That place is already filled")
            continue
        if win(board,ln):
            printb(board)
            print("you win")
            return 1, moves
    else:
        print("draw")
        printb(board)
        return 0, moves

def reset():
    global board, values, vbuf
    board=array([[0 for i in range(ln)] for i in range(ln)])
    values=array([[0 for i in range(ln)] for i in range(ln)],dtype="float64")
    vbuf=[]
if __name__ == '__main__':
    main()