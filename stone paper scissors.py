import random
import time
from dataclasses import dataclass, field

@dataclass
class RPSRules:
    # Rules can be extended easily!
    defeats: dict = field(default_factory=lambda: {
        "rock":     ["scissors"],
        "paper":    ["rock"],
        "scissors": ["paper"],
    })

    def result(self, p1: str, p2: str) -> str:
        if p1 == p2:
            return "tie"
        return "win" if p2 in self.defeats[p1] else "lose"


class SmartAI:
    """
    Learns from player's previous moves.
    Computer increases probability of choosing a counter-move.
    """
    def __init__(self, rules: RPSRules):
        self.rules = rules
        self.player_history = []

    def choose(self):
        moves = list(self.rules.defeats.keys())

        if not self.player_history:
            return random.choice(moves)

        # Predict the player's next move as their most common one
        predicted = max(set(self.player_history), key=self.player_history.count)

        # Counter that predicted move
        counters = [m for m in moves if predicted in self.rules.defeats[m]]

        # Weighted randomness
        weights = []
        for m in moves:
            if m in counters:
                weights.append(0.6)   # AI biases towards winning
            else:
                weights.append(0.2)

        return random.choices(moves, weights=weights, k=1)[0]


class RPSGame:
    def __init__(self, rounds=3):
        self.rules = RPSRules()
        self.ai = SmartAI(self.rules)
        self.rounds = rounds
        self.score = {"player": 0, "computer": 0, "ties": 0}

    def get_player_choice(self):
        moves = list(self.rules.defeats.keys())
        while True:
            choice = input(f"Choose {', '.join(moves)}: ").strip().lower()
            if choice in moves:
                return choice
            print("Invalid input. Try again.")

    def play_round(self):
        player = self.get_player_choice()
        computer = self.ai.choose()
        self.ai.player_history.append(player)

        print(f"\nYou chose:      {player}")
        time.sleep(0.3)
        print(f"Computer chose: {computer}")
        time.sleep(0.3)

        outcome = self.rules.result(player, computer)

        if outcome == "win":
            print("👉 You WIN this round!")
            self.score["player"] += 1
        elif outcome == "lose":
            print("👎 You LOSE this round!")
            self.score["computer"] += 1
        else:
            print("🤝 It's a TIE.")
            self.score["ties"] += 1

    def play(self):
        print("\n=== Advanced Rock–Paper–Scissors ===")
        print("AI learns from your behavior!\n")

        for r in range(1, self.rounds + 1):
            print(f"\n--- Round {r} of {self.rounds} ---")
            self.play_round()

        print("\n=== Final Score ===")
        print(f"You:       {self.score['player']}")
        print(f"Computer:  {self.score['computer']}")
        print(f"Ties:      {self.score['ties']}")

        if self.score["player"] > self.score["computer"]:
            print("\n🎉 You WIN the game!")
        elif self.score["player"] < self.score["computer"]:
            print("\n💀 You LOSE the game!")
        else:
            print("\n🤝 It's a TIE game!")


if __name__ == "__main__":
    game = RPSGame(rounds=5)  # You can change number of rounds here
    game.play()


