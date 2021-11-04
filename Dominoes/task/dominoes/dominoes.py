# Write your code here
from dataclasses import dataclass, field
import random


# Create dominoes dataclass
@dataclass
class Dominoes:
    # Dominoes game elements
    all_pieces: list = field(default_factory=list)
    stock_pieces: list = field(default_factory=list)
    computer_pieces: list = field(default_factory=list)
    player_pieces: list = field(default_factory=list)
    domino_snake: list = field(default_factory=list)
    status: str = field(default=str)

    # Starting amount of pieces
    stock_pieces_amount: int = field(default=14)
    computer_pieces_amount: int = field(default=7)
    player_pieces_amount: int = field(default=7)

    def __post_init__(self):
        self.shuffle_pieces()
        self.starting_piece()

    def shuffle_pieces(self, mode="all"):
        if mode == "all":
            self.all_pieces = self.create_pieces()
            self.assign_pieces(self.stock_pieces, self.stock_pieces_amount)
            self.assign_pieces(self.computer_pieces, self.computer_pieces_amount)
            self.assign_pieces(self.player_pieces, self.player_pieces_amount)

    @staticmethod
    def create_pieces() -> list:
        complete_set = []
        for i in range(7):
            for j in range(7):
                if [j, i] not in complete_set:
                    complete_set.append([i, j])
        return complete_set

    def assign_pieces(self, location, number):
        random.seed()
        random.shuffle(self.all_pieces)
        for i in range(number):
            location.append(self.all_pieces.pop())

    def starting_piece(self):
        while True:
            computer_doubles = []
            player_doubles = []

            # Add doubles to computer list
            for domino in self.computer_pieces:
                if domino[0] == domino[1]:
                    computer_doubles.append(domino)

            # Add doubles to player list
            for domino in self.player_pieces:
                if domino[0] == domino[1]:
                    player_doubles.append(domino)

            # If both lists are empty: reshuffle
            # Else determine who has the highest double
            if len(computer_doubles) == 0 and len(player_doubles) == 0:
                self.shuffle_pieces()
            else:
                # If both have doubles
                if bool(computer_doubles) and bool(player_doubles):
                    if max(computer_doubles) > max(player_doubles):
                        self.status = "player"
                    else:
                        self.status = "computer"
                # If only computer has doubles
                # Else player has doubles
                elif bool(computer_doubles):
                    self.status = "player"
                else:
                    self.status = "computer"

                # Assign domino snake and remove domino depending on
                # who had the highest double, and remove the highest
                # double from the one who had it.
                if self.status == "player":
                    self.domino_snake.append(max(computer_doubles))
                    self.computer_pieces.remove(max(computer_doubles))
                    self.computer_pieces_amount -= 1
                else:
                    self.domino_snake.append(max(player_doubles))
                    self.player_pieces.remove(max(player_doubles))
                    self.player_pieces_amount -= 1

                # Double has been determined, exiting the loop
                break


def main():
    # Create dataclass with variables
    dominoes = Dominoes()

    print(f"Stock pieces: {dominoes.stock_pieces}")
    print(f"Computer pieces: {dominoes.computer_pieces}")
    print(f"Player pieces: {dominoes.player_pieces}")
    print(f"Domino snake: {dominoes.domino_snake}")
    print(f"Status: {dominoes.status}")


if __name__ == '__main__':
    main()
