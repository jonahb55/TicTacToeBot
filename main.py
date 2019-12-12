from genome import Genome
from board import Board
from board import Symbol
from bot import Bot
import random
import pickle


class Player:
    """Represents an interface for the user to play the game."""

    def play(self, board, player_symbol):
        """Plays a single turn and modifys the board."""
        print()
        print("Your turn (" + player_symbol.value + "):")
        print(board.text())
        board.set(int(input("Where would you like to move? (0-9) ")),
                  player_symbol)


def run_game(player1, player2, debug=False):
    board = Board()
    players = (player1, player2)
    player_symbols = (Symbol.O, Symbol.X)
    turn = -1
    while board.winner() == None and not board.filled():
        turn += 1
        players[turn % 2].play(board, player_symbols[turn % 2])

    if board.filled() and board.winner() == None:  # tie
        return None
    else:
        return player_symbols.index(board.winner())


def print_winner(winner):
    if winner == None:
        print("Tie!")
    elif winner == 0:
        print("O wins!")
    elif winner == 1:
        print("X wins!")


def evolve():
    population_size = 200
    population = []
    for _ in range(population_size):
        population.append(Bot())

    for generation_number in range(10000):
        print(generation_number)
        winners = []
        while len(population) >= 2:
            result = run_game(population[0], population[1])
            if result == None:
                result = random.getrandbits(1)
            winners.append(population[result])
            population = population[2:]

        population = []
        while len(population) < population_size:
            population.append(
                Bot(parents=(random.choice(winners), random.choice(winners))))

    pickle.dump(population, open("bot.p", "wb"))
    print_winner(run_game(population[0], Player(), debug=True))


def read():
    bot = pickle.load(open("bot.p", "rb"))[0]
    print_winner(run_game(bot, Player(), debug=True))


read()
