import pygame
#from Tools.scripts.generate_opcode_h import header

from game_render import GameRenderer
from round import Round
import os
from utils import load_assets, scale_assets, get_card_size
from player import Player
#from points_screen import wake_up_screen, end_screen
#from boty import Bot

game_round = Round(1, "human", 1)
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.SysFont("../assets/Berylium/Berylium.tft", 24)
card_size = get_card_size(screen_height)
assets = load_assets(os.path.join(os.pardir, "assets"), "karta", "stół", "rewers")
assets = scale_assets(assets, card_size, (screen_width, screen_height))
state = game_round.create_example_state(screen, assets, card_size, "variant2")

def variant1(screen):
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
                    if card.crows == 9:
                        player.ninecrows += 1
                print("Gracz: ",player.player_number," punkty: ", player.crows, "9 kruków: ", player.ninecrows)
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
            winner = "player1!" if player1.ninecrows == max(player.ninecrows for player in players) else "Nie ty"
            end_screen(screen, players, winner)
            running = False
        elif wake_up:
            wake_up_screen(screen, players)
        wake_up = False

    pygame.quit()


variant1(screen)
