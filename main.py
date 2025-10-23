import random


hearts = ["🂱", "🂲", "🂳", "🂴", "🂵", "🂶", "🂷", "🂸", "🂹", "🂺", "🂻", "🂽", "🂾"]
spades = ["🂡", "🂢", "🂣", "🂤", "🂥", "🂦", "🂧", "🂨", "🂩", "🂪", "🂫", "🂭", "🂮"]
diamonds = ["🃁", "🃂", "🃃", "🃄", "🃅", "🃆", "🃇", "🃈", "🃉", "🃊", "🃋", "🃍", "🃎"]
clubs = ["🃑", "🃒", "🃓", "🃔", "🃕", "🃖", "🃗", "🃘", "🃙", "🃚", "🃛", "🃝", "🃞"]
all_cards = hearts + spades + diamonds + clubs

card_values = {
    "🂱": 1,
    "🂲": 2,
    "🂳": 3,
    "🂴": 4,
    "🂵": 5,
    "🂶": 6,
    "🂷": 7,
    "🂸": 8,
    "🂹": 9,
    "🂺": 10,
    "🂻": 11,
    "🂽": 12,
    "🂾": 13,
    "🂡": 1,
    "🂢": 2,
    "🂣": 3,
    "🂤": 4,
    "🂥": 5,
    "🂦": 6,
    "🂧": 7,
    "🂨": 8,
    "🂩": 9,
    "🂪": 10,
    "🂫": 11,
    "🂭": 12,
    "🂮": 13,
    "🃁": 1,
    "🃂": 2,
    "🃃": 3,
    "🃄": 4,
    "🃅": 5,
    "🃆": 6,
    "🃇": 7,
    "🃈": 8,
    "🃉": 9,
    "🃊": 10,
    "🃋": 11,
    "🃍": 12,
    "🃎": 13,
    "🃑": 1,
    "🃒": 2,
    "🃓": 3,
    "🃔": 4,
    "🃕": 5,
    "🃖": 6,
    "🃗": 7,
    "🃘": 8,
    "🃙": 9,
    "🃚": 10,
    "🃛": 11,
    "🃝": 12,
    "🃞": 13,
}


def create_deck():
    new_deck = all_cards.copy()
    random.shuffle(new_deck)
    return new_deck


def get_card_value(card):
    return card_values.get(card, 0)


def determine_joker(top_card):
    top_value = get_card_value(top_card)
    joker_value = (top_value % 13) + 1
    return joker_value


def deal_hands(deck, num_players=2, hand_size=7):
    hands = [[] for _ in range(num_players)]
    for _ in range(hand_size):
        for player in range(num_players):
            if deck:
                hands[player].append(deck.pop())
    return hands, deck


def can_pair(card1, card2, joker_value):
    val1 = get_card_value(card1)
    val2 = get_card_value(card2)

    if val1 == joker_value or val2 == joker_value:
        return True

    return val1 == val2


def find_best_pairs(hand, joker_value):
    if len(hand) == 0:
        return [], []

    value_groups = {}
    jokers = []

    for card in hand:
        val = get_card_value(card)
        if val == joker_value:
            jokers.append(card)
        else:
            if val not in value_groups:
                value_groups[val] = []
            value_groups[val].append(card)

    pairs = []
    unpaired = []

    for val, cards in value_groups.items():
        while len(cards) >= 2:
            pairs.append((cards.pop(), cards.pop()))
        unpaired.extend(cards)

    unpaired_after_jokers = []
    for card in unpaired:
        if jokers:
            pairs.append((card, jokers.pop()))
        else:
            unpaired_after_jokers.append(card)

    unpaired_after_jokers.extend(jokers)

    return pairs, unpaired_after_jokers


def is_winner(hand, joker_value):
    pairs, unpaired = find_best_pairs(hand, joker_value)
    return len(unpaired) == 0


def ai_choose_discard(hand, joker_value, discard_pile):
    pairs, unpaired = find_best_pairs(hand, joker_value)

    if not unpaired:
        return hand[0] if hand else None

    best_discard = None
    worst_score = -1

    for candidate in unpaired:
        candidate_val = get_card_value(candidate)

        if candidate_val == joker_value:
            continue

        test_hand = hand.copy()
        test_hand.remove(candidate)

        match_count = sum(1 for c in test_hand if get_card_value(c) == candidate_val)

        joker_count = sum(1 for c in test_hand if get_card_value(c) == joker_value)

        score = match_count * 10 + joker_count

        if best_discard is None or score < worst_score:
            worst_score = score
            best_discard = candidate

    if best_discard:
        return best_discard

    for card in unpaired:
        if get_card_value(card) != joker_value:
            return card

    return unpaired[0] if unpaired else hand[0]


def ai_decide_action(hand, discard_pile, deck, joker_value):
    if not discard_pile:
        return "deck"

    top_discard = discard_pile[-1]
    top_discard_value = get_card_value(top_discard)

    if top_discard_value == joker_value:
        return "discard"

    pairs_before, unpaired_before = find_best_pairs(hand, joker_value)

    test_hand = hand.copy()
    test_hand.append(top_discard)
    pairs_after, unpaired_after = find_best_pairs(test_hand, joker_value)

    improvement = len(unpaired_before) - len(unpaired_after)

    if improvement > 0:
        return "discard"

    direct_match = False
    for card in hand:
        if get_card_value(card) == top_discard_value:
            direct_match = True
            break

    if direct_match:
        has_joker = any(get_card_value(c) == joker_value for c in hand)
        if (
            has_joker
            or len([c for c in hand if get_card_value(c) == top_discard_value]) >= 1
        ):
            return "discard"

    return "deck"


def play_game(hands, deck, joker_card, joker_value, num_players=2):
    discard_pile = []
    current_player = 0
    turn = 0
    max_turns = 200

    print(f"\n{'='*60}")
    print(f"JUTPATTI GAME START")
    print(f"{'='*60}")
    print(f"Joker card revealed: {joker_card} (Value: {get_card_value(joker_card)})")
    print(f"Joker value for this game: {joker_value}")
    print(f"{'='*60}\n")

    # Show initial hands
    for i, hand in enumerate(hands):
        pairs, unpaired = find_best_pairs(hand, joker_value)
        print(f"Player {i + 1}'s starting hand: {' '.join(hand)}")
        print(f"  Pairs: {len(pairs)} | Unpaired: {len(unpaired)}")
    print()

    while turn < max_turns:
        turn += 1
        player_hand = hands[current_player]

        print(f"\n--- Turn {turn}: Player {current_player + 1}'s turn ---")
        print(f"Hand ({len(player_hand)} cards): {' '.join(player_hand)}")

        if not deck and len(discard_pile) > 1:
            top_card = discard_pile.pop()
            deck.extend(discard_pile)
            random.shuffle(deck)
            discard_pile = [top_card]
            print(f"Deck empty! Shuffling discard pile back into deck...")

        # FIRST: Decide action and pick a card from deck or discard pile
        action = ai_decide_action(player_hand, discard_pile, deck, joker_value)

        if action == "discard" and discard_pile:
            picked_card = discard_pile.pop()
            player_hand.append(picked_card)
            print(f"Player {current_player + 1} picks from discard pile: {picked_card}")
        elif deck:
            picked_card = deck.pop()
            player_hand.append(picked_card)
            print(f"Player {current_player + 1} draws from deck: {picked_card}")
        else:
            print(f"No cards available to draw!")
            break

        # Now player has 8 cards - check for win!
        print(f"After picking: {len(player_hand)} cards")
        pairs, unpaired = find_best_pairs(player_hand, joker_value)
        print(f"Current status - Pairs: {len(pairs)} | Unpaired: {len(unpaired)}")

        # Check if player has won (with 8 cards, should have 4 pairs, 0 unpaired)
        if is_winner(player_hand, joker_value):
            print(f"\n{'='*60}")
            print(f"PLAYER {current_player + 1} WINS!")
            print(f"{'='*60}")
            print(f"Winning hand ({len(player_hand)} cards): {' '.join(player_hand)}")
            pairs, _ = find_best_pairs(player_hand, joker_value)
            print(f"All {len(pairs)} pairs formed:")
            for i, (c1, c2) in enumerate(pairs, 1):
                print(
                    f"  Pair {i}: {c1} ({get_card_value(c1)}) - {c2} ({get_card_value(c2)})"
                )
            return current_player + 1

        # SECOND: Player must discard a card (back to 7 cards)
        discard_card = ai_choose_discard(player_hand, joker_value, discard_pile)
        if discard_card in player_hand:
            player_hand.remove(discard_card)
            discard_pile.append(discard_card)
            print(f"Player {current_player + 1} discards: {discard_card}")
            print(f"After discarding: {len(player_hand)} cards")

        # Next player
        current_player = (current_player + 1) % num_players

    print(f"\n{'='*60}")
    print("Game ended without a winner (max turns reached)")
    print(f"{'='*60}")

    # Show final standings
    for i, hand in enumerate(hands):
        pairs, unpaired = find_best_pairs(hand, joker_value)
        print(f"Player {i + 1}: {len(pairs)} pairs, {len(unpaired)} unpaired cards")

    return None


def play_game_silent(hands, deck, joker_card, joker_value, num_players=2):
    """Play the game without printing (for simulation)"""
    discard_pile = []
    current_player = 0
    turn = 0
    max_turns = 200  # TODO: Prevent infinite loops

    while turn < max_turns:
        turn += 1
        player_hand = hands[current_player]

        if not deck and len(discard_pile) > 1:
            top_card = discard_pile.pop()
            deck.extend(discard_pile)
            random.shuffle(deck)
            discard_pile = [top_card]

        action = ai_decide_action(player_hand, discard_pile, deck, joker_value)

        if action == "discard" and discard_pile:
            picked_card = discard_pile.pop()
            player_hand.append(picked_card)
        elif deck:
            picked_card = deck.pop()
            player_hand.append(picked_card)
        else:
            break

        if is_winner(player_hand, joker_value):
            return current_player + 1

        discard_card = ai_choose_discard(player_hand, joker_value, discard_pile)
        if discard_card in player_hand:
            player_hand.remove(discard_card)
            discard_pile.append(discard_card)

        current_player = (current_player + 1) % num_players

    return None


def simulate_games(num_simulations=5000, num_players=2, hand_size=7):
    """Simulate multiple games to calculate win probabilities"""
    print("\n" + "=" * 60)
    print(f"RUNNING {num_simulations} GAME SIMULATIONS")
    print("=" * 60)
    print(f"Players: {num_players}")
    print(f"Cards per hand: {hand_size}")
    print()

    player_wins = [0 for _ in range(num_players)]
    draws = 0

    for game_num in range(1, num_simulations + 1):
        if game_num % 500 == 0:
            print(f"Completed {game_num}/{num_simulations} games...")

        deck = create_deck()

        hands, deck = deal_hands(deck, num_players, hand_size)

        if deck:
            joker_card = deck[0]
            joker_value = determine_joker(joker_card)

            winner = play_game_silent(hands, deck, joker_card, joker_value, num_players)

            if winner:
                player_wins[winner - 1] += 1
            else:
                draws += 1

    print("\n" + "=" * 60)
    print("SIMULATION RESULTS")
    print("=" * 60)

    total_games = sum(player_wins) + draws

    for i in range(num_players):
        win_percentage = (player_wins[i] / total_games) * 100
        print(
            f"Player {i + 1} (goes {'first' if i == 0 else 'second'}): {player_wins[i]} wins ({win_percentage:.2f}%)"
        )

    draw_percentage = (draws / total_games) * 100
    print(f"Draws: {draws} ({draw_percentage:.2f}%)")
    print()

    if player_wins[0] > player_wins[1]:
        advantage = ((player_wins[0] - player_wins[1]) / total_games) * 100
        print(f"Player 1 (first player) has a {advantage:.2f}% advantage!")
    elif player_wins[1] > player_wins[0]:
        advantage = ((player_wins[1] - player_wins[0]) / total_games) * 100
        print(f"Player 2 (second player) has a {advantage:.2f}% advantage!")
    else:
        print("Both players have equal chances!")

    print("=" * 60)
    print()


def main():
    print("\n" + "=" * 60)
    print("JUTPATTI CARD GAME SIMULATOR")
    print("=" * 60)

    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--simulate":
        num_sims = 5000
        if len(sys.argv) > 2:
            num_sims = int(sys.argv[2])
        simulate_games(num_simulations=num_sims)
        return

    num_players = 2
    hand_size = 7  # IMPORTANT: Must be odd: 5, 7, 9, 11

    print(f"Players: {num_players}")
    print(f"Cards per hand: {hand_size}")

    # Create and shuffle deck
    deck = create_deck()

    hands, deck = deal_hands(deck, num_players, hand_size)

    if deck:
        joker_card = deck[0]
        joker_value = determine_joker(joker_card)

        winner = play_game(hands, deck, joker_card, joker_value, num_players)

        if winner:
            print(f"\nFinal Result: Player {winner} is the champion!\n")
        else:
            print("\nGame ended in a draw\n")
    else:
        print("Error: Not enough cards in deck!")


if __name__ == "__main__":
    main()
