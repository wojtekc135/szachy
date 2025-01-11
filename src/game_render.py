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
        # font.render(text, True, pygame.Color(color)).get_size()[0] * 0.5
        self.screen.blit(self.assets["background"], (0, 0))
        player_type = "gracza" if game_round.player_type == "human" else "bota"
        text = f"Tura {player_type} {str(game_round.player_number)}: {action_text}"
        font = pygame.font.SysFont("arial", 24)
        message_box(self.screen, text,
                    self.font, "black", "white",
                    x=0.5 * self.screen.get_width() - 0.5 * font.render(text, True, pygame.Color("black")).get_size()[
                        0],
                    y=0.0 * self.screen.get_height())

        if state["face_down_pile"]:
            face_down_hand = [state["face_down_pile"][-1]]
        else:
            face_down_hand = []

        if state["face_up_pile"]:
            face_up_hand = [state["face_up_pile"][-1]]
        else:
            face_up_hand = []
        for state_type in [state["hand_temp"], state["hand1"], state["hand2"], state["hand3"], state["hand4"],
                           face_down_hand, face_up_hand, state["button_Użyj karty"],
                           state["button_Nie używaj umiejętności"],
                           state["button_Co robi?"], state["button_Pobudka"]]:
            for object in state_type:
                object.draw(self.screen)
        pygame.display.flip()
    def draw_text_at_bottom(self, text):
        text_surface = self.font.render(text, True, (255, 255, 255))  # Biały tekst
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 20))  # Na dole
        self.screen.blit(text_surface, text_rect)