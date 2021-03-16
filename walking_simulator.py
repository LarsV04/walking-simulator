import sys
import random
import pygame
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
# import een paar dingen

# maakt variabelen voor de resolutie en een paar kleuren
size = screen_width, screen_height = 1600, 900
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
yellow = 255, 255, 0

# paar algemene variabelen
max_progress = 1000000
max_fps = 60
all_confetti = []
program_frame = 0
fps = 0

# variabelen voor random events
event_object = []
event_active = -1

bullets = []

# maakt een scherm met de resolutie width en height
screen = pygame.display.set_mode(size)

# laad een font
text_font = pygame.font.Font("./dogica.ttf", 30)

# zorgt voor een icon en titel van het programma
pygame.display.set_caption("Walking Simulator")
icon = pygame.image.load("./images/player/walk1.png").convert_alpha()
pygame.display.set_icon(icon)

# CLASSES
# maakt de player class
class character:
    def __init__(self, y_pos):
        self.x = 0
        self.y = y_pos
        self.x_movement = 0
        self.y_movement = 0
        self.sprint = 100
        self.shield = 60
        self.shielding = False
        self.progress = 0
        self.width = 14
        self.height = 42
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.run_frame = 0
        self.run_speed = 1000  # normaal is 10
        self.jump_height = 16
        self.alive = True
        self.gun_cooldown = 120
        self.shoot = False
        self.stand_still = 0
        self.sprites = [pygame.image.load("./images/player/walk1.png").convert_alpha(),
                        pygame.image.load("./images/player/walk2.png").convert_alpha(),
                        pygame.image.load("./images/player/walk3.png").convert_alpha(),
                        pygame.image.load("./images/player/walk4.png").convert_alpha()]
        self.event_sprites =    [pygame.image.load("./images/player/player_shield.png").convert_alpha(),
                                 pygame.image.load("./images/player/player_pjew1.png").convert_alpha(),
                                 pygame.image.load("./images/player/player_pjew2.png").convert_alpha()]

    # maakt een functie om alle sprites goed te maken
    def load_sprites(self):
        for i in range(0, 4):
            # maakt de sprites de goede grootte
            self.sprites[i] = pygame.transform.scale(self.sprites[i], (self.width*2, self.height))

            # maakt de flipped versies van de elke sprite
            self.sprites.append(pygame.transform.flip(self.sprites[i], True, False))

        for i in range(0, 3):
            self.event_sprites[i] = pygame.transform.scale(self.event_sprites[i], (self.width*2, self.height))

# maakt classes voor de maps
class desert:
    spawn_height = 770
    hitbox = [(0, 770, screen_width, 50)]
    bg = pygame.image.load("./images/map_bgs/desert.png").convert()
    bg = pygame.transform.scale(bg, (screen_width, screen_height))

class mountain:
    spawn_height  = 570
    hitbox = [(0, 290, 150, 80), (150, 350, 100, 50), (250, 380, 90, 50),
              (340, 410, 90, 50), (430, 430, 30, 50), (460, 460, 10, 50),
              (470, 490, 30, 50), (500, 510, 10, 50), (510, 530, 30, 50),
              (540, 540, 40, 50), (580, 560, 60, 50), (640, 570, 40, 50),
              (680, 590, 50, 50), (730, 620, 20, 50), (750, 660, 30, 50),
              (780, 670, 10, 50), (790, 680, 240, 50), (1030, 670, 20, 50),
              (1050, 660, 40, 50), (1090, 640, 50, 50), (1140, 630, 50, 50),
              (1190, 600, 70, 50), (1260, 590, 90, 50), (1350, 570, 250, 50)]
    bg = pygame.image.load("./images/map_bgs/mountain.png").convert()
    bg = pygame.transform.scale(bg, (screen_width, screen_height))

class tabletop:
    spawn_height = 570
    hitbox = [(0, 570, 410, 100), (410, 520, 30, 70), (440, 490, 70, 50),
              (510, 450, 90, 50), (600, 470, 100, 60), (700, 450, 50, 70),
              (750, 500, 60, 50), (810, 530, 30, 60), (840, 570, 190, 100),
              (1030, 530, 170, 60), (1200, 570, 160, 100), (1360, 530, 20, 60),
              (1380, 500, 60, 50), (1440, 530, 10, 60), (1450, 570, 150, 100)]
    bg = pygame.image.load("./images/map_bgs/tabletop.png").convert()
    bg = pygame.transform.scale(bg, (screen_width, screen_height))

class crystal:
    spawn_height = 630
    hitbox = [(0, 690, 30, 30), (30, 680, 40, 30), (70, 670, 40, 30),
              (110, 660, 40, 30), (150, 650, 40, 30), (190, 640, 40, 30),
              (230, 630, 40, 30), (270, 620, 40, 30), (310, 610, 40, 30),
              (350, 600, 40, 30), (390, 590, 40, 30), (430, 600, 20, 30),
              (450, 610, 20, 30), (470, 620, 20, 30), (490, 630, 20, 30),
              (510, 640, 20, 30), (530, 650, 20, 30), (550, 660, 20, 30),
              (570, 670, 20, 30), (590, 680, 20, 30), (610, 690, 20, 30),
              (630, 700, 20, 30), (650, 710, 20, 30), (670, 720, 20, 30),
              (690, 730, 20, 30), (710, 740, 20, 30), (730, 730, 20, 30),
              (750, 720, 20, 30), (770, 710, 20, 30), (790, 700, 20, 30),
              (810, 690, 20, 30), (830, 680, 20, 30), (850, 670, 20, 30),
              (870, 660, 20, 30), (890, 650, 20, 30), (910, 640, 20, 30),
              (930, 630, 50, 30), (980, 620, 50, 30), (1030, 610, 50, 30),
              (1080, 600, 50, 30), (1130, 590, 50, 30), (1180, 580, 50, 30),
              (1230, 570, 50, 30), (1280, 560, 50, 30), (1330, 550, 50, 30),
              (1380, 540, 50, 30), (1430, 530, 30, 30), (1460, 540, 10, 30),
              (1470, 550, 10, 30), (1480, 560, 10, 30), (1490, 570, 10, 30),
              (1500, 580, 10, 30), (1510, 590, 10, 30), (1520, 600, 10, 30),
              (1530, 610, 10, 30), (1540, 620, 10, 30), (1550, 630, 10, 30),
              (1560, 640, 10, 30), (1570, 650, 10, 30), (1580, 660, 10, 30),
              (1590, 670, 10, 30)]
    bg = pygame.image.load("./images/map_bgs/crystal.png").convert()
    bg = pygame.transform.scale(bg, (screen_width, screen_height))

# maakt de class voor confetti :)
class confetti:
    def __init__(self):
        self.x = random.randrange(0, screen_width, 10)
        self.y = 0
        self.move_y = random.randrange(5, 10, 1)
        self.move_x = random.randrange(-10, 10, 1)
        self.color = (random.randrange(1, 255, 1), random.randrange(
            1, 255, 1), random.randrange(1, 255, 1))

#class voor de bird random event
class birb:
    def __init__(self, x_val, y_val):
        self.x = x_val
        self.y = y_val-20
        self.width = 60
        self.height = 40
        self.frame = 0
        self.x_movement = random.randrange(2, 8, 2)
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.sprites = [pygame.image.load("./images/bird_event/birb1.png").convert_alpha(),
                        pygame.image.load("./images/bird_event/birb2.png").convert_alpha()]

# class voor de ninja zelf van het ninja event
class ninja:
    def __init__(self, min_y):
        self.x = 1550
        self.y = min_y
        self.width = 40
        self.height = 60
        self.frame = -66
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.sprites = [pygame.image.load("./images/ninja_event/ninja1.png").convert_alpha(),
                        pygame.image.load("./images/ninja_event/ninja2.png").convert_alpha(),
                        pygame.image.load("./images/ninja_event/ninja3.png").convert_alpha(),
                        pygame.image.load("./images/ninja_event/ninja4.png").convert_alpha(),
                        pygame.image.load("./images/ninja_event/ninja5.png").convert_alpha(),
                        pygame.image.load("./images/ninja_event/ninja6.png").convert_alpha(),
                        pygame.image.load("./images/ninja_event/ninja7.png").convert_alpha(),
                        pygame.image.load("./images/ninja_event/ninja8.png").convert_alpha(),
                        pygame.image.load("./images/ninja_event/ninja8.png").convert_alpha()]
        self.smoke = pygame.image.load("./images/ninja_event/smoke.png").convert_alpha()

    def spawn_smoke(self, alpha):
        # zorgt voor de alpha
        self.smoke.set_alpha(alpha)

        # scaled de smoke
        self.smoke = pygame.transform.scale(self.smoke, (34, 34))

        # plaatst smoke op de goede plekken
        screen.blit(self.smoke, (self.x-6, self.y+5))
        screen.blit(self.smoke, (self.x-6, self.y+32))
        screen.blit(self.smoke, (self.x+5, self.y+18))


# class voor de sterren die de ninja gooit gooit
class ninja_star:
    def __init__(self, x_val, y_val, move_y):
        self.x = x_val
        self.y = y_val
        self.y_movement = move_y
        self.x_movement = 15
        self.width = 20
        self.height = 20
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.sprites = [pygame.image.load("./images/ninja_event/shuriken1.png").convert_alpha(),
                        pygame.image.load("./images/ninja_event/shuriken2.png").convert_alpha()]

# class voor de bandiet
class bandit:
    def __init__(self, y_val):
        self.x = 1550
        self.y = y_val
        self.width = 36
        self.height = 60
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.frame = 0
        self.sprites = [pygame.image.load("./images/bandit_event/bandit1.png").convert_alpha(),
                        pygame.image.load("./images/bandit_event/bandit2.png").convert_alpha(),
                        pygame.image.load("./images/bandit_event/bandit3.png").convert_alpha(),
                        pygame.image.load("./images/bandit_event/bandit4.png").convert_alpha(),
                        pygame.image.load("./images/bandit_event/bandit5.png").convert_alpha(),
                        pygame.image.load("./images/bandit_event/bandit6.png").convert_alpha(),
                        pygame.image.load("./images/bandit_event/bandit7.png").convert_alpha(),
                        pygame.image.load("./images/bandit_event/bandit8.png").convert_alpha(),
                        pygame.image.load("./images/bandit_event/bandit9.png").convert_alpha(),
                        pygame.image.load("./images/bandit_event/bandit10.png").convert_alpha()
                        ]

# class voor bullets
class bullet:
    def __init__(self, x_val, y_val, side_multiplier):
        self.x = x_val
        self.y = y_val
        self.x_movement = 160
        self.side = side_multiplier
        self.sprite = pygame.image.load("./images/bandit_event/bullet.png").convert_alpha()

    # zorgt ervoor dat de bullets bewegen en een texture krijgen
    def check_bullet(self):
        self.x += self.x_movement * self.side
        self.sprite = pygame.transform.scale(self.sprite, (45, 45))
        screen.blit(self.sprite, (self.x, self.y))

# COLLISION
# checkt of de player collide met de y-waarde van de grond
def ground_col_y(hitbox_a, hitbox_b):
    # voor elke ground hitbox
    for i in hitbox_b:
        # als de player tussen de grondhitboxes zit
        if hitbox_a[0]+hitbox_a[2] > i[0] and hitbox_a[0] < i[0]+i[2]:
            # berekent het verschil van de het y-midden van de speler en van het object
            difference = i[1]-(hitbox_a[1]+hitbox_a[3])

            # als het verschil kleiner is dan de afstanden van de twee middens naar de zijkanten weet je dat die collide
            if difference <= 0:
                # returnt true en het verschil zodat de player weer boven de grond gehaald kan worden
                return True, difference

    # anders returnt die false met het verschil
    return False, difference

# checkt of de player collide met de x-waarde van de grond
def ground_col_x(hitbox_a, hitbox_b):
    # voor hitbox in de map hitbox variabele
    for i in hitbox_b:
        # berekent het verschil tussen de 2 x-middelpunten van de player en de grond
        difference = i[0]+(i[2]/2)-(hitbox_a[0]+(hitbox_a[2]/2))

        # als het verschil kleiner is dan de afstand vanaf het middelpunt
        #  tot de muur van beide dan weet je dat ze colliden
        if abs(difference) < (i[2]/2)+(hitbox_a[2]/2) and hitbox_a[1]+hitbox_a[3] > i[1]:
            # difference/abs(difference) geeft ook terug aan welke kan t van de muur de player zit, returnt dan -1 of 1
            return True, difference/abs(difference)
    # als niks collide retur false
    return False, 0

# checkt of de player collide met andere hitboxes
def check_collision(hitbox_a, hitbox_b):
    # berekent 2 middens in de 2 hitboxes
    a_middle = hitbox_a[0]+(hitbox_a[2]/2), hitbox_a[1]+(hitbox_a[3]/2)
    b_middle = hitbox_b[0]+(hitbox_b[2]/2), hitbox_b[1]+(hitbox_b[3]/2)

    # telt voor beide assen de afstand naar de zeikant bij elkaar op
    min_x_diff = (a_middle[0]-hitbox_a[0]) + (b_middle[0]-hitbox_b[0])
    min_y_diff = (a_middle[1]-hitbox_a[1]) + (b_middle[1]-hitbox_b[1])

    # als de afstand voor de middens van die as kleiner is dan de minimale afstand die hierboven werd berekent word de variabele true
    coll_x = abs(a_middle[0]-b_middle[0]) < min_x_diff
    coll_y = abs(a_middle[1]-b_middle[1]) < min_y_diff

    # returnt true als beide true zijn, anders false
    return coll_x and coll_y

# MOVEMENT
# berekent hoe ver je loopt omdat het steeds minder word, hoeveel verder je komt
def movement(movement, progress):
    # eerst maakt het een multiplier van 1
    multiplier = 1

    # voor 10% werkt de formule tegenstrijdig dus daarom doen we het pas na de eerste 10%
    if progress > max_progress / 10:
        multiplier = (max_progress/(progress*10))

    # returnt de nieuwe movement
    return multiplier * movement

# returnt hoeveel de player beweegt, en de positie van de player
def move_player(player, ground, framerate):
    # maakt voor elke frame weer de movement 0, zo moet je de knop ingedrukt houden
    player.x_movement = 0

    # Hetzelfde voor shielding
    player.shielding = False

    # voor verschillende knoppen zorgt die dat de movement aangepast word
    if keys[pygame.K_s] and player.shield > 2:
        player.shield -= 3
        player.shielding = True
        player.x_movement = 0
    elif keys[pygame.K_d]:
        player.x_movement = player.run_speed
    # progress moet groter zijn dan de run speed want anders loop je links van het scherm af
    elif keys[pygame.K_a] and player.progress > player.run_speed*2:
        player.x_movement = -2*player.run_speed
    # hetzelfde als bij de vorige
    elif player.progress > player.run_speed/5:
        player.x_movement = player.run_speed/-5

    if not keys[pygame.K_s] and player.shield < 60:
        player.shield += .5

    # roept de grond x-collide functie aan
    coll_x, x_multiplier = ground_col_x(player.hitbox, ground.hitbox)

    # als die collide, dan zorgt die ervoor dat de movement die frame weer 0 word
    if coll_x:
        player.x_movement -= abs(player.x_movement)*x_multiplier

    # veranderd de x_movement zodat het klopt met de framerate
    if framerate > 0:
        player.x_movement *= max_fps/framerate

    # keymods hebben allemaal waardes, maar alleen left-shift heeft een oneven waarde, daarom als je de rest neemt
    # en je drukt left-shift in krijg je een oneven waarde, hierdoor kan je alle andere keymods (alt, shift, ctrl) ook in drukken
    if keymod % 2 == 1 and not keys[pygame.K_s]:
        # zolang je genoeg kan sprinten, gaat er van je sprint meter af en word je snelheid keer 2 gedaan
        if player.sprint >= 3:
            player.sprint -= 3
            player.x_movement *= 2
        # als die op is dan word je speed verlaagd
        else:
            player.x_movement *= 0.85
    # en zodra je de sprint key los laat recharged je sprint meter maar je speed word nog steeds verlaagd
    elif player.sprint < 100:
        player.sprint += 0.05
        player.x_movement *= 0.85

    # ja het sprinten is uiteindelijk trager dan niet sprinten :)

    # roept de functie y-collision aan
    coll_y, height_diff = ground_col_y(player.hitbox, ground.hitbox)

    # als je collide
    if coll_y:
        # en je drukt op spatie dan spring je
        if keys[pygame.K_SPACE] and not keys[pygame.K_s]:
            player.y_movement = player.jump_height
        # anders word je op de grond gezet als je collide
        elif player.y_movement < 0:
            player.y_movement = 0
            player.y += height_diff

    # als je niet collide dan krijg je een valversnelling van 1 per seconde
    else:
        player.y_movement -= .9

    # past de y-waarde van de player aan door naar de y-movement te kijken
    player.y -= player.y_movement

    # checkt of de speler ctrl indrukt om te schieten
    if 63 < keymod < 67 and player.gun_cooldown >= 60 and player.stand_still == 0 and not player.shielding:
        player.shoot = True
        player.gun_cooldown -= 60
        player.stand_still = 18
    # als de gun cooldown kleiner is dan 120 blijft die de gun_cooldown erbij doen zodat je later weer kan schieten
    elif player.gun_cooldown < 120:
        player.gun_cooldown += .5
        player.shoot = False

    # voor de eerste 18 frames van de cooldown sta je stil
    if player.stand_still > 0:
        player.x_movement = 0
        player.stand_still -= 1


    # de progress word berekent door de functie movement()
    player.progress += movement(player.x_movement, player.progress)

    # en de player x-waarde word berekend en aangepast
    player.x = (player.progress/max_progress)*screen_width

    # de hitbox word ook aangepast naar de nieuwe coordinaten
    player.hitbox = (player.x, player.y, player.width, player.height)

    return player


# DISPLAYING
# voor test purposes :)
def display_hitboxes(ground):
    # voor elke ground hitbox maakt die een rectangle
    for i in ground.hitbox:
        pygame.draw.rect(screen, black, i, 2)

# Laat de player zien op het scherm
def display_player(player, frame):
    # maakt een hitbox rectangle voor testen
    # pygame.draw.rect(screen, green, player.hitbox, 1)

    # kiest de goede sprite voor als die naar links of rechts gaat
    if player.x_movement > 0:
        screen.blit(
            player.sprites[frame], (player.hitbox[0]-player.hitbox[2]/2, player.hitbox[1]))
    elif player.x_movement < 0:
        screen.blit(player.sprites[frame+4], (player.hitbox[0]-player.hitbox[2]/2, player.hitbox[1]))
    # voor de startpositie heb je geen movement dus moest deze nog toevoegen
    elif player.stand_still == 0:
        screen.blit(player.sprites[0], (player.x-player.width/2, player.y))

    if player.shielding:
        # makes a surface for the shield
        shield_surface = pygame.Surface((50,50), pygame.SRCALPHA, 32)
        pygame.draw.circle(shield_surface, (0, 64, 255), (25,25), 25, 3)
        pygame.draw.circle(shield_surface, (0, 128, 255, 128), (25,25), 24)

        # maakt de player shield animatie
        player_center = (int(player.x + player.width / 2), int(player.y + player.height / 2))
        screen.blit(player.event_sprites[0], (player.x-player.width/2, player.y))
        screen.blit(shield_surface, (player_center[0]-25, player_center[1]-25))
    elif player.stand_still > 0:
        frame = player.stand_still // 12
        screen.blit(player.event_sprites[frame+1], (player.x-7, player.y))


# laat zien hoeveel je kan sprinten
def display_sprint(max_sprint, sprint_now):
    # zorgt ervoor dat die een waarde heeft vn hoever de meter gevuld is en de width van de meter
    fill_meter = sprint_now/max_sprint
    meter_width = 200

    # maakt een lijn in het rood voor de achterkant van de meter
    pygame.draw.line(screen, red, (50, 50), (50+meter_width, 50), 20)

    # als de meter meer dan 0.01 gevuld is dan begint de groene lijn, deze geeft aan hoeveel de meter gevuld is
    # en het moet meer dan 0.01 zijn omdat anders de lijn verticaal word omdat de x-waarde dan niet verschilt van de lijn
    if fill_meter > 0.01:
        pygame.draw.line(screen, green, (50, 50),
                         (50+(meter_width*fill_meter), 50), 20)

    # maakt nog een kleine outline om de meter mooier eruit te laten zien
    pygame.draw.rect(screen, black, (50, 40, meter_width, 20), 2)

# laat zien hoelang je nog een shield hebt
def display_shield(shield_now):
    # zorgt ervoor dat die een waarde heeft vn hoever de meter gevuld is en de width van de meter
    fill_meter = shield_now/60
    meter_width = 200

    # maakt een lijn in het rood voor de achterkant van de meter
    pygame.draw.line(screen, red, (50, 80), (50+meter_width, 80), 20)

    # als de meter meer dan 0.01 gevuld is dan begint de blauwe lijn, deze geeft aan hoeveel de meter gevuld is
    # en het moet meer dan 0.01 zijn omdat anders de lijn verticaal word omdat de x-waarde dan niet verschilt van de lijn
    if fill_meter > 0.01:
        pygame.draw.line(screen, blue, (50, 80), (50+(meter_width*fill_meter), 80), 20)

    # maakt nog een kleine outline om de meter mooier eruit te laten zien
    pygame.draw.rect(screen, black, (50, 70, meter_width, 20), 2)

# laat het aantal schoten van de player zien
def display_gun(player):
    # zorgt ervoor dat die een waarde heeft vn hoever de meter gevuld is en de width van de meter
    fill_meter = player.gun_cooldown/120
    meter_width = 200

    # maakt een lijn in het rood voor de achterkant van de meter
    pygame.draw.line(screen, red, (50, 110), (50+meter_width, 110), 20)

    # als de meter meer dan 0.01 gevuld is dan begint de blauwe lijn, deze geeft aan hoeveel de meter gevuld is
    # en het moet meer dan 0.01 zijn omdat anders de lijn verticaal word omdat de x-waarde dan niet verschilt van de lijn
    if fill_meter > 0.01:
        pygame.draw.line(screen, yellow, (50, 110), (50+(meter_width*fill_meter), 110), 20)

    # maakt nog een kleine outline om de meter mooier eruit te laten zien
    pygame.draw.rect(screen, black, (50, 100, meter_width, 20), 2)
    pygame.draw.line(screen, black, (150, 100), (150, 120), 2)


# END SCREEN
# zorgt ervor dat de confetti beweegt en geprint op het scherm geprint word
def make_confetti(all_confetti):
    if len(all_confetti) < 100:
        all_confetti.append(confetti())

    # voor elke confetti
    for i in all_confetti:
        # verander de plek
        i.x += i.move_x
        i.y += i.move_y
        # maakt een cirkel met kleur op die plek
        pygame.draw.circle(screen, i.color, (i.x, i.y), 7)

        # als ze uit het beeld zijn removed die de confetti zodat er een nieuwe gemaakt kan worden
        if 0 > i.x > screen_width or i.y > screen_height:
            all_confetti.remove(i)
    return all_confetti

# maakt 2 buttons voor de opties op het eindscherm
def buttons(mouse):
    # maakt 2 blokken met de goede kleur en alfa waarde
    retry_block = pygame.Surface((200, 100))
    retry_block.fill(white)
    retry_block.set_alpha(96)
    quit_block = pygame.Surface((200, 100))
    quit_block.fill(white)
    quit_block.set_alpha(96)

    # als je over de boxes hovered veranderd de alfa van beide
    if 550 < mouse[0] < 750 and 450 < mouse[1] < 550:
        retry_block.set_alpha(160)
    elif 850 < mouse[0] < 1050 and 450 < mouse[1] < 550:
        quit_block.set_alpha(160)

    # print de blokken met de achtergrondkleur van de buttons
    screen.blit(retry_block, (550, 450))
    screen.blit(quit_block, (850, 450))

    # maakt de outlines
    pygame.draw.rect(screen, black, (550, 450, 200, 100), 3)
    pygame.draw.rect(screen, black, (850, 450, 200, 100), 3)

    # maakt de tekst in de buttons
    retry_text = text_font.render("replay", False, black)
    quit_text = text_font.render("quit", False, black)
    screen.blit(retry_text, (560, 485))
    screen.blit(quit_text, (890, 485))


# EVENTS
# functie voor de vogel event
def check_birb(player, birb):
    # beweegt de vogel, maakt de nieuwe hitbox en geeft hem steeds meer snelheid
    bird = birb[0]
    bird.x -= bird.x_movement
    bird.x_movement *= 1.02
    bird.hitbox = (bird.x, bird.y, bird.width, bird.height)

    frame = int(bird.frame/8)

    # hier tekent hij de vogel
    bird.sprites[0] = pygame.transform.scale(bird.sprites[0], (bird.width, bird.height+10))
    bird.sprites[1] = pygame.transform.scale(bird.sprites[1], (bird.width, bird.height+10))
    screen.blit(bird.sprites[frame%2], (bird.x, bird.y-5))

    # als hij langs de player is dan hoeft hij niet meer te checken of die collide
    if bird.width+bird.x > player.x:
        player.alive = not check_collision(player.hitbox, bird.hitbox)

    # returnt de bird waarde, de player waarde en of de bird van het scherm af is
    birb[0] = bird
    return birb, player, bird.x < -100

# functie voor ninja event
def check_ninja(player, objects, keys):
    # berekent de y-movement van de ninja ster
    new_star_rotation = ((objects[0].y - player.y)/(objects[0].x - player.x)) * 15 - 1.5
    object_numb = 1

    # maakt een variabele voor de ninja zodat ik er makkelijker bij kan
    this_ninja = objects[0]

    # maakt een frame counter
    frame = int(this_ninja.frame/6)

    # maakt 15 ninja sterren
    while len(objects) < 16 and frame > 5:
        # met elke een net andere rotatie
        objects.append(ninja_star(this_ninja.x, this_ninja.y + 20, new_star_rotation))

        # resized de images
        objects[object_numb].sprites[0] = pygame.transform.scale(objects[object_numb].sprites[0], (30, 30))
        objects[object_numb].sprites[1] = pygame.transform.scale(objects[object_numb].sprites[1], (30, 30))

        # veranderd de rotatie steeds een beetje
        new_star_rotation += .25

        # add 1 zodat hij elke resized
        object_numb += 1

    # maakt een variabele of de sterren van het scherm af zijn
    off_screen = False

    # voor elke ninja ster
    if frame > 5:
        # voor elke ster
        for i in range(1,16):
            # verplaatst de hitbox, x en y coordinaten
            objects[i].x -= objects[i].x_movement
            objects[i].y -= objects[i].y_movement
            objects[i].hitbox = (objects[i].x, objects[i].y, objects[i].width, objects[i].height)

            # tekent het plaatje op de goede plek
            screen.blit(objects[i].sprites[frame%2], (objects[i].x-5, objects[i].y-5))

            # kijkt of die hem raakt als de player niet shield
            if player.alive and objects[i].x+objects[i].width > player.x and not player.shielding:
                player.alive = not check_collision(player.hitbox, objects[i].hitbox)
            # anders kijkt hij of het object het scherm af is
            elif objects[i].x < -100:
                off_screen = True

    # zorgt ervoor dat de frames van de ninja goed getekend worden
    if frame < 0:
        this_ninja.spawn_smoke((abs(frame+1)/10)*255)
    elif frame < 8:
        this_ninja.sprites[frame] = pygame.transform.scale(this_ninja.sprites[frame], (this_ninja.width, this_ninja.height))
        screen.blit(this_ninja.sprites[frame], (this_ninja.x, this_ninja.y))
    elif frame < 18:
        this_ninja.spawn_smoke(((frame-8)/10)*255)

    # zet de aangepaste ninja terug naar de object lijst
    objects[0] = this_ninja

    # returnt alles
    return objects, player, off_screen

# functie voor bandit event
def check_bandit(player, objects, keymod):
    # maakt killobject false
    kill_object = False

    # maakt een tijdelijk variabele om hem makkelijker te accessen
    bandit = objects[0]

    # veranderd de jitbox van bandit
    bandit.hitbox = (bandit.x, bandit.y, bandit.width, bandit.height)

    # maakt een frame counter per 10 frames
    frame = int(bandit.frame/10)

    # voor elk van de 10 frames showt het programma de sprite
    if frame < 10:
        bandit.sprites[frame] = pygame.transform.scale(bandit.sprites[frame], (bandit.width, bandit.height))
        screen.blit(bandit.sprites[frame], (bandit.x, bandit.y-(bandit.height-player.height)))
    # als de animatie is afgelopen haalt hij het object weg
    else:
        kill_object = True

    # als de player voor frame 7 van de animatie schiet gaat die dood
    if frame < 7 and player.shoot:
        kill_object = True
    # als de player links van de bandit zit en de player heeft niet teruggeschoten gaat ie dood
    elif frame >= 7 and player.x < bandit.x:
        player.alive = False
        if len(bullets) < 1:
            bullets.append(bullet(bandit.x, bandit.y, -1))

    # objects[0] word weer veranderd
    objects[0] = bandit

    # returnt de waardes
    return objects, player, kill_object

# maakt de lijst met maps
map_list = [desert(), mountain(), tabletop(), crystal()]

# kiest een random map uit die lijst
Ground = map_list[random.randrange(0, len(map_list), 1)]

# laad de player en de sprites en vergroot alle sprites uiteindelijk
Player = character(Ground.hitbox[0][1]-50)
Player.load_sprites()

# voor altijd
while True:
    # krijgt de ingedrukte keys en muis-positie
    mouse = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    keymod = pygame.key.get_mods()

    # berekent het percentage waar de player is
    percentage = (Player.progress/max_progress)*100

    # maakt een loop met alle events
    for event in pygame.event.get():
        # quit als het kruisje word aangeklikt
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and (not Player.alive or percentage >= 100):
            # als er met de muis op de goede plekken word geklikt
            if 450 < mouse[1] < 550 and 550 < mouse[0] < 750:
                # herlaad alle dingen
                Ground = map_list[random.randrange(0, len(map_list), 1)]
                Ground.bg = pygame.transform.scale(Ground.bg, (screen_width, screen_height))
                Player = character(Ground.hitbox[0][1]-50)
                Player.load_sprites()
                all_confetti = []
                event_object = []
                event_active = -1
            elif 450 < mouse[1] < 550 and 850 < mouse[0] < 1050:
                # quit de game
                pygame.quit()
                sys.exit()

    # zorgt voor 60 fps en zorgt voor een frame counter
    msElapsed = clock.tick(60)

    # program frame counter
    program_frame += 1

    # maakt de achtergrond het goede plaatje
    screen.blit(Ground.bg, (0, 0))

    # berekent je fps elke 15 frames en displayt hem op het scherm
    if program_frame % 15 == 0:
        fps = int(1000/msElapsed)
    fps_text = text_font.render(str(fps), False, black)
    screen.blit(fps_text, (1530, 10))

    # laat hitboxes zien van de grond om de maps classes goed te maken
    # display_hitboxes(Ground)

    # zorgt ervoor dat de snelheid van de animatie een beetje overeen komt met de snelheid waarmee je loopt
    Player.run_frame += (Player.x_movement/Player.run_speed)

    # zorgt voor de 4 frames die loopen
    sprite_frame = int(Player.run_frame) // 5 % 4

    # voor elke bullet
    for this_bullet in bullets:
        # verplaatst en displayt de bullet
        this_bullet.check_bullet()

        # als de bullet van het scherm af is verwijderd die hem
        if -20 > this_bullet.x > screen_width+20:
            bullets.remove(this_bullet)

    # als de player schiet spawnt er een bullet voor hem
    if Player.shoot:
        bullets.append(bullet(Player.x+Player.width, Player.y, 1))

    # voor elke event
    if event_active != -1:
        # add 1 bij de frames van elk event object
        event_object[0].frame += 1

        # runt daarna de goede functie voor elke event
        if event_active == 0:
            event_object, Player, kill_object = check_birb(Player, event_object)
        elif event_active == 1:
            event_object, Player, kill_object = check_ninja(Player, event_object, keys)
        elif event_active == 2:
            event_object, Player, kill_object = check_bandit(Player, event_object, keymod)

        # als het object weer buiten het scherm is killt die het object
        if kill_object:
            event_object = []
            event_active = -1

    # als je nog leeft en nog niet bij t einde bent
    if Player.alive and percentage < 100:
        # runt elke frame de move_player functie
        Player = move_player(Player, Ground, fps)

        # runt de functie display player
        display_player(Player, sprite_frame)

        # laat de sprint en shield balk zien
        display_sprint(100, Player.sprint)
        display_shield(Player.shield)
        display_gun(Player)

        # voor random events
        if random.randrange(1, 5*max_fps, 1) == 1 and event_active == -1:
            event_classes = [birb(1700, Player.y), ninja(Ground.spawn_height-250), bandit(Ground.spawn_height-40)]
            event_active = random.randrange(0, len(event_classes), 1)
            event_object.append(event_classes[event_active])

    # als je het hebt gehaald
    elif percentage >= 100 and Player.alive:
        # zorgt voor de confetti
        all_confetti = make_confetti(all_confetti)

        # print de buttons
        buttons(mouse)

        # maakt de achtergrondkleur van de tekst voor leesbaarheid
        text_block = pygame.Surface((screen_width, 70))
        text_block.set_alpha(128)
        text_block.fill((255, 255, 255))
        screen.blit(text_block, (0, 330))

        # maakt de tekst de game winnen
        ending_text = text_font.render("Congratulations, you have beaten the game!", False, black)
        screen.blit(ending_text, (190, 350))
    # als je dood bent gegaan door een event
    elif not Player.alive:
        # zorgt voor de confetti
        all_confetti = make_confetti(all_confetti)

        # print de buttons
        buttons(mouse)

        # maakt de achtergrondkleur van de tekst voor leesbaarheid
        text_block = pygame.Surface((screen_width, 70))
        text_block.set_alpha(128)
        text_block.fill((255, 255, 255))
        screen.blit(text_block, (0, 330))

        # maakt de tekst voor verliezen
        ending_text = text_font.render("You died", False, black)
        screen.blit(ending_text, (700, 350))

    # laat het scherm zien
    pygame.display.update()
