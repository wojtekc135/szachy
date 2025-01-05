from input_handler import InputHandler

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

    def choose_stack_type(self,state):
        card = InputHandler.choose_from(state["face_up_pile"] + state["face_down_pile"])
        stack_type = card.location
        return stack_type

    def choose_card_from_stack(self,state, stack_type, index):
        card = state[stack_type][index]
        return card

    def choose_card_from_hand(self,state, hand_name):
        card = InputHandler.choose_from(state[hand_name])
        return card
