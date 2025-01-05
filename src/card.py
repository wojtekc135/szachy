import pygame
from utils import message_box

pygame.init()


class Card:
    def __init__(self, screen, front_image, back_image, known_for_player, show_front, location, location_number,
                 highlighted, selected_info, card_size, id):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.front_image = front_image
        self.back_image = back_image
        self.card_size = card_size
        self.show_front = show_front
        self.image = front_image if show_front else back_image

        self.highlighted = highlighted
        self.known_for_player = known_for_player
        self.location = location
        self.location_number = location_number
        self.selected_info = selected_info
        self.id = id

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
        if self.location_number == 5:
            return h13_centerx, self.screen_height - h13_centery - 3 * self.card_size[0]
        if self.location_number == 6:
            return h13_centerx + 3 * (self.card_size[0] + gap_12), self.screen_height - h13_centery - 3 * self.card_size[0]
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
        """Tworzy prostokąt obramowujący kartę, uwzględniając highlight."""
        rect = self.image.get_rect(topleft=(base_x + offset_x, base_y + offset_y))
        if self.highlighted:
            rect = rect.inflate(20, 20)
            rect.move_ip(0, -10)
        return rect

    def check_click(self, mouse_pos, event):
        if self.rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            return True

    def display_message_under_card(self, screen, text, font=pygame.font.SysFont("Arial", 24), color="black",
                                   rect_color="white", padding=10):
        "Przykład card.selected_info = 'wybrano' wtedy karta bedzie miała informacje pod sobą inaczej trzeba dać False"
        rect_x = self.rect.centerx - (font.size(text)[0] + 2 * padding) / 2 + 1  # poprawic
        rect_y = self.rect.centery - (font.size(text)[1] + 2 * padding) + 0.5 * self.card_size[1] + 45
        message_box(screen, text, font, color, rect_color, rect_x, rect_y, padding)

    def draw(self, screen):
        self.update_position()
        screen.blit(self.image, self.rect)
        if self.selected_info != False:
            self.display_message_under_card(screen, self.selected_info)