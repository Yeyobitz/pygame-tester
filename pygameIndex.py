import pygame
import sys
import os
import random
import math
import sqlite3 # conexion desde pygame a la base de datos
from datetime import datetime

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FantasyMichiHats")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fuentes
font = pygame.font.SysFont(None, 36)

# Determinar la ruta base
base_path = os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), 'Assets')

# Cargar imágenes
cat_image = pygame.image.load(os.path.join(base_path, 'cat.png'))
warrior_image = pygame.image.load(os.path.join(base_path, 'warrior.png'))
mage_image = pygame.image.load(os.path.join(base_path, 'mage.png'))
archer_image = pygame.image.load(os.path.join(base_path, 'archer.png'))
equipments = {
    "Casco 1": pygame.image.load(os.path.join(base_path, 'helmet1.png')),
    "Casco 2": pygame.image.load(os.path.join(base_path, 'helmet2.png')),
    "Casco 3": pygame.image.load(os.path.join(base_path, 'helmet3.png')),
    "Capa 1": pygame.image.load(os.path.join(base_path, 'cape1.png')),
    "Capa 2": pygame.image.load(os.path.join(base_path, 'cape2.png')),
    "Capa 3": pygame.image.load(os.path.join(base_path, 'cape3.png')),
    "Gorro 1": pygame.image.load(os.path.join(base_path, 'hat1.png')),
    "Gorro 2": pygame.image.load(os.path.join(base_path, 'hat2.png')),
    "Gorro 3": pygame.image.load(os.path.join(base_path, 'hat3.png'))
}
tower_image = pygame.image.load(os.path.join(base_path, 'tower.png'))
enemy_image = pygame.image.load(os.path.join(base_path, 'enemy.png'))
background_images = [
    pygame.image.load(os.path.join(base_path, 'background1.png')),
    pygame.image.load(os.path.join(base_path, 'background2.png')),
    pygame.image.load(os.path.join(base_path, 'background3.png'))
]
projectile_images = {
    "Espada": pygame.image.load(os.path.join(base_path, 'projectile_sword.png')),
    "Báculo": pygame.image.load(os.path.join(base_path, 'projectile_staff.png')),
    "Arco": pygame.image.load(os.path.join(base_path, 'projectile_bow.png'))
}
menu_background_image = pygame.image.load(os.path.join(base_path, 'menu_background.png'))  # Cargar la imagen de fondo del menú

# Cargar música de fondo
pygame.mixer.music.load(os.path.join(base_path, 'background_music.mp3'))
pygame.mixer.music.play(-1)  # Reproduce la música en bucle

# Conectar a la base de datos SQLite
try:
    conn = sqlite3.connect(os.path.join(base_path, 'game_data.db'))
    c = conn.cursor()
    print("Conexión a la base de datos SQLite establecida.")
except sqlite3.Error as e:
    print(f"Error al conectar con la base de datos SQLite: {e}")


# Crear tablas si no existen
c.execute('''
CREATE TABLE IF NOT EXISTS User (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    email TEXT,
    created_at TIMESTAMP
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS Character (
    character_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    name TEXT,
    class TEXT,
    level INTEGER,
    experience INTEGER,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS Game (
    game_id INTEGER PRIMARY KEY,
    character_id INTEGER,
    current_level INTEGER,
    current_score INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (character_id) REFERENCES Character(character_id)
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS Hat (
    hat_id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    class TEXT,
    image_url TEXT
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS Tower (
    tower_id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    level INTEGER,
    damage INTEGER,
    range INTEGER,
    image_url TEXT
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS Character_Inventory (
    inventory_id INTEGER PRIMARY KEY,
    character_id INTEGER,
    hat_id INTEGER,
    FOREIGN KEY (character_id) REFERENCES Character(character_id),
    FOREIGN KEY (hat_id) REFERENCES Hat(hat_id)
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS Level_Progression (
    progression_id INTEGER PRIMARY KEY,
    character_id INTEGER,
    tower_id INTEGER,
    level INTEGER,
    experience INTEGER,
    FOREIGN KEY (character_id) REFERENCES Character(character_id),
    FOREIGN KEY (tower_id) REFERENCES Tower(tower_id)
)
''')
conn.commit()
print("Tablas creadas o verificadas.")

# Variables del juego
characters = []
towers = []
enemies = []
projectiles = []
selected_class = None
selected_equipment = None
current_map = 0
enemy_spawn_time = 2000  # Tiempo en milisegundos entre oleadas de enemigos
last_enemy_spawn_time = pygame.time.get_ticks()
experience_needed = 100
enemies_defeated = 0
win_condition = 10  # Cantidad de enemigos que deben ser eliminados para ganar el nivel
enemies_escaped = 0
lost_condition = 10  # Cantidad de enemigos que deben escapar para perder el nivel
paused = False


# Clases
class Character:
    def __init__(self, name, char_class, image, equipment, character_id=None):
        self.name = name
        self.char_class = char_class
        self.image = image
        self.equipment = equipment
        self.level = 1
        self.experience = 0
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.character_id = character_id

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if self.equipment:
            screen.blit(equipments[self.equipment], (self.rect.x + 50, self.rect.y))

    def shoot(self):
        if enemies:
            closest_enemy = min(enemies, key=lambda enemy: math.hypot(enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y))
            if self.equipment in ["Casco 1", "Casco 2", "Casco 3"]:
                projectile_image = projectile_images["Espada"]
            elif self.equipment in ["Capa 1", "Capa 2", "Capa 3"]:
                projectile_image = projectile_images["Báculo"]
            elif self.equipment in ["Gorro 1", "Gorro 2", "Gorro 3"]:
                projectile_image = projectile_images["Arco"]
            new_projectile = Projectile(self.rect.centerx, self.rect.top, projectile_image, closest_enemy)
            projectiles.append(new_projectile)

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= experience_needed:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        print(f"{self.name} ha subido al nivel {self.level}!")
        create_multiple_enemies(self.level)  # Crear múltiples enemigos cuando el personaje sube de nivel
        # Actualizar el nivel del personaje en la base de datos
        c.execute('UPDATE Character SET level = ?, experience = ? WHERE character_id = ?', 
                  (self.level, self.experience, self.character_id))
        conn.commit()
        print(f"Nivel del personaje {self.name} actualizado en la base de datos.")

class Tower:
    def __init__(self, x, y):
        self.image = tower_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.level = 1

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def place_character(self, character):
        character.rect.centerx = self.rect.centerx
        character.rect.centery = self.rect.centery - self.rect.height // 2

class Enemy:
    def __init__(self):
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.speed = random.randint(1, 3)

    def move(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:  # Si el enemigo sale del lado izquierdo de la pantalla
            global enemies_escaped
            enemies_escaped += 1
            enemies.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Projectile:
    def __init__(self, x, y, image, target):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.target = target

    def move(self):
        dx, dy = self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx, dy = dx / distance * self.speed, dy / distance * self.speed
            self.rect.x += dx
            self.rect.y += dy

            # Check if hit the target
            if self.rect.colliderect(self.target.rect):
                if self.target in enemies:
                    enemies.remove(self.target)
                    if characters:
                        characters[0].gain_experience(10)
                    if self in projectiles:
                        projectiles.remove(self)
        else:
            if self in projectiles:
                projectiles.remove(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

def create_character(name, char_class, equipment):
    if char_class == "Guerrero":
        char_image = warrior_image
    elif char_class == "Mago":
        char_image = mage_image
    elif char_class == "Arquero":
        char_image = archer_image
    # Insertar el personaje en la base de datos
    c.execute('INSERT INTO Character (user_id, name, class, level, experience, created_at) VALUES (?, ?, ?, ?, ?, ?)', 
              (1, name, char_class, 1, 0, datetime.now()))
    conn.commit()
    character_id = c.lastrowid
    new_character = Character(name, char_class, char_image, equipment, character_id)
    characters.append(new_character)
    print(f"Personaje {name} creado e insertado en la base de datos con ID {character_id}.")

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def select_class():
    global selected_class
    running = True
    while running:
        screen.blit(menu_background_image, (0, 0))  # Dibujar la imagen de fondo del menú
        draw_text("Selecciona una clase:", font, BLACK, screen, 20, 20)
        draw_text("1. Guerrero", font, BLACK, screen, 20, 60)
        draw_text("2. Mago", font, BLACK, screen, 20, 100)
        draw_text("3. Arquero", font, BLACK, screen, 20, 140)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_class = "Guerrero"
                    running = False
                elif event.key == pygame.K_2:
                    selected_class = "Mago"
                    running = False
                elif event.key == pygame.K_3:
                    selected_class = "Arquero"
                    running = False
        
        pygame.display.flip()

def select_equipment():
    global selected_equipment
    running = True
    while running:
        screen.blit(menu_background_image, (0, 0))  # Dibujar la imagen de fondo del menú
        draw_text("Selecciona un equipamiento:", font, BLACK, screen, 20, 20)
        if selected_class == "Guerrero":
            draw_text("1. Casco 1", font, BLACK, screen, 20, 60)
            draw_text("2. Casco 2", font, BLACK, screen, 20, 100)
            draw_text("3. Casco 3", font, BLACK, screen, 20, 140)
        elif selected_class == "Mago":
            draw_text("1. Capa 1", font, BLACK, screen, 20, 60)
            draw_text("2. Capa 2", font, BLACK, screen, 20, 100)
            draw_text("3. Capa 3", font, BLACK, screen, 20, 140)
        elif selected_class == "Arquero":
            draw_text("1. Gorro 1", font, BLACK, screen, 20, 60)
            draw_text("2. Gorro 2", font, BLACK, screen, 20, 100)
            draw_text("3. Gorro 3", font, BLACK, screen, 20, 140)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if selected_class == "Guerrero":
                    if event.key == pygame.K_1:
                        selected_equipment = "Casco 1"
                        running = False
                    elif event.key == pygame.K_2:
                        selected_equipment = "Casco 2"
                        running = False
                    elif event.key == pygame.K_3:
                        selected_equipment = "Casco 3"
                        running = False
                elif selected_class == "Mago":
                    if event.key == pygame.K_1:
                        selected_equipment = "Capa 1"
                        running = False
                    elif event.key == pygame.K_2:
                        selected_equipment = "Capa 2"
                        running = False
                    elif event.key == pygame.K_3:
                        selected_equipment = "Capa 3"
                        running = False
                elif selected_class == "Arquero":
                    if event.key == pygame.K_1:
                        selected_equipment = "Gorro 1"
                        running = False
                    elif event.key == pygame.K_2:
                        selected_equipment = "Gorro 2"
                        running = False
                    elif event.key == pygame.K_3:
                        selected_equipment = "Gorro 3"
                        running = False

        pygame.display.flip()

def create_enemy():
    new_enemy = Enemy()
    enemies.append(new_enemy)

def create_multiple_enemies(num_enemies):
    for _ in range(num_enemies):
        create_enemy()

def show_start_screen():
    while True:
        screen.fill(WHITE)
        title_text = font.render("FantasyMichiHats", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        play_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 250, 200, 50)
        exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 50)
        register_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 150, 200, 50)  # Botón de registro

        pygame.draw.rect(screen, BLACK, play_button)
        pygame.draw.rect(screen, BLACK, exit_button)
        pygame.draw.rect(screen, BLACK, register_button)  # Dibujar el botón de registro

        play_text = font.render("Iniciar Sesión", True, WHITE)
        exit_text = font.render("Salir", True, WHITE)
        register_text = font.render("Registrar", True, WHITE)  # Texto del botón de registro

        screen.blit(play_text, (play_button.x + play_button.width // 2 - play_text.get_width() // 2, play_button.y + 10))
        screen.blit(exit_text, (exit_button.x + exit_button.width // 2 - exit_text.get_width() // 2, exit_button.y + 10))
        screen.blit(register_text, (register_button.x + register_button.width // 2 - register_text.get_width() // 2, register_button.y + 10))  # Mostrar el texto de registro

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    login_screen()  # Ir a la pantalla de inicio de sesión
                if register_button.collidepoint(event.pos):
                    register_screen()  # Ir a la pantalla de registro
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

def get_input_text(prompt):
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        
        screen.fill(WHITE)
        draw_text(prompt, font, BLACK, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50)
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        
        pygame.display.flip()
        pygame.time.Clock().tick(30)

def register_screen():
    username = get_input_text("Ingrese nombre de usuario:")
    password = get_input_text("Ingrese contraseña:")
    email = get_input_text("Ingrese email:")

    try:
        c.execute('INSERT INTO User (username, password, email, created_at) VALUES (?, ?, ?, ?)', 
                  (username, password, email, datetime.now()))
        conn.commit()
        print(f"Usuario {username} registrado correctamente.")
        login_screen()  # Ir a la pantalla de inicio de sesión después de registrar
    except sqlite3.IntegrityError:
        print(f"El nombre de usuario {username} ya existe.")
        register_screen()  # Volver a intentar el registro si el nombre de usuario ya existe

def login_screen():
    username = get_input_text("Ingrese nombre de usuario:")
    password = get_input_text("Ingrese contraseña:")
    
    c.execute('SELECT user_id FROM User WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    
    if user:
        print(f"Usuario {username} ha iniciado sesión correctamente.")
        main_menu(user[0])
    else:
        print("Nombre de usuario o contraseña incorrectos.")
        login_screen()  # Volver a intentar el inicio de sesión si los datos son incorrectos

def main_menu(user_id):
    while True:
        screen.fill(WHITE)
        screen.blit(menu_background_image, (0, 0))  # Asumiendo que tienes una imagen de fondo para el menú

        title_text = font.render("FantasyMichiHats", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        play_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 250, 200, 50)
        modify_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 50)
        exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 450, 200, 50)

        pygame.draw.rect(screen, BLACK, play_button)
        pygame.draw.rect(screen, BLACK, modify_button)
        pygame.draw.rect(screen, BLACK, exit_button)

        play_text = font.render("Jugar", True, WHITE)
        modify_text = font.render("Modificar Cuenta", True, WHITE)
        exit_text = font.render("Salir", True, WHITE)

        screen.blit(play_text, (play_button.x + play_button.width // 2 - play_text.get_width() // 2, play_button.y + 10))
        screen.blit(modify_text, (modify_button.x + modify_button.width // 2 - modify_text.get_width() // 2, modify_button.y + 10))
        screen.blit(exit_text, (exit_button.x + exit_button.width // 2 - exit_text.get_width() // 2, exit_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    main(user_id)  # Iniciar el juego
                    # Después de que main() retorna (al volver al menú principal), 
                    # necesitamos reinicializar algunas variables globales
                    global enemies, projectiles, towers, characters, paused
                    enemies = []
                    projectiles = []
                    towers = []
                    characters = []
                    paused = False
                    current_map = 0
                    enemies_defeated = 0
                    enemies_escaped = 0
                if modify_button.collidepoint(event.pos):
                    modify_account_screen(user_id)  # Modificar cuenta
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def modify_account_screen(user_id):
    new_password = get_input_text("Ingrese nueva contraseña:")
    new_email = get_input_text("Ingrese nuevo email:")

    c.execute('UPDATE User SET password = ?, email = ? WHERE user_id = ?', (new_password, new_email, user_id))
    conn.commit()
    print(f"Datos de la cuenta actualizados correctamente para el usuario con ID {user_id}.")
    main_menu(user_id)  # Volver al menú principal después de modificar la cuenta

def get_player_name():
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        
        screen.fill(WHITE)
        draw_text("Ingrese su nombre de jugador:", font, BLACK, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50)
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        
        pygame.display.flip()
        pygame.time.Clock().tick(30)
        
def draw_pause_menu():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    draw_text("PAUSA", font, WHITE, screen, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 150)

    continue_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
    main_menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 25, 200, 50)
    exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)

    pygame.draw.rect(screen, WHITE, continue_button)
    pygame.draw.rect(screen, WHITE, main_menu_button)
    pygame.draw.rect(screen, WHITE, exit_button)

    draw_text("Continuar", font, BLACK, screen, continue_button.x + 50, continue_button.y + 15)
    draw_text("Menú Principal", font, BLACK, screen, main_menu_button.x + 20, main_menu_button.y + 15)
    draw_text("Salir", font, BLACK, screen, exit_button.x + 75, exit_button.y + 15)

    return continue_button, main_menu_button, exit_button

def switch_map():
    global current_map, enemies, projectiles
    current_map = (current_map + 1) % len(background_images)
    enemies = []
    projectiles = []

def main(user_id):
    global last_enemy_spawn_time, enemies_defeated, enemies_escaped, paused
    clock = pygame.time.Clock()

    # Obtener el nombre del jugador
    player_name = get_player_name()

    # Seleccionar clase
    select_class()

    # Seleccionar equipamiento
    select_equipment()

    # Crear personaje
    if selected_class and selected_equipment:
        create_character(player_name, selected_class, selected_equipment)

    # Crear torres iniciales
    towers.append(Tower(10, 300))
    #towers.append(Tower(400, 300))

    # Colocar el personaje sobre la primera torre
    if characters:
        towers[0].place_character(characters[0])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and characters:
                    characters[0].shoot()
                elif event.key == pygame.K_p:
                    paused = not paused  # Alternar el estado de pausa
            elif event.type == pygame.MOUSEBUTTONDOWN and paused:
                if continue_button.collidepoint(event.pos):
                    paused = False
                elif main_menu_button.collidepoint(event.pos):
                    return  # Volver al menú principal
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        if not paused:
            # Dibujar fondo
            screen.blit(background_images[current_map], (0, 0))

            # Dibujar y atacar con torres
            for tower in towers:
                tower.draw(screen)

            # Crear oleadas de enemigos
            current_time = pygame.time.get_ticks()
            if current_time - last_enemy_spawn_time > enemy_spawn_time:
                create_enemy()
                last_enemy_spawn_time = current_time

            # Mover y dibujar enemigos
            for enemy in enemies:
                enemy.move()
                enemy.draw(screen)

            # Mover y dibujar proyectiles
            for projectile in projectiles:
                projectile.move()
                projectile.draw(screen)

            # Dibujar personaje
            if characters:
                characters[0].draw(screen)
                draw_text(f'Nombre: {characters[0].name}', font, BLACK, screen, 20, 20)
                draw_text(f'Clase: {characters[0].char_class}', font, BLACK, screen, 20, 60)
                draw_text(f'Nivel: {characters[0].level}', font, BLACK, screen, 20, 100)
                draw_text(f'Experiencia: {characters[0].experience}', font, BLACK, screen, 20, 140)

            # Verificar condición de victoria
            if enemies_defeated >= win_condition:
                draw_text("¡Victoria!", font, BLACK, screen, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)
                pygame.display.flip()
                pygame.time.wait(3000)  # Espera 3 segundos antes de cambiar el mapa
                enemies_defeated = 0
                switch_map()

            # Verificar condición de derrota
            if enemies_escaped >= lost_condition:
                draw_text("¡Derrota!", font, BLACK, screen, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)
                pygame.display.flip()
                pygame.time.wait(3000)  # Espera 3 segundos antes de salir
                pygame.quit()
                sys.exit()

        if paused:
            continue_button, main_menu_button, exit_button = draw_pause_menu()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    show_start_screen()

