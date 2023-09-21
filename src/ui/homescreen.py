import pygame
from pygame import Surface
import re

from core.sound import Sound

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = "#FFCE00"
RED = "#FF0000"

def credits_screen(screen: Surface):
    # Liste des chaînes de caractères à afficher avec des espacements
    credits_list = [
        "CREDIT 1",
        "CREDIT 2",
        "CREDIT 3",
    ]

    bg = pygame.image.load("./assets/img/space_bg_1.png")
    bg = pygame.transform.scale(bg,screen.get_size())


    # Police de texte
    police = pygame.font.Font("./assets/font/geom.TTF", 36)

    # Positions de départ pour afficher les crédits
    y_positions = [screen.get_height() + 200 * i for i in range(len(credits_list))]

    # État du jeu
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.blit(bg, (0, 0))

        # Afficher toutes les chaînes de caractères simultanément
        for i, credit in enumerate(credits_list):
            if y_positions[i] >= -200:  # Attendre que l'espacement soit atteint
                text_credit = police.render(credit, True, WHITE)
                text_rect = text_credit.get_rect(center=(screen.get_width() / 2, y_positions[i]))
                screen.blit(text_credit, text_rect)

                # Déplacer le texte vers le haut
                y_positions[i] -= 2  # Réglez la vitesse de défilement ici

        if all(y <= -200 for y in y_positions):
            # Toutes les chaînes de caractères ont été affichées, revenir au home screen
            running = False

        pygame.display.flip()

def home_screen(screen: Surface) -> tuple[str, int] | str:
    # Police de texte
    police = pygame.font.Font("./assets/font/geom.TTF", 36)
    titlePolice = pygame.font.Font("./assets/font/geom.TTF", 75)


    pygame.display.set_caption('Home Screen')

    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 60
    SPACE_BETWEEN = 300
    bg = pygame.image.load("./assets/img/backgrounds/space_bg_1.png")

    bg = pygame.transform.scale(bg,screen.get_size())

    # Boutons
    start_button = pygame.Rect(screen.get_width()/2-BUTTON_WIDTH/2-SPACE_BETWEEN, screen.get_height()/2-25, BUTTON_WIDTH, BUTTON_HEIGHT)
    credits_button = pygame.Rect(screen.get_width()/2-BUTTON_WIDTH/2, screen.get_height()/2-25, BUTTON_WIDTH, BUTTON_HEIGHT)
    quit_button = pygame.Rect(screen.get_width()/2-BUTTON_WIDTH/2+SPACE_BETWEEN, screen.get_height()/2-25, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Entrées pour l'IP et le port
    ip_text = "0.0.0.0"
    port_text = "6942"
    IP_WIDTH = 300
    PORT_WIDTH = 150
    ip_rect = pygame.Rect(screen.get_width()/2-300, screen.get_height()/2+200, IP_WIDTH, 40)
    port_rect = pygame.Rect(screen.get_width()/2+100, screen.get_height()/2+200, PORT_WIDTH, 40)
    active_rect = None  # Zone de texte active (IP ou port)

    error_text = ""

    Sound.get().loop_music('title_screen')

    # État du jeu
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    print("Clic sur Start")
                    # Vérifier l'adresse IP avec une expression régulière
                    ip_pattern = r'(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}'
                    if re.match(ip_pattern, ip_text) and port_text.isdigit():
                        error_text = ""
                        return ip_text, int(port_text)
                        # Ajoutez ici le code pour lancer le jeu
                    else:
                        print("Adresse IP ou port incorrects")
                        error_text = "ADRESSE IP OU PORT INCORRECTS"

                    # Ajoutez ici le code pour lancer le jeu
                elif credits_button.collidepoint(event.pos):
                    print("Clic sur Credit")
                    credits_screen(screen)
                    # Ajoutez ici le code pour les credits du jeu
                elif quit_button.collidepoint(event.pos):
                    running = False
                    return "quit"
                elif ip_rect.collidepoint(event.pos):
                    active_rect = ip_rect
                elif port_rect.collidepoint(event.pos):
                    active_rect = port_rect
                else:
                    active_rect = None
            if event.type == pygame.KEYDOWN:
                if active_rect:
                    if event.key == pygame.K_BACKSPACE:
                        if active_rect == ip_rect:
                            ip_text = ip_text[:-1]
                        elif active_rect == port_rect:
                            port_text = port_text[:-1]
                    else:
                        if active_rect == ip_rect:
                            if ip_rect.w > IP_WIDTH+20:
                                ip_text += event.unicode

                        elif active_rect == port_rect:
                            if port_rect.w > PORT_WIDTH+25:
                                port_text += event.unicode

        screen.fill(WHITE)

        # Dessinez l'arrière-plan
        screen.blit(bg, (0, 0))  # Dessinez l'image de fond en haut à gauche (0, 0)



        # Dessiner les boutons
        pygame.draw.rect(screen, WHITE, start_button, 2)
        pygame.draw.rect(screen, WHITE, credits_button, 2)
        pygame.draw.rect(screen, WHITE, quit_button, 2)

        # Afficher le texte des boutons
        text_start = police.render("START", True, WHITE)
        text_credits = police.render("CREDITS", True, WHITE)
        text_quit = police.render("QUIT", True, WHITE)
        text_title = titlePolice.render("ROBOT RUMBLE", True, YELLOW)

        screen.blit(text_start, (start_button.x + start_button.width/2 - text_start.get_width()/2, start_button.y + start_button.height/2 - text_start.get_height()/2))
        screen.blit(text_credits, (credits_button.x + credits_button.width/2 - text_credits.get_width()/2, credits_button.y + credits_button.height/2 - text_credits.get_height()/2))
        screen.blit(text_quit, (quit_button.x + quit_button.width/2 - text_quit.get_width()/2, quit_button.y + quit_button.height/2 - text_quit.get_height()/2))
        screen.blit(text_title, (screen.get_width()/2-300,150))

        if error_text != "":
            text_error = police.render(error_text, True, RED)
            screen.blit(text_error, (screen.get_width()/2-text_error.get_width()/2, ip_rect.y+100))

        # Afficher les entrées pour l'IP et le port
        pygame.draw.rect(screen, WHITE, ip_rect, 2)
        pygame.draw.rect(screen, WHITE, port_rect, 2)

        # Afficher le texte de l'IP et du port
        title_ip = police.render("ADRESSE IP", True, WHITE)
        title_port = police.render("PORT", True, WHITE)

        text_ip = police.render(ip_text, True, WHITE)
        text_port = police.render(port_text, True, WHITE)

        IP_WIDTH = text_ip.get_width()
        PORT_WIDTH = text_port.get_width()

        screen.blit(title_ip, (ip_rect.x + 5, ip_rect.y - 50))
        screen.blit(title_port, (port_rect.x + 5, port_rect.y - 50))
        screen.blit(text_ip, (ip_rect.x + 5, ip_rect.y + 5))
        screen.blit(text_port, (port_rect.x + 5, port_rect.y + 5))

        pygame.display.flip()

    # Quitter Pygame
    #pygame.quit()
