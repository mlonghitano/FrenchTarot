from copy import deepcopy

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def set_score(self, score):
        self.score = score

class GameState:
    def __init__(self, players):
        self.players = deepcopy(players)  # Deepcopy to copy the list of Player objects

def validate_cards(cards):
    # Existing cards in the game
    valid_cards = ['f', '1h', '21'] + [str(i) for i in range(1, 21)] + ['r', 'd', 'c', 'v']
    
    # Check if each card is valid and count occurrences of each card
    card_counts = {}
    for card in cards:
        if card not in valid_cards:
            return False, f"'{card}' is not a recognized card."
        
        card_counts[card] = card_counts.get(card, 0) + 1
        
        # Ensure no numbered card (1-10) appears more than 5 times
        if card.isnumeric() and int(card) <= 10 and card_counts[card] > 5:
            return False, f"'{card}' appears more than 5 times."
        
        # Ensure cards 11-21, '1h', 'f', and '21' appear only once
        if card in ['f', '1h', '21'] or (card.isnumeric() and int(card) > 10) and card_counts[card] > 1:
            return False, f"'{card}' appears more than once."
        
        # Ensure face cards appear at most 4 times
        if card in ['r', 'd', 'c', 'v'] and card_counts[card] > 4:
            return False, f"'{card}' appears more than 4 times."
            
    return True, ""

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

    # List to hold game states, works as a stack
    game_states = []  

    # Play the rounds
    round_counter = 0
    while round_counter < num_rounds:
        print(f"\nRound {round_counter + 1}")

        # Save the current game state before making changes
        current_state = GameState(players)
        game_states.append(current_state)

        while True:
            try:
                taker_index = int(input("Enter the index (0-3) of the player who is the taker for this round: "))
                if taker_index in [0, 1, 2, 3]:
                    break
                else:
                    print("Invalid input! Please enter a number between 0 and 3.")
            except ValueError:
                print("Invalid input! Please enter a number between 0 and 3.")

        taker = players[taker_index]

        bid = input("Enter the bid (small, guard, guard without, guard against): ").lower()

        if bid == "small" or bid == "guard":
            print("Reminder: Please add the points from the middle cards to your final score.")
        elif bid == "guard without":
            print("Reminder: You will not see the middle cards but their points will be added to your final score.")
        elif bid == "guard against":
            print("Reminder: You will not see the middle cards and their points will be given to your opponents.")

        cards = input("Enter the cards won by the taker this round, separated by spaces (e.g. r d 3 10): ").lower().split()

        valid, error_message = validate_cards(cards)
        while not valid:
            print(f"Invalid card input: {error_message}")
            cards = input("Enter the cards won by the taker this round, separated by spaces (e.g. r d 3 10): ").lower().split()
            valid, error_message = validate_cards(cards)

        score_won = calculate_score(cards, bid)
        taker.score += score_won * 3

        print(f"\n{taker.name} scored {score_won * 3} points this round. Their total score is now {taker.score}.")

        for j, player in enumerate(players):
            if j != taker_index:
                player.score -= score_won
                print(f"{player.name}'s total score is now {player.score}.")

        undo_input = input("Do you want to undo this round? (y/n): ")
        if undo_input.lower() == 'y' and game_states:
            last_state = game_states.pop()  # Get the last saved state
            players = last_state.players  # Restore players from the saved state
            print("Round undone. Please re-enter details for this round.")
            continue  # Jump to the beginning of the loop
        round_counter += 1  # Only increment if round is not undone

if __name__ == "__main__":
    main()
