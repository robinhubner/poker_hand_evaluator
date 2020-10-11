# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 18:06:49 2020

@author: robin
"""

import random as rnd
from itertools import combinations
from collections import defaultdict
import pandas as pd

class Card(object):
    def __init__(self, value, color):
        self.value = value
        self.color = color
        
    def __repr__(self):
        card_names = {10 : 'T', 11 : 'J', 12 : 'Q', 13 : 'K' , 14 : 'A'}
        name = str(self.value) if self.value < 10 else card_names[self.value]
        return name + self.color

        
class Deck(object):
    def __init__(self):
        self.cards = self._shuffle()
        
    def _shuffle(self):
        cards = []
        for color in '♠♥♦♣':
            for value in range(2,15):
                cards.append(Card(value,color))
        rnd.shuffle(cards)
        return cards
    
    def give(self, qty):
        return [self.cards.pop() for _ in range(qty)]
        

def evaluating_hand(pocket,board): 
    card_7 = pocket + board
    card_7 = sorted(card_7, key=lambda c:c.value, reverse = True)
    best_rank = -1 
    for card_5 in combinations(card_7,5):
        rank, cards = evaluate_5(card_5)
        if rank > best_rank:
            best_rank = rank
            best_cards = cards
    return best_rank, best_cards

def evaluate_5(card_5):
    # List that continues the cards ordered by value
    value2card = defaultdict(list)    
    
    # List that continues the cards grouped by value count
    count2card = defaultdict(list)

    for c in card_5 :
        value2card[c.value].append(c)
    for v in value2card.values() :
        count2card[len(v)] +=v

    # Set that contains each unique value of card_5
    unique_values = {c.value for c in card_5}
    
    # Set that countains the elements of the same color
    color = {c.color for c in card_5}
    
    # Variable if straight is true
    straight = (len(unique_values) == 5 and (max(unique_values)-min(unique_values)) == 4) or (unique_values == {5,4,3,2,14})

    # Variable if flush is true
    flush = len(color) == 1

    # Royal Flush
    if unique_values == {14,13,12,11,10} and flush :
        return 9, card_5 

    # Straigh Flush
    if straight and flush :
        if unique_values == {5,4,3,2,14} :
            card_5 = card_5[1:] + card_5[:1]
        return 8, card_5        
        
    # Four of a Kind
    if 4 in count2card :
        return 7, count2card[4] + count2card[1]

    # Full House
    if 3 in count2card and 2 in count2card :
        return 6, count2card[3] + count2card[2]
  
    # Flush
    if flush :
        return 5, card_5
  
    # Straight
    if straight :
        if unique_values == {5,4,3,2,14} :
            card_5 = card_5[1:] + card_5[:1]
        return 4, card_5
        
    # Three of a Kind
    if 3 in count2card :
        return 3, count2card[3] + count2card[1]
    
    # Two Pair
    if 2 in count2card and len(count2card[2]) == 4 :
        return 2, count2card[2] + count2card[1]    
    
    # Check Pair
    if 2 in count2card :
        return 1, count2card[2] + count2card[1]
        
   # High Card 
    return 0, card_5

def compare_hands(hands, board) :
    best_rank = -1
    best_pocket = []
    for pocket in hands :
        if evaluating_hand(pocket, board)[0] > best_rank :
            best_rank = evaluating_hand(pocket, board)[0]
            best_pocket = best_pocket[:]
            best_pocket.append(pocket)
        elif evaluating_hand(pocket, board)[0] == best_rank :
            best_pocket.append(pocket)
    print('Best Rank :' + str(best_rank))
    print('Best Pocket :' + str(best_pocket))    


 
deck = Deck()
pocket_a = deck.give(2)
pocket_b = deck.give(2)
board =deck.give(5)
print('Player_A ' + str(pocket_a))
print('Player_B ' + str(pocket_b))
print('Board ' + str(board))

compare_hands([pocket_a,pocket_b],board)








# =============================================================================
# def calculate_odds (n) :            
#     
#     '''Function that calculated the odds of each poker hand depending on the 
#     input sample size n'''
#     
#     results = []
#     for i in range(0,n) :
#         deck = Deck()
#         pocket = deck.give(2)
#         board =deck.give(5)
#         results.append(evaluating_hand(pocket,board)[0])
# 
#     result_df = pd.DataFrame()
#     result_df['counts'] = pd.Series(results).value_counts()
#     result_df['probability'] = (["{0:.2f}%".format(val * 100 / n) for val in result_df['counts']])
#     print(result_df)
# =============================================================================
