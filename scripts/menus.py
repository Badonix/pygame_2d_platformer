import pygame


def main_menu(surface):
    # Load button images
    play_img = pygame.image.load("./data/play.png")
    quit_img = pygame.image.load("./data/quit.png")
    about_img = pygame.image.load("./data/about.png")

    # Resize images (e.g., to 100x50 pixels)
    new_size = (100, 50)  # Change this to your desired size
    play_img = pygame.transform.scale(play_img, new_size)
    quit_img = pygame.transform.scale(quit_img, new_size)
    about_img = pygame.transform.scale(about_img, new_size)

    # Remove white background (set colorkey)
    play_img.set_colorkey((255, 255, 255))  # Removes white background
    quit_img.set_colorkey((255, 255, 255))  # Removes white background
    about_img.set_colorkey((255, 255, 255))  # Removes white background

    # Alternatively, if your images have alpha transparency, use convert_alpha()
    # play_img = pygame.image.load('./data/play.png').convert_alpha()
    # quit_img = pygame.image.load('./data/quit.png').convert_alpha()
    # about_img = pygame.image.load('./data/about.png').convert_alpha()

    # Calculate total height of all buttons plus spacing
    button_height = (
        play_img.get_height()
    )  # All buttons have the same height after resizing
    spacing = 20  # Space between buttons
    total_height = (button_height * 3) + (
        spacing * 2
    )  # 3 buttons, 2 spaces between them

    # Calculate starting y-position to center the buttons vertically
    screen_height = surface.get_height()
    start_y = (screen_height - total_height) // 2

    # Define button positions and rects
    play_rect = play_img.get_rect(topleft=(30, start_y))
    quit_rect = quit_img.get_rect(topleft=(30, start_y + button_height + spacing))
    about_rect = about_img.get_rect(
        topleft=(30, start_y + 2 * (button_height + spacing))
    )

    # Draw buttons on the surface
    surface.blit(play_img, play_rect.topleft)
    surface.blit(quit_img, quit_rect.topleft)
    surface.blit(about_img, about_rect.topleft)

    # Return the rects for handling clicks (optional)
    return play_rect, quit_rect, about_rect
