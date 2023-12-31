import re
from time import perf_counter

import pygame
from core.imageloader import ImageLoader
from core.spritesheets import SpriteSheet
from objects.player import PLAYER_SPRITESHEETS

import core.sound

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = "#FFCE00"
RED = "#FF0000"


def credits_screen(screen: pygame.Surface, bg: pygame.Surface):
    # Liste des chaînes de caractères à afficher avec des espacements
    credits_list = [
        "Il etait une fois un robot...".upper(),
        "Qui dans un monde ou les humains, apres avoir conquis le systeme solaire,".upper(),
        "ont disparu suite a une crise ecologique inter-planetaire".upper(),
        "et ou les robots se retrouvent seuls dans un monde pollue par les dechets".upper(),
        "trouve une solution frolant le genie.".upper(),
        "Consistant a passer le systeme solaire dans une machine a laver geante".upper(),
        "elle impressionne la NIGG (Nation Inter-Galactique Generale)".upper(),
        "qui accepta immediatement le projet.".upper(),
        "Malheureusement toutes les planetes du systeme solaire retrecirent au lavage !".upper(),
        "Le systeme solaire devenu inhabitable,".upper(),
        "une guerre civile dechirat la civilisation des robots".upper(),
        "qui pour ahiniler leurs opposants".upper(),
        "utilisaient des pistolets a trou noir leur permettant de devenir maitres de la gravite.".upper(),
        "",
        "CREDITS",
        "THANKS TO WUBS FOR HIS SICK PIXEL ART GUN GENERATOR",
        "HUGE THANKS TO DEEP FOLD FOR HIS AMAZING PLANET AND SPACE BACKGROUND GENERATOR",
        "S/O DAVID HARRINGTON FOR HIS CUTE ANIMATED ROBOT SPRITE",
        "HONORABLE MENTION TO ROBTOP FOR THE GEOMETRY DASH FONT CURRENTLY BEING DISPLAYED",
        "",
        "GAME DESIGN: GASPARD CULIS",
        "NETWORKING: TIMOTHE TABOADA",
        "SOUND DESIGN: HIPPOLYTE CHAUVIN",
        "UI DESIGN: NOHA BOUTEMEUR"
    ]

    # Police de texte
    police = pygame.font.Font("./assets/font/geom.TTF", 36)

    # Positions de départ pour afficher les crédits
    y_positions = [screen.get_height() + 200.0 * i for i in range(len(credits_list))]

    # État du jeu
    running = True

    t0 = perf_counter()
    while running:
        delta = perf_counter() - t0
        t0 = perf_counter()
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
                y_positions[i] -= 90*delta  # Réglez la vitesse de défilement ici

        if all(y <= -200 for y in y_positions):
            # Toutes les chaînes de caractères ont été affichées, revenir au home screen
            running = False

        pygame.display.flip()


def home_screen(screen: pygame.Surface, bg: pygame.Surface) -> tuple[str, int, str, int] | str:
    """
    Returns either a tuple of:
    - ip: str
    - port: int
    - username: str
    - avatar_index: int
    Or a status text such as:
    - "quit"
    """
    # Police de texte
    police = pygame.font.Font("./assets/font/geom.TTF", 36)
    titlePolice = pygame.font.Font("./assets/font/geom.TTF", 75)

    pygame.display.set_caption('Home Screen')

    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 60
    SPACE_BETWEEN = 350
    SPACE_BETWEEN_Y = 200

    # Boutons
    start_button = pygame.Rect(screen.get_width() / 2 - BUTTON_WIDTH / 2 - SPACE_BETWEEN, screen.get_height() / 2 - SPACE_BETWEEN_Y,
                               BUTTON_WIDTH, BUTTON_HEIGHT)
    credits_button = pygame.Rect(screen.get_width() / 2 - BUTTON_WIDTH / 2, screen.get_height() / 2 - SPACE_BETWEEN_Y, BUTTON_WIDTH,
                                 BUTTON_HEIGHT)
    quit_button = pygame.Rect(screen.get_width() / 2 - BUTTON_WIDTH / 2 + SPACE_BETWEEN, screen.get_height() / 2 - SPACE_BETWEEN_Y,
                              BUTTON_WIDTH, BUTTON_HEIGHT)

    # Entrées pour l'IP et le port
    ip_text = "0.0.0.0"
    port_text = "6942"
    name_text = ""
    selected_player_index = 0
    IP_WIDTH = 300
    PORT_WIDTH = 150
    NAME_WIDTH = 500
    ip_rect = pygame.Rect(screen.get_width() / 2 - IP_WIDTH / 2 - SPACE_BETWEEN, screen.get_height() / 2, IP_WIDTH, 40)
    port_rect = pygame.Rect(screen.get_width() / 2 - PORT_WIDTH / 2, screen.get_height() / 2, PORT_WIDTH, 40)
    name_rect = pygame.Rect(screen.get_width() / 2 - IP_WIDTH / 2 + SPACE_BETWEEN, screen.get_height() / 2, IP_WIDTH, 40)
    active_rect = None  # Zone de texte active (IP, port ou name)

    PLAYER_PREVIEW_SIZE = 48 * 3
    PLAYER_PREVIEW_COUNT = len(PLAYER_SPRITESHEETS)
    player_selection_rect = pygame.Rect(
        screen.get_width() / 2 - (PLAYER_PREVIEW_SIZE + 12) * PLAYER_PREVIEW_COUNT / 2,
        screen.get_height() / 2 + SPACE_BETWEEN_Y, 
        (PLAYER_PREVIEW_SIZE + 12) * PLAYER_PREVIEW_COUNT,
        PLAYER_PREVIEW_SIZE + 12
    )

    player_preview_images = list(map(
        lambda x: SpriteSheet(
            x.idle.spritesheet_path,
            x.idle.rows,
            x.idle.cols,
            x.idle.frame_delay,
            x.idle.frame_count,
            pygame.Vector2(PLAYER_PREVIEW_SIZE)
        ),
        PLAYER_SPRITESHEETS
    ))

    player_preview_rects = [
        pygame.Rect(
            screen.get_width() / 2 + (a - PLAYER_PREVIEW_COUNT/2) * (PLAYER_PREVIEW_SIZE + 12) + 6,
            screen.get_height() / 2 + SPACE_BETWEEN_Y, 
            PLAYER_PREVIEW_SIZE, 
            PLAYER_PREVIEW_SIZE
        ) for a in range(PLAYER_PREVIEW_COUNT)
    ]


    error_text = ""

    core.sound.Sound.get().loop_music('title_screen')

    # État du jeu
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    core.sound.Sound.get().play('button')
                    print("Clic sur Start")
                    # Vérifier l'adresse IP avec une expression régulière
                    ip_pattern = r'(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}'
                    if re.match(ip_pattern, ip_text) and port_text.isdigit():
                        error_text = ""
                        screen.blit(bg, (0, 0))  # Dessinez l'image de fond en haut à gauche (0, 0)
                        text_title = titlePolice.render("LOADING...", True, YELLOW)
                        screen.blit(text_title, (screen.get_width() / 2 - text_title.get_width() / 2, 150))
                        pygame.display.flip()
                        return ip_text, int(port_text), name_text, selected_player_index
                        # Ajoutez ici le code pour lancer le jeu
                    else:
                        print("Adresse IP ou port incorrects")
                        error_text = "ADRESSE IP OU PORT INCORRECTS"

                    # Ajoutez ici le code pour lancer le jeu
                elif credits_button.collidepoint(event.pos):
                    core.sound.Sound.get().play('button')
                    print("Clic sur Credit")
                    credits_screen(screen, bg)
                    # Ajoutez ici le code pour les credits du jeu
                elif quit_button.collidepoint(event.pos):
                    core.sound.Sound.get().play('button')
                    running = False
                    return "quit"
                elif ip_rect.collidepoint(event.pos):
                    active_rect = ip_rect
                elif port_rect.collidepoint(event.pos):
                    active_rect = port_rect
                elif name_rect.collidepoint(event.pos):
                    active_rect = name_rect
                else:
                    active_rect = None
                    # Mabe clicked on a player selector
                    for i in range(len(player_preview_rects)):
                        if player_preview_rects[i].collidepoint(event.pos):
                            selected_player_index = i
            if event.type == pygame.KEYDOWN:
                if active_rect:
                    if event.key == pygame.K_BACKSPACE:
                        if active_rect == ip_rect:
                            ip_text = ip_text[:-1]
                        elif active_rect == port_rect:
                            port_text = port_text[:-1]
                        elif active_rect == name_rect:
                            name_text = name_text[:-1]
                    else:
                        if active_rect == ip_rect:
                            if ip_rect.w > IP_WIDTH + 20:
                                ip_text += event.unicode

                        elif active_rect == port_rect:
                            if port_rect.w > PORT_WIDTH + 25:
                                port_text += event.unicode
                        elif active_rect == name_rect:
                            if name_rect.w > NAME_WIDTH + 25:
                                name_text += event.unicode.upper()

        screen.fill(WHITE)

        # Dessinez l'arrière-plan
        screen.blit(bg, (0, 0))  # Dessinez l'image de fond en haut à gauche (0, 0)

        # Afficher les rect simples
        pygame.draw.rect(screen, WHITE, player_selection_rect, 2)
        pygame.draw.rect(screen, WHITE, player_preview_rects[selected_player_index].move(pygame.Vector2(0, 6)), 2)

        # Player previews
        for i, r in zip(player_preview_images, player_preview_rects):
            screen.blit(i.get_frame(), r)

        # Dessiner les boutons
        pygame.draw.rect(screen, WHITE, start_button, 2)
        pygame.draw.rect(screen, WHITE, credits_button, 2)
        pygame.draw.rect(screen, WHITE, quit_button, 2)

        # Afficher le texte des boutons
        text_start = police.render("START", True, WHITE)
        text_credits = police.render("CREDITS", True, WHITE)
        text_quit = police.render("QUIT", True, WHITE)
        text_title = titlePolice.render("ROBOT RUMBLE", True, YELLOW)

        screen.blit(text_start, (start_button.x + start_button.width / 2 - text_start.get_width() / 2,
                                 start_button.y + start_button.height / 2 - text_start.get_height() / 2))
        screen.blit(text_credits, (credits_button.x + credits_button.width / 2 - text_credits.get_width() / 2,
                                   credits_button.y + credits_button.height / 2 - text_credits.get_height() / 2))
        screen.blit(text_quit, (quit_button.x + quit_button.width / 2 - text_quit.get_width() / 2,
                                quit_button.y + quit_button.height / 2 - text_quit.get_height() / 2))
        screen.blit(text_title, (screen.get_width() / 2 - 300, 150))

        if error_text != "":
            text_error = police.render(error_text, True, RED)
            screen.blit(text_error, (screen.get_width() / 2 - text_error.get_width() / 2, ip_rect.y + 100))

        # Afficher les entrées pour l'IP et le port
        pygame.draw.rect(screen, WHITE, ip_rect, 2)
        pygame.draw.rect(screen, WHITE, port_rect, 2)
        pygame.draw.rect(screen, WHITE, name_rect, 2)

        # Afficher le texte de l'IP et du port
        title_ip = police.render("ADRESSE IP", True, WHITE)
        title_port = police.render("PORT", True, WHITE)
        title_name = police.render("NAME", True, WHITE)

        text_ip = police.render(ip_text, True, WHITE)
        text_port = police.render(port_text, True, WHITE)
        text_name = police.render(name_text, True, WHITE)

        IP_WIDTH = text_ip.get_width()
        PORT_WIDTH = text_port.get_width()
        NAME_WIDTH = text_name.get_width()

        screen.blit(title_ip, (ip_rect.x + 5, ip_rect.y - 50))
        screen.blit(title_port, (port_rect.x + 5, port_rect.y - 50))
        screen.blit(title_name, (name_rect.x + 5, name_rect.y - 50))
        screen.blit(text_ip, (ip_rect.x + 5, ip_rect.y + 5))
        screen.blit(text_port, (port_rect.x + 5, port_rect.y + 5))
        screen.blit(text_name, (name_rect.x + 5, name_rect.y + 5))

        pygame.display.flip()

    # Quitter Pygame
    # pygame.quit()
