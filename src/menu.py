#Ustawienie pozycji przycisków w zależności od screen_width, screen_height.

import pygame
import sys
import webbrowser
from menu_button import Button
import os
from variant2 import idz_na_calosc
from variant1 import  variant1
pygame.init()
# Ustawienie ikony gry
game_icon = pygame.image.load("../assets/ikonka.png")
pygame.display.set_icon(game_icon)

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()

# Rozmiary okna gry, oryginalnie otwiera się w fullscreenie:
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
fullscreen = True  # Domyślnie tryb pełnoekranowy
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Nazwa okna gry:
pygame.display.set_caption("Sen")

# Tło gry:
BG = pygame.image.load("../assets/menu.png")
BG_SCALED = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
OP = pygame.image.load("../assets/menu_rozmazane.png")
OP_SCALED = pygame.transform.scale(OP, (SCREEN_WIDTH, SCREEN_HEIGHT))
TABLE = pygame.image.load("../assets/stół.png")
TABLE_SCALED = pygame.transform.scale(TABLE, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Ścieżki muzyczne
music_tracks = [
    '../assets/muzyka/Cozy day.mp3',
    '../assets/muzyka/Memories.mp3',
    '../assets/muzyka/Coffee.mp3'
]
current_track_index = 0  # Aktualny indeks ścieżki
pygame.mixer.music.load(music_tracks[current_track_index])
pygame.mixer.music.play(-1)

volume_level = 1.0  # Globalny poziom głośności

def load_gif_frames(folder_path):
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png"):  # Sprawdź rozszerzenie plików
            frame = pygame.image.load(os.path.join(folder_path, filename))
            frame = pygame.transform.scale(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Skalowanie do rozmiaru ekranu
            frames.append(frame)
    return frames

GIF_FRAMES = load_gif_frames("../assets/klatki")
current_frame = 0  # Indeks aktualnej klatki
frame_delay = 300  # Opóźnienie między klatkami w milisekundach
last_frame_update = pygame.time.get_ticks()  # Czas ostatniej zmiany klatki


def change_music(direction):
    global current_track_index
    pygame.mixer.music.stop()
    current_track_index = (current_track_index + direction) % len(music_tracks)
    pygame.mixer.music.load(music_tracks[current_track_index])
    pygame.mixer.music.play(-1)


def get_font(size):  # Zwraca czcionkę o określonym rozmiarze
    return pygame.font.Font("../assets/Berylium/Berylium.ttf", size)


def get_title(size):
    return pygame.font.Font("../assets/ringbearer/RINGM___.TTF", size)


def toggle_fullscreen():
    global fullscreen, SCREEN
    fullscreen = not fullscreen
    if fullscreen:
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH - 10, SCREEN_HEIGHT - 50))


def main_menu():
    global current_frame, last_frame_update

    #Wymiary przycisków menu na podstawie rozdzielczości monitora:
    menu_button_width = int(SCREEN_WIDTH * 0.3 // 2)
    menu_button_height = int(SCREEN_HEIGHT * 0.1)

    while True:
        SCREEN.blit(GIF_FRAMES[current_frame], (0, 0))  # Wyświetlenie klatki GIF-a

        # Animacja GIF-a
        current_time = pygame.time.get_ticks()
        if current_time - last_frame_update > frame_delay:  # Sprawdzenie opóźnienia
            current_frame = (current_frame + 1) % len(GIF_FRAMES)  # Przejście do następnej klatki
            last_frame_update = current_time

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_title(int(SCREEN_HEIGHT*0.19)).render("Sen", True, "#8a6539")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH * 0.12, SCREEN_HEIGHT*0.14))

        PLAY_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("../assets/przycisk.png"), (menu_button_width, menu_button_height)),
            pos=(SCREEN_WIDTH * 0.12, SCREEN_HEIGHT*0.33),
            text_input="Graj", font=get_font(int(SCREEN_HEIGHT * 0.05)),  # Rozmiar czcionki jako proporcja wysokości
            base_color="#8a633a", hovering_color="White")

        OPTIONS_BUTTON = Button(
            image=pygame.transform.scale(pygame.image.load("../assets/przycisk.png"), (menu_button_width, menu_button_height)),
            pos=(SCREEN_WIDTH * 0.12, SCREEN_HEIGHT*0.49),
            text_input="Ustawienia", font=get_font(int(SCREEN_HEIGHT * 0.05)),
            base_color="#8a633a", hovering_color="White")

        RULES_BUTTON = Button(
            image=pygame.transform.scale(pygame.image.load("../assets/przycisk.png"), (menu_button_width, menu_button_height)),
            pos=(SCREEN_WIDTH * 0.12, SCREEN_HEIGHT*0.65),
            text_input="Zasady Gry", font=get_font(int(SCREEN_HEIGHT * 0.05)),
            base_color="#8a633a", hovering_color="White")

        QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("../assets/przycisk.png"), (menu_button_width, menu_button_height)),
            pos=(SCREEN_WIDTH * 0.12, SCREEN_HEIGHT*0.81),
            text_input="Wyjście", font=get_font(int(SCREEN_HEIGHT * 0.05)),
            base_color="#8a633a", hovering_color="White")


        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, RULES_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if RULES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    open_rules()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:  # F11 to klawisz skrótu
                    toggle_fullscreen()

        pygame.display.update()


def open_rules():
    # Funkcja otwierająca stronę z zasadami gry
    url = "https://gry.nk.com.pl/wp-content/uploads/2022/03/SEN-instrukcja.pdf"
    webbrowser.open(url)


def play():
    # Rozmiar czcionki dla przycisków
    play_button_font_size = int(SCREEN_HEIGHT * 0.05)

    while True:
        SCREEN.blit(OP_SCALED, (0, 0))
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        # Nagłówek:
        PLAY_TEXT = get_title(int(SCREEN_HEIGHT * 0.06)).render("WYBIERZ WARIANT GRY:", True, "#8a6539")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.2))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        # Przyciski dla trybów gry:
        MODE_1 = Button(image=None, pos=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.4),
                        text_input="Nie takie kruki straszne",
                        font=get_font(play_button_font_size), base_color="White", hovering_color="#F4A460", scale=1)
        MODE_2 = Button(image=None, pos=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5), text_input="Idź na całość",
                        font=get_font(play_button_font_size), base_color="White", hovering_color="#F4A460", scale=1)
        MODE_3 = Button(image=None, pos=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.6), text_input="Wiem, co mam",
                        font=get_font(play_button_font_size), base_color="White", hovering_color="#F4A460", scale=1)

        # Przycisk powrotu:
        PLAY_BACK = Button(image=None, pos=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.85), text_input="Powrót",
                           font=get_font(play_button_font_size), base_color="#5b4224", hovering_color="White", scale=1)

        # Wyświetlenie przycisków:
        for button in [MODE_1, MODE_2, MODE_3, PLAY_BACK]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if MODE_1.checkForInput(PLAY_MOUSE_POS):
                    print("Wybrano tryb: Nietakie kruki straszne") #
                    variant1(SCREEN)  # Zastąp odpowiednią funkcją
                if MODE_2.checkForInput(PLAY_MOUSE_POS):
                    idz_na_calosc(SCREEN)  # Zastąp odpowiednią funkcją
                    print("Wybrano tryb: Idź na całość")  # Zastąp odpowiednią funkcją
                if MODE_3.checkForInput(PLAY_MOUSE_POS):
                    print("Wybrano tryb: Wiem, co mam")  # Zastąp odpowiednią funkcją
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:  # F11 to klawisz skrótu
                    toggle_fullscreen()

        pygame.display.update()


def show_authors():

    while True:
        AUTHOR_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(TABLE_SCALED, (0, 0))

        header_font_size = int(SCREEN_HEIGHT * 0.07)
        AUTHOR_TEXT = get_font(header_font_size).render("Autorzy gry:", True, "#8a6539")
        AUTHOR_RECT = AUTHOR_TEXT.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.15))
        SCREEN.blit(AUTHOR_TEXT, AUTHOR_RECT)

        # Lista autorów gry
        AUTHOR_NAMES = [
            "Wojtek Cieślik - Gameplay",
            "Hania Szlęk - Grafika",
            "Maja Skóra - Menu gry",
            "Olga Chruściel - Boty",
            "Joanna Frączyk - Core logic",
            "Magdalena Majda, Wiktoria Szczepaniak - Warianty gry"
        ]

        # Rozmiar czcionki dla autorów
        author_font_size = int(SCREEN_HEIGHT * 0.05)

        # Pozycje i odstępy dla autorów
        author_start_y = int(SCREEN_HEIGHT * 0.25)
        author_gap = int(SCREEN_HEIGHT * 0.07)

        y_offset = author_start_y
        for name in AUTHOR_NAMES:
            author_text = get_font(author_font_size).render(name, True, "White")
            author_rect = author_text.get_rect(center=(SCREEN_WIDTH * 0.5, y_offset))
            SCREEN.blit(author_text, author_rect)
            y_offset += author_gap

        # Przycisk powrotu
        button_font_size = int(SCREEN_HEIGHT * 0.05)
        AUTHOR_BACK = Button(
            image=None,
            pos=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.9),
            text_input="Powrót",
            font=get_font(button_font_size),
            base_color="#5b4224",
            hovering_color="White",
            scale=1
        )

        # Obsługa myszy i przycisku
        AUTHOR_BACK.changeColor(pygame.mouse.get_pos())
        AUTHOR_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if AUTHOR_BACK.checkForInput(AUTHOR_MOUSE_POS):
                    options()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:  # F11 to klawisz skrótu
                    toggle_fullscreen()

        pygame.display.update()


def options():
    global SCREEN, fullscreen, current_track_index, volume_level  # Dodanie globalnej zmiennej indeksu muzyki

    # Proporcje dla elementów
    title_font_size = int(SCREEN_HEIGHT * 0.08)
    option_font_size = int(SCREEN_HEIGHT * 0.045)
    button_font_size = int(SCREEN_HEIGHT * 0.05)
    arrow_scale_ratio = 0.4  # Skala przycisków strzałek

    # Pusty prostokąt, który ma się znaleźć pod napisami
    prost = pygame.image.load('../assets/przycisk2.png')
    prost_scale = pygame.transform.scale(prost, (SCREEN_WIDTH*0.28//2, SCREEN_HEIGHT*0.088))

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(OP_SCALED, (0, 0))

        # Napisy na ustawienia dźwięku, rozdzielczości, ekranu oraz wielki napis ustawienia
        OPTIONS_TITLE = get_title(title_font_size).render("USTAWIENIA", True, "#8a6539")
        OPTIONS_RECT_T = OPTIONS_TITLE.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.2))
        SCREEN.blit(OPTIONS_TITLE, OPTIONS_RECT_T)

        OPTIONS_DZW = get_font(int(button_font_size*1.25)).render("Muzyka", True, "#8a633a")
        OPTIONS_EKR = get_font(int(button_font_size*1.25)).render("Ekran", True, "#8a633a")
        OPTIONS_GLOS = get_font(int(button_font_size*1.25)).render("Głośność", True,"#8a633a")  # Dodanie napisu "Dźwięk"

        OPTIONS_RECT_D = OPTIONS_DZW.get_rect(center=(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.343))
        OPTIONS_RECT_E = OPTIONS_EKR.get_rect(center=(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.605))
        OPTIONS_RECT_G = OPTIONS_GLOS.get_rect(center=(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.476))

        SCREEN.blit(prost_scale, (SCREEN_WIDTH * 0.52, SCREEN_HEIGHT * 0.3))
        SCREEN.blit(prost_scale, (SCREEN_WIDTH * 0.52, SCREEN_HEIGHT * 0.56))
        SCREEN.blit(prost_scale, (SCREEN_WIDTH * 0.52, SCREEN_HEIGHT * 0.43))
        SCREEN.blit(OPTIONS_DZW, OPTIONS_RECT_D)
        SCREEN.blit(OPTIONS_EKR, OPTIONS_RECT_E)
        SCREEN.blit(OPTIONS_GLOS, OPTIONS_RECT_G)

        # Wyświetlanie aktualnie odtwarzanej muzyki
        current_music_name = os.path.splitext(os.path.basename(music_tracks[current_track_index]))[0]  # Pobiera nazwę pliku bez rozszerzenia
        current_music_text = get_font(option_font_size).render(current_music_name, True,"#241c1b")
        current_music_rect = current_music_text.get_rect(center=(SCREEN_WIDTH * 0.588, SCREEN_HEIGHT * 0.343))
        SCREEN.blit(current_music_text, current_music_rect)

        # Napisy z informacją o trybie ekranu:
        if fullscreen:
            screen_mode_text = get_font(option_font_size).render("Pełny ekran", True,"#241c1b")
        else:
            screen_mode_text = get_font(option_font_size).render("Okno", True, "#241c1b")
        screen_mode_rect = screen_mode_text.get_rect(center=(SCREEN_WIDTH * 0.589, SCREEN_HEIGHT * 0.605))
        SCREEN.blit(screen_mode_text, screen_mode_rect)

        # Wyświetlanie aktualnego poziomu głośności
        volume_text = get_font(option_font_size).render(f"{int(volume_level * 100)}%", True,"#241c1b")
        volume_rect = volume_text.get_rect(center=(SCREEN_WIDTH * 0.593, SCREEN_HEIGHT * 0.476))
        SCREEN.blit(volume_text, volume_rect)

        # Przyciski powrotu
        OPTIONS_BACK = Button(
            image=None,
            pos=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.85),
            text_input="Powrót",
            font=get_font(button_font_size),
            base_color="#5b4224", hovering_color="White",
            scale=1
        )
        OPTIONS_BACK.changeColor(pygame.mouse.get_pos())
        OPTIONS_BACK.update(SCREEN)

        # Przycisk autorzy
        OPTIONS_AUT = Button(
            image=None,
            pos=(SCREEN_WIDTH * 0.66, SCREEN_HEIGHT * 0.865),
            text_input="Autorzy",
            font=get_font(button_font_size),
            base_color="#8a633a", hovering_color="White",
            scale=1
        )
        OPTIONS_AUT.changeColor(pygame.mouse.get_pos())
        OPTIONS_AUT.update(SCREEN)

        # Przyciski strzałek do zmiany trybu ekranu
        OPTIONS_ARROW_L = Button(
            image=pygame.image.load("../assets/strzałka2.png"),
            pos=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.605),
            text_input=None,
            font=get_font(option_font_size),
            base_color="#674a29", hovering_color="White",
            scale=arrow_scale_ratio
        )
        OPTIONS_ARROW_R = Button(
            image=pygame.image.load("../assets/strzałka.png"),
            pos=(SCREEN_WIDTH * 0.68, SCREEN_HEIGHT * 0.605),
            text_input=None,
            font=get_font(option_font_size),
            base_color="#674a29", hovering_color="White",
            scale=arrow_scale_ratio
        )
        OPTIONS_ARROW_L.update(SCREEN)
        OPTIONS_ARROW_R.update(SCREEN)

        # Przyciski do zmiany muzyki
        MUSIC_ARROW_L = Button(
            image=pygame.image.load("../assets/strzałka2.png"),
            pos=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.343),
            text_input=None,
            font=get_font(option_font_size),
            base_color="#674a29", hovering_color="White",
            scale=arrow_scale_ratio
        )
        MUSIC_ARROW_R = Button(
            image=pygame.image.load("../assets/strzałka.png"),
            pos=(SCREEN_WIDTH * 0.68, SCREEN_HEIGHT * 0.343),
            text_input=None,
            font=get_font(option_font_size),
            base_color="#674a29", hovering_color="White",
            scale=arrow_scale_ratio
        )
        MUSIC_ARROW_L.update(SCREEN)
        MUSIC_ARROW_R.update(SCREEN)

        # Przyciski strzałek do regulacji głośności
        VOLUME_ARROW_L = Button(
            image=pygame.image.load("../assets/strzałka2.png"),
            pos=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.476),
            text_input=None,
            font=get_font(option_font_size),
            base_color="#674a29", hovering_color="White",
            scale=arrow_scale_ratio
        )
        VOLUME_ARROW_R = Button(
            image=pygame.image.load("../assets/strzałka.png"),
            pos=(SCREEN_WIDTH * 0.68, SCREEN_HEIGHT * 0.476),
            text_input=None,
            font=get_font(option_font_size),
            base_color="#674a29", hovering_color="White",
            scale=arrow_scale_ratio
        )
        VOLUME_ARROW_L.update(SCREEN)
        VOLUME_ARROW_R.update(SCREEN)

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTIONS_ARROW_L.checkForInput(OPTIONS_MOUSE_POS) or OPTIONS_ARROW_R.checkForInput(OPTIONS_MOUSE_POS):
                    toggle_fullscreen()
                if OPTIONS_AUT.checkForInput(OPTIONS_MOUSE_POS):
                    show_authors()
                if MUSIC_ARROW_L.checkForInput(OPTIONS_MOUSE_POS):
                    change_music(-1)
                if MUSIC_ARROW_R.checkForInput(OPTIONS_MOUSE_POS):
                    change_music(1)

                # Obsługa zmiany głośności
                if VOLUME_ARROW_L.checkForInput(OPTIONS_MOUSE_POS):
                    volume_level = max(0, volume_level - 0.1)  # Zmniejsz głośność
                    pygame.mixer.music.set_volume(volume_level)
                if VOLUME_ARROW_R.checkForInput(OPTIONS_MOUSE_POS):
                    volume_level = min(1, volume_level + 0.1)  # Zwiększ głośność
                    pygame.mixer.music.set_volume(volume_level)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:  # F11 to klawisz skrótu
                    toggle_fullscreen()

        pygame.display.update()

main_menu()

