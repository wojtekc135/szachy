import random

class Bot():
    def __init__(self):
        self.name=name
        self.dream=[None]*4
    def start_game(selfself, initial_card):
        self.dream=initial_cards
        self.known_cards=random.sample(range(4), 2)

    def take_turn(selfself, top_discard, draw_pile_top, special_action=False):
        known_dream = [self.dream[i] if i in self.known_cards else None for i in range(4)]
        if top_discard and any(card is not None and card>top_discard for card in known_dream):
            to_replace=self._choose_card_to_replace(top_discard)
            return "replace", to_replace, draw_pile_top

        if special_action and random.random()<0.5:
            return "special"

        if sum(card or 10 for card in self.dream) <= 15 and random.random()<0.3:
            return "pobudka"

        return "pass"
