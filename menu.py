#ustawić tło do ustawień, dodać w ustawieniach napisy dźwięk, rozdzielczość, ekran OK
#ogarnąć działanie ekranu (fullscreen, windowed) OK

import pygame
import sys
import webbrowser
from button import Button
import os

pygame.init()

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

def get_font(size):  # Zwraca czcionkę o określonym rozmiarze
    return pygame.font.Font("assets/Berylium/Berylium.ttf", size)

def get_title(size):
    return pygame.font.Font("assets/ringbearer/RINGM___.TTF", size)

def main_menu():
    while True:
        SCREEN.blit(BG_SCALED, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_title(170).render("Sen", True, "#8a6539")
        MENU_RECT = MENU_TEXT.get_rect(center=(200, 120))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/przycisk.png"), pos=(200, 290),
                             text_input="Graj", font=get_font(43), base_color="#674a29", hovering_color="White", scale=2)
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/przycisk.png"), pos=(200, 440),
                                text_input="Ustawienia", font=get_font(43), base_color="#674a29", hovering_color="White", scale=2)
        RULES_BUTTON = Button(image=pygame.image.load("assets/przycisk.png"), pos=(200, 590),
                              text_input="Zasady Gry", font=get_font(43), base_color="#674a29", hovering_color="White", scale=2)
        QUIT_BUTTON = Button(image=pygame.image.load("assets/przycisk.png"), pos=(200, 740),
                             text_input="Wyjście", font=get_font(43), base_color="#674a29", hovering_color="White", scale=2)

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

        pygame.display.update()

def open_rules():
    # Funkcja otwierająca stronę z zasadami gry
    url = "https://gry.nk.com.pl/wp-content/uploads/2022/03/SEN-instrukcja.pdf"
    webbrowser.open(url)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green", scale=1)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def options():
    global SCREEN, fullscreen  # Zmienna globalna dla okna gry i trybu fullscreen
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(OP_SCALED, (0, 0))

        # Napisy na ustawienia dźwięku, rozdzielczości, ekranu
        OPTIONS_DZW = get_font(43).render("Dźwięk", True, "#674a29")
        OPTIONS_ROZ = get_font(43).render("Rozdzielczość", True, "#674a29")
        OPTIONS_EKR = get_font(43).render("Ekran", True, "#674a29")

        OPTIONS_RECT_D = OPTIONS_DZW.get_rect(center=(620, 200))
        OPTIONS_RECT_R = OPTIONS_ROZ.get_rect(center=(620, 350))
        OPTIONS_RECT_E = OPTIONS_EKR.get_rect(center=(620, 500))

        SCREEN.blit(OPTIONS_DZW, OPTIONS_RECT_D)
        SCREEN.blit(OPTIONS_ROZ, OPTIONS_RECT_R)
        SCREEN.blit(OPTIONS_EKR, OPTIONS_RECT_E)

        # Napisy z informacją o trybie ekranu:
        if fullscreen:
            screen_mode_text = get_font(43).render("Pełny ekran", True, "#674a29")
        else:
            screen_mode_text = get_font(43).render("Okno", True, "#674a29")
        screen_mode_rect = screen_mode_text.get_rect(center=(875, 500))
        SCREEN.blit(screen_mode_text, screen_mode_rect)

        # Przycisk back:
        OPTIONS_BACK = Button(image=None, pos=(620, 650),
                              text_input="Powrót", font=get_font(43), base_color="#674a29", hovering_color="White", scale=1)
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        # Przyciski strzałek do zmiany trybu ekranu:
        OPTIONS_ARROW_L = Button(image=pygame.image.load("assets/strzałka2.png"), pos=(750, 500),
                                  text_input=None, font=get_font(43), base_color="#674a29", hovering_color="White", scale=0.35)
        OPTIONS_ARROW_R = Button(image=pygame.image.load("assets/strzałka.png"), pos=(1000, 500),
                                  text_input=None, font=get_font(43), base_color="#674a29", hovering_color="White", scale=0.35)
        OPTIONS_ARROW_L.update(SCREEN)
        OPTIONS_ARROW_R.update(SCREEN)

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTIONS_ARROW_L.checkForInput(OPTIONS_MOUSE_POS) or OPTIONS_ARROW_R.checkForInput(OPTIONS_MOUSE_POS):
                    fullscreen = not fullscreen
                    if fullscreen:
                        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    else:
                        SCREEN = pygame.display.set_mode((SCREEN_WIDTH - 10, SCREEN_HEIGHT - 50)) # Okno mniejsze

        pygame.display.update()

main_menu()

