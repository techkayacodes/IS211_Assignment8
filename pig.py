import random
import sys
import time
import argparse

# The Die class represents a die with the ability to roll and return a value between 1 and 6.
class Die:
    def __init__(self):
        self.value = random.randint(1, 6)

    def roll(self):
        self.value = random.randint(1, 6)
        return self.value

# The Player class represents a player in the game, with methods to manage the player's turn.
class Player:
    def __init__(self, name, is_human=True):
        self.name = name
        self.is_human = is_human
        self.turn_total = 0
        self.total_score = 0

    def take_turn(self):
        self.turn_total = 0
        while True:
            if self.is_human:
                choice = input(f"{self.name}, would you like to roll or hold? (r/h): ")
            else:
                choice = 'r' if self.turn_total < 20 else 'h'
                print(f"Computer chooses to {'roll' if choice == 'r' else 'hold'}.")

            if choice == 'r':
                roll = Die().roll()
                print(f"{self.name} rolled a {roll}")
                if roll == 1:
                    self.turn_total = 0
                    print("No points added, your turn is over.")
                    break
                else:
                    self.turn_total += roll
                    print(f"Turn total is {self.turn_total} and total score is {self.total_score}")
            elif choice == 'h':
                self.total_score += self.turn_total
                print(f"{self.name} holds. Total score is {self.total_score}")
                break
            else:
                print("Invalid choice. Please enter 'r' to roll or 'h' to hold.")

# The ComputerPlayer class inherits from Player and defines the computer's strategy.
class ComputerPlayer(Player):
    def take_turn(self):
        self.turn_total = 0
        while True:
            threshold = min(25, 100 - self.total_score)
            if self.turn_total >= threshold:
                choice = 'h'
            else:
                choice = 'r'

            print(f"{self.name} chooses to {'roll' if choice == 'r' else 'hold'}.")

            if choice == 'r':
                roll = Die().roll()
                print(f"{self.name} rolled a {roll}")
                if roll == 1:
                    self.turn_total = 0
                    print("No points added, your turn is over.")
                    break
                else:
                    self.turn_total += roll
                    print(f"Turn total is {self.turn_total} and total score is {self.total_score}")
            elif choice == 'h':
                self.total_score += self.turn_total
                print(f"{self.name} holds. Total score is {self.total_score}")
                break

# The PlayerFactory class creates a player based on the specified type.
class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return Player(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type. Expected 'human' or 'computer'.")

# The PigGame class manages the game flow, players, and determines when the game ends.
class PigGame:
    def __init__(self):
        self.players = []
        self.current_player = None

    def next_player(self):
        if self.current_player is None:
            self.current_player = self.players[0]
        else:
            current_index = self.players.index(self.current_player)
            self.current_player = self.players[(current_index + 1) % len(self.players)]

    def play_game(self):
        print("Pig Game Starting!")
        while all(player.total_score < 100 for player in self.players):
            self.next_player()
            print(f"It's {self.current_player.name}'s turn.")
            self.current_player.take_turn()

        winner = max(self.players, key=lambda player: player.total_score)
        print(f"{winner.name} wins with a score of {winner.total_score}!")

# The TimedGameProxy class adds a time limit to the PigGame.
class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = time.time()

    def play_game(self):
        while all(player.total_score < 100 for player in self.game.players) and time.time() - self.start_time < 60:
            self.game.next_player()
            print(f"It's {self.game.current_player.name}'s turn.")
            self.game.current_player.take_turn()

        if time.time() - self.start_time >= 60:
            winner = max(self.game.players, key=lambda player: player.total_score)
            print(f"Time's up! {winner.name} wins with a score of {winner.total_score}!")
        else:
            winner = max(self.game.players, key=lambda player: player.total_score)
            print(f"{winner.name} wins with a score of {winner.total_score}!")

# Main execution
if __name__ == "__main__":
    random.seed(0)

    parser = argparse.ArgumentParser(description='Play the game of Pig!')
    parser.add_argument('--player1', choices=['human', 'computer'], default='human', help="Specify if player1 is 'human' or 'computer'. Defaults to 'human'.")
    parser.add_argument('--player2', choices=['human', 'computer'], default='computer', help="Specify if player2 is 'human' or 'computer'. Defaults to 'computer'.")
    parser.add_argument('--timed', action='store_true', help='Set if the game is timed')

    args = parser.parse_args()

    player1 = PlayerFactory.create_player(args.player1, "Player 1")
    player2 = PlayerFactory.create_player(args.player2, "Player 2")

    game = PigGame()
    game.players = [player1, player2]

    if args.timed:
        game_proxy = TimedGameProxy(game)
        game_proxy.play_game()
    else:
        game.play_game()