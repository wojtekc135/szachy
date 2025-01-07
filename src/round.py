import pygame
from pygame.font import get_fonts

from player import Player
from input_handler import InputHandler
from card import Card
from random import choice, randint, shuffle
from action_button import ActionButton
from button import Button

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

    def create_example_state(self, screen, assets, card_size, variant):
        state = {
            "temp_hand": [],
            "hand1": [],
            "hand2": [],
            "hand3": [],
            "hand4": [],
            "face_down_pile": [],
            "face_up_pile": []
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
                c = Card(screen, card_name, assets["card_back"], False, False, hand, i, False, False, card_size, id, 0)
                state[hand].append(c)
                if c.crows == 9:
                    return 0

                id += 1

        # Przydziel karty do face_up_pile (ustalona liczba kart)
        for i in range(60):
            card_name = choice(all_cards)
            state["face_up_pile"].append(
                Card(screen, card_name, assets["card_back"], True, True, "face_up_pile", i, False, False,
                     card_size, id, 0)
            )
            id += 1

        # Przydziel karty do face_down_pile (ustalona liczba kart)
        for i in range(60):
            card_name = choice(all_cards)
            state["face_down_pile"].append(
                Card(screen, card_name, assets["card_back"], False, False, "face_down_pile", i, False, False,
                     card_size, id, 0)
            )
            id += 1

        button_img = pygame.image.load("../assets/przycisk.png").convert_alpha()
        button_width, button_height = 200, 50
        button_img = pygame.transform.scale(button_img, (button_width, button_height))
        use_card_button = ActionButton(100, 100, "use card", button_img, False)
        swap_card_button = ActionButton(100, 200, "swap card", button_img, False)
        do_not_use_card_button = ActionButton(100, 300, "do not use card", button_img, False)
        EXAMPLE_SWAP_button = ActionButton(100, 400, "swap card chosen_pile_bottom <-> hand", button_img, False)
        what_card_do_button = ActionButton(100, 700, "what card do", button_img, False)
        woke_button = ActionButton(button_width * 8.5, button_height * 2, "pobudka", button_img,
                                   False)  # kontrowersyjne ustawienie, ale takie refactoruje
        action_buttons = [use_card_button, swap_card_button, what_card_do_button, do_not_use_card_button,
                          EXAMPLE_SWAP_button, woke_button]
        if variant == "variant3":
            tell_two_cards_button = ActionButton(100, 500, "tell the two cards value", button_img, False)
            action_buttons.append(tell_two_cards_button)
        state["action_buttons"] = action_buttons
        for localisation in state:
            if localisation != "action_buttons":
                for card in state[localisation]:
                    card.update_position()  # zainicjalizowanie kart bardzo  ważne
        return state

    def debug(self, state):
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
            if  localization != "action_buttons":
                print(localization, end=" ")
                for card in state[localization]:
                    print(" " + str(card.id), end="")
                print(" ", end="")
            print("")

    def swap_card(self, state, card1, card2):
        state[card1.location][card1.location_number], state[card2.location][card2.location_number] = \
            state[card2.location][card2.location_number], state[card1.location][card1.location_number]
        card1.location, card2.location = card2.location, card1.location
        card1.location_number, card2.location_number = card2.location_number, card1.location_number
        # card1.show_front = False
        return state, card1, card2

    def choose_stack_type(self, state):
        card = InputHandler.choose_from(state["face_up_pile"] + state["face_down_pile"])
        stack_type = card.location
        return stack_type

    def choose_card_from_stack(self, state, stack_type, index):
        card = state[stack_type][index]
        return card

    def choose_card_from_stack_up(self,state, stack_type):
        card = state[stack_type][-1]
        return card
    def choose_card_from_stack_bottom(self, state, stack_type):
        card = state[stack_type][0]
        return card

    def choose_card_from_hand(self, state, hand_name):
        card = InputHandler.choose_from(state[hand_name])
        card.clicked = True
        return card

    # eh
    def add_to_pile(self, state, card, target_pile):
        # nie widze potrzeby tej funkcji, bo karty nigdzie nie znikają, wystarczy używać tylko swapa chyba
        state[card.location] = target_pile
        card.location = target_pile

        card.location_number = 0
        state[card.location_number] = 0
        for i, c in enumerate(state[target_pile]):
            c.location_number = i

        card.clicked = False
        card.show_front = target_pile == "face_up_pile"

    def human_show_2_cards(self, hand, game_renderer, game_round, state):
        action_text = "Podglądnij 2 karty"
        picked_set = set() # znowu niepotrzebna zmiana stabilnej wersji ktora działała,  nie wiem moze to dziala, a moze beda bledy
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

    def show_all_buttons(self, state):
        for button in state["action_buttons"]:
            button.show = True


    def hide_all_action_buttons(self,state):
        for button in state["action_buttons"]:
            button.show = False

    def show_action_buttons_choose_option_and_hide_buttons(self,state, game_round, game_renderer, action_text):
        self.show_all_buttons(state)
        game_renderer.draw_state(game_round, state, action_text)
        chosen_button = InputHandler.choose_from(state["action_buttons"])
        self.hide_all_action_buttons(state)
        return chosen_button

    def swap_card2(self):
        return

    def use_card(self, game_round, game_renderer, state, card_from_stack):
        # nie wiem czy tu ma byc card from stack
        Player.human_use_ability(self, state, Card, game_round, game_renderer)
        card_from_stack.show_front = False
        game_renderer.draw_state(game_round, state, "Używasz karty")
        pygame.time.wait(1000)
        return

    def do_not_use_card(self,game_renderer, game_round, state):
        game_renderer.draw_state(game_round, state, "Odkładasz kartę na stos odkryty")
        # game_round.add_to_pile(state, card_from_stack, "face_up_pile")  # Do poprawy
        pygame.time.wait(1000)
        return

    def what_card_do(self,game_renderer, game_round, state, card_from_stack):
        # nie  wiem czy tu ma byc card from   stack
        game_renderer.draw_state(game_round, state, "Sprawdzasz działanie karty")
        pygame.time.wait(1000)
        # Dodaj logikę wyświetlania opisu działania karty: edit mozna stworzyc funkcje ktora blituje kwadrat z tekstem
        # po prostu i dodac ja do utils, zmienic ustawienie kart na ekranie zeby bylo wiecej miejsca
        game_renderer.draw_state(game_round, state, f"Karta: {card_from_stack.get_description()}")
        pygame.time.wait(2000)
        return

    def wake_up(self):
        pass # dodac tu wywołanie wake up co sie dzieje, bo wybieranie przycisku juz poprawilem w examplach

    def swap_bottom_chosen_pile_with_hand(self,game_renderer,game_round,state, chosen_stack_type): #example
        game_renderer.draw_state(game_round, state, " Wybierz karte z ręki")
        card_from_hand = game_round.choose_card_from_hand(state, "hand1")
        card_from_stack = self.choose_card_from_stack_bottom(state,chosen_stack_type)
        game_renderer.draw_state(game_round, state, "Zamienianie miejscami")
        pygame.time.wait(500)
        state, new_card_from_hand, new_card_from_stack = game_round.swap_card(state, card_from_stack, card_from_hand)
        # aktualizacja kard, żeby np niewkładały się obrocone czy coś, moze trzeba cos dodac jeszcze
        new_card_from_stack.selected_info = False
        if new_card_from_stack.location == "face_down_pile":
            new_card_from_stack.show_front = False
        elif new_card_from_stack.location == "face_up_pile":
            new_card_from_stack.show_front = True
        # Trzeba to ładnie zrobić i oczywiscie jak bot wybiera to nie ma byc show_front, moze jedynie know for player
        new_card_from_hand.show_front = True
        new_card_from_hand.selected_info = False
        game_renderer.draw_state(game_round, state, f"Zamieniono miejscami")

        """
        elif game_round.player_type == "bot":
            new_card_from_hand.selected_info = False
            new_card_from_hand.show_front = False
            new_card_from_hand.highlighted = True
        """

    def human_take_bottom_card_from_any_pile_add_it_on_front_to_hand(self,state, game_round, game_renderer): #example
        game_renderer.draw_state(game_round, state, "Wybierz stos")
        chosen_stack_type = self.choose_stack_type(state) #choose_from_stack  ma w srodu input handler dlatego rozgrywka ,,pausuje" i czeka na wybor karty
        chosen_card_from_stack = self.choose_card_from_stack_bottom(state, chosen_stack_type) # tego tu moze nie byc tylko  trzeba odpowiednio inne opcje zrobic argumenty to jest tylko zeby sie nic narazie nie popsulo bo moja funkcja to przyklad
        # zrobcie moze zamiast create example state, juz poprawne rozdanie kart na poczatku rozgrywki, bo to pisze ze jest example, ta funkcja to tez przyklad tylko
        chosen_button = self.show_action_buttons_choose_option_and_hide_buttons(state,game_round,game_renderer,"wybierz opcje")
        chosen_option = chosen_button.text
        if chosen_option == "use card":
            self.use_card(game_round,game_renderer,state,chosen_card_from_stack)
        elif chosen_option == "swap card":
            self.swap_card2()
        elif chosen_option == "swap card chosen_pile_bottom <-> hand":
            self.swap_bottom_chosen_pile_with_hand(game_renderer,game_round,state, chosen_stack_type)
        elif chosen_option == "do not use  card":
            self.do_not_use_card(game_renderer,game_round,state)
        elif chosen_option == "what card do":  # Co robi karta
            self.what_card_do(game_renderer,game_round,state,chosen_card_from_stack)
        elif chosen_option == "pobudka":
            self.wake_up()

        game_round.debug(state)

    def bot_take_bottom_card_from_any_pile_POP(self, state, game_round, game_renderer):
        pass

    def human_take_card_from_any_pile_POP(self, state, game_round, game_renderer):
        game_renderer.draw_state(game_round, state, "Wybierz stos")
        stack_type = game_round.choose_stack_type(state)
        stack_index_to_choose = -1  # 0 spód karty, -1 góra
        # if stack_type == "face_down_pile":
            # game_round.swap_card(state, game_round.choose_card_from_stack(state, stack_type, 0),game_round.choose_card_from_stack(state, stack_type, -1))
        card_from_stack = game_round.choose_card_from_stack(state, stack_type, stack_index_to_choose)
        if stack_type == "face_down_pile":
            card_from_stack.show_front = True
            card_from_stack.highlighted = True
            use_card_button_rect = Button(image=pygame.image.load("../assets/przycisk.png"), pos=(100, 100),
                             text_input="Uzyj karty", font=font, base_color="#8a633a", hovering_color="White",
                             scale=1.1)
            swap_card_button_rect = Button(image=pygame.image.load("../assets/przycisk.png"), pos=(100, 200),
                             text_input="Zamień kartę", font=font, base_color="#8a633a", hovering_color="White",
                             scale=1.1)
            do_not_use_button_rect = Button(image=pygame.image.load("../assets/przycisk.png"), pos=(100, 300),
                             text_input="Nie bierz karty", font=font, base_color="#8a633a", hovering_color="White",
                             scale=1.1)
            what_card_do_button_rect = Button(image=pygame.image.load("../assets/przycisk.png"), pos=(100, 700),
                             text_input="Co robi karta?", font=font, base_color="#8a633a", hovering_color="White",
                             scale=1.1)

            decision_made = False
            action_buttons = [use_card_button_rect, swap_card_button_rect, do_not_use_button_rect,
                              what_card_do_button_rect]
            while not decision_made:
                for button in action_buttons:
                    button.update(SCREEN)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for button in action_buttons:
                            if button.checkForInput(event.pos):
                                if button == use_card_button_rect:
                                    decision_made = True
                                    # Logika dla use card
                                    print("Używasz karty")
                                    game_renderer.draw_state(game_round, state, "Używasz karty")
                                    pygame.time.wait(1000)
                                    return
                                elif button == swap_card_button_rect:
                                    decision_made = True
                                    break
                                elif button == do_not_use_button_rect:
                                    decision_made = True
                                    game_renderer.draw_state(game_round, state, "Odkładasz kartę na stos odkryty")
                                    s, c1, c2 = game_round.swap_card(state, card_from_stack, game_round.choose_card_from_stack(state, -1))
                                    c1.show_front = True
                                    c1.highlighted = False
                                    c2.show_front = False
                                    c2.highlighted = False
                                    pygame.time.wait(1000)
                                    return
                                elif button == what_card_do_button_rect:
                                    decision_made = True
                                    # Tu dodaj logikę dla 'What does card do?'
                                    game_renderer.draw_state(game_round, state, "Sprawdzasz działanie karty")
                                    pygame.time.wait(1000)
                                    # Wyświetl opis karty
                                    game_renderer.draw_state(game_round, state,
                                                             f"Karta: {card_from_stack.get_description()}")
                                    pygame.time.wait(2000)
                                    return
        game_renderer.draw_state(game_round, state, " Wybierz karte z ręki")

        card_from_hand = game_round.choose_card_from_hand(state, "hand1")
        card_from_hand.highlighted = True

        game_renderer.draw_state(game_round, state, "Zamienianie miejscami")
        pygame.time.wait(500)
        state, new_card_from_hand, new_card_from_stack = game_round.swap_card(state, card_from_stack, card_from_hand)
        state[stack_type].pop(-1) #usuniecie karty z gry

        #pokazanie karty którą wybraliśmy (przez chwilę)
        if game_round.player_type == "human":
            #new_card_from_hand.selected_info = "niewidoczna"
            if stack_type == "face_down_pile":
                new_card_from_hand.show_front = False
            else:
                new_card_from_hand.show_front = True
                game_renderer.draw_state(game_round, state, "Patrz")
                pygame.time.wait(500)
                new_card_from_hand.show_front = False
                game_renderer.draw_state(game_round, state, "Koniec patrzenia")
        elif game_round.player_type == "bot":
            new_card_from_hand.selected_info = "niewidoczna"
            new_card_from_hand.show_front = False

        # aktualizacja kard, żeby np niewkładały się obrocone czy coś, moze trzeba cos dodac jeszcze
        new_card_from_stack.selected_info = False
        if new_card_from_stack.location == "face_down_pile":
            new_card_from_stack.show_front = False
        elif new_card_from_stack.location == "face_up_pile":
            new_card_from_stack.show_front = True
            new_card_from_stack.clicked = False
        card_from_stack.highlighted = False
        new_card_from_hand.highlighted = False
        new_card_from_hand.selected_info = False

        """
        elif game_round.player_type == "bot":
            new_card_from_hand.selected_info = False
            new_card_from_hand.show_front = False
            new_card_from_hand.highlighted = True
        """

        game_round.debug(state)
        game_renderer.draw_state(game_round, state, "Zamieniono miejscami")

    def bot_take_card_from_any_pile_POP(self, state, game_round, game_renderer):
        print("robot! ᕙ(  •̀ ᗜ •́  )ᕗ") #do zrobienia


    def wake_up_option(self, state, game_renderer, game_round, screen):
        # Dodałem wwybranie opcji wake_up_do zrefaktorowanych metod,  wakeup wyswietla sie zazwsze kiedy wybieranie innych opcji jak np. swap
        # bedzie to pewnie mozna usunac po implementacji do metody wake_up na ktora zrobilem miejsce
        wake_up = False
        button_img = pygame.image.load("../assets/przycisk.png").convert_alpha()
        button_width, button_height = 200, 100
        button_img = pygame.transform.scale(button_img, (button_width, button_height))
        font = pygame.font.Font("../assets/Berylium/Berylium.ttf", 50 )
        better_button = ActionButton(button_width * 8.5,button_height, "Pobudka", button_img,True, font, 90, (138, 99, 58))

        decision_made = False
        while not decision_made:
            game_renderer.draw_state(game_round, state, "Możesz kliknac pobudke lub wybrac karte")
            better_button.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN: #POPRAWIĆ, żeby mozna nacisnąć przycisk lub karte, a nie że jak nie naciśniemy przyciku to potem ejscze raz tzreba na karte
                    mouse_pos = pygame.mouse.get_pos()
                    if better_button.check_click(mouse_pos, event):#button_rect.collidepoint(event.pos):
                        decision_made = True
                        wake_up = True
                        game_renderer.draw_state(game_round, state, "POBUDKA")
                        return wake_up
                    else:
                        decision_made = True
                        break

    def variant3_options(self,screen, running, state, game_round, game_renderer):
        game_renderer.draw_state(game_round, state, "Wybierz stos")
        chosen_stack_type = self.choose_stack_type(state)
        chosen_card_from_stack = self.choose_card_from_stack_bottom(state, chosen_stack_type)
        chosen_button = self.show_action_buttons_choose_option_and_hide_buttons(state,game_round,game_renderer,"wybierz opcje")
        chosen_option = chosen_button.text
        if chosen_option == "use card":
            self.use_card(game_round,game_renderer,state,chosen_card_from_stack)
        elif chosen_option == "swap card":
            self.swap_bottom_chosen_pile_with_hand(game_renderer,game_round,state, chosen_stack_type)
        elif chosen_option == "what card do":
            self.what_card_do(game_renderer,game_round,state,chosen_card_from_stack)
        elif chosen_option == "pobudka":
            self.wake_up()
        elif chosen_option == "tell the two cards value":
            self.show_text_bar(screen, running)

        game_round.debug(state)

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

