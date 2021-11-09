# Write your code here
from dataclasses import dataclass, field
import random


# Create dominoes dataclass
@dataclass
class Dominoes:
    # Dominoes game elements
    complete_set: list = field(default_factory=list)
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
        self.create_pieces()
        self.shuffle_pieces()
        self.starting_piece()

    def shuffle_pieces(self, mode="all"):
        if mode == "all":
            self.all_pieces = self.complete_set.copy()
            self.assign_pieces(self.stock_pieces, self.stock_pieces_amount)
            self.assign_pieces(self.computer_pieces, self.computer_pieces_amount)
            self.assign_pieces(self.player_pieces, self.player_pieces_amount)

    def create_pieces(self):
        for i in range(7):
            for j in range(7):
                if [j, i] not in self.complete_set:
                    self.complete_set.append([i, j])

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


def user_interface(data: Dominoes):
    header = "=" * 70
    empty_line = ""
    print(header)
    print(f"Stock pieces: {data.stock_pieces_amount}")
    print(f"Computer pieces: {data.computer_pieces_amount}")
    print(empty_line)

    if len(data.domino_snake) <= 6:
        for piece in data.domino_snake:
            print(piece, end='')
    else:
        first_part = data.domino_snake[:3]
        second_part = data.domino_snake[-3:]

        for piece in first_part:
            print(piece, end='')

        print("...", end='')

        for piece in second_part:
            print(piece, end='')

    print(empty_line)
    print(empty_line)
    print("Your pieces:")

    for i, piece in enumerate(data.player_pieces):
        print(f"{i+1}: {piece}")

    print(empty_line)


def take_turn(data: Dominoes, participant, move):
    if participant == "player":
        piece = data.player_pieces
    else:
        piece = data.computer_pieces

    if move == 0:
        piece.append(data.stock_pieces.pop())
    elif move < 0:
        data.domino_snake.insert(0, piece.pop(abs(move) - 1))
    else:
        data.domino_snake.append(piece.pop(move - 1))

    data.player_pieces_amount = len(data.player_pieces)
    data.computer_pieces_amount = len(data.computer_pieces)
    data.stock_pieces_amount = len(data.stock_pieces)


def main():
    # Create dataclass with variables
    dominoes = Dominoes()

    while True:
        user_interface(dominoes)

        if dominoes.player_pieces_amount == 0:
            print("Status: The game is over. You won!")
            break
        elif dominoes.computer_pieces_amount == 0:
            print("Status: The game is over. The computer won!")
            break

        # To be added, draw condition with following output:
        # Status: The game is over. It's a draw!

        if dominoes.status == "player":
            print("Status: It's your turn to make a move. Enter your command.")

            try:
                user_action = int(input())
                assert abs(user_action) <= dominoes.player_pieces_amount
            except (ValueError, AssertionError):
                print("Invalid input. Please try again.")
                continue

            take_turn(dominoes, "player", user_action)
            dominoes.status = "computer"
        else:
            input("Status: Computer is about to make a move. Press Enter to continue...")
            computer_action = random.randint(-dominoes.computer_pieces_amount, dominoes.computer_pieces_amount)

            take_turn(dominoes, "computer", computer_action)
            dominoes.status = "player"


if __name__ == '__main__':
    main()
