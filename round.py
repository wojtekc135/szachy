class Round:
    def __init__(self, round_number):
        self.round_number = round_number

    def count_known_for_player(self, hand):
        sum = 0
        for card in hand:
            if card.known_for_player:
                sum += 1
        return sum
