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
                "temp_hand": [],
                "hand1": [],
                "hand2": [],
                "hand3": [],
                "hand4": [],
                "face_down_pile": [],
                "face_up_pile": []
                "action_buttons": []
                }
            action_text (str): Tekst opisujący akcję wykonywaną przez gracza.

        Returns:
            None
        Przykład użycia:
            game_renderer.draw_state(game_round, state, "Wybierz ze stosu odkrytego")
        """
        #font.render(text, True, pygame.Color(color)).get_size()[0] * 0.5
        self.screen.blit(self.assets["background"], (0, 0))
        player_type = "gracza" if game_round.player_type == "human" else "bota"
        text = f"Tura {player_type} {str(game_round.player_number)}: {action_text}"
        font = pygame.font.SysFont("arial", 24)
        message_box(self.screen, text,
                    self.font, "black", "white",
                    x=0.5 * self.screen.get_width() - 0.5*font.render(text, True, pygame.Color("black")).get_size()[0],
                    y=0.0 * self.screen.get_height())

        # state["face_down_pile"][-1] wyświetlanie tylko ostatnich kart z stosów
        # żeby nie bybło problemu jak stos pusty
        if state["face_down_pile"]:
            face_down_hand = [state["face_down_pile"][-1]]
        else:
            face_down_hand = []

        if state["face_up_pile"]:
            face_up_hand = [state["face_up_pile"][-1]]
        else:
            face_up_hand = []

        for state_type in [state["temp_hand"], state["hand1"], state["hand2"], state["hand3"], state["hand4"],
                     face_down_hand, face_up_hand, state["action_buttons"]]:
            for object in state_type:
                object.draw(self.screen)
        pygame.display.flip()
