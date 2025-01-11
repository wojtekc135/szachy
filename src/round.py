import pygame
from pygame.font import get_fonts
from input_handler import InputHandler
from card import Card
from random import choice, randint, shuffle
from action_button import ActionButton
from  special_abilities import *

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font("../assets/Berylium/Berylium.ttf", 45)


class Round:
    def __init__(self, round_number, player_type, player_number):
        self.round_number = round_number
        self.player_type = player_type
        self.player_number = player_number

    def count_known_for_player(self, hand):
        sum = 0
        for card in hand:
            if card.known_for_player:
                sum += 1
        return sum

    def create_buttons(self, state):
        button_img = pygame.image.load("../assets/przycisk.png").convert_alpha()
        button_width, button_height = 200, 50
        button_img = pygame.transform.scale(button_img, (button_width, button_height))
        use_card_button = ActionButton(100, 100, "button_Użyj karty", button_img, False)
        do_not_use_card_button = ActionButton(100, 300, "button_Nie używaj umiejętności", button_img, False)
        what_card_do_button = ActionButton(100, 700, "button_Co robi?", button_img, False)  # opis umiejetnoesi karty
        woke_button = ActionButton(button_width * 8.5, button_height * 2, "button_Pobudka", button_img, height=90,
                                   show=False)  # kontrowersyjne ustawienie, ale takie refactoruje
        tell_two_cards_button = ActionButton(100, 500, "button_tell the two cards value", button_img, False)
        action_buttons = [use_card_button, what_card_do_button, do_not_use_card_button,
                          woke_button, tell_two_cards_button]
        for button in action_buttons:
            state[button.location] = [button]
        return state

    def create_example_state(self, screen, assets, card_size, variant):
        state = {
            "hand_temp": [],
            "hand1": [],
            "hand2": [],
            "hand3": [],
            "hand4": [],
            "face_down_pile": [],
            "face_up_pile": [],
            "button_Użyj karty": [],
            "button_Nie używaj umiejętności": [],
            "button_Co robi?": [],
            "button_Pobudka": [],
            "button_tell the two cards value": []
        }

        num_cards = 6
        all_cards = []
        for i in range(num_cards):
            all_cards.append(assets["cards"][i])

        id = 0

        # Przydziel karty do rąk graczy
        for hand in ["hand1", "hand2", "hand3", "hand4"]:
            for i in range(4):
                card_name = choice(all_cards)
                c = Card(screen, card_name, assets["card_back"], False, False, hand, i, False, False, card_size, id, 0,
                         None)
                state[hand].append(c)
                if c.crows == 9:
                    return 0

                id += 1

        # Przydziel karty do face_up_pile (ustalona liczba kart)
        for i in range(10):
            card_name = choice(all_cards)
            state["face_up_pile"].append(
                Card(screen, card_name, assets["card_back"], True, True, "face_up_pile", 0, False, False,
                     card_size, id, 0, None)
            )
            id += 1
        # Przydziel karty do face_down_pile (ustalona liczba kart)
        for i in range(10):
            card_name = choice(all_cards)
            state["face_down_pile"].append(
                Card(screen, card_name, assets["card_back"], False, False, "face_down_pile", 0, False, False, #blad nie moze   byc i naprawione
                     card_size, id, 0, None)
            )
            id += 1
        # nadanie kart specjalnych! uwaga!
        #take two nie dziala
        state["face_down_pile"][-2].ability = "swap"
        state["face_down_pile"][-1].ability = "look"

        for localisation in state:
            if localisation[:4] == "hand" or localisation[:4] == "face":
                for card in state[localisation]:
                    card.update_position()  # zainicjalizowanie kart bardzo  ważne
        state = self.create_buttons(state)
        return state

    def debug(self, state):
        print("card id: ")
        for localization in state:
            if localization[:4] == "hand" or localization[:4] == "face":
                print(localization, end=" ")
                for card in state[localization]:
                    print(" " + str(card.id), end="")
                print("")
        print("")

    def swap_card(self, state, card1, card2):
        state[card1.location][card1.location_number], state[card2.location][card2.location_number] = \
            state[card2.location][card2.location_number], state[card1.location][card1.location_number]
        card1.location, card2.location = card2.location, card1.location
        card1.location_number, card2.location_number = card2.location_number, card1.location_number
        return state, card1, card2

    def choose_card_from_stack(self, state, stack_type, index):
        card = state[stack_type][index]
        return card

    def choose_card_from_stack_up(self, state, stack_type):
        card = state[stack_type][-1]
        return card

    def choose_card_from_hand(self, state, hand_name):
        card = InputHandler.choose_from(state[hand_name])
        card.clicked = True
        return card

    def human_show_2_cards(self, hand, game_renderer, game_round, state):
        action_text = "Podglądnij 2 karty"
        picked_set = set()  # znowu niepotrzebna zmiana stabilnej wersji ktora działała,  nie wiem moze to dziala, a moze beda bledy
        game_renderer.draw_state(game_round, state, action_text)
        while game_round.count_known_for_player(hand) < 2:
            picked_card = game_round.choose_card_from_hand(state, "hand1")
            if not picked_card.known_for_player:
                picked_set.add(picked_card)
                picked_card.show_front = True
                picked_card.highlighted = True
                picked_card.known_for_player = True
                # picked_card.selected_info = "Niewidoczna"
                game_renderer.draw_state(game_round, state, "Podgladnie...")
        pygame.time.wait(0)
        for c in picked_set:
            c.show_front = False
            c.highlighted = False

    def bot_show_2_cards(self, hand, game_renderer, game_round, state):
        action_text = "Boty podglądają karty"
        game_renderer.draw_state(game_round, state, action_text)
        while game_round.count_known_for_player(hand) < 2:
            picked_card = choice(hand)
            if not picked_card.known_for_player:
                pygame.time.wait(100)
                picked_card.known_for_player = True
                picked_card.show_front = False
                picked_card.highlighted = True
                game_renderer.draw_state(game_round, state, action_text)
                picked_card.highlighted = False


    def end_screen(self, screen, players, winner):
        # "przycisk"
        screen_width, screen_height = screen.get_size()
        button_img = pygame.image.load("../assets/przycisk.png").convert_alpha()
        button_width, button_height = 800, 800
        button_img = pygame.transform.scale(button_img, (button_width, button_height))
        button_x = (screen_width - button_width) // 2
        button_y = (screen_height - button_height) // 2
        font = pygame.font.Font("../assets/Berylium/Berylium.ttf", 50)
        screen.blit(button_img, (button_x, button_y))

        # Nagłówek
        header_text = "Wygrałeś!" if winner == "player1" else "Przegrałeś"
        header_surface = font.render(header_text, True, (255, 255, 255))  # White color

        header_x = button_x + (button_width - header_surface.get_width()) // 2
        header_y = button_y
        screen.blit(header_surface, (header_x, header_y))

        # Tabelka wyników
        row_height = 150
        for i, player in enumerate(players):
            row_text = f"Gracz {player.player_number} | {player.crows}"
            row_surface = font.render(row_text, True, (138, 99, 58))  # White color

            row_x = button_x + (button_width - row_surface.get_width()) // 2
            row_y = header_y + (i + 1) * row_height
            screen.blit(row_surface, (row_x, row_y))

        pygame.display.flip()

        # czekanie na koniec gry
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    return -1  # zwracanie żeby wrócić do menu? Wojtek?

    def wake_up(self, variant, state, players, screen):
        end_game = False
        player1 = players[0]  # wyświetlamy tylko dla żywego gracza czyli player1
        # UAGA każdy wariant ma prawdopodobnie inne licznei kruków, to kazdy musi sbie dostosować
        if variant == 2:
            player1 = players[0]
            waker = player1  # tylko gracz może budzić (najwyżej potem można zmeinic)
            for player in players:
                cur_hand = "hand" + str(player.player_number)
                hand_counting = state[cur_hand]
                for card in hand_counting:
                    if card.crows != 9:
                        player.crows += 50
                        if player.crows >= 100: end_game = True  # warunek zakończenia gry# END GAME JEST TUTAJ!!!!
                        break
                print("Gracz: ", player.player_number, " punkty: ", player.crows)
                # jesteśmy hojni i jak dwaj gracze mają tylko karty z 9 krukami to niech oboje sobie nic dodają :)

        # TUTAJ DLA WSZYSTKICH WARIANTÓW
        if end_game:
            winner = "WYGRYWASZ!!!" if player1.crows < 100 else "Nie ty"  # chyba każdy wariant ma wygraną od 100 krókó, jak nie zróbcie if -MM
            winner = str(player1)
            self.end_screen(screen, players, winner)
            return "koniec gry"

        # Tutaj wyśwuietlanie tabelki dla wszytskich wariantów
        print("hello from wakey")
        screen_width, screen_height = screen.get_size()
        button_img = pygame.image.load("../assets/przycisk.png").convert_alpha()
        button_width, button_height = 800, 800
        button_img = pygame.transform.scale(button_img, (button_width, button_height))
        button_x = (screen_width - button_width) // 2
        button_y = (screen_height - button_height) // 2
        font = pygame.font.Font("../assets/Berylium/Berylium.ttf", 50)
        screen.blit(button_img, (button_x, button_y))

        # Nagłówek
        header_text = "Aktualne punkty"
        header_surface = font.render(header_text, True, (255, 255, 255))  # White color
        header_x = button_x + (button_width - header_surface.get_width()) // 2
        header_y = button_y
        screen.blit(header_surface, (header_x, header_y))

        # Dolny tekst
        bottom_text = "Kliknij, aby kontynuować"
        bottom_surface = font.render(bottom_text, True, (255, 255, 255))
        bottom_x = button_x + (button_width - bottom_surface.get_width()) // 2
        bottom_y = button_y + button_height - bottom_surface.get_height() - 10  # 20 px margines od dołu
        screen.blit(bottom_surface, (bottom_x, bottom_y))

        # Tabelka wyników
        row_height = 150
        for i, player in enumerate(players):
            row_text = f"Gracz {player.player_number} | {player.crows}"
            row_surface = font.render(row_text, True, (138, 99, 58))  # White color

            row_x = button_x + (button_width - row_surface.get_width()) // 2
            row_y = header_y + (i + 1) * row_height
            screen.blit(row_surface, (row_x, row_y))

        pygame.display.flip()

        # czekanie na input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

    def human_swap_chosen_pile_up_with_hand(self, game_renderer, game_round, state, chosen_card_from_stack):  # example
        chosen_card_from_stack.highlighted = True
        game_renderer.draw_state(game_round, state, "Wybierz karte z ręki")
        card_from_hand = game_round.choose_card_from_hand(state, "hand1")
        card_from_hand.highlighted = True
        game_renderer.draw_state(game_round, state, "Zamienianie miejscami")
        pygame.time.wait(500)  # todo wydłużyć czas
        state, new_card_from_hand, new_card_from_stack = game_round.swap_card(state, chosen_card_from_stack,
                                                                              card_from_hand)
        new_card_from_stack.highlighted = False
        new_card_from_hand.highlighted = False
        new_card_from_stack.show_front = True
        # pokazanie karty, którą wybraliśmy (przez chwilę)
        new_card_from_hand.show_front = True
        game_renderer.draw_state(game_round, state, "Patrz")
        pygame.time.wait(500)
        new_card_from_hand.show_front = False
        game_renderer.draw_state(game_round, state, "Koniec patrzenia")
    def human_take_card_from_face_down_pile(self, game_renderer, game_round, state, chosen_card_from_stack):
        def move_in_temp_card_to_face_up_pile():
            card1.location = "face_up_pile"
            card1.location_number = len(state["face_up_pile"])
            state["face_up_pile"].append(card1)
            state["hand_temp"].pop()
        def move_in_temp_to_hand_and_hand_to_face_up_pile(card2):
            card1.location = card2.location
            card1.location_number = card2.location_number
            card2.location_number = len(state["face_up_pile"])
            card2.location = "face_up_pile"
            card2.show_front = True
            state["face_up_pile"].append(card2)
            state["hand1"][card1.location_number] = card1
            state["hand_temp"].pop()
            card1.show_front = True
            game_renderer.draw_state(game_round, state, "Patrz")
            pygame.time.wait(500)
            card1.show_front = False
            game_renderer.draw_state(game_round, state, "Koniec patrzenia")

        def choose_card_and_move_to_hand_or_face_down_pile():
            game_renderer.draw_state(game_round, state, "Zamień dobraną karte z ręką lub stosem odkrytym")
            card2 = InputHandler.choose_from(state["face_up_pile"] + state["hand1"])
            if card2.location == "face_up_pile":
                move_in_temp_card_to_face_up_pile()  # card1 is in hand_temp
            if card2.location == "hand1":
                move_in_temp_to_hand_and_hand_to_face_up_pile(card2)
        # dodanie karty do hand_temp, usunięcie z wybranego  stosu
        card1 = chosen_card_from_stack
        card1.location = "hand_temp"
        card1.location_number = 0
        card1.show_front = True
        state["hand_temp"].append(card1)
        state["face_down_pile"].pop()
        # wybranie  karty z atrybutem location, która wskaże gdzie ma pójść
        if state["hand_temp"][0].ability==None:
            choose_card_and_move_to_hand_or_face_down_pile()
        else:
            if state["hand_temp"][0].ability == "swap":
                text ="Karta specjalna: Możesz zamienić dowolne 2 karty z rąk graczy (bez odkrywania ich)"
            elif state["hand_temp"][0].ability == "look":
                text = "Karta specjalna:  Możesz podejrzeć dowolną kartę z rąk graczy"
            elif state["hand_temp"][0].ability == "take":
                text ="Karta specjalna: Wybierasz 2 karty z góry zakrytego stosu jedną odkładasz na stos odkryty i robisz to co zawsze"
            # pokazanie  przyciskow
            state["button_Użyj karty"][0].show = True
            state["button_Nie używaj umiejętności"][0].show = True
            game_renderer.draw_state(game_round,state,text)
            chosen_option = InputHandler.choose_from(state["button_Użyj karty"] + state["button_Nie używaj umiejętności"])
            print("kliknieto",chosen_option)
            # po nacisnieciu przycisku ukrycie przyciskow
            state["button_Użyj karty"][0].show = False
            state["button_Nie używaj umiejętności"][0].show = False
            # wykonanie tury
            if chosen_option.location == "button_Użyj karty":
                if state["hand_temp"][0].ability == "swap":
                    move_in_temp_card_to_face_up_pile()
                    special_ability_swap(game_round,game_renderer,state)
                elif state["hand_temp"][0].ability == "look":# I am your father
                    move_in_temp_card_to_face_up_pile()
                    special_ability_look(game_round,game_renderer,state)
                # take two  nie dziala
                elif state["hand_temp"][0].ability == "take":
                    move_in_temp_card_to_face_up_pile()
                    special_ability_take_two(game_round,game_renderer,state)
                    # po skonczeniu take two wybrana karta ma byc w hand_temp z  lokalizacja 0 zeby poznisza funkcja  mogla dzialac choose_card...
                    choose_card_and_move_to_hand_or_face_down_pile()
            elif chosen_option.location == "button_Nie używaj umiejętności":
                choose_card_and_move_to_hand_or_face_down_pile()
        self.debug(state)

    def human_turn_idz_na_calosc(self, state, game_round, game_renderer,players):  # example
        state["button_Pobudka"][0].show = True
        game_renderer.draw_state(game_round, state, "Wybierz stos lub kliknij pobudka")
        object = InputHandler.choose_from(state["face_up_pile"] + state["face_down_pile"] + state["button_Pobudka"])
        state["button_Pobudka"][0].show = False
        object_type = object.location
        if object_type == "button_Pobudka":
             if self.wake_up(2,state,players, game_renderer.screen) == "koniec gry":
                return "koniec gry" # w petli gry dodalem if basic_variant_turn == koniec gry: running = False, menu cos nie teges
        chosen_stack_type = object_type
        chosen_card_from_stack = self.choose_card_from_stack_up(state, chosen_stack_type)
        if object_type == "face_up_pile":
            self.human_swap_chosen_pile_up_with_hand(game_renderer, game_round, state, chosen_card_from_stack)
        if object_type == "face_down_pile":
            self.human_take_card_from_face_down_pile(game_renderer, game_round, state, chosen_card_from_stack)

    def bot_turn_idz_na_calosc(self,game_round,game_renderer,state):
        game_renderer.draw_state(game_round, state, "Bot cos robi")
        pygame.time.wait(500)
        print("robot! ᕙ(  •̀ ᗜ •́  )ᕗ")  # do zrobienia

    def show_text_bar(self, screen, running):
        input_rect = pygame.Rect(300, 250, 200, 50)
        text_color = (0, 0, 0)
        input_color_active = (255, 255, 255)
        input_color_inactive = (200, 200, 200)
        input_color = input_color_inactive
        active = False
        user_text = ""  # Tekst wpisany przez użytkownika
        font = pygame.font.Font(None, 36)

        while running:
            # screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return None

                # Kliknięcie myszą
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = True
                        input_color = input_color_active
                    else:
                        active = False
                        input_color = input_color_inactive

                # Wprowadzanie tekstu
                if event.type == pygame.KEYDOWN and active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        try:
                            value = int(user_text)
                            print(f"Wprowadzona wartość: {value}")
                            return value
                        except ValueError:
                            print("Nieprawidłowa liczba!")
                            user_text = ""
                    else:
                        if event.unicode.isdigit():
                            user_text += event.unicode

            pygame.draw.rect(screen, input_color, input_rect, border_radius=5)
            text_surface = font.render(user_text, True, text_color)
            screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))
            pygame.display.flip()
