import pygame

def wake_up_screen(screen, players):
    # "przycisk"
    print("hello from wakey")
    screen_width, screen_height = screen.get_size()
    button_img = pygame.image.load("../assets/przycisk.png").convert_alpha()
    button_width, button_height = 800, 800
    button_img = pygame.transform.scale(button_img, (button_width, button_height))
    button_x = (screen_width - button_width) // 2
    button_y = (screen_height - button_height) // 2
    font = pygame.font.Font("../assets/Berylium/Berylium.ttf", 50)
    screen.blit(button_img, (button_x, button_y))

    # Nagłówek
    header_text = "Aktualne punkty"
    header_surface = font.render(header_text, True, (255, 255, 255))  # White color
    header_x = button_x + (button_width - header_surface.get_width()) // 2
    header_y = button_y
    screen.blit(header_surface, (header_x, header_y))

    # Dolny tekst
    bottom_text = "Kliknij, aby kontynuować"
    bottom_surface = font.render(bottom_text, True, (255, 255, 255))
    bottom_x = button_x + (button_width - bottom_surface.get_width()) // 2
    bottom_y = button_y + button_height - bottom_surface.get_height() - 10  # 20 px margines od dołu
    screen.blit(bottom_surface, (bottom_x, bottom_y))

    # Tabelka wyników
    row_height = 150
    for i, player in enumerate(players):
        row_text = f"Gracz {player.player_number} | {player.crows}"
        row_surface = font.render(row_text, True, (138, 99, 58))  # White color

        row_x = button_x + (button_width - row_surface.get_width()) // 2
        row_y = header_y + (i + 1) * row_height
        screen.blit(row_surface, (row_x, row_y))

    pygame.display.flip()

    # czekanie na input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def end_screen(screen, players, winner):
    #"przycisk"
    screen_width, screen_height = screen.get_size()
    button_img = pygame.image.load("../assets/przycisk.png").convert_alpha()
    button_width, button_height = 800, 800
    button_img = pygame.transform.scale(button_img, (button_width, button_height))
    button_x = (screen_width - button_width) // 2
    button_y = (screen_height - button_height) // 2
    font = pygame.font.Font("../assets/Berylium/Berylium.ttf", 50)
    screen.blit(button_img, (button_x, button_y))

    #Nagłówek
    header_text = "Wygrałeś!" if winner == "player1" else "Przegrałeś"
    header_surface = font.render(header_text, True, (255, 255, 255))  # White color

    header_x = button_x + (button_width - header_surface.get_width()) // 2
    header_y = button_y
    screen.blit(header_surface, (header_x, header_y))

    #Tabelka wyników
    row_height = 150
    for i, player in enumerate(players):

        row_text = f"Gracz {player.player_number} | {player.crows}"
        row_surface = font.render(row_text, True, (138, 99, 58))  # White color

        row_x = button_x + (button_width - row_surface.get_width()) // 2
        row_y = header_y + (i + 1) * row_height
        screen.blit(row_surface, (row_x, row_y))

    pygame.display.flip()

    #czekanie na koniec gry
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False