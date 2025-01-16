import pygame
import random
from game_render import GameRenderer
from round import Round
import os
from utils import load_assets, scale_assets, get_card_size
from player import Player
from boty import Bot

# Inicjalizacja gry
pygame.init()
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
img = pygame.image.load('../assets/design.png')
pygame.display.set_icon(img)

def variant1(screen):
    # Tworzenie graczy
    player1 = Player(True, 1)
    player2 = Player(True, 2)
    player3 = Player(True, 3)
    player4 = Player(True, 4)
    players = [player1, player2, player3, player4]

    # Tworzenie bota
    bot = Bot()
    initial_cards = [random.randint(1, 9) for _ in range(4)]
    bot.start_game(initial_cards)

    end_game = False
    wake_up = False
    running = True

    game_renderer = GameRenderer(screen, assets, font)
    game_round.debug(state)

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
                if not wake_up:
                    game_round.human_take_card_from_any_pile(state, game_round, game_renderer)
            else:
                # Logika tury bota
                top_discard = state["discard_pile"][-1] if state["discard_pile"] else None
                draw_pile_top = random.randint(1, 9)  # Symulacja wierzchniej karty zakrytego stosu
                special_action_available = True  # Jeśli akcje specjalne są dostępne

                decision = bot.take_turn(top_discard, draw_pile_top, special_action_available)

                if decision[0] == "replace":
                    _, index, new_card = decision
                    state["discard_pile"].append(bot.dream[index])
                    bot.dream[index] = new_card
                elif decision[0] == "special":
                    print(f"{bot.name} używa akcji specjalnej!")
                    # Tutaj implementujesz specjalną akcję bota
                elif decision[0] == "pobudka":
                    print(f"{bot.name} ogłasza POBUDKA!")
                    wake_up = True
                elif decision[0] == "pass":
                    print(f"{bot.name} nie wykonuje akcji.")

        # Pobudka i zakończenie rundy
        if wake_up:
            waker = player1  # Tylko gracz może budzić (możesz zmienić później)
            for player in players:
                cur_hand = "hand" + str(player.player_number)
                hand_counting = state[cur_hand]
                for card in hand_counting:
                    if card.crows == 9:
                        player.ninecrows += 1
                print("Gracz:", player.player_number, "punkty:", player.crows, "9 kruków:", player.ninecrows)

        # Aktualizacja rundy
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
            # end_screen(screen, players, winner)  # Zaimplementuj, jeśli używasz tej funkcji
            running = False
        elif wake_up:
            # wake_up_screen(screen, players)  # Zaimplementuj, jeśli używasz tej funkcji
            pass
        wake_up = False

    pygame.quit()

variant1(screen)
