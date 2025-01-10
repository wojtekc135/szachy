import pygame
class ActionButton:
    # na szybko
    def __init__(self, x, y, location, bg_image, show, font = pygame.font.Font("../assets/Berylium/Berylium.ttf", 50 ), height=50, text_color=(138, 99, 58)):
        self.location = location
        self.font = font
        self.text_color = text_color
        self.show = show

        # Renderowanie tekstu i obliczanie szerokości przycisku na podstawie tekstu
        self.text_surface = font.render(location, True, text_color)
        text_width = self.text_surface.get_width()
        self.width = text_width + 20  # Dodanie marginesów po 10 pikseli z każdej strony
        self.height = height

        # Skalowanie obrazu tła
        self.image = pygame.transform.scale(bg_image, (self.width, self.height))

        # Ustawianie prostokąta przycisku
        self.rect = self.image.get_rect(topleft=(x, y))

        # Pozycja tekstu wewnątrz przycisku
        self.text_position = (
            self.rect.x + (self.width - text_width) // 2,
            self.rect.y + (self.height - self.text_surface.get_height()) // 2
        )

    def draw(self, screen):
        if self.show == True:
            screen.blit(self.image, self.rect.topleft)
            screen.blit(self.text_surface, self.text_position)
            pygame.display.flip()

    def check_click(self, mouse_pos, event): # ta metoda musi byc identyczna jak check click z klasy card zeby input handler dobrze dzialal
        if self.rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
            return True