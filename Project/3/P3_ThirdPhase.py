from enum import Enum, auto


class Direction(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()


class Ship:
    def __init__(self, size, direction, top_left, bottom_right):
        self.size = size
        self.direction = direction
        self.top_left = top_left
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
            # print(chr(65 + i), ' ', end='')
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

    def insert_ship(self, size):
        print('insert a ship with size ', size, ' in your map, using its top_left and bottom_right coordinate.')
        repeat = True
        while repeat :
            print('top_left: ', end='')
            answer = input()
            top_left_row = ord(answer[0].upper()) - 65
            top_left_column = int(answer[1:]) - 1
            if top_left_row >= self.map.size or top_left_column >= self.map.size or self.map.board[top_left_row][top_left_column].situation is Situation.FULL:
                print('Invalid input. Please choose an acceptable block.')
            else:
                repeat = False

        repeat = True
        while repeat :
            print('bottom right: ', end='')
            answer = input()
            bottom_right_row = ord(answer[0].upper()) - 65
            bottom_right_column = int(answer[1:]) - 1
            if bottom_right_row >= self.map.size or bottom_right_column >= self.map.size or self.map.board[bottom_right_row][bottom_right_column].situation is Situation.FULL:
                print('Invalid input. Please choose an acceptable block.')
            else:
                repeat = False

        if top_left_row != bottom_right_row and top_left_column != bottom_right_column:
            print('The selected coordinates are not either in a single row or in a single column. Try again.')
            self.insert_ship(size)
            return

        if top_left_row == bottom_right_row:
            direction = Direction.HORIZONTAL
            if bottom_right_column - top_left_column != size:
                print('The size of the ship is not correct. Try again.')
                self.insert_ship(size)
                return
            for i in range(size):
                if self.map.board[top_left_row][top_left_column + i].situation is not Situation.EMPTY:
                    print('There is a blocking point in the selection area. Try again.')
                    self.insert_ship(size)
                    return

            for i in range(size):
                self.map.board[top_left_row][top_left_column + i].situation = Situation.FULL

            self.ships.append(Ship(size, direction, self.map.board[top_left_row][top_left_column],
                                   self.map.board[bottom_right_row][bottom_right_column]))
        elif top_left_column == bottom_right_column:
            direction = Direction.VERTICAL
            if bottom_right_row - top_left_row != size:
                print('The size of the ship is not correct. Try again.')
                self.insert_ship(size)
                return
            for i in range(size):
                if self.map.board[top_left_row + i][top_left_column].situation is not Situation.EMPTY:
                    print('There is a blocking point in the selection area. Try again.')
                    self.insert_ship(size)
                    return

            for i in range(size):
                self.map.board[top_left_row + i][top_left_column].situation = Situation.FULL

            self.ships.append(Ship(size, direction, self.map.board[top_left_row][top_left_column],
                                   self.map.board[bottom_right_row][bottom_right_column]))

    def shoot(self, enemy):
        print('Hey ', self.name, ', it\'s your turn: ')
        answer = input()
        row = ord(answer[0].upper()) - 65
        column = int(answer[1:]) - 1
        while enemy.map.board[row][column].situation != Situation.EMPTY and enemy.map.board[row][column].situation != Situation.FULL:
            print('Invalid input. Please choose an acceptable block.')
            answer = input()
            row = ord(answer[0].upper()) - 65
            column = int(answer[1]) - 1

        if enemy.map.board[row][column].situation == Situation.EMPTY:
            enemy.map.board[row][column].situation = Situation.WATER
        else:
            enemy.map.board[row][column].situation = Situation.EXPLODED


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
player1 = Player('Taha')
player1.map = map1
player2 = Player('Amir')
player2.shoot(player1)
map1.display()