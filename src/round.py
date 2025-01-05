class Round:
    def __init__(self, round_number):
        self.round_number = round_number

    def count_known_for_player(self, hand):
        sum = 0
        for card in hand:
            if card.known_for_player:
                sum += 1
        return sum

    def print_state(self, state):
        """
        print("localization numbers: ", end="")
        for localization in state:
            print(localization, end=" ")
            for card in state[localization]:
                print(" "+ str(card.location_number),end="")
            print(" ")
        print("")
        """
        print("card id: ", end="")
        for localization in state:
            print(localization, end=" ")
            for card in state[localization]:
                print(" " + str(card.id), end="")
            print(" ", end="")
        print("")
