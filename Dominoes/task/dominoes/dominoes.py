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
        # self.ai_set_values()
        # print(self.computer_values)

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


def take_turn(data: Dominoes, move):
    # Get pieces from player or computer
    if data.status == "player":
        pieces = data.player_pieces
    else:
        pieces = data.computer_pieces

    # Make index for chosen piece
    # and retrive selected piece
    piece_index = abs(move) - 1
    selected_piece = pieces[piece_index]

    # Action depending on user input
    if move == 0:
        pieces.append(data.stock_pieces.pop())
    elif move < 0:
        if data.domino_snake[0][0] != selected_piece[1]:
            pieces[piece_index] = selected_piece[::-1]
        data.domino_snake.insert(0, pieces.pop(piece_index))
    else:
        if data.domino_snake[-1][1] != selected_piece[0]:
            pieces[piece_index] = selected_piece[::-1]
        data.domino_snake.append(pieces.pop(piece_index))

    data.player_pieces_amount = len(data.player_pieces)
    data.computer_pieces_amount = len(data.computer_pieces)
    data.stock_pieces_amount = len(data.stock_pieces)


def computer_turn(data: Dominoes):
    value_count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    snake_computer_pieces = data.computer_pieces[::] + data.domino_snake[::]
    for domino in snake_computer_pieces:
        value_count[domino[0]] += 1
        value_count[domino[1]] += 1

    domino_scores = {}

    for domino in data.computer_pieces:
        score = value_count[domino[0]] + value_count[domino[1]]
        domino_scores.setdefault(score, []).append(domino)

    while True:
        highest_score = domino_scores.pop([max(domino_scores.keys())][0]).pop()
        idx = data.computer_pieces.index(highest_score)
        if valid_move(data, idx):
            return idx
        else:
            if len(domino_scores) > 0:
                continue
            else:
                return 0


def valid_move(data: Dominoes, move) -> bool:
    if move == 0:
        return True

    if data.status == "computer":
        piece = data.computer_pieces[abs(move) - 1]
    else:
        piece = data.player_pieces[abs(move) - 1]

    left_side = data.domino_snake[0]
    right_side = data.domino_snake[-1]

    if left_side[0] in piece and move < 0:
        return True
    elif right_side[1] in piece and move > 0:
        return True
    else:
        return False


def get_action(data: Dominoes) -> int:
    if data.status == "player":
        pieces_amount = data.player_pieces_amount
    else:
        pieces_amount = data.computer_pieces_amount

    while True:
        # Check if user input is valid
        try:
            if data.status == "player":
                action = int(input())
            else:
                action = computer_turn(data)
            assert abs(action) <= pieces_amount
        except (ValueError, AssertionError):
            if data.status == "player":
                print("Invalid input. Please try again.")
            continue

        # Check if move is valid
        try:
            assert valid_move(data, action)
        except AssertionError:
            if data.status == "player":
                print("Illegal move. Please try again.")
            continue
        else:
            break

    return action


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
        elif dominoes.stock_pieces_amount == 0:
            print("Status: The game is over. It's a draw!")
            exit()

        # To be added, draw condition with following output:
        # Status: The game is over. It's a draw!

        if dominoes.status == "player":
            print("Status: It's your turn to make a move. Enter your command.")

            take_turn(dominoes, get_action(dominoes))
            dominoes.status = "computer"
        else:
            input("Status: Computer is about to make a move. Press Enter to continue...")

            take_turn(dominoes, get_action(dominoes))
            dominoes.status = "player"


if __name__ == '__main__':
    main()
