import pygame
from pygame import Surface
from pygame.key import ScancodeWrapper
import re

def home_screen(screen: Surface) -> (str, int):
    # Couleurs
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = "#FFCE00"
    RED = "#FF0000"
    # Police de texte
    police = pygame.font.Font("./assets/font/geom.TTF", 36)
    titlePolice = pygame.font.Font("./assets/font/geom.TTF", 75)


    pygame.display.set_caption('Home Screen')

    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 60
    SPACE_BETWEEN = 300
    bg = pygame.image.load("./assets/img/space_bg.png")

    bg = pygame.transform.scale(bg,screen.get_size())

    # Boutons
    start_button = pygame.Rect(screen.get_width()/2-BUTTON_WIDTH/2-SPACE_BETWEEN, screen.get_height()/2-25, BUTTON_WIDTH, BUTTON_HEIGHT)
    option_button = pygame.Rect(screen.get_width()/2-BUTTON_WIDTH/2, screen.get_height()/2-25, BUTTON_WIDTH, BUTTON_HEIGHT)
    quit_button = pygame.Rect(screen.get_width()/2-BUTTON_WIDTH/2+SPACE_BETWEEN, screen.get_height()/2-25, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Entrées pour l'IP et le port
    ip_text = ""
    port_text = ""
    IP_WIDTH = 250
    PORT_WIDTH = 150
    ip_rect = pygame.Rect(screen.get_width()/2-300, screen.get_height()/2+200, IP_WIDTH, 40)
    port_rect = pygame.Rect(screen.get_width()/2+100, screen.get_height()/2+200, PORT_WIDTH, 40)
    active_rect = None  # Zone de texte active (IP ou port)

    error_text = ""



    # État du jeu
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
                elif option_button.collidepoint(event.pos):
                    print("Clic sur Option")
                    # Ajoutez ici le code pour les options du jeu
                elif quit_button.collidepoint(event.pos):
                    running = False
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
        pygame.draw.rect(screen, WHITE, option_button, 2)
        pygame.draw.rect(screen, WHITE, quit_button, 2)

        # Afficher le texte des boutons
        text_start = police.render("START", True, WHITE)
        text_option = police.render("OPTION", True, WHITE)
        text_quit = police.render("QUIT", True, WHITE)
        text_title = titlePolice.render("ROBOT RUMBLE", True, YELLOW)

        screen.blit(text_start, (start_button.x + start_button.width/2 - text_start.get_width()/2, start_button.y + start_button.height/2 - text_start.get_height()/2))
        screen.blit(text_option, (option_button.x + option_button.width/2 - text_option.get_width()/2, option_button.y + option_button.height/2 - text_option.get_height()/2))
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
    pygame.quit()