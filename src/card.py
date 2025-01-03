import pygame
from utils import message_box


class Card:
    def __init__(self, screen, front_image, back_image, show_front, location, location_number, highlighted, card_size):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.front_image = front_image
        self.back_image = back_image
        self.card_size = card_size
        self.show_front = show_front
        self.image = front_image if show_front else back_image
        self.highlighted = highlighted
        self.location = location
        self.location_number = location_number

    def update_position(self):
        """Aktualizuje pozycję karty w zależności od jej lokalizacji i stanu."""
        self.update_image()
        base_x, base_y = self.calculate_base_position()
        offset_x, offset_y = self.calculate_offset()
        self.rect = self.get_updated_rect(base_x, base_y, offset_x, offset_y)

    def update_image(self):
        """Aktualizuje obraz karty w zależności od stanu (awers/rewers) i orientacji."""
        if self.location in ("hand2", "hand4"):
            self.image = pygame.transform.rotate(
                self.front_image if self.show_front else self.back_image,
                90 if self.location == "hand2" else -90
            )
        else:
            self.image = self.front_image if self.show_front else self.back_image

    def calculate_base_position(self):
        """Oblicza podstawową pozycję karty w zależności od jej lokalizacji."""
        gap = 1.5
        gap_12 = self.card_size[0] * 0.5
        hand_length = gap * self.card_size[0] * 3 + self.card_size[0]
        h13_centerx = (self.screen_width - hand_length) / 2
        h13_centery = ((self.screen_height - self.card_size[1]) * 0.1) / 2
        if self.location == "hand1":
            return h13_centerx, self.screen_height - h13_centery - self.card_size[1]
        elif self.location == "hand2":
            return h13_centerx - self.card_size[1] - gap_12, 0.9 * self.screen_height - self.card_size[0]
        elif self.location == "hand3":
            return h13_centerx, h13_centery
        elif self.location == "hand4":
            return h13_centerx + hand_length + gap_12, 0.1 * self.screen_height
        elif self.location == "face_down_pile":
            return self.screen_width / 2 - self.card_size[0] * gap / 2 - self.card_size[0] * 0.5, \
                   self.screen_height / 2 - self.card_size[1] * 0.5
        elif self.location == "face_up_pile":
            return self.screen_width / 2 + self.card_size[0] * gap / 2 - self.card_size[0] * 0.5, \
                   self.screen_height / 2 - self.card_size[1] * 0.5
        else:
            return 0, 0

    def calculate_offset(self):
        """Oblicza przesunięcie karty w zależności od jej numeru w lokalizacji."""
        gap = 1.5
        if self.location in ("hand1", "hand3"):
            return gap * self.card_size[0] * self.location_number, 0
        elif self.location in ("hand2", "hand4"):
            return 0, (-gap if self.location == "hand2" else gap) * self.card_size[0] * self.location_number
        return 0, 0

    def get_updated_rect(self, base_x, base_y, offset_x, offset_y):
        """Tworzy prostokąt obramowujący kartę."""
        rect = self.image.get_rect(topleft=(base_x + offset_x, base_y + offset_y))
        if self.highlighted:
            rect = rect.inflate(20, 20)
            rect.move_ip(0, -10)
        return rect

    def draw(self, screen):
        self.update_position()
        screen.blit(self.image, self.rect)
