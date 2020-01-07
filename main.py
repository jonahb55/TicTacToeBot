from genome import Genome
from board import Board
from board import Symbol
from bot import Bot
import random
import pickle
import time
import math
from multiprocessing import Pool
import os


class Player:
    """Represents an interface for the user to play the game."""

    def play(self, board, player_symbol):
        """Plays a single turn and modifys the board."""
        print()
        print("Your turn (" + player_symbol.value + "):")
        print(board.text())
        board.set(int(input("Where would you like to move? (0-9) ")),
                  player_symbol)


def run_game(player1, player2, tie_randomize=False):
    """Plays one game and determines the winner (0=p1,1=p2,None=tie)"""
    board = Board()
    players = (player1, player2)
    player_symbols = (Symbol.O, Symbol.X)
    turn = -1
    while board.winner() == None and not board.filled():
        turn += 1
        players[turn % 2].play(board, player_symbols[turn % 2])

    if board.filled() and board.winner() == None:  # tie
        if tie_randomize:
            return random.getrandbits(1)
        else:
            return None
    else:
        return player_symbols.index(board.winner())


def format_duration(duration):
    """Writes a duration in human readable format."""
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
    """Prints a winner in human readable format."""
    if winner == None:
        print("Tie!")
    elif winner == 0:
        print("O wins!")
    elif winner == 1:
        print("X wins!")


def play_process(matchup):
    winner = run_game(matchup[0]["bot"], matchup[1]["bot"], tie_randomize=True)
    return matchup[winner]


def play_reference(bot):
    if random.getrandbits(1) == 0:
        winner = run_game(bot, reference_bot, tie_randomize=True)
        success = winner == 0
    else:
        winner = run_game(reference_bot, bot, tie_randomize=True)
        success = winner == 1
    if success:
        return 1
    else:
        return 0


# Main code
reference_genome = Genome(text="Aa-Aa-Aa-Aa-aa-aa-aa-aa-Aa-Aa-Aa-Aa-aa-aa-aa-aa-AA-AA-AA-AA-aa-aa-aa-aa-Aa-Aa-Aa-Aa-aa-aa-aa-aa-Aa-Aa-Aa-Aa-aa-aa-aa-aa-AA-AA-AA-aa-AA-AA-AA-AA-aa-aa-aa-aa-AA-AA-AA-aa-AA-AA-AA-AA-aa-aa-aa-aa-AA-AA-AA-aa-AA-AA-AA-AA-aa-aa-aa-aa-AA-AA-AA-aa-AA-AA-AA-AA-aa-aa-aa-aa-AA-AA-AA-aa-AA-AA-AA-AA-aa-aa-aa-aa-AA-AA-AA-aa-AA-AA-AA-AA-aa-aa-aa-aa-AA-AA-AA-aa-AA-AA-AA-AA-aa-aa-aa-aa-AA-AA-AA-aa-AA-AA-AA-AA")
reference_bot = Bot(genome=reference_genome)
pool = Pool(32)


def trial(title, generation_count, population_sizes, mutation_rate, sexual, sample_rate):
    """Runs one trial and returns a list of bots and stats"""
    # Create starting populations
    populations = []
    for size in population_sizes:
        population = []
        for _ in range(size):
            population.append(Bot())
        populations.append(population)

    ratings = []
    sizes = []
    for generation in range(generation_count):
        # Evaluate generation
        print(time.strftime("%a %b %-d %-I:%M:%S %p"), "-", title,
              "- evaluating generation", generation + 1, "of", generation_count)

        sizes.append([len(x) for x in populations])

        generation_ratings = []
        for population in populations:
            sample = random.sample(
                population, round(len(population)*sample_rate))
            sample_result = pool.map(play_reference, sample)
            generation_ratings.append(sum(sample_result) / len(sample))
        ratings.append(generation_ratings)

        # Run generation
        print(time.strftime("%a %b %-d %-I:%M:%S %p"), "-", title,
              "- running generation", generation + 1, "of", generation_count)

        full_population = []
        for i in range(len(populations)):
            for bot in populations[i]:
                full_population.append({"bot": bot, "population_number": i})
        random.shuffle(full_population)

        matchups = []
        while len(full_population) >= 2:
            matchups.append([full_population[0], full_population[1]])
            full_population = full_population[2:]

        winners = pool.map(play_process, matchups)

        # Create next generation
        print(time.strftime("%a %b %-d %-I:%M:%S %p"), "-", title,
              "- breeding generation", generation + 1, "of", generation_count)

        winner_populations = []
        for _ in population_sizes:
            winner_populations.append([])
        for winner in winners:
            winner_populations[winner["population_number"]].append(
                winner["bot"])

        for i in range(len(population_sizes)):
            populations[i] = []
            if len(winner_populations[i]) == 0:  # all were eliminated, restart species
                for _ in range(2):
                    populations[i].append(Bot())
            for _ in range(len(winner_populations[i]) * 2):
                if sexual:
                    parents = [random.choice(
                        winner_populations[i]), random.choice(winner_populations[i])]
                    child = Bot(parents=parents)
                else:
                    parent = random.choice(winner_populations[i])
                    child = Bot(genome=parent.genome)
                child.genome.mutate(mutation_rate)
                populations[i].append(child)
    return {"title": title, "bots": populations, "ratings": ratings, "sizes": sizes}


def save_result(results):
    """Saves results using csv and pickle."""
    try:
        os.mkdir("results/" + results["title"])
    except FileExistsError:
        pass

    pickle.dump(results["bots"], open("results/" + results["title"] + "/bots.p", "wb"))

    rating_csv = open("results/" + results["title"] + "/ratings.csv", "w")
    sizes_csv = open("results/" + results["title"] + "/sizes.csv", "w")
    fields = "Generation"
    for i in range(len(results["ratings"][0])):
        fields += ",Population " + str(i + 1)
    rating_csv.write(fields + "\n")
    sizes_csv.write(fields + "\n")

    for i in range(len(results["ratings"])):
        line = str(i + 1)
        for value in results["ratings"][i]:
            line += "," + str(value)
        rating_csv.write(line + "\n")

    for i in range(len(results["sizes"])):
        line = str(i + 1)
        for value in results["sizes"][i]:
            line += "," + str(value)
        sizes_csv.write(line + "\n")

    rating_csv.close()
    sizes_csv.close()

save_result(trial("control", generation_count=30000, population_sizes=[200], mutation_rate=0.05, sexual=True, sample_rate=0.2))
save_result(trial("no_mutation", generation_count=30000, population_sizes=[200], mutation_rate=0, sexual=True, sample_rate=0.2))
save_result(trial("asexual", generation_count=30000, population_sizes=[200], mutation_rate=0.05, sexual=False, sample_rate=0.2))
save_result(trial("coevolution_2", generation_count=30000, population_sizes=[100, 100], mutation_rate=0.05, sexual=True, sample_rate=0.2))
save_result(trial("coevolution_4", generation_count=30000, population_sizes=[50, 50, 50, 50], mutation_rate=0.05, sexual=True, sample_rate=0.2))

# result = trial("Test", generation_count=10, population_sizes=[200], mutation_rate=0.05, sexual=True, sample_rate=0.5)
# pickle.dump(result, open("result.p", "wb"))

# result = pickle.load(open("result.p", "rb"))
# print_winner(run_game(result[0][0], Player()))

# print_winner(run_game(reference_bot, Player()))
