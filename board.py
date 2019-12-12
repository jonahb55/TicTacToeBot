from enum import Enum


class Symbol(Enum):
    """Represents an X or O."""
    X = "X"
    O = "O"
    EMPTY = "-"


class Board:
    """Represents the state of a board."""
    symbols = []

    def __init__(self):
        self.symbols = [Symbol.EMPTY] * 9

    def set(self, position, value):
        """Changes the symbol for a single position."""
        if self.symbols[position] == Symbol.EMPTY:
            self.symbols[position] = value

    def text(self):
        """Provides a text representation of the board."""
        lines = []
        for line_number in range(3):
            line = []
            for position in range(3):
                line.append(self.symbols[line_number * 3 + position].value)
            lines.append(" ".join(line))
        return "\n".join(lines)

    def filled(self):
        """Determines if board is filled."""
        return Symbol.EMPTY not in self.symbols

    def winner(self):
        """Determines the winner of the game."""
        win_positions = [
            (0, 1, 2),  # horizontal top
            (3, 4, 5),  # horizontal middle
            (6, 7, 8),  # horizontal bottom
            (0, 3, 6),  # verical left
            (1, 4, 7),  # vertical center
            (2, 5, 8),  # vertical right
            (0, 4, 8),  # diagonal top left to bottom right
            (2, 4, 6)  # diagonal top right to bottom left
        ]

        for win_symbol in (Symbol.X, Symbol.O):
            for win_position in win_positions:
                win = True
                for position in win_position:
                    if self.symbols[position] != win_symbol:
                        win = False
                        break
                if win:
                    return win_symbol
        return None
