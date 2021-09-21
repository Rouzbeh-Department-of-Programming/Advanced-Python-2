import os
from enum import Enum, auto
from pyautogui import hotkey
from time import sleep


class Direction(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()


class Ship:
    def __init__(self, size, direction, top_left, bottom_right):
        self.size = size
        self.direction = direction
        self.top_left = top_left
        self.bottom_right = bottom_right

    def check_if_is_destroyed(self, owner):
        if self.direction is Direction.HORIZONTAL:
            for i in range(self.size):
                if owner.map.board[self.top_left.y][self.top_left.x + i].situation is Situation.FULL:
                    return False
            return True
        else:
            for i in range(self.size):
                if owner.map.board[self.top_left.y + i][self.top_left.x].situation is Situation.FULL:
                    return False
            return True

    def destroy(self, owner, enemy):
        if self.direction is Direction.HORIZONTAL:
            for i in range(self.size):
                owner.map.board[self.top_left.y][self.top_left.x + i].situation = Situation.COMPLETED
        else:
            for i in range(self.size):
                owner.map.board[self.top_left.y + i][self.top_left.x].situation = Situation.COMPLETED

        if self.size == 5:
            enemy.score += 5
        elif self.size == 3:
            enemy.score += 8
        elif self.size == 2:
            enemy.score += 12
        elif self.size == 1:
            enemy.score += 25

        owner.ships.remove(self)


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
            print(chr(65 + i), ' ', end='')
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
            print(chr(65 + i), ' ', end='')
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
        print('Insert a ship with size', size)

        repeat = True
        while repeat:
            print('Enter the top-left coordinate. (example: a1) ', end='')
            answer = input()
            top_left_row = ord(answer[0].upper()) - 65
            top_left_column = int(answer[1:]) - 1
            if top_left_row >= self.map.size or top_left_column >= self.map.size:
                print('Invalid input. Try again.')
            else:
                repeat = False

        repeat = True
        while repeat:
            print('Enter the bottom-right coordinate. (example: a1) ', end='')
            answer = input()
            bottom_right_row = ord(answer[0].upper()) - 65
            bottom_right_column = int(answer[1:]) - 1
            if bottom_right_row >= self.map.size or bottom_right_column >= self.map.size:
                print('Invalid input. Try again.')
            else:
                repeat = False

        if top_left_row != bottom_right_row and top_left_column != bottom_right_column:
            print('The selected coordinates are either not a single row or in a single column.')
            self.insert_ship(size)
            return

        if top_left_row == bottom_right_row:
            direction = Direction.HORIZONTAL
            if bottom_right_column - top_left_column + 1 != size:
                print('The size of the selected area is not valid. Try again.')
                self.insert_ship(size)
                return

            for i in range(size):
                if self.map.board[top_left_row][top_left_column + i].situation is Situation.FULL:
                    print('There are some blocking points.')
                    return

            for i in range(size):
                self.map.board[top_left_row][top_left_column + i].situation = Situation.FULL
        else:
            direction = Direction.VERTICAL
            if bottom_right_row - top_left_row + 1 != size:
                print('The size of the selected area is not valid. Try again.')
                self.insert_ship(size)
                return

            for i in range(size):
                if self.map.board[top_left_row + i][top_left_column].situation is Situation.FULL:
                    print('There are some blocking points.')
                    self.insert_ship(size)
                    return

            for i in range(size):
                self.map.board[top_left_row + i][top_left_column].situation = Situation.FULL

        self.ships.append(Ship(size, direction, self.map.board[top_left_row][top_left_column],
                               self.map.board[bottom_right_row][bottom_right_column]))

    def shoot(self, enemy):
        print('Hey ' + self.name + ', it\'s your turn.')
        answer = input()
        row = ord(answer[0].upper()) - 65
        column = int(answer[1:]) - 1
        while row >= enemy.map.size or column >= enemy.map.size or (
                enemy.map.board[row][column].situation is not Situation.EMPTY and enemy.map.board[row][
            column].situation is not Situation.FULL):
            print('Invalid input. Choose an acceptable block.')
            answer = input()
            row = ord(answer[0].upper()) - 65
            column = int(answer[1:]) - 1

        if enemy.map.board[row][column].situation is Situation.EMPTY:
            enemy.map.board[row][column].situation = Situation.WATER
        else:
            enemy.map.board[row][column].situation = Situation.EXPLODED
            self.score += 1

    def play(self, enemy):
        enemy.map.display()
        self.shoot(enemy)
        for ship in enemy.ships:
            if ship.check_if_is_destroyed(enemy):
                ship.destroy(enemy, self)


class GameMode(Enum):
    SINGLE = auto()
    MULTI = auto()


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.turn = 1

    def run(self):
        ship_sizes = (5, 3)

        for i in ship_sizes:
            clear_console_pycharm()
            print(self.player1.name + ', build your map.')
            self.player1.map.display_for_owner()
            self.player1.insert_ship(i)

        for i in ship_sizes:
            clear_console_pycharm()
            print(self.player2.name + ', build your map.')
            self.player2.map.display_for_owner()
            self.player2.insert_ship(i)

        for i in range(5):
            clear_console_pycharm()
            self.display_scores()
            self.player1.play(self.player2)

            clear_console_pycharm()
            self.display_scores()
            self.player2.map.display()
            sleep(2)

            clear_console_pycharm()
            self.display_scores()
            self.player2.play(self.player1)

            clear_console_pycharm()
            self.display_scores()
            self.player1.map.display()
            sleep(2)

    def display_scores(self):
        print('\t' + self.player1.name + ': ' + str(self.player1.score) + '\t' + self.player2.name + ': ' + str(
            self.player2.score))

    def check_if_finished(self):
        pass

    def finish(self):
        pass


def clear_console():
    os.system('cls')


def clear_console_pycharm():
    hotkey('ctrl', 'alt', 'l')


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

p1 = Player('Ali')
p2 = Player('Mohammad')

game = Game(p1, p2)
game.run()
