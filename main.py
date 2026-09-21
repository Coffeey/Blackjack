from hand import Hand
from dealer_hand import DealerHand
from deck import Deck
from data import CARD_VALUES
import savegame

def play_again():
    choice = input("Play again? (y/n): ")
    while True:
        if choice is not "y" and choice is not "n":
            choice = input("Enter valid response (y/n): ")
            continue
        break
            
    return choice == "y"

def check_draw():
    return players_hand.value == dealers_hand.value

def reset_cards():
    players_hand.reset()
    dealers_hand.reset()
    deck.reset()

def validate_bet(bet_str:str):
    if not bet_str.isdigit():
        return False, -1

    as_int = int(bet_str)
    if as_int > stats["bankroll"]:
        return False, -1

    if as_int % 2 != 0:
        return False, -1

    if as_int == 0:
        return False, -1
    
    return True, as_int

def hit_or_stay():
    choice = input("Hit or Stay? (h/s):")
    while True:
        if choice is not "h" and choice is not "s":
            choice = input("Enter valid response (h/s): ")
            continue
        break
                
    return choice

def take_bet():
    bet_str = input("Enter bet (even number): ")

    while True:
        valid, value = validate_bet(bet_str)
        if not valid:
            bet_str = input("Invalid bet, try again: ")
            continue

        return value

def draw_header(stage):
    if stage == "START_HAND":
        print("")
        print("-----------------------------------------")
        print("/////////////////////////////////////////")
        print("-----------------------------------------")
        print(f" Bank: {stats["bankroll"]}")
        print("               NEW HAND")
        print("-----------------------------------------")
        return
    elif stage == "PLAYER_TURN":
        print("")
        print("-----------------------------------------")
        print(f" Bank: {stats["bankroll"]}")
        print("               YOUR TURN")
        print("-----------------------------------------")
        return
    elif stage == "DEALER_TURN":
        print("")
        print("-----------------------------------------")
        print(f" Bank: {stats["bankroll"]}")
        print("             DEALERS TURN")
        print("-----------------------------------------")
        return
    elif stage == "SHOWDOWN":
        print("")
        print("-----------------------------------------")
        print(f" Bank: {stats["bankroll"]}")
        print("               SHOWDOWN")
        print("-----------------------------------------")
        return
    elif stage == "RESTART_CHOICE":
        print("")
        print("-----------------------------------------")
        print(f" Bank: {stats["bankroll"]}")
        print("             PLAY AGAIN?")
        print("-----------------------------------------")

def set_stage(stage):
    global hand_stage
    hand_stage = stage

def compute_winnings(bet, context):
    temp = 0
    if(context == "loss"):
        temp = -bet
    elif(context == "win_default"):
        temp = bet
    elif(context == "win_natural"):
        temp = int(bet*1.5)
    elif(context == "draw"):
        temp = 0
    return temp

def update_stats(won_this_hand, previous_bankroll, current_bankroll):
    if(won_this_hand):
        stats["hands_won_conseq"] += 1
    else:
        stats["hands_won_conseq"] = 0

    if(current_bankroll > previous_bankroll):
        stats["all_time_winnings"] += current_bankroll - previous_bankroll
    elif (previous_bankroll > current_bankroll):
        stats["all_time_loss"] += previous_bankroll - current_bankroll

    if(current_bankroll <= 0):
        stats["bankruptcys"] += 1

    if(won_this_hand):
        stats["hands_won_total"] += 1

    stats["hands_played"] += 1

stats = savegame.load()

deck = Deck()
players_hand = Hand("player")
dealers_hand = DealerHand()

hand_stage = None
set_stage("START_HAND")
running = True

while running:
    if(hand_stage == "START_HAND"):
        reset_cards()

        if(stats["bankroll"] <= 0):
            stats["bankroll"] = 100

        draw_header(hand_stage)
        
        current_bet = take_bet()

        players_hand.hit(deck)
        players_hand.hit(deck)
        dealers_hand.hit(deck)
        dealers_hand.hit(deck)

        print("")
        print(f"Players hand: {players_hand.cards[0]}, {players_hand.cards[1]} ({players_hand.value})")

        if(players_hand.natural()):
            print("BLACKJACK!")
            set_stage("DEALER_TURN")
            continue

        print(f"Dealers hand: {dealers_hand.cards[0]} ({CARD_VALUES[dealers_hand.cards[0]]}) - Second card hidden")
        set_stage("PLAYER_TURN")
        draw_header(hand_stage)

    elif(hand_stage == "PLAYER_TURN"):
        action = hit_or_stay()

        if action == "h":
            players_hand.hit(deck)
            print(f"Your hit: {players_hand.cards[-1]}, ({players_hand.value})")

            if players_hand.is_bust():
                print(f"BUUUUUUUST")
                prev_bankroll = stats["bankroll"]
                stats["bankroll"] += compute_winnings(current_bet, "loss")
                update_stats(False, prev_bankroll, stats["bankroll"])
                set_stage("RESTART_CHOICE")
            elif players_hand.value == 21:
                set_stage("DEALER_TURN")
        
        elif(action == "s"):
            set_stage("DEALER_TURN")

    elif(hand_stage == "DEALER_TURN"):
        draw_header(hand_stage)
        if not dealers_hand.revealed:
            print(f"Dealer reveals: {dealers_hand.cards[0]}, >{dealers_hand.cards[1]}< ({dealers_hand.value})")
            dealers_hand.revealed = True

        while dealers_hand.value <= 16:
            dealers_hand.hit(deck)
            print(f"Dealer hit a {dealers_hand.cards[-1]} ({dealers_hand.value})")

        set_stage("SHOWDOWN")
        continue

    elif hand_stage == "SHOWDOWN":
        draw_header(hand_stage)
        showdown_context = None
        print(f"You: {players_hand.value}, Dealer: {dealers_hand.value}")
        if dealers_hand.natural() and players_hand.natural():
            print(f"COMPETING NATURALS! DRAW!")
            showdown_context = "draw"
        elif players_hand.natural() and not dealers_hand.natural():
            print(f"YOUR NATURAL WINS!")
            showdown_context = "win_natural"
        elif dealers_hand.natural() and not players_hand.natural():
            print(f"DEALER BLACKJACK! You lose...")
            showdown_context = "loss"
        elif dealers_hand.is_bust():
            print(f"Dealer busts, YOU WIN!!!")
            showdown_context = "win_default"
        elif check_draw():
            print(f"DRAW!")
            showdown_context = "draw"
        elif players_hand.value > dealers_hand.value:
            print(f"YOU WIN!")
            showdown_context = "win_default"
        else:
            print(f"You lose...")
            showdown_context = "loss"

        bankroll_before = stats["bankroll"]
        stats["bankroll"] += compute_winnings(current_bet, showdown_context)

        set_stage("RESTART_CHOICE")
        update_stats(bankroll_before<stats["bankroll"], bankroll_before, stats["bankroll"])

    elif(hand_stage == "RESTART_CHOICE"):

        savegame.save(stats)

        draw_header(hand_stage)
        if(play_again()):
            set_stage("START_HAND")
        else:
            running = False

        
