import pygame
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, scale=1):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.scale = scale  # Skalowanie przycisku

        # Jeśli obrazek jest podany, skaluj go
        if self.image is not None:
            width = self.image.get_width()
            height = self.image.get_height()
            self.image = pygame.transform.scale(self.image, (int(width * self.scale), int(height * self.scale)))

        # Tworzenie tekstu
        self.text = self.font.render(self.text_input, True, self.base_color)

        # Jeśli obrazek jest None, używamy tylko tekstu
        if self.image is None:
            self.image = self.text

        # Przygotowanie prostokąta dla obrazu i tekstu
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        # Rysowanie przycisku na ekranie
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        # Sprawdzanie, czy kliknięto w przycisk
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        # Zmiana koloru tekstu przy najechaniu myszką
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
