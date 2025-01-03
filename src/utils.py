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
