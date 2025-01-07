
import pygame
from input_handler import  InputHandler



class Player:
    def __init__(self, isHuman, player_number):
        self.isHuman = isHuman
        self.player_number = player_number
        self.crows = 0
    # nowy wariant wyswietla runde na podstawie player, ale nie aktualizuje player_nuber nie tak jak bylo w stabilnej wersji gry,
    # nie wiem czy ta klasa ma sens, bo  robi to co round, ale human_use_ability ma sens, nie znam sie na programowaniu obiektowym xd) - Wojtek

    #szczerze tez się nie znam, ale chciałam mieć żeby mi coś wrony poszczególnych graczy trzymało do wyświetlania wyniku
    # teoretycznie use ability też można wrzucić do card jakoś ale tam jest już tłoczno, to se tutaj miejsce wykorzystałam - Madzia

    def human_use_ability(self, state, card, game_round, game_renderer):
        ######## temporary befor card get abilities
        card.ability = "take"
        ########

        if card.ability == "take":

            temp_hand = "temp_hand"
            game_renderer.draw_state(game_round, state, "Wybierz ZE STOSU ZKATYREGO")
            stack_type = game_round.choose_stack_type(state) #poprawić zeby zakryty tylk mozna kliknac
            stack_type = "face_down_pile"
            stack_index_to_choose = -1  # 0 spód karty, -1 góra
            game_round.swap_card(state, game_round.choose_card_from_stack(state, stack_type, 0),
                                 game_round.choose_card_from_stack(state, stack_type, -1))
            card1 = game_round.choose_card_from_stack(state, stack_type, stack_index_to_choose)
            state[temp_hand].append(card1)
            card1.location = temp_hand
            card1.location_number = 5
            card1.show_front = True
            game_round.debug(state)
            del state[stack_type][-1]
            print("CHEKER", state[temp_hand][-1].location)
            game_round.debug(state)

            game_renderer.draw_state(game_round, state, " Wybierz druga")
            stack_type = game_round.choose_stack_type(state)
            stack_type = "face_down_pile"
            game_round.swap_card(state, game_round.choose_card_from_stack(state, stack_type, 0),
                                 game_round.choose_card_from_stack(state, stack_type, -1))
            card2 = game_round.choose_card_from_stack(state, stack_type, stack_index_to_choose)
            state[temp_hand].append(card2)
            card2.location = temp_hand
            card2.location_number = 6
            card2.show_front = True
            game_round.debug(state)
            del state[stack_type][-1]
            print("CHEKER", state[temp_hand][-1].location)
            game_round.debug(state)

            game_renderer.draw_state(game_round, state, " Wybierz którą z nich chcesz użyć")
            picked_card = InputHandler.choose_from(state[temp_hand])
            if picked_card.location_number == card1.location_number: #ta druga wtedy dajemy na stos odkryty
                state["face_up_pile"].append(card2)
                card2.location = "face_up_pile"
                card2.location_number = state["face_up_pile"][-1].location_number + 1 # o jeden wiekszy niż ostatniego elementu
                del state[temp_hand][-1]
            else:
                print("usuń lewa:", card2.id)
                state["face_up_pile"].append(card2)
                card2.location = "face_up_pile"
                card2.location_number = state["face_up_pile"][-1].location_number + 1  # o jeden wiekszy niż ostatniego elementu
                del state[temp_hand][0]
            game_round.debug(state)
            game_round.human_take_card_from_any_pile_POP(state, game_round, game_renderer)

        if card.ability == "look":
            game_renderer.draw_state(self, state, "Podejrzyj karte z jakiejkolwiek reki")
            picked_card = InputHandler.choose_from(state["hand1"] + state["hand2"] + state["hand3"] + state["hand4"])
            picked_card.selected_info = "wybrano"

            if not picked_card.known_for_player:
                picked_card.show_front = True
                picked_card.known_for_player = True
                picked_card.selected_info = "Niewidoczna"
                game_renderer.draw_state(self, state, "Patrz")

                pygame.time.wait(1000)

                picked_card.show_front = False
                picked_card.known_for_player = False
                game_renderer.draw_state(self, state, "Koniec patrzenia")

        if card.ability == "swap":
            # wybranie karty z dowolnej reki
            game_renderer.draw_state(self, state, "Wybierz pierwsza karte do wymiany")
            card1 = InputHandler.choose_from(state["hand1"] + state["hand2"] + state["hand3"] + state["hand4"])
            card1.selected_info = "wybrano"

            game_renderer.draw_state(self, state, " Wybierz druga karte do wymiany")
            card2 = InputHandler.choose_from(state["hand1"] + state["hand2"] + state["hand3"] + state["hand4"])
            card2.selected_info = "wybrano"

            state, card1, card2 = self.swap_card(state, card1,
                                                       card2)
            card2.selected_info = False
            if self.isHuman == "human":
                card1.selected_info = "niewidoczna"
            else:
                card1.selected_info = False
            game_renderer.draw_state(self, state, "Zamienianie miejscami")
            pygame.time.wait(500)