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
        if (card in ['f', '1h', '21'] and card_counts[card] > 1) or (card.isnumeric() and int(card) > 10 and card_counts[card] > 1):
            return False, f"'{card}' appears more than once."
        
        # Ensure face cards appear at most 4 times
        if card in ['r', 'd', 'c', 'v'] and card_counts[card] > 4:
            return False, f"'{card}' appears more than 4 times."
            
    return True, ""

def calculate_score(cards, bid, num_players):
    honor_card_values = {'f': 4.5, '1h': 4.5, '21': 4.5}
    face_card_values = {'r': 4.5, 'd': 3.5, 'c': 2.5, 'v': 1.5}
    other_card_values = {str(i): 0.5 for i in range(1, 21)} #has been checked and includes all cards from 1 - 20 in string format 
    other_card_values.update(face_card_values)  # Update the dictionary with face card values

    honor_cards = [card for card in cards if card in honor_card_values]
    other_cards = [card for card in cards if card in other_card_values]

    honor_points = sum(honor_card_values[card] for card in honor_cards)
    other_points = sum(other_card_values[card] for card in other_cards)

    points = honor_points + other_points
    honor_count = len(honor_cards)

    required_points = {0: 56, 1: 51, 2: 41, 3: 36}
    points_threshold = required_points[honor_count]

    print(f"The taker had {honor_count} honor card(s). The required score threshold was {points_threshold} points.")

    points_difference = abs(points - points_threshold)

    bid_multiplier = {'small': 1, 'guard': 2, 'guard without': 4, 'guard against': 6}

    petit_bonus = input("Petit bonus? (y/n): ")
    petit_bonus = 10 if petit_bonus.lower() == 'y' else 0

    handful_bonus = 0
    handful_input = input("Handful bonus? (y/n): ")
    if handful_input.lower() == 'y':
        if num_players == 3:
            handful_bonus_values = {10: 20, 13: 30, 15: 40}
        elif num_players == 4:
            handful_bonus_values = {10: 20, 13: 30, 15: 40}
        elif num_players == 5:
            handful_bonus_values = {8: 20, 10: 30, 13: 40}
        
        handful_cards = int(input(f"How many cards? {list(handful_bonus_values.keys())}: "))
        handful_bonus = handful_bonus_values.get(handful_cards, 0)

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
    return (score if points >= points_threshold else -score, points_difference, petit_bonus, handful_bonus, slam_bonus, bid_multiplier[bid], points, points_threshold)

def distribute_scores_three_players(players, taker_index, score_won):
    taker = players[taker_index]
    taker.score += score_won * 2
    for i, player in enumerate(players):
        if i != taker_index:
            player.score -= score_won

def distribute_scores_four_players(players, taker_index, score_won):
    taker = players[taker_index]
    taker.score += score_won * 3
    for i, player in enumerate(players):
        if i != taker_index:
            player.score -= score_won

def distribute_scores_five_players(players, taker_index, partner_index, score_won):
    taker = players[taker_index]
    partner = players[partner_index]
    
    # Taker gets score_won * 2 and partner gets the score_won
    taker.score += score_won * 2
    partner.score += score_won

    # Other players lose the score equally
    loss_per_player = score_won  # This equals to score_won, but kept for clarity.
    for i, player in enumerate(players):
        if i != taker_index and i != partner_index:
            player.score -= loss_per_player

def main():
    # Get the number of players (3, 4, or 5)
    while True:
        try:
            num_players = int(input("Enter the number of players (3, 4, or 5): "))
            if num_players in [3, 4, 5]:
                break
            else:
                print("Invalid input! Please enter 3, 4, or 5.")
        except ValueError:
            print("Invalid input! Please enter 3, 4, or 5.")

    # Initialize players
    player_names = []
    for i in range(num_players):
        player_name = input(f"Enter the name of player {i+1}: ")
        player_names.append(player_name)

    # Ensure entered names match number of players
    while len(set(player_names)) != num_players:
        print(f"You entered {len(set(player_names))} unique names but indicated there would be {num_players} players.")
        player_names = [input(f"Enter the name of player {i+1}: ") for i in range(num_players)]

    players = [Player(name) for name in player_names]

    # Get the number of rounds
    num_rounds = int(input("Enter the number of rounds: "))

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
                taker_number = int(input(f"Which player number (1-{num_players}) is going to be the taker for this round? "))
                taker_index = taker_number - 1
                if 1 <= taker_number <= num_players:
                    break
                else:
                    print(f"Invalid input! Please enter a number between 1 and {num_players}.")
            except ValueError:
                print(f"Invalid input! Please enter a number between 1 and {num_players}.")


        taker = players[taker_index]

        bid_options = ["small", "guard", "guard without", "guard against"]

        bid = input("Enter the bid (small, guard, guard without, guard against): ").lower()
        while bid not in bid_options:
            print("Invalid input! Please enter a valid bid type (small, guard, guard without, guard against).")
            bid = input("Enter the bid (small, guard, guard without, guard against): ").lower()

        if bid == "small" or bid == "guard":
            print("Reminder: Please add the points from the middle cards to your final score.")
        elif bid == "guard without":
            print("Reminder: You will not see the middle cards, and their points will be omitted from all final scores.")
        elif bid == "guard against":
            print("Reminder: You will not see the middle cards and their points will be given to your opponents.")

        cards = input("Enter the cards won by the taker this round, separated by spaces (e.g. r d 3 10): ").lower().split()

        valid, error_message = validate_cards(cards)
        while not valid:
            print(f"Invalid card input: {error_message}")
            cards = input("Enter the cards won by the taker this round, separated by spaces (e.g. r d 3 10): ").lower().split()
            valid, error_message = validate_cards(cards)

        score_won, points_difference, petit_bonus, handful_bonus, slam_bonus, bid_multiplier, points, points_threshold = calculate_score(cards, bid, num_players)


        print(f" The hand scored is {points}")
        print(f" The takers score is {score_won} = (25 + |{points} - {points_threshold}| + {petit_bonus}) * {bid_multiplier} + {handful_bonus} + {slam_bonus}")

        if num_players == 3:
            distribute_scores_three_players(players, taker_index, score_won)

        elif num_players == 4:
            distribute_scores_four_players(players, taker_index, score_won)

        elif num_players == 5:
            while True:
                try:
                    partner_number = int(input(f"Which player number (1-{num_players}) had the called king or queen? "))
                    if 1 <= partner_number <= num_players:
                        partner_index = partner_number - 1
                        break
                    else:
                        print(f"Invalid input! Please enter a number between 1 and {num_players}.")
                except ValueError:
                    print(f"Invalid input! Please enter a number between 1 and {num_players}.")

            distribute_scores_five_players(players, taker_index, partner_index, score_won)

        for player in players:
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