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

    def draw_state(self, cur_player, state, action_text):
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
        player_type = "gracza" if cur_player.isHuman == "human" else "bota"
        message_box(self.screen, f"Tura {player_type} {cur_player.player_number}: {action_text}",
                    self.font, "black", "white",
                    x=0.74 * self.screen.get_width(),
                    y=0.028 * self.screen.get_height())
        if state["face_down_pile"]:
            face_down_hand = [state["face_down_pile"][-1]]
        else:
            face_down_hand = None

        if state["face_down_pile"]:
            face_up_hand = [state["face_up_pile"][-1]]
        else:
            face_up_hand = None

        for hand in [state["hand1"], state["hand2"], state["hand3"], state["hand4"],
                     face_down_hand, face_up_hand]:
            for card in hand:
                card.draw(self.screen)
                if card.clicked:
                    pygame.draw.rect(self.screen, (255, 0, 0), card.rect.inflate(10, 10), width=4, border_radius=10)

        pygame.display.flip()
