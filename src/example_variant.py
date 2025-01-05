import pygame
from game_render import GameRenderer
from src.round import Round
import os
from utils import load_assets, scale_assets, get_card_size

game_round = Round(1, "human", 1)
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.SysFont("arial", 24)
card_size = get_card_size(screen_height)
assets = load_assets(os.path.join(os.pardir, "assets"), "karta", "stół", "rewers")
assets = scale_assets(assets, card_size, (screen_width, screen_height))
state = game_round.create_example_state(screen, assets, card_size)


def example_variant(screen):
    pygame.init()
    game_round.debug(state)
    game_renderer = GameRenderer(screen, assets, font)
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
                game_round.human_take_bottom_card_from_any_pile(state, game_round, game_renderer)
            else:
                game_round.human_take_bottom_card_from_any_pile(state, game_round, game_renderer)

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


example_variant(screen)
