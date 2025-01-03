class Player:
    def __init__(self, isHuman, player_number):
        self.isHuman = isHuman
        self.player_number = player_number

    def swap_card(self, state, card1, card2):
        state[card1.location][card1.location_number], state[card2.location][card2.location_number] = \
            state[card2.location][card2.location_number], state[card1.location][card1.location_number]
        card1.location, card2.location = card2.location, card1.location
        card1.location_number, card2.location_number = card2.location_number, card1.location_number
        return state, card1, card2
