import pygame
import sys
import random
import math

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

# Cargar imágenes
cat_image = pygame.image.load('cat.png')
warrior_image = pygame.image.load('warrior.png')
mage_image = pygame.image.load('mage.png')
archer_image = pygame.image.load('archer.png')
equipments = {
    "Espada": pygame.image.load('sword.png'),
    "Báculo": pygame.image.load('staff.png'),
    "Arco": pygame.image.load('bow.png')
}
tower_image = pygame.image.load('tower.png')
enemy_image = pygame.image.load('enemy.png')
background_image = pygame.image.load('background.png')
projectile_images = {
    "Espada": pygame.image.load('projectile_sword.png'),
    "Báculo": pygame.image.load('projectile_staff.png'),
    "Arco": pygame.image.load('projectile_bow.png')
}
menu_background_image = pygame.image.load('menu_background.png')  # Cargar la imagen de fondo del menú

# Cargar música de fondo
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)  # Reproduce la música en bucle

# Variables del juego
characters = []
towers = []
enemies = []
projectiles = []
selected_class = None
selected_equipment = None
enemy_spawn_time = 2000  # Tiempo en milisegundos entre oleadas de enemigos
last_enemy_spawn_time = pygame.time.get_ticks()
experience_needed = 100
enemies_defeated = 0
win_condition = 10  # Cantidad de enemigos que deben ser eliminados para ganar el nivel
enemies_escaped = 0
lost_condition = 10  # Cantidad de enemigos que deben escapar para perder el nivel

# Clases
class Character:
    def __init__(self, name, char_class, image, equipment):
        self.name = name
        self.char_class = char_class
        self.image = image
        self.equipment = equipment
        self.level = 1
        self.experience = 0
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if self.equipment:
            screen.blit(self.equipment, (self.rect.x + 50, self.rect.y))

    def shoot(self):
        if enemies:
            closest_enemy = min(enemies, key=lambda enemy: math.hypot(enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y))
            if self.equipment == equipments["Espada"]:
                projectile_image = projectile_images["Espada"]
            elif self.equipment == equipments["Báculo"]:
                projectile_image = projectile_images["Báculo"]
            elif self.equipment == equipments["Arco"]:
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
    new_character = Character(name, char_class, char_image, equipment)
    characters.append(new_character)

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
            draw_text("1. Espada", font, BLACK, screen, 20, 60)
        elif selected_class == "Mago":
            draw_text("1. Báculo", font, BLACK, screen, 20, 60)
        elif selected_class == "Arquero":
            draw_text("1. Arco", font, BLACK, screen, 20, 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_equipment = equipments.get("Espada" if selected_class == "Guerrero" else "Báculo" if selected_class == "Mago" else "Arco")
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

        pygame.draw.rect(screen, BLACK, play_button)
        pygame.draw.rect(screen, BLACK, exit_button)

        play_text = font.render("Iniciar Juego", True, WHITE)
        exit_text = font.render("Salir", True, WHITE)

        screen.blit(play_text, (play_button.x + play_button.width // 2 - play_text.get_width() // 2, play_button.y + 10))
        screen.blit(exit_text, (exit_button.x + play_button.width // 2 - exit_text.get_width() // 2, exit_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return  # Empezar el juego
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

def main():
    global last_enemy_spawn_time, enemies_defeated
    clock = pygame.time.Clock()
    player_name = "Michi"

    # Mostrar pantalla de inicio
    show_start_screen()

    # Seleccionar clase
    select_class()

    # Seleccionar equipamiento
    select_equipment()

    # Crear personaje
    if selected_class and selected_equipment:
        create_character(player_name, selected_class, selected_equipment)

    # Crear torres iniciales
    towers.append(Tower(200, 300))
    towers.append(Tower(400, 300))

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
        
        # Dibujar fondo
        screen.blit(background_image, (0, 0))

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
            pygame.time.wait(3000)  # Espera 3 segundos antes de salir
            pygame.quit()
            sys.exit()

        # Verificar condición de derrota
        if enemies_escaped >= lost_condition:
            draw_text("¡Derrota!", font, BLACK, screen, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(3000)  # Espera 3 segundos antes de salir
            pygame.quit()
            sys.exit()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
