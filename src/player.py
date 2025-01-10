
import pygame
from input_handler import  InputHandler



class Player:
    def __init__(self, isHuman, player_number):
        self.isHuman = isHuman
        self.player_number = player_number
        self.crows = 0

    def human_use_ability(self, state, card, game_round, game_renderer):
        ######## tymczasowe, bo karty nie mają na razie umiejetnosci i nie wiemy variantu jak obsługiwac
        card.ability = "swap"
        ########

        if card.ability == "take":

            temp_hand = "hand_temp"
            game_renderer.draw_state(game_round, state, "Wybierz ZE STOSU ZKATYREGO")

            stack_type = InputHandler.choose_from(state["face_down_pile"])  # I beg you
            stack_type = "face_down_pile" #don't change those two lines or it all BREAKS

            stack_index_to_choose = -1  # 0 spód karty, -1 góra
            game_round.swap_card(state, game_round.choose_card_from_stack(state, stack_type, -1),
                                 game_round.choose_card_from_stack(state, stack_type, 0))
            card1 = game_round.choose_card_from_stack(state, stack_type, stack_index_to_choose)
            state[temp_hand].append(card1)
            card1.location = temp_hand
            card1.location_number = 5
            card1.show_front = True
            game_round.debug(state)
            del state[stack_type][-1] # wiem że miałam nie usuwać, ale potem by się duplikowały karty - MM
            game_renderer.draw_state(game_round, state, "Jeszcze jedną :D")
            game_round.debug(state)

            stack_type = InputHandler.choose_from(state["face_down_pile"])  # I beg you
            stack_type = "face_down_pile" #don't change those two lines or it all BREAKS

            game_round.swap_card(state, game_round.choose_card_from_stack(state, stack_type, -1),
                                 game_round.choose_card_from_stack(state, stack_type, 0))
            card2 = game_round.choose_card_from_stack(state, stack_type, stack_index_to_choose)
            state[temp_hand].append(card2)
            card2.location = temp_hand
            card2.location_number = 6
            card2.show_front = True
            game_round.debug(state)
            del state[stack_type][-1]
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

            #Teraz gracz decyduje sie na akcje z karta B1,B2,B3
            #todo wysweitlac odpowiednie przyciski jak dowiem sie co robia
            game_renderer.draw_state(self, state, "B1 B2 lub B3")
            chosen_button = self.show_action_buttons_choose_option_and_hide_buttons(state,game_round,game_renderer,"wybierz opcje")
            chosen_option = chosen_button.text
            if chosen_option == "Użyj karty":
                self.use_card(game_round,game_renderer,state,picked_card)
            elif chosen_option == "swap card":
                self.swap_card2()
            elif chosen_option == "swap card chosen_pile_bottom <-> hand":
                self.swap_bottom_chosen_pile_with_hand(game_renderer,game_round,state, picked_card)
            elif chosen_option == "Nie używaj umiejętności":
                self.do_not_use_card(game_renderer,game_round,state)
            elif chosen_option == "Co robi?":  # Co robi karta
                self.what_card_do(game_renderer,game_round,state,picked_card)

        if card.ability == "look": # DONE :D
            game_renderer.draw_state(self, state, "Podejrzyj karte z jakiejkolwiek reki")
            picked_card = InputHandler.choose_from(state["hand1"] + state["hand2"] + state["hand3"] + state["hand4"])
            picked_card.highlighted = True
            if not picked_card.known_for_player:
                picked_card.show_front = True
                picked_card.known_for_player = True
                game_renderer.draw_state(self, state, "Patrz")

                pygame.time.wait(1000)

                picked_card.show_front = False
                picked_card.known_for_player = False
                picked_card.highlighted = False
                game_renderer.draw_state(self, state, "Koniec patrzenia")

        if card.ability == "swap":
            # wybranie karty z dowolnej reki
            game_renderer.draw_state(self, state, "Wybierz pierwsza karte (z graczy) do wymiany")
            card1 = InputHandler.choose_from(state["hand1"] + state["hand2"] + state["hand3"] + state["hand4"])
            card1.highlighted = True

            game_renderer.draw_state(self, state, " Wybierz druga karte (z graczy) do wymiany")
            card2 = InputHandler.choose_from(state["hand1"] + state["hand2"] + state["hand3"] + state["hand4"])
            card2.highlighted = True

            state, card1, card2 = self.swap_card(state, card1,
                                                       card2)

            game_renderer.draw_state(self, state, "Zamienianie miejscami")
            pygame.time.wait(500)
            card1.highlighted = False
            card2.highlighted = False
            game_renderer.draw_state(self, state, "Zamieniono")
            pygame.time.wait(900)