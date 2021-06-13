# tariq@bluecrowtech.com  intro-to-programming nanodegree
# rps_game.py v2021-01-25
# Rock Paper Scissors game

# !/usr/bin/env python3

"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""
import random
import inspect
import sys
import time
import os


moves = ['rock', 'paper', 'scissors']

strategies = {
        'fixed': 'starts with a random choice and does not change.',
        'random': 'makes a new random choice each turn.',
        'cycle': 'starts with a random choice and cycles through each choice.',
        'reflect': 'plays what the opponent played the previous turn.'
        }


def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


def print_beats(one, two):
    if ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock')):
        print(f"'{one.capitalize()}' beats '{two.capitalize()}'!")
        return True
    else:
        return False


def get_player_classes():
    player_class_names = []

    # https://docs.python.org/3/library/inspect.html#inspect.getmembers
    # https://docs.python.org/3/library/sys.html#sys.modules
    # sys.modules is a dictionary that maps module names to loaded modules
    # sys.modules[__name__] uses __name__ as a key to get current module
    # inspect.getmembers will return all the members of an object in a list
    # This method adds the class name for all Player type classes to a list
    # Original suggestion https://stackoverflow.com/questions/1796180

    for n, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if (issubclass(obj, sys.modules[__name__].Player)):
            player_class_names.append(obj.__name__)

    return player_class_names


def select_random_player_class():
    random_player_class = random.choice(get_player_classes())

    if random_player_class == "Player":
        return Player()
    elif random_player_class == "CyclePlayer":
        return CyclePlayer()
    elif random_player_class == "ReflectPlayer":
        return ReflectPlayer()
    else:
        return RandomPlayer()


class Player:
    strategy = "Fixed"
    is_human = False

    def __init__(self):
        self.points = 0
        self.player_name = "Computer"

    def move(self):
        return 'rock'

    def learn(self, my_move, their_move):
        pass

    def add_points(self, points):
        self.points += points

    def get_player_name(self):
        pass


class RandomPlayer(Player):
    strategy = "Random"

    def move(self):
        return random.choice(moves)


class HumanPlayer(Player):
    strategy = "Human"
    is_human = True

    def move(self):
        move = "none"
        while move not in moves:
            move = input("Rock, paper, scissors (or quit):\n").lower()
            if move == 'quit':
                break

        return move

    def get_player_name(self):
        self.player_name = input("Please enter your name:\n")


class ReflectPlayer(Player):
    strategy = "Reflect"

    def __init__(self):
        super().__init__()
        self.their_move = "unknown"

    def learn(self, my_move, their_move):
        self.their_move = their_move

    def move(self):
        if self.their_move == "unknown":
            return random.choice(moves)
        else:
            return self.their_move


class CyclePlayer(Player):
    strategy = "Cycle"

    def __init__(self):
        super().__init__()
        self.my_move = random.choice(moves)

    def learn(self, my_move, their_move):
        self.my_move = my_move

    def move(self):
        # Set self.move to the next move in the list of valid moves
        # Start at the begining when we get to the end of the list
        self.my_move = moves[(moves.index(self.my_move) + 1) % len(moves)]
        return self.my_move


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.player_quit = False
        self.current_round = 1
        self.current_streak = 0
        self.last_winner = "none"
        self.max_streak_length = 3

    def play_round(self):
        print(f"**********Round {self.current_round}***********")

        move1 = self.p1.move()
        move2 = self.p2.move()

        if move1 != 'quit' and move2 != 'quit':
            self.print_moves(move1, move2)

            self.keep_score(move1, move2)

            print(f"\nLength of current streak: {self.current_streak}")
            self.print_score()

            self.p1.learn(move1, move2)
            self.p2.learn(move2, move1)

            self.current_round += 1
        else:
            self.player_quit = True
            time.sleep(1)

    def print_moves(self, move1, move2):
        print(f"Player 1 ({self.p1.player_name}) threw '{move1}'!\n"
              f"Player 2 ({self.p2.player_name}) threw '{move2}'!")

    def keep_score(self, move1, move2):
        if print_beats(move1, move2):
            result = f"{self.p1.player_name} (Player 1) wins!"
            self.p1.add_points(1)

        elif print_beats(move2, move1):
            result = f"{self.p2.player_name} (Player 2) wins!"
            self.p2.add_points(1)

        else:
            result = "Tie!"

        print(result)
        time.sleep(4)

        self.update_streak(result)

    def update_streak(self, current_winner):
        if current_winner == self.last_winner:
            self.current_streak += 1
        elif current_winner == "Tie!":
            self.current_streak = 0
            self.last_winner = "none"
        else:
            self.current_streak = 1
            self.last_winner = current_winner

    def print_score(self):
        print("Score\n"
              "--------------\n"
              f"Player 1 ({self.p1.player_name}): {self.p1.points}\n"
              f"Player 2 ({self.p2.player_name}): {self.p2.points}"
              )

    def declare_winner(self):
        if (self.p1.points > self.p2.points):
            print(f"Player 1 ({self.p1.player_name}) Wins The Game!")
        elif (self.p2.points > self.p1.points):
            print(f"Player 2 ({self.p2.player_name}) Wins The Game!")
        else:
            print("Tie!")

    def show_player_strategies(self):
        print(f"Player 1 is using '{self.p1.strategy}' strategy.")
        print(f"Player 2 is using '{self.p2.strategy}' strategy.")

    def show_game_rules(self):
        print('********************************************************\n'
              'Rock, Paper, Scissors! - "jian dao, shi tou, bu"\n'
              '********************************************************\n\n'
              'This game will continue until you type "quit,"\n'
              'or if any player wins 3 throws in a row.\n\n'
              'Your opponent will use one of the strategies below.\n')

        for strategy, description in strategies.items():
            time.sleep(1)
            print(f"{strategy.capitalize()}: {description.capitalize()}")

        time.sleep(1)
        show_strategy = input("\nShow player strategies? "
                              "(enter 'y' or 'n'):\n").lower()

        while show_strategy not in ['y', 'n']:
            show_strategy = input("Please enter 'y' or 'n':\n").lower()

        if show_strategy == 'y':
            print("\nYou cheater ;-)!")
            time.sleep(2)
            print("Just kidding! Have fun!\n")
            self.show_player_strategies()
        else:
            print("\nI see you enjoy a challenge!\n")

        time.sleep(2)

    def get_player_names(self):
        if self.p1.is_human:
            self.p1.get_player_name()
        elif self.p2.is_human:
            self.p2.get_player_name()

    def game_over(self):
        return (self.player_quit or
                self.current_streak >= self.max_streak_length)

    def play_game(self):
        os.system('clear')

        self.show_game_rules()

        self.get_player_names()

        print("\n")
        print("Game start!")
        time.sleep(2)

        while not self.game_over():
            self.play_round()
            print("\n")

        print("Game over!")
        time.sleep(2)
        self.print_score()
        self.declare_winner()

        print(f"Your Opponent was using "
              f"{self.p2.strategy.capitalize()} strategy.")


if __name__ == '__main__':

    game = Game(HumanPlayer(), select_random_player_class())

    game.play_game()
