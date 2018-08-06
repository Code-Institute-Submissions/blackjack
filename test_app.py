import unittest
import app
import copy

class TestApp(unittest.TestCase):
    """ 
    test suite for the game of blackjack
    """
    

    def test_create_deck(self):
        """
        can it show a card
        """
        deck = app.create_deck()            # default
        deckX2 = app.create_deck(2)         # 2 decks
        deckX3 = app.create_deck(3)         # 3 decks
        deckX4 = app.create_deck(4)         # 4 decks
        
        self.assertEqual(len(deck),    52, "incorrect num of cards for 1 deck" )
        self.assertEqual(len(deckX2), 104, "incorrect num of cards for 2 decks")
        self.assertEqual(len(deckX3), 156, "incorrect num of cards for 3 decks")
        self.assertEqual(len(deckX4), 208, "incorrect num of cards for 4 decks")
        
        
    def test_shuffle(self):
        """
        check to see if the order changes
        """
        shuffled_deck = []
        deck = app.create_deck()
        
        print("deck:\n", deck)
        # apply deep.copy
        shuffled_deck = app.shuffle(deck)
        print("shuffled_deck:\n", shuffled_deck)
        # self.assertListEqual(shuffled_deck, deck, "deck wasnt changed/shuffled!")
        # why doesnt this work?????????????????????????????
        self.assertListEqual(shuffled_deck, deck, "deck wasnt changed/shuffled!")
    
    
    def test_draw_card(self):
        """ check to see if it actually draws a card
            note:   burn_card() should be part of this function
        """
        
        deck = app.create_deck()
        card = app.draw_card(deck)

        
        self.assertEqual(len(card), 2)
    
        
        
    def test_burn_card(self):
        """ check to see if it actually draws a card
            note:   burn_card() should be part of this function
        """

        deck = app.create_deck()
        deck_orginal = copy.deepcopy(deck) # shallow copy not working reliably 
        card = app.draw_card(deck)
        deck = app.burn_card(deck, card)
        
        self.assertEqual(len(deck), len(deck_orginal) - 1)
    
    
    
    if __name__ == "__main__":
        unittest.main()