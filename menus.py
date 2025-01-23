import pygame


def main_menu(surface):
    play_img = pygame.image.load("./data/play.png")
    quit_img = pygame.image.load("./data/quit.png")
    about_img = pygame.image.load("./data/about.png")

    # Remove white background (set colorkey)
    play_img.set_colorkey((255, 255, 255))  # Removes white background
    quit_img.set_colorkey((255, 255, 255))  # Removes white background
    about_img.set_colorkey((255, 255, 255))  # Removes white background

    # Calculate total height of all buttons plus spacing
    button_height = play_img.get_height()  # All buttons have the same height
    spacing = 20  # Space between buttons
    total_height = (button_height * 3) + (spacing * 2)  # 3 buttons, 2 spaces

    # Calculate starting positions for centering
    screen_width, screen_height = surface.get_size()
    start_x = (screen_width - play_img.get_width()) // 2
    start_y = (screen_height - total_height) // 2

    # Define button positions and rects
    play_rect = play_img.get_rect(topleft=(start_x, start_y))
    quit_rect = quit_img.get_rect(topleft=(start_x, start_y + button_height + spacing))
    about_rect = about_img.get_rect(
        topleft=(start_x, start_y + 2 * (button_height + spacing))
    )

    # Draw buttons on the surface
    surface.blit(play_img, play_rect.topleft + play_img.get_width())
    surface.blit(quit_img, quit_rect.topleft + play_img.get_width())
    surface.blit(about_img, about_rect.topleft + play_img.get_width())

    # Return the rects for handling clicks
    return play_rect, quit_rect, about_rect
