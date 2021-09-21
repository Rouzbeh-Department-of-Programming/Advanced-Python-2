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
        ship_sizes = (5, 3, 3, 2, 2, 2, 1, 1, 1, 1)

        self.player1.map = Map(10)
        for i in ship_sizes:
            clear_console_pycharm()
            print(self.player1.name + ', build your map.')
            self.player1.map.display_for_owner()
            self.player1.insert_ship(i)

        self.player2.map = Map(10)
        for i in ship_sizes:
            clear_console_pycharm()
            print(self.player2.name + ', build your map.')
            self.player2.map.display_for_owner()
            self.player2.insert_ship(i)

        while True:
            clear_console_pycharm()
            self.display_scores()
            self.player1.play(self.player2)

            clear_console_pycharm()
            self.display_scores()
            self.player2.map.display()
            sleep(2)

            if self.check_if_finished():
                break

            clear_console_pycharm()
            self.display_scores()
            self.player2.play(self.player1)

            clear_console_pycharm()
            self.display_scores()
            self.player1.map.display()
            sleep(2)

            if self.check_if_finished():
                break

        self.finish()

    def display_scores(self):
        print('\t' + self.player1.name + ': ' + str(self.player1.score) + '\t' + self.player2.name + ': ' + str(
            self.player2.score))

    def check_if_finished(self):
        if len(self.player1.ships) == 0 or len(self.player2.ships) == 0:
            return True
        else:
            return False

    def finish(self):
        clear_console_pycharm()
        self.display_scores()

        if len(self.player1.ships) == 0:
            print('Well well well! The game is finished and the winner is', self.player2.name, ':)))))')
        else:
            print('Well well well! The game is finished and the winner is', self.player1.name, ':)))))')


def clear_console():
    os.system('cls')


def clear_console_pycharm():
    hotkey('ctrl', 'alt', 'l')


def display_menu():
    clear_console_pycharm()
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
    clear_console_pycharm()

    if len(players) < 2:
        print('There is not enough players to start a game.')
        sleep(2)
        return

    print('OK. Here is the list of the players.\n')
    for i in range(len(players)):
        print(str(i + 1) + '. ' + players[i].name)

    print('\nChoose the appropriate index for the player 1:')
    player1_index = int(input())

    if player1_index < 1 or player1_index > len(players):
        print('Invalid input. Try again.')
        sleep(2)
        return

    print('\nOK. Now choose the appropriate index for the player 2:')
    player2_index = int(input())

    if player2_index < 1 or player2_index > len(players) or player2_index == player1_index:
        print('Invalid input. Try again.')
        sleep(2)
        return

    game = Game(players[player1_index - 1], players[player2_index - 1])
    game.run()

    print('press \'enter\' to go back to the menu.')
    input()


def play_with_bot():
    print('This part is under construction :)')
    sleep(2)


def create_new_user():
    clear_console_pycharm()
    print('OK. Choose a username for yourself.')
    username = input()

    for player in players:
        if player.name == username:
            print('There is already a player with this username.')
            sleep(2)
            return
    # this part could be done by overriding __eq__ method of class Player, and using count method on players list

    players.append(Player(username))


def show_scoreboard():
    clear_console_pycharm()
    for i in range(len(players)):
        print(str(i + 1) + '. ' + players[i].name + ' - ' + str(players[i].score) + ' points')
    print('\npress \'enter\' to go back to the menu.')
    input()


players = []

choice = 0
while choice != 5:
    display_menu()
    choice = int(input())
    process_choice()
