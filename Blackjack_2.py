import pydealer

def main_deck():
    deck = pydealer.Deck()
    deck.shuffle()
    return deck

def get_bet(wallet):  
    while True:
        bet = input(f"How much do you want to bet? $")
        if bet.isdigit():
            amount = int(bet)
            if 0 < amount <= wallet:
                break
            else: 
                print(f"Bet should be between 1 and {wallet}. Please provide a valid bet.")
        else:
            print("Incorrect input. Please specify a whole number.")
    
    return amount

def get_wallet(amount):
    print(f"You have ${amount} in your wallet.")
    return amount

def deal_initial_cards(deck):
    return deck.deal(2)

def display_hand(hand, player_name):
    if player_name == "Dealer":
        print(f"{player_name}'s hand: {hand[0]} and hidden card")
    else:
        print(f"{player_name}'s hand: {', '.join(map(str, hand))}")

def calculate_hand_value(hand):
    value = 0
    num_aces = 0

    for card in hand:
        if card.value.isnumeric():
            value += int(card.value)
        elif card.value in ['Jack', 'Queen', 'King']:
            value += 10
        elif card.value == 'Ace':
            num_aces += 1

    while value <= 11 and num_aces:
        value += 10
        num_aces -= 1

    return value

def main():
    wallet = get_wallet(100)
    while True:
        bet = get_bet(wallet)
        wallet -= bet

        deck = main_deck()
        player_hand = deal_initial_cards(deck)
        dealer_hand = deal_initial_cards(deck)

        display_hand(player_hand, "Player")
        display_hand(dealer_hand, "Dealer")

        while True:
            player_value = calculate_hand_value(player_hand)
            if player_value == 21:
                print("Blackjack! You win!")
                wallet += 2 * bet
                break

            action = input("Do you want to hit or stand? (hit/stand) ").lower()
            if action == "hit":
                player_hand += deck.deal(1)
                display_hand(player_hand, "Player")
                if calculate_hand_value(player_hand) > 21:
                    print("Bust! You lose.")
                    break
            elif action == "stand":
                while calculate_hand_value(dealer_hand) < 17:
                    dealer_hand += deck.deal(1)
                display_hand(dealer_hand, "Dealer")

                dealer_value = calculate_hand_value(dealer_hand)
                print(f"Dealer's hand value: {dealer_value}")

                if dealer_value > 21:
                    print("Dealer busts! You win!")
                    wallet += 2 * bet
                elif dealer_value == player_value:
                    print("It's a tie!")
                    wallet += bet
                elif dealer_value > player_value:
                    print("Dealer wins!")
                else:
                    print("You win!")
                    wallet += 2 * bet

                break

        get_wallet(wallet)

        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            break

if __name__ == "__main__":
    main()
