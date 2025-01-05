import pygame
from utils import message_box


class GameRenderer:
    """
    Klasa odpowiedzialna za rysowanie stanu gry na ekranie.
    Obsługuje renderowanie tła, kart i tekstów w trakcie gry.
    """

    def __init__(self, screen, assets, font):
        self.screen = screen
        self.assets = assets
        self.font = font

    def draw_state(self, game_round, state, action_text):
        """
        Rysuje bieżący stan gry, w tym tło, karty graczy i tekst akcji.
        Args:
            cur_player (Player): Bieżący gracz (człowiek lub bot).
            state (dict): Stan gry, zawierający ręce graczy i stosy kart.
            state = {
                "hand1": [],
                "hand2": [],
                "hand3": [],
                "hand4": [],
                "face_down_pile": [],
                "face_up_pile": []
                }
            action_text (str): Tekst opisujący akcję wykonywaną przez gracza.

        Returns:
            None
        Przykład użycia:
            game_renderer.draw_state(cur_player, state, "Wybierz ze stosu odkrytego", round_number)
        """
        self.screen.blit(self.assets["background"], (0, 0))
        player_type = "gracza" if game_round.player_type == "human" else "bota"
        message_box(self.screen, f"Tura {player_type} {str(game_round.player_number)}: {action_text}",
                    self.font, "black", "white",
                    x=0.74 * self.screen.get_width(),
                    y=0.028 * self.screen.get_height())
        # for cards in [state["hand1"], state["hand2"], state["hand3"], state["hand4"],
        #              state["face_down_pile"], state["face_up_pile"]]:
        #     for card in cards:

        if state["face_down_pile"]:
            face_down_hand = [state["face_down_pile"][-1]]
        else:
            face_down_hand = []

        if state["face_up_pile"]:
            face_up_hand = [state["face_up_pile"][-1]]
        else:
            face_up_hand = []

        for hand in [state["hand1"], state["hand2"], state["hand3"], state["hand4"],
                     face_down_hand, face_up_hand]:
            for card in hand:
                card.draw(self.screen)
        pygame.display.flip()