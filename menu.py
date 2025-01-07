#Naprawienie volume level - sprawienie, że nie resetuje się po wyjściu z opcji.

import pygame
import sys
import webbrowser
from button import Button
import os

pygame.init()
# Ustawienie ikony gry
game_icon = pygame.image.load("assets/ikonka.png")
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
BG = pygame.image.load("assets/menu.png")
BG_SCALED = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
OP = pygame.image.load("assets/menu_rozmazane.png")
OP_SCALED = pygame.transform.scale(OP, (SCREEN_WIDTH, SCREEN_HEIGHT))
TABLE = pygame.image.load("assets/stół.png")
TABLE_SCALED = pygame.transform.scale(TABLE, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Ścieżki muzyczne
music_tracks = [
    'assets/muzyka/Cozy day.mp3',
    'assets/muzyka/Memories.mp3',
    'assets/muzyka/Coffee.mp3'
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

GIF_FRAMES = load_gif_frames("assets/klatki")
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
    return pygame.font.Font("assets/Berylium/Berylium.ttf", size)


def get_title(size):
    return pygame.font.Font("assets/ringbearer/RINGM___.TTF", size)


def toggle_fullscreen():
    global fullscreen, SCREEN
    fullscreen = not fullscreen
    if fullscreen:
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH - 10, SCREEN_HEIGHT - 50))


def main_menu():
    global current_frame, last_frame_update
    while True:
        SCREEN.blit(GIF_FRAMES[current_frame], (0, 0))  # Wyświetlenie klatki GIF-a

        # Animacja GIF-a
        current_time = pygame.time.get_ticks()
        if current_time - last_frame_update > frame_delay:  # Sprawdzenie opóźnienia
            current_frame = (current_frame + 1) % len(GIF_FRAMES)  # Przejście do następnej klatki
            last_frame_update = current_time

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_title(170).render("Sen", True, "#8a6539")
        MENU_RECT = MENU_TEXT.get_rect(center=(200, 120))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/przycisk.png"), pos=(200, 290),
                             text_input="Graj", font=get_font(45), base_color="#8a633a", hovering_color="White",
                             scale=1.1)
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/przycisk.png"), pos=(200, 440),
                                text_input="Ustawienia", font=get_font(45), base_color="#8a633a",
                                hovering_color="White", scale=1.1)
        RULES_BUTTON = Button(image=pygame.image.load("assets/przycisk.png"), pos=(200, 590),
                              text_input="Zasady Gry", font=get_font(45), base_color="#8a633a", hovering_color="White",
                              scale=1.1)
        QUIT_BUTTON = Button(image=pygame.image.load("assets/przycisk.png"), pos=(200, 740),
                             text_input="Wyjście", font=get_font(45), base_color="#8a633a", hovering_color="White",
                             scale=1.1)

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
    while True:
        SCREEN.blit(OP_SCALED, (0, 0))
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        # Nagłówek:
        PLAY_TEXT = get_title(50).render("WYBIERZ WARIANT GRY:", True, "#8a6539")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(760, 160))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        # Przyciski dla trybów gry:
        MODE_1 = Button(image=None, pos=(760, 300), text_input="Nie takie kruki straszne", font=get_font(45),
                        base_color="White", hovering_color="#F4A460", scale=1)
        MODE_2 = Button(image=None, pos=(760, 400), text_input="Idź na całość", font=get_font(45),
                        base_color="White", hovering_color="#F4A460", scale=1)
        MODE_3 = Button(image=None, pos=(760, 500), text_input="Wiem, co mam", font=get_font(45),
                        base_color="White", hovering_color="#F4A460", scale=1)

        # Przycisk powrotu:
        PLAY_BACK = Button(image=None, pos=(750, 730),
                              text_input="Powrót", font=get_font(43), base_color="#5b4224", hovering_color="White",
                              scale=1)

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
                    print("Wybrano tryb: Nie takie kruki straszne")  # Zastąp odpowiednią funkcją
                if MODE_2.checkForInput(PLAY_MOUSE_POS):
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

        AUTHOR_TEXT = get_font(50).render("Autorzy gry:", True, "#8a6539")
        AUTHOR_RECT = AUTHOR_TEXT.get_rect(center=(780, 150))
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

        y_offset = 250
        for name in AUTHOR_NAMES:
            author_text = get_font(40).render(name, True, "White")
            author_rect = author_text.get_rect(center=(780, y_offset))
            SCREEN.blit(author_text, author_rect)
            y_offset += 50

        AUTHOR_BACK = Button(image=None, pos=(780, 650),
                             text_input="Powrót", font=get_font(43), base_color="#5b4224", hovering_color="White",
                             scale=1)

        AUTHOR_BACK.changeColor(AUTHOR_MOUSE_POS)
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


    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(OP_SCALED, (0, 0))

        #Pusty prostokąt, który ma się znaleźć pod napisami
        prost = pygame.image.load('assets/przycisk2.png')

        # Napisy na ustawienia dźwięku, rozdzielczości, ekranu oraz wielki napis ustawienia
        OPTIONS_TITLE = get_title(74).render("USTAWIENIA", True, "#8a6539")
        OPTIONS_DZW = get_font(57).render("Muzyka", True, "#8a633a")
        OPTIONS_EKR = get_font(57).render("Ekran", True, "#8a633a")
        OPTIONS_GLOS = get_font(57).render("Głośność", True, "#8a633a")  # Dodanie napisu "Dźwięk"

        OPTIONS_RECT_T = OPTIONS_TITLE.get_rect(center=(770, 180))
        OPTIONS_RECT_D = OPTIONS_DZW.get_rect(center=(610, 320))
        OPTIONS_RECT_E = OPTIONS_EKR.get_rect(center=(610, 520))
        OPTIONS_RECT_G = OPTIONS_GLOS.get_rect(center=(610, 420))  # Wysokość dla napisu "Dźwięk"


        SCREEN.blit(prost,(790,280))
        SCREEN.blit(prost, (790,380))
        SCREEN.blit(prost, (790,480))
        SCREEN.blit(OPTIONS_TITLE, OPTIONS_RECT_T)
        SCREEN.blit(OPTIONS_DZW, OPTIONS_RECT_D)
        SCREEN.blit(OPTIONS_EKR, OPTIONS_RECT_E)
        SCREEN.blit(OPTIONS_GLOS, OPTIONS_RECT_G)

        # Wyświetlanie aktualnie odtwarzanej muzyki
        current_music_name = os.path.splitext(os.path.basename(music_tracks[current_track_index]))[0]  # Pobiera nazwę pliku bez rozszerzenia
        current_music_text = get_font(43).render(current_music_name, True, "#241c1b")
        current_music_rect = current_music_text.get_rect(center=(900, 320))
        SCREEN.blit(current_music_text, current_music_rect)

        # Napisy z informacją o trybie ekranu:
        if fullscreen:
            screen_mode_text = get_font(43).render("Pełny ekran", True, "#241c1b")
        else:
            screen_mode_text = get_font(43).render("Okno", True, "#241c1b")
        screen_mode_rect = screen_mode_text.get_rect(center=(900, 520))
        SCREEN.blit(screen_mode_text, screen_mode_rect)

        # Wyświetlanie aktualnego poziomu głośności
        volume_text = get_font(43).render(f"{int(volume_level * 100)}%", True, "#241c1b")
        volume_rect = volume_text.get_rect(center=(900, 420))
        SCREEN.blit(volume_text, volume_rect)

        # Przyciski powrotu
        OPTIONS_BACK = Button(image=None, pos=(750, 730),
                              text_input="Powrót", font=get_font(43), base_color="#5b4224", hovering_color="White",
                              scale=1)
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        # Przycisk autorzy
        OPTIONS_AUT = Button(image=None, pos=(1010, 750), text_input="Autorzy", font=get_font(43), base_color="#8a633a",
                             hovering_color="White", scale=1)
        OPTIONS_AUT.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_AUT.update(SCREEN)

        # Przyciski strzałek do zmiany trybu ekranu
        OPTIONS_ARROW_L = Button(image=pygame.image.load("assets/strzałka2.png"), pos=(750, 520),
                                 text_input=None, font=get_font(43), base_color="#674a29", hovering_color="White",
                                 scale=0.35)
        OPTIONS_ARROW_R = Button(image=pygame.image.load("assets/strzałka.png"), pos=(1050, 520),
                                 text_input=None, font=get_font(43), base_color="#674a29", hovering_color="White",
                                 scale=0.35)
        OPTIONS_ARROW_L.update(SCREEN)
        OPTIONS_ARROW_R.update(SCREEN)

        # Przyciski do zmiany muzyki
        MUSIC_ARROW_L = Button(image=pygame.image.load("assets/strzałka2.png"), pos=(750, 320),
                                text_input=None, font=get_font(43), base_color="#674a29", hovering_color="White",
                                scale=0.35)
        MUSIC_ARROW_R = Button(image=pygame.image.load("assets/strzałka.png"), pos=(1050, 320),
                                text_input=None, font=get_font(43), base_color="#674a29", hovering_color="White",
                                scale=0.35)
        MUSIC_ARROW_L.update(SCREEN)
        MUSIC_ARROW_R.update(SCREEN)

        # Przyciski strzałek do regulacji głośności
        VOLUME_ARROW_L = Button(image=pygame.image.load("assets/strzałka2.png"), pos=(750, 420),
                                 text_input=None, font=get_font(43), base_color="#674a29", hovering_color="White",
                                 scale=0.35)
        VOLUME_ARROW_R = Button(image=pygame.image.load("assets/strzałka.png"), pos=(1050, 420),
                                 text_input=None, font=get_font(43), base_color="#674a29", hovering_color="White",
                                 scale=0.35)
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

