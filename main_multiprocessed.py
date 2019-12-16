from genome import Genome
from board import Board
from board import Symbol
from bot import Bot
import random
import pickle
import time
import math
from multiprocessing import Pool


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


def format_duration(duration):
    temp_duration = duration
    hours = math.floor(temp_duration/3600)
    temp_duration -= hours*3600
    minutes = math.floor(temp_duration/60)
    seconds = temp_duration - minutes*60
    duration_formatted = ""
    if hours > 0:
        duration_formatted = str(hours) + "h "
    if minutes > 0:
        duration_formatted = duration_formatted + str(minutes) + "m "
    duration_formatted = duration_formatted + str(seconds) + "s"
    return(duration_formatted[:-1])


def print_winner(winner):
    if winner == None:
        print("Tie!")
    elif winner == 0:
        print("O wins!")
    elif winner == 1:
        print("X wins!")


def play_process(players):
    result = run_game(players[0], players[1])
    if result == None:
        result = random.getrandbits(1)
    return players[result]


def evolve():
    population_size = 200
    generation_count = 10000
    mutation_rate = 0.05
    pool = Pool(4)

    population = []
    for _ in range(population_size):
        population.append(Bot())

    game_count = 0
    game_total = population_size * generation_count * 0.5
    start_time = time.time()
    for _ in range(generation_count):
        matchups = []
        while len(population) >= 2:
            matchups.append([population[0], population[1]])
            population = population[2:]

        winners = pool.map(play_process, matchups)

        population = []
        while len(population) < population_size:
            child = Bot(parents=(random.choice(
                winners), random.choice(winners)))
            child.genome.mutate(mutation_rate)
            population.append(child)

        game_count += population_size / 2
        game_rate = (time.time() - start_time) / game_count
        percent = round((game_count / game_total) * 100, 3)
        etr = round((game_total - game_count) * game_rate)
        fill = " " * (7 - len(str(percent)))
        print("  " + str(percent) + "%" + fill + "- " + format_duration(etr) + "s ETR       ", end="\r")

    pickle.dump(population, open("bots_multi.p", "wb"))
    print()
    print_winner(run_game(population[0], Player(), debug=True))


def read():
    bot = pickle.load(open("bots_multi.p", "rb"))[0]
    print_winner(run_game(bot, Player(), debug=True))


evolve()
