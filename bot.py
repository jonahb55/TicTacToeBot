from enum import Enum
import random
import statistics as stats
from genome import Genome
from genome import Gene
from board import Symbol
from board import Board


class Direction(Enum):
    """Represents the four scan directions."""
    VERTICAL = 0
    HORZIONTAL = 1
    DIAGONAL_UP = 2  # lower left to upper right
    DIAGONAL_DOWN = 3  # upper left to lower right


class Bot:
    """Represents a bot with a genome capable of playing Tic-Tac-Toe."""
    genome = Genome(random_len=132)

    def __init__(self, genome=None, parents=None):
        if genome != None:
            self.genome = genome
            return
        if parents != None:
            self.genome = Genome(
                gametes=(parents[0].genome.gamete(), parents[1].genome.gamete()))

    def __trait(self, number):
        """Retrieves a single trait from the genome."""
        values = []
        value_lookup = {
            Gene.HOMOZYGOUS_RECESSIVE: -1,
            Gene.HETEROZYGOUS: 0,
            Gene.HOMOZYGOUS_DOMINANT: 1
        }
        for i in range(number * 4, number * 4 + 4):
            values.append(value_lookup[self.genome.genes[i]])
        return (stats.mean(values))

    def __count_symbol(self, board, target_symbol, position, direction):
        """Counts the number of matching symbols on the board from a positon in a direction."""
        lookup = {
            0: {
                Direction.VERTICAL: [3, 6],
                Direction.HORZIONTAL: [1, 2],
                Direction.DIAGONAL_UP: [],
                Direction.DIAGONAL_DOWN: [4, 8]
            },
            1: {
                Direction.VERTICAL: [4, 7],
                Direction.HORZIONTAL: [0, 2],
                Direction.DIAGONAL_UP: [3],
                Direction.DIAGONAL_DOWN: [5]
            },
            2: {
                Direction.VERTICAL: [5, 8],
                Direction.HORZIONTAL: [0, 1],
                Direction.DIAGONAL_UP: [4, 6],
                Direction.DIAGONAL_DOWN: []
            },
            3: {
                Direction.VERTICAL: [0, 6],
                Direction.HORZIONTAL: [4, 5],
                Direction.DIAGONAL_UP: [1],
                Direction.DIAGONAL_DOWN: [7]
            },
            4: {
                Direction.VERTICAL: [1, 7],
                Direction.HORZIONTAL: [3, 5],
                Direction.DIAGONAL_UP: [2, 6],
                Direction.DIAGONAL_DOWN: [0, 8]
            },
            5: {
                Direction.VERTICAL: [2, 8],
                Direction.HORZIONTAL: [3, 4],
                Direction.DIAGONAL_UP: [7],
                Direction.DIAGONAL_DOWN: [1]
            },
            6: {
                Direction.VERTICAL: [0, 3],
                Direction.HORZIONTAL: [7, 8],
                Direction.DIAGONAL_UP: [2, 4],
                Direction.DIAGONAL_DOWN: []
            },
            7: {
                Direction.VERTICAL: [1, 4],
                Direction.HORZIONTAL: [6, 8],
                Direction.DIAGONAL_UP: [5],
                Direction.DIAGONAL_DOWN: [3]
            },
            8: {
                Direction.VERTICAL: [2, 5],
                Direction.HORZIONTAL: [6, 7],
                Direction.DIAGONAL_UP: [],
                Direction.DIAGONAL_DOWN: [0, 4]
            }
        }
        count = 0
        for check_pos in lookup[position][direction]:
            if board.symbols[check_pos] == target_symbol:
                count += 1
        return count

    def play(self, board, player_symbol):
        """Plays a single turn and modifys the board."""
        opponents = {
            Symbol.X: Symbol.O,
            Symbol.O: Symbol.X
        }

        weights = []
        for position in range(9):
            weights.append(self.__trait(position))
            for direction in list(Direction):
                count = self.__count_symbol(
                    board, player_symbol, position, direction)
                weights[position] += self.__trait(9 +
                                                  (direction.value * 6) + count)
                count = self.__count_symbol(
                    board, opponents[player_symbol], position, direction)
                weights[position] += self.__trait(12 +
                                                  (direction.value * 6) + count)

        positions = [x for x in enumerate(
            weights) if board.symbols[x[0]] == Symbol.EMPTY]
        positions_max = max([x[1] for x in positions])
        positions = [x[0] for x in positions if x[1] == positions_max]
        board.set(random.choice(positions), player_symbol)
