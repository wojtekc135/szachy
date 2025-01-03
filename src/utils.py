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