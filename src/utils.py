import os
import pygame


def load_assets(folder, card_prefix, background_prefix, card_back_prefix):
    """
    Ładuje zasoby gry (karty, tło, rewers kart) z folderu.
    Args:
        folder (str): Ścieżka do folderu z zasobami.
        card_prefix (str): Prefiks dla plików kart.
        background_prefix (str): Prefiks dla plików tła.
        card_back_prefix (str): Prefiks dla plików rewersu kart.
    Returns:
        dict: Zasoby gry (karty, tło, rewers kart) w postaci słownika:
            - "cards": Lista załadowanych kart.
            - "background": Załadowane tło.
            - "card_back": Załadowany rewers kart.
    Example:
        assets = load_assets(os.path.join(os.pardir, "assets"), "karta", "stół", "rewers")
    """
    assets = {"cards": [], "background": "", "card_back": ""}
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            path = os.path.join(folder, filename)
            if filename.startswith(card_prefix):
                assets["cards"].append(pygame.image.load(path))
            elif filename.startswith(background_prefix):
                assets["background"] = pygame.image.load(path)
            elif filename.startswith(card_back_prefix):
                assets["card_back"] = pygame.image.load(path)
    return assets


def scale_assets(assets, card_size, background_size):
    """
    Skaluje zasoby gry (karty, tło, rewers kart) do określonych rozmiarów.
    Args:
        assets (dict): Słownik z załadowanymi zasobami (karty, tło, rewers kart).
        card_size (tuple): Rozmiar kart (szerokość, wysokość).
        background_size (tuple): Rozmiar tła (szerokość, wysokość).
    Returns:
        dict: Przeskalowane zasoby gry w postaci słownika:
            - "cards": Lista przeskalowanych kart.
            - "background": Przeskalowane tło.
            - "card_back": Przeskalowany rewers kart.
    Example:
        assets = scale_assets(assets, card_size, (screen_width, screen_height))
    """
    scaled_background = pygame.transform.scale(assets["background"], background_size)
    scaled_cards = [pygame.transform.scale(card, card_size) for card in assets["cards"]]
    scaled_card_back = pygame.transform.scale(assets["card_back"], card_size)
    return {"cards": scaled_cards, "background": scaled_background, "card_back": scaled_card_back}


def get_card_size(screen_height, card_scale=5, card_aspect_ratio=1080 / 1520):
    """
        Oblicza rozmiar karty na podstawie wysokości ekranu.
        Args:
            screen_height (int): Wysokość ekranu.
            card_scale (int, optional): Współczynnik skali karty, karta będzie 5 razy mniejsza od screen_height (domyślnie 5).
            card_aspect_ratio (float, optional): Proporcje karty w folderze assets (domyślnie 1080 / 1520).
        Returns:
            tuple: Rozmiar karty (szerokość, wysokość).
        Example:
            card_size = get_card_size(screen_height)
        """
    card_size = [((screen_height / card_scale) * card_aspect_ratio), (screen_height / card_scale)]
    return card_size


def message_box(screen, text, font, color, rect_color, x, y, padding=10):
    """
    Rysuje prostokąt z wycentrowanym tekstem w zadanej lokalizacji na ekranie.
    Args:
        screen (Surface): Ekran Pygame, na którym ma być rysowany tekst.
        text (str): Tekst do wyświetlenia.
        font (Font): Czcionka używana do renderowania tekstu.
        color (str): Kolor tekstu.
        rect_color (str): Kolor tła prostokąta.
        x (int): Współrzędna x lewego górnego rogu prostokąta.
        y (int): Współrzędna y lewego górnego rogu prostokąta.
        padding (int, opcjonalnie): Odstęp między tekstem a krawędziami prostokąta. Domyślnie 10.
    Returns:
        None
    """
    text_surface = font.render(text, True, pygame.Color(color))
    text_width, text_height = text_surface.get_size()
    # Calculate the rectangle dimensions
    rect_width = text_width + 2 * padding
    rect_height = text_height + 2 * padding
    rect_x = x
    rect_y = y
    pygame.draw.rect(screen, pygame.Color(rect_color), (rect_x, rect_y, rect_width, rect_height))
    screen.blit(text_surface, (rect_x + padding, rect_y + padding))
