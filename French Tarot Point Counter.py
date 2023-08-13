class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

def calculate_score(cards, bid):
    honor_card_values = {'f': 4.5, '1h': 4.5, '21': 4.5}
    face_card_values = {'r': 4.5, 'd': 3.5, 'c': 2.5, 'v': 1.5}
    other_card_values = {str(i): 0.5 for i in range(1, 21)}
    other_card_values.update(face_card_values)  # Update the dictionary with face card values

    honor_cards = [card for card in cards if card in honor_card_values]
    other_cards = [card for card in cards if card in other_card_values]

    honor_points = sum(honor_card_values[card] for card in honor_cards)
    other_points = sum(other_card_values[card] for card in other_cards)

    points = honor_points + other_points
    honor_count = len(honor_cards)

    required_points = {0: 56, 1: 51, 2: 41, 3: 36}
    points_threshold = required_points[honor_count] if honor_count in required_points else 36

    print(f"The taker had {honor_count} honor card(s). The required score threshold was {points_threshold} points.")

    points_difference = points - points_threshold if points > points_threshold else points_threshold - points

    bid_multiplier = {'small': 1, 'guard': 2, 'guard without': 4, 'guard against': 6}

    petit_bonus = input("Petit bonus? (y/n): ")
    petit_bonus = 10 if petit_bonus.lower() == 'y' else 0

    handful_bonus = 0
    handful_input = input("Handful bonus? (y/n): ")
    if handful_input.lower() == 'y':
        handful_cards = int(input("How many cards? (10, 13, or 15): "))
        handful_bonus_values = {10: 20, 13: 30, 15: 40}
        handful_bonus = handful_bonus_values[handful_cards] if handful_cards in handful_bonus_values else 0

    slam_bonus = 0
    slam_input = input("Slam Bonus? (y/n): ")
    if slam_input.lower() == 'y':
        slam_declared = input("Was the slam declared? (y/n): ")
        if slam_declared.lower() == 'y':
            slam_met = input("Slam met? (y/n): ")
            if slam_met.lower() == 'y':
                slam_bonus = 400
            else:
                slam_bonus = -200
        else:
            slam_bonus = 200

    score = (25 + points_difference + petit_bonus) * bid_multiplier[bid] + slam_bonus + handful_bonus
    return score if points >= points_threshold else -score

def main():
    # Get the number of rounds
    num_rounds = int(input("Enter the number of rounds: "))

    # Initialize players
    player_names = ["Michael", "Joe", "Devin", "Seth"]
    players = [Player(name) for name in player_names]

    # Play the rounds
    for i in range(num_rounds):
        print(f"\nRound {i+1}")
        taker_index = int(input("Enter the index (0-3) of the player who is the taker for this round: "))
        taker = players[taker_index]

        bid = input("Enter the bid (small, guard, guard without, guard against): ").lower()

        if bid == "small" or bid == "guard":
            print("Reminder: Please add the points from the middle cards to your final score.")
        elif bid == "guard without":
            print("Reminder: You will not see the middle cards but their points will be added to your final score.")
        elif bid == "guard against":
            print("Reminder: You will not see the middle cards and their points will be given to your opponents.")

        cards = input("Enter the cards won by the taker this round, separated by spaces (e.g. r d 3 10): ").lower().split()

        score_won = calculate_score(cards, bid)
        taker.score += score_won * 3

        print(f"\n{taker.name} scored {score_won * 3} points this round. Their total score is now {taker.score}.")

        for j, player in enumerate(players):
            if j != taker_index:
                player.score -= score_won
                print(f"{player.name}'s total score is now {player.score}.")

if __name__ == "__main__":
    main()
