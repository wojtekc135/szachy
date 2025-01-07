import pygame
#from Tools.scripts.generate_opcode_h import header

from game_render import GameRenderer
from round import Round
import os
from utils import load_assets, scale_assets, get_card_size
from player import Player

game_round = Round(1, "human", 1)
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.SysFont("arial", 24)
card_size = get_card_size(screen_height)
assets = load_assets(os.path.join(os.pardir, "assets"), "karta", "stół", "rewers")
assets = scale_assets(assets, card_size, (screen_width, screen_height))
state = game_round.create_example_state(screen, assets, card_size, "variant2")

def wake_up_screen(screen, players):
    # "przycisk"
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

def end_screen(screen, players, winner):
    #"przycisk"
    screen_width, screen_height = screen.get_size()
    button_img = pygame.image.load("../assets/przycisk.png").convert_alpha()
    button_width, button_height = 800, 800
    button_img = pygame.transform.scale(button_img, (button_width, button_height))
    button_x = (screen_width - button_width) // 2
    button_y = (screen_height - button_height) // 2
    font = pygame.font.Font("../assets/Berylium/Berylium.ttf", 50)
    screen.blit(button_img, (button_x, button_y))

    #Nagłówek
    header_text = "Wygrałeś!" if winner == "player1" else "Przegrałeś"
    header_surface = font.render(header_text, True, (255, 255, 255))  # White color

    header_x = button_x + (button_width - header_surface.get_width()) // 2
    header_y = button_y
    screen.blit(header_surface, (header_x, header_y))

    #Tabelka wyników
    row_height = 150
    for i, player in enumerate(players):

        row_text = f"Gracz {player.player_number} | {player.crows}"
        row_surface = font.render(row_text, True, (138, 99, 58))  # White color

        row_x = button_x + (button_width - row_surface.get_width()) // 2
        row_y = header_y + (i + 1) * row_height
        screen.blit(row_surface, (row_x, row_y))

    pygame.display.flip()

    #czekanie na koniec gry
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


#Bardzo szybki wariant przez to jak działa liczenie kruków
def idz_na_calosc(screen):
    pygame.init()

    player1 = Player(True,1)
    player2 = Player(True, 2)
    player3 = Player(True, 3)
    player4 = Player(True, 4)
    players = [player1, player2, player3, player4]

    end_game = False
    game_round.debug(state)
    game_renderer = GameRenderer(screen, assets, font)
    wake_up = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        cur_hand = "hand" + str(game_round.player_number)

        if game_round.round_number <= 4:
            if game_round.player_type == "human":
                game_round.human_show_2_cards(state[cur_hand], game_renderer, game_round, state)
            else:
                game_round.bot_show_2_cards(state[cur_hand], game_renderer, game_round, state)

        elif game_round.round_number > 4:
            if game_round.player_type == "human":
                wake_up = game_round.wake_up_option(state, game_renderer, game_round, screen)
                if(not wake_up):
                    game_round.human_take_card_from_any_pile(state, game_round, game_renderer)
            else:
                game_round.bot_take_card_from_any_pile(state, game_round, game_renderer)

        #pobudka
        if wake_up:
            waker = player1 #tylko gracz może budzić (najwyżej potem można zmeinic)
            for player in players:
                cur_hand = "hand" + str(player.player_number)
                hand_counting = state[cur_hand]
                for card in hand_counting:
                    if card.crows != 9:
                        player.crows += 50
                        if player.crows >= 100: end_game = True  # warunek zakończenia gry
                        break
                print("Gracz: ",player.player_number," punkty: ", player.crows)
                #jesteśmy hojni i jak dwaj gracze mają tylko karty z 9 krukami to niech oboje sobie nic dodają :)


        # aktualizacja rundy
        game_round.round_number += 1
        if game_round.round_number % 4 == 1:
            game_round.player_type = "human"
        else:
            game_round.player_type = "bot"
        if game_round.round_number % 4 == 0:
            game_round.player_number = 4
        else:
            game_round.player_number = game_round.round_number % 4
        pygame.time.wait(200)

        if end_game:
            winner ="player1!" if player1.crows <100 else "Nie ty"
            winner = str(player1)
            end_screen(screen, players, winner)
            running = False
        elif wake_up:
            wake_up_screen(screen, players)
        wake_up = False

    pygame.quit()


idz_na_calosc(screen)
