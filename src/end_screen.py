from itertools import count

import pygame
def end_screen(screen, players, winner):
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
    header_text = "WYGRAŁEŚ" if winner == "player1" else "PRZEGRAŁEŚ"
    header_surface = font.render(header_text, True, (255, 255, 255))  # White color

    header_x = button_x + (button_width - header_surface.get_width()) // 2
    header_y = button_y
    screen.blit(header_surface, (header_x, header_y))

    # Tabelka wyników
    row_height = 150
    for i, player in enumerate(players):
        row_text = f"Gracz {player.player_number} | {player.crows}"
        if player.player_number == 1:
            row_text = f"Twój wynik | {player.crows}"
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


def wake_up(variant, state, players, screen, additional_points):
    end_game = False
    player1 = players[0]  # wyświetlamy tylko dla żywego gracza czyli player1
    waker = player1
    kara = 0

    if variant == 2:
        min_crows = float('inf')
        waker_crows = 0
        waker_minimum = False
        count_nines_big = 0

        #reset onlynines
        for player in players:
            player.onynines = 1

        #Najpier sprawdznie czy jakiś gracz ma 9 kruków
        for player in players:
            cur_hand = "hand" + str(player.player_number)
            hand_counting = state[cur_hand]
            for card in hand_counting:
                if card.crows != 9:
                    player.onlynine = 0

        #Jak ma to będziemy robić liczenie 50 lub 0
        for player in players:
            if player.onlynine == 1:
                count_nines_big = 1

        if count_nines_big:
            for player in players:
                cur_hand = "hand" + str(player.player_number)
                hand_counting = state[cur_hand]
                for card in hand_counting:
                    if card.crows != 9:
                        player.crows += 50
                        if player.crows >= 100:
                            end_game = True  # warunek zakończenia gry# END GAME JEST TUTAJ!!!!
                            break
                print("Gracz: ", player.player_number, " punkty: ", player.crows)
                # jesteśmy hojni i jak dwaj gracze mają tylko karty z 9 krukami to niech oboje sobie nic dodają :)

        else: #liczenie jak nie ma nikt 9 kruków
            # Reset liczby kruków przed nowym obliczeniem
            for player in players:
                player.current_crows = 0

            # Obliczanie liczby kruków dla każdego gracza zdobytyuch w tej TURZE
            for player in players:
                cur_hand = "hand" + str(player.player_number)
                hand_counting = state[cur_hand]
                for card in hand_counting:
                    player.current_crows += card.crows
                    if player == player1:
                        print(card.crows)

                # Sprawdzenie minimalnej liczby kruków
                if player.current_crows < min_crows:
                    min_crows = player.crows
                if player == waker:
                    waker_crows = player.crows
            # przypisanie nowych kruków do punktacji
            for player in players:
                player.crows += player.current_crows
                # Sprawdzenie warunku końca gry
                if player.crows >= 100:
                    end_game = True
            # Sprawdzenie, czy gracz wzywający "POBUDKA!" ma najmniej kruków
            if waker_crows == min_crows:
                # Sprawdzenie, czy więcej niż jeden gracz ma minimalną liczbę kruków (remis)
                min_count = sum(1 for player in players if player.crows == min_crows)
                if min_count > 1:
                    waker_minimum = True  # Remis w najniższej liczbie kruków
                    kara = 1
                else:
                    waker_minimum = True  # Tylko waker ma najmniej kruków
                    kara = 1
            # Dodanie kary, jeśli waker nie ma najmniej kruków i nie ma remisu
            if not waker_minimum:
                waker.crows += 5
                kara = 1

    elif variant == 1:
        lk = {}
        cp = {}
        max_crows = 0
        min_crows = 100
        for player in players:
            cur_hand = "hand" + str(player.player_number)
            hand_counting = state[cur_hand]
            lk[player] = 0
            cp[player] = 0
            for card in hand_counting:
                cp[player] += card.crows
                min_crows = min(min_crows, player.crows)
                if card.crows == 9:
                    lk[player] += 1
            max_crows = max(max_crows, lk[player])
        max_crows_players = [player for player in players if lk[player] == max_crows and player]
        print(max_crows_players)
        min_crows_player = [player for player in players if player.crows == min_crows]
        for player in players:
            if len(max_crows_players) != 1:
                player.crows += cp[player]
                if player not in min_crows_player:
                    player.crows += 5
            else:
                if player in max_crows_players:
                    player.crows += cp[player] - (lk[player]*9)
                else:
                    player.crows += cp[player]
                    if player not in min_crows_player:
                        player.crows += 5
            if player.crows >= 100:
                end_game = True
                break

    elif variant == 3:
        min_crows = float('inf')
        waker_crows = 0
        for player in players:
            cur_hand = "hand" + str(player.player_number)
            hand_counting = state[cur_hand]
            for card in hand_counting:
                player.crows += card.crows
            player.crows += additional_points[player.player_number - 1]
            if player.crows < min_crows:
                min_crows = player.crows
            if player == waker:
                waker_crows = player.crows
            if player.crows >= 100:
                end_game = True
                break
        if waker_crows > min_crows:
            waker.crows += 5
            kara = 1
            print(f"Gracz {waker.player_number} otrzymuje 5 kruków za karę!")

    elif variant == 0:
        min_crows = float('inf')
        waker_crows = 0
        waker_minimum = False

        # Reset liczby kruków przed nowym obliczeniem
        for player in players:
            player.current_crows = 0

        # Obliczanie liczby kruków dla każdego gracza zdobytyuch w tej TURZE
        for player in players:
            cur_hand = "hand" + str(player.player_number)
            hand_counting = state[cur_hand]
            for card in hand_counting:
                player.current_crows += card.crows
                if player == player1:
                    print(card.crows)

            # Sprawdzenie minimalnej liczby kruków
            if player.current_crows < min_crows:
                min_crows = player.crows

            if player == waker:
                waker_crows = player.crows


        #przypisanie nowych kruków do punktacji
        for player in players:
            player.crows += player.current_crows
            # Sprawdzenie warunku końca gry
            if player.crows >= 100:
                end_game = True

        # Sprawdzenie, czy gracz wzywający "POBUDKA!" ma najmniej kruków
        if waker_crows == min_crows:
            # Sprawdzenie, czy więcej niż jeden gracz ma minimalną liczbę kruków (remis)
            min_count = sum(1 for player in players if player.crows == min_crows)
            if min_count > 1:
                waker_minimum = True  # Remis w najniższej liczbie kruków
                kara = 1
            else:
                waker_minimum = True  # Tylko waker ma najmniej kruków
                kara = 1
        # Dodanie kary, jeśli waker nie ma najmniej kruków i nie ma remisu
        if not waker_minimum:
            waker.crows += 5
            kara = 1

    # TUTAJ DLA WSZYSTKICH WARIANTÓW
    if end_game:
        winner = str(player1)
        if player1.crows == min(player.crows for player in players):
            winner = "player1"
        end_screen(screen, players, winner)
        return "koniec gry"

    # Tutaj wyśwuietlanie tabelki dla wszytskich wariantów
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
        if player.player_number == 1:
            row_text = f"Twój wynik | {player.crows}"
            if kara == 1:  # Sprawdzenie zmiennej kara
                row_text += " | KARA +5"
        else:
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
