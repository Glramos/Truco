"""Truco Hands Probability Programm."""
import Database as db
import itertools
import os


try:
    path = r"C:\Users\Gabriel Ramos\Documents\Python Scripts\Truco"
    os.remove("games_probabilities.db")
except OSError:
    pass

games_probabilities = db.DatabaseGames("games_probabilities.db")

especial_cards = [(6, 4), (7, 0), (3, 1), (7, 2), (8, 3)]
ranks = {0: "queen", 1: "jack", 2: "king", 3: "ace", 4: "two", 5: "three",
         6: "joker", 7: "seven", 8: "four"}
suits = {0: "diamonds", 1: "spades", 2: "hearts", 3: "clubs", 4: "none"}

cards = list(itertools.product(range(0, 6), range(0, 4)))
cards.extend(especial_cards)
cards.remove((3, 1))
cards.reverse()

deck = []

for card in cards:
    if card[0] != 6:
        name = ranks[card[0]] + " of " + suits[card[1]]
    else:
        name = "joker"

    deck.append(name)

possible_hands = list(itertools.permutations(deck, 3))

cards_frequency = {5: 4, 4: 4, 3: 3, 2: 4, 1: 4, 0: 4}
for myhand in possible_hands:
    hands = db.DatabaseHands("hands.db")
    cards_probabilities = db.DatabaseProbability("cards_probabilities.db")

    probability = []
    probabilityW = None
    probabilityD = None
    probabilityL = None
    flag = []

    deck_less = []

    for card in cards:
        if card[0] != 6:
            name = ranks[card[0]] + " of " + suits[card[1]]
        else:
            name = "joker"

        deck_less.append(name)

        if card[0] not in flag and card not in especial_cards:
            flag.append(card[0])
            probabilityW = ((len(cards)-1) - cards.index(card)
                            - (cards_frequency[card[0]] - 1))/(len(cards)-1)
            probabilityD = (cards_frequency[card[0]] - 1)/(len(cards)-1)
            probabilityL = cards.index(card)/(len(cards)-1)
            probability.append((name, probabilityW, probabilityD,
                                probabilityL))
        elif card in especial_cards:
            flag.append(card[0])
            probabilityW = ((len(cards)-1) - cards.index(card))/(len(cards)-1)
            probabilityD = 0.0
            probabilityL = cards.index(card)/(len(cards)-1)
            probability.append((name, probabilityW, probabilityD,
                                probabilityL))
        else:
            probability.append((name, probabilityW, probabilityD,
                                probabilityL))

    for card in myhand:
        deck_less.remove(card)

    permutations = list(itertools.permutations(deck_less, 3))

    hands.insert(permutations)

    cards_probabilities.insert(probability)

    games = []

    for entry in range(1, hands.count()+1):
        hand = hands.search(entry)

        game = []

        for card1, card2 in zip(myhand, hand):
            my_probabilities = cards_probabilities.search(card1)
            other_probabilities = cards_probabilities.search(card2)

            if my_probabilities[0] > other_probabilities[0]:
                game.append("win")
            elif my_probabilities[0] == other_probabilities[0]:
                game.append("draw")
            else:
                game.append("lose")

        games.append(game)

    results = []

    for game in games:
        if game.count("win") >= 2:
            results.append("win")
        elif game[0] == "win" and game.count("draw") != 0:
            results.append("win")
        elif game[0] == "draw" and game[1] != "lose" and game.count("win") != 0:
            results.append("win")
        elif game.count("draw") == 3:
            results.append("draw")
        else:
            results.append("lose")

    win = results.count("win")/len(games)
    draw = results.count("draw")/len(games)
    lose = results.count("lose")/len(games)

    statistics = [win, draw, lose]

    games_probabilities.insert(myhand[0], myhand[1], myhand[2],
                               statistics[0], statistics[1], statistics[2])

    hands.__del__()
    cards_probabilities.__del__()

    path = r"C:\Users\Gabriel Ramos\Documents\Python Scripts\Truco"
    dir = os.listdir(path)
    for file in dir:
        if file == "hands.db" or file == "cards_probabilities.db":
            os.remove(file)
    print(games_probabilities.count())

games_probabilities.__del__()
