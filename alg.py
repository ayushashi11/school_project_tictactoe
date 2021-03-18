from numpy import array
#from pprint import pprint
from colorama import Style, Fore
from random import randint, choice
LN=3
board=array([[0 for i in range(LN)] for i in range(LN)])
values=array([[0 for i in range(LN)] for i in range(LN)],dtype="float64")
TOLERANCE=0
player_goes_first = False
def win(_board,LN=LN):
    d1,d2=0,0
    for i in range(LN):
        s=sum(_board[:,i])
        if abs(s)==LN:return s//LN
        s=sum(_board[i,:])
        if abs(s)==LN:return s//LN
        d1+=_board[i,i]
        d2+=_board[LN-i-1,i]
    else:
        if abs(d1)==LN:return d1//LN
        if abs(d2)==LN:return d2//LN
        return 0
def aremovesleft(_board):
    return 0 in board.reshape(-1)
def printb(_board,v=[" ",f"{Fore.LIGHTGREEN_EX}O{Fore.RESET}",f"{Fore.LIGHTRED_EX}X{Fore.RESET}"]):
    for i in range(LN):
        line=v[_board[i][0]]
        for j in range(1,LN):
            line+="|"+v[_board[i][j]]
        print(line)
        print("-"*(2*LN-1)) if i<LN-1 else 0
def set(x,y,p,LN=LN):
    board[x][y]=p
    s=TOLERANCE if p==-1 else 1
    values[x][y]=0
    iv=values.copy()
    for j in range(LN):
        if (not j==y) and board[x][j]==0:
            values[x][j]+=s#s*(abs(y-j)+1)
    for i in range(LN):
        if (not i==x) and board[i][y]==0:
            values[i][y]+=s#s*(abs(x-i)+1)
    if x==y:
        for i in range(LN):
            if (not x==i) and board[i][i]==0:
                values[i][i]+=s#s*(abs(x+y-i-j)+1)
    if x+y==LN-1:
        for i in range(LN):
            if (not y==i) and board[LN-i-1][i]==0:
                values[LN-i-1][i]+=s#s*(abs(x-y-i+j)+1)

def findbest(_values,LN=LN):
    #best,bi,bj=-float('inf'),-1,-1
    if sum(sum(values))==0:
        return randint(0,LN-1),randint(0,LN-1)
    mask = _values == _values.max()
    coords = []
    for i in range(LN):
        for j in range(LN):
            if mask[i][j]:
                coords.append((i,j))
    return choice(coords)

def main():
    moves = 0
    if player_goes_first:
        c=int(input(">> "))
        x,y=c//3, c%3
        set(x,y,1)
        moves += 1
    while aremovesleft(board):
        i,j=findbest(values)
        set(i,j,-1)
        if win(board,LN):
            printb(board)
            print("i win")
            return -1, moves
        printb(board)
        c=int(input(">> "))
        x,y=c//3, c%3
        if board[x][y]==0:
            set(x,y,1)
            moves += 1
        else:
            print("That place is already filled")
            continue
        if win(board,LN):
            printb(board)
            print("you win")
            return 1, moves
    else:
        print("draw")
        printb(board)
        return 0, moves

def reset():
    global board, values
    board=array([[0 for i in range(LN)] for i in range(LN)])
    values=array([[0 for i in range(LN)] for i in range(LN)],dtype="float64")
if __name__ == '__main__':
    main()