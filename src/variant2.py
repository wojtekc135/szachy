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

#Bardzo szybki wariant przez to jak działa liczenie kruków
def idz_na_calosc(screen):
    variant = 2
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
                pass
                game_round.human_show_2_cards(state[cur_hand], game_renderer, game_round, state)
            else:
                pass
                game_round.bot_show_2_cards(state[cur_hand], game_renderer, game_round, state)

        elif game_round.round_number > 4:
            if game_round.player_type == "human":
                game_round.human_turn_variant2(state, game_round, game_renderer, screen, players)
            else:
                pass
                game_round.bot_turn_variant2(state, game_round, game_renderer)

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


    pygame.quit()


idz_na_calosc(screen)
