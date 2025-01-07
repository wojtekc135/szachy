class Player:
    def __init__(self, isHuman, player_number):
        self.isHuman = isHuman
        self.player_number = player_number
        self.crows = 0
        self.ninecrows = 0
    # nowy wariant wyswietla runde na podstawie player, ale nie aktualizuje player_nuber nie tak jak bylo w stabilnej wersji gry,
    # nie wiem czy ta klasa ma sens, bo  robi to co round, ale human_use_ability ma sens, nie znam sie na programowaniu obiektowym xd) - Wojtek

    #szczerze tez się nie znam, ale chciałam mieć zeby mi coś wrony gracza trzymało do wyniku
    # teoretycznie use ability też można wrzucić do card jakoś ale tam jest już tłoczno to se tutaj miejsce wykorzystałam - Madzia

    def human_use_ability(self, state, card, game_round, game_renderer):
        temp_hand = "temp_hand"
        stack_type = "face_down_pile"
        stack_index_to_choose = -1  # 0 spód stacku, -1 góra

        game_renderer.draw_state(game_round, state, " Wybierz pierwsza karte ze stosu zakrytego")
        card1 = game_round.choose_card_from_stack(state, stack_type, stack_index_to_choose)
        card1.location = temp_hand
        card1.location_number = 5
        card1.show_front = True
        state[stack_type].pop()

        game_renderer.draw_state(game_round, state, " Wybierz druga")
        card2 = game_round.choose_card_from_stack(state, stack_type, stack_index_to_choose)
        card2.location = temp_hand
        card2.location_number = 5
        card2.show_front = True
        state[stack_type].pop()

        game_renderer.draw_state(game_round, state, " Wybierz którą z nich chcesz zachować")
        picked_card = InputHandler.choose_from(temp_hand)
        #trzeba dorobić fukcnję ze daje na GÓRE stosu odkrytego



        #############
        if card.ability == "take":
            game_renderer.draw_state(game_round, state, "Ciągnij pierwsza karty ze stosu zakrytego")
            card1 = InputHandler.choose_from(state["face_down_pile"])
            card1.selected_info = "wybrano"

            #przypisanie do reki tymczasowe
            card1.location = cur_hand
            card1.location_number = 5


            game_renderer.draw_state(cur_player, state, "Ciągnij druga karty ze stosu zakrytego")
            card2 = InputHandler.choose_from(state["face_down_pile"])
            card2.selected_info = "wybrano"
            card2.location = cur_hand
            card2.location_number = 6
            game_renderer.draw_state(cur_player, state, "Ciągnij druga karty ze stosu zakrytego")

            pygame.time.wait(500)


            #chooseCard
            #B1 or B2 or B3

        if card.ability == "look":
            game_renderer.draw_state(cur_player, state, "Podejrzyj karte z jakiejkolwiek reki")
            picked_card = InputHandler.choose_from(state["hand1"] + state["hand2"] + state["hand3"] + state["hand4"])
            picked_card.selected_info = "wybrano"

            if not picked_card.known_for_player:
                picked_card.show_front = True
                picked_card.known_for_player = True
                picked_card.selected_info = "Niewidoczna"
                game_renderer.draw_state(cur_player, state, "Patrz")

                pygame.time.wait(1000)

                picked_card.show_front = False
                picked_card.known_for_player = False
                game_renderer.draw_state(cur_player, state, "Koniec patrzenia")



        if card.ability == "swap":
            # wybranie karty z dowolnej reki
            game_renderer.draw_state(cur_player, state, "Wybierz pierwsza karte do wymiany")
            card1 = InputHandler.choose_from(state["hand1"] + state["hand2"] + state["hand3"] + state["hand4"])
            card1.selected_info = "wybrano"

            game_renderer.draw_state(cur_player, state, " Wybierz druga karte do wymiany")
            card2 = InputHandler.choose_from(state["hand1"] + state["hand2"] + state["hand3"] + state["hand4"])
            card2.selected_info = "wybrano"

            state, card1, card2 = cur_player.swap_card(state, card1,
                                                       card2)

            card2.selected_info = False
            if cur_player.isHuman == "human":
                card1.selected_info = "niewidoczna"
            else:
                card1.selected_info = False
            game_renderer.draw_state(cur_player, state, "Zamienianie miejscami")
            pygame.time.wait(500)