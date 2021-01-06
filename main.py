import alg
from math import ceil
import mysql.connector as msc
conn = msc.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="tictactoe"
    )

if not conn.is_connected():
    conn.connect()
    print("reconnecting")

curs = conn.cursor()

curs.execute(
    """create table if not exists scores(
        name varchar(50) not null,
        score int(3) not null,
        win_time timestamp default now()
    )"""
    )

#curs.execute("insert into scores(name, score) values('god', 64)")
#curs.execute("insert into scores(name, score) values('loser', 0)")
#conn.commit()

def get_scores(PAGE=1):
    curs.execute("select * from scores order by score DESC, win_time")
    all=curs.fetchall()
    print("-"*81)
    print(f"||{'name':^50}|{'score':^5}|{'date and time (UTC)':^20}||")
    print("-"*81)
    for name, score, date in all[(PAGE-1)*10:PAGE*10]:
        print(f"||{name:<50}|{score:>5}|{str(date):^20}||")
    print("-"*81)
    print("|{:>79}|".format(f"PAGE {PAGE} of {ceil(len(all)/10)}"))
    print("-"*81)

def insert(score, name=None):
    name = name or input("Enter name (less than 50 characters): ")
    if name == "":
        print("Name cant be empty")
        insert(score)
    curs.execute(f"insert into scores(name, score) values('{name}', {score})")
    conn.commit()

def game():
    res, nmoves = alg.main()
    input("(press any key to continue)")
    if res == 1:
        insert(64-nmoves)
    elif res == -1:
        insert(64-nmoves, "computer")

def main():
    alg.player_goes_first =eval(open("settings.txt").read())
    print("-"*62)
    print("|{:^60}|\n|{:^60}|".format("Welcome to TicTacToe!","(press any key to continue)"))
    input("-"*62+"\n")
    while True:
        choice = int(input(
        """
        Press:-
        1. To play the Game
        2. To see the HighScores
        3. To Quit
        4. How to Play
        5. Settings
        >>> """
        ))
        if choice == 1:
            game()
            alg.reset()
        elif choice == 2:
            get_scores()
            if input("Do you want to see another page(Yes/No): ").lower() == "yes":
                get_scores(
                    int(input("Enter page: "))
                )
        elif choice == 3:
            print("THANKS FOR PLAYING 😄")
            break
        elif choice == 4:
            print(
                """
                the computer would play X and you would play O
                in front of you,
                a board would be printed like this
                        O| |O
                        -----
                        X|X|
                        -----
                        X| |
                >>> 
                you have to type the indices of the matrix where you want to place your O
                like typing
                >>> 0 1
                would result in
                        O|O|O
                        -----
                        X|X|
                        -----
                        X| |
                """
                )
        elif choice == 5:
            print(f"There is a single setting\nPlayer goes first: {alg.player_goes_first}")
            if input("Do you wish to flip it(Yes/No)? ").lower() == "yes":
                alg.player_goes_first = not alg.player_goes_first
                open("settings.txt","w").write(str(alg.player_goes_first))
        else:
            print("INVALID CHOICE")
            input("(press any key to continue)")
    input("(press any key to continue)")

if __name__ == '__main__':
    main()
        
