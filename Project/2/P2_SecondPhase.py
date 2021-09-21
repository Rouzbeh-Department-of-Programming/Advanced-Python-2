from enum import Enum, auto


class Direction(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()


class Ship:
    def __init__(self, size, direction, top_lest, bottom_right):
        self.size = size
        self.direction = direction
        self.top_lest = top_lest
        self.bottom_right = bottom_right

    def check_if_is_destroyed(self):
        pass

    def destroy(self):
        pass


class Situation(Enum):
    EMPTY = auto()
    FULL = auto()
    WATER = auto()
    EXPLODED = auto()
    COMPLETED = auto()


class Location:
    def __init__(self, x, y, situation):
        self.x = x
        self.y = y
        self.situation = situation


class Map:
    def __init__(self, size):
        self.size = size
        self.board = []
        for i in range(size):
            self.board.append([])
            for j in range(size):
                self.board[i].append(Location(j, i, Situation.EMPTY))

    def display(self):
        print('   ', end='')
        for i in range(self.size):
            print(i + 1, ' ', end='')
        print()

        for i in range(self.size):
            print(i + 1, ' ', end='')
            for j in self.board[i]:
                if j.situation is Situation.EMPTY or j.situation is Situation.FULL:
                    print('-  ', end='')
                elif j.situation is Situation.WATER:
                    print('W  ', end='')
                elif j.situation is Situation.EXPLODED:
                    print('E  ', end='')
                elif j.situation is Situation.COMPLETED:
                    print('C  ', end='')
            print()

    def display_for_owner(self):
        print('   ', end='')
        for i in range(self.size):
            print(i + 1, ' ', end='')
        print()

        for i in range(self.size):
            print(i + 1, ' ', end='')
            for j in self.board[i]:
                if j.situation is Situation.FULL:
                    print('F  ', end='')
                else:
                    print('-  ', end='')
            print()


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.ships = []
        self.map = Map(10)

    def insert_ship(self, ship):
        pass

    def shoot(self, enemy):
        pass


class GameMode(Enum):
    SINGLE = auto()
    MULTI = auto()


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.turn = 1

    def run(self):
        pass

    def display_scores(self):
        pass

    def check_if_finished(self):
        pass

    def finish(self):
        pass


def display_menu():
    print('\t\tBATTLESHIP')
    print('1. Play with a friend')
    print('2. Play with a bot')
    print('3. Create a new user')
    print('4. Scoreboard')
    print('5. Exit')


def process_choice():
    if choice == 1:
        play_with_friend()
    elif choice == 2:
        play_with_bot()
    elif choice == 3:
        create_new_user()
    elif choice == 4:
        show_scoreboard()
    elif choice == 5:
        pass
    else:
        print('Invalid input')


def play_with_friend():
    print('a multiplayer game has been started.')


def play_with_bot():
    print('a single player game has been started.')


def create_new_user():
    print('a new user has been created.')


def show_scoreboard():
    print('scoreboard has been shown.')


choice = 0
# while choice != 5:
#     display_menu()
#     choice = int(input())
#     process_choice()

map1 = Map(5)
map1.board[0][3].situation = Situation.FULL
map1.board[0][4].situation = Situation.FULL
map1.board[1][1].situation = Situation.WATER
map1.board[2][3].situation = Situation.EXPLODED
map1.board[4][0].situation = Situation.COMPLETED
map1.board[4][1].situation = Situation.COMPLETED

map1.display()
print('\n_________________\n')
map1.display_for_owner()
