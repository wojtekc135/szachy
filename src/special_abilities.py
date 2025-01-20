from input_handler  import InputHandler
import pygame



def special_ability_look(game_round,game_renderer, state):
    # działa
    game_renderer.draw_state(game_round, state, "Podejrzyj karte z jakiejkolwiek reki")
    picked_card = InputHandler.choose_from(state["hand1"] + state["hand2"] + state["hand3"] + state["hand4"])
    picked_card.highlighted = True
    picked_card.show_front = True
    game_renderer.draw_state(game_round, state, "Patrz")
    pygame.time.wait(2000)
    picked_card.show_front = False
    picked_card.highlighted = False
    game_renderer.draw_state(game_round, state, "Koniec patrzenia")


def special_ability_swap(game_round,game_renderer, state):
    # działa
    game_renderer.draw_state(game_round, state, "Wybierz pierwsza karte (z graczy) do wymiany")
    card1 = InputHandler.choose_from(state["hand1"] + state["hand2"] + state["hand3"] + state["hand4"])
    card1.highlighted = True
    game_renderer.draw_state(game_round, state, " Wybierz druga karte (z graczy) do wymiany")
    card2 = InputHandler.choose_from(state["hand1"] + state["hand2"] + state["hand3"] + state["hand4"])
    card2.highlighted = True
    state, card1, card2 = game_round.swap_card(state, card1, card2)
    game_renderer.draw_state(game_round, state, "Zamienianie miejscami")
    pygame.time.wait(500)
    card1.highlighted = False
    card2.highlighted = False
    game_renderer.draw_state(game_round, state, "Zamieniono")
    pygame.time.wait(900)


# Special ability nie działał i tylko bardziej popsułem. Usunelem to z example state, niech ktos zrobi example state poprawny
# Zmieniłem nowy game flow, który jest zgodny z instrukcją, take two musi sie troche zmienić, ale tylko troche
# karta która zostaje na końcu ma pójść do hand_temp z localization_number = 0 i potem zrobiłem że po wykonaniu take two
# karta z temp_hand 0 jest dawana juz albo do odkrytego albo do reki, tylko musi skonczyc w hand_temp localisation_number 0
def special_ability_take_two(game_round, game_renderer, state):
    temp_hand = "hand_temp"
    game_renderer.draw_state(game_round, state, "Wybierz z stosu zakrytego")
    stack_type = InputHandler.choose_from(state["face_down_pile"])  # I beg you
    stack_type = "face_down_pile"  # don't change those two lines or it all BREAKS #Ale dziwne, ale jak działa to nie ruszam :)

    stack_index_to_choose = -1
    card1 = game_round.choose_card_from_stack(state, stack_type, stack_index_to_choose)
    state[temp_hand].append(card1)
    card1.location = temp_hand
    card1.location_number = 5
    card1.show_front = True
    del state[stack_type][
        -1]  # wiem że miałam nie usuwać, ale potem by się duplikowały karty - MM, wiesz co robisz spoko
    game_renderer.draw_state(game_round, state, "Jeszcze jedną :D")
    stack_type = InputHandler.choose_from(state["face_down_pile"])  # I beg you
    stack_type = "face_down_pile"  # don't change those two lines or it all BREAKS # zmieniłem D;
    card2 = game_round.choose_card_from_stack(state, stack_type, stack_index_to_choose)
    state[temp_hand].append(card2)
    card2.location = temp_hand
    card2.location_number = 6
    card2.show_front = True
    del state[stack_type][-1]
    game_renderer.draw_state(game_round, state, "Wybierz którą z nich chcesz użyć")
    picked_card = InputHandler.choose_from(state[temp_hand])
    print("1")

    ###########
    if picked_card.location_number == card1.location_number:  # ta druga wtedy dajemy na stos odkryty
        state["face_up_pile"].append(card2)
        card2.location = "face_up_pile"
        card2.location_number = state["face_up_pile"][
                                    -1].location_number + 1  # o jeden wiekszy niż ostatniego elementu # fajnie :) mozesz zobaczyc jak  zrobilem  to samo inną komendą haha
        state["hand_temp"].append(card1)
        card1.location = "hand_temp"
        card1.location_number = 0
    else:
        # to samo? chyba jakis blad proboje naprawic
        state["face_up_pile"].append(card1)
        card1.location = "face_up_pile"
        card1.location_number = state["face_up_pile"][-1].location_number + 1  # o jeden wiekszy niż ostatniego elementu
        state["hand_temp"].append(card2)
        card2.location = "hand_temp"
        card2.location_number = 0
    state[temp_hand].pop(0)
    state[temp_hand].pop(0)




