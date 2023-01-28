import pygame
import math
import random
import sys
import time
global walls
global heal_items_list
global enemy_list

class Player:
    def __init__(self):
        # Load the player image and set the starting position
        self.image = pygame.image.load("player.png")
        self.x = 200
        self.y = 150
        self.width = 24
        self.height = 24
        self.health = 100
        self.alive = True
        self.attack_range = 50
        self.speed = 0.3
        self.attack_damage = 50
        self.rect = pygame.Rect(
            self.x, self.y, self.width + self.x, self.y + self.height
        )

    def move(self, walls):
        # Get the keys that are pressed
        keys = pygame.key.get_pressed()

        # Save the original position of the player
        original_x = self.x
        original_y = self.y

        # Move the player
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        # Check for collisions with the walls
        for wall in walls:
            if wall.check_collision(self):
                self.x = original_x
                self.y = original_y

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, (self.x, self.y))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.alive = False

    def update(self):
        self.rect = pygame.Rect(
            self.x, self.y, self.width + self.x, self.y + self.height
        )


class Wall:
    def __init__(self, x, y, width, height, image_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.alive = True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, player):
        if (
            player.x + player.width > self.x
            and player.x < self.x + self.width
            and player.y + player.height > self.y
            and player.y < self.y + self.height
        ):
            return True
        else:
            return False

    def update(self):
        self.rect = pygame.Rect(
            self.x, self.y, self.width + self.x, self.y + self.height
        )


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, player, walls, image_path, attack_range, health):
        self.x = x
        self.y = y
        self.speed = speed
        self.player = player
        self.walls = walls
        self.image = pygame.image.load(image_path)
        self.attack_range = attack_range
        self.health = health
        self.damage = 5
        self.alive = True
        self.attack_range = 5
        self.width = 32
        self.height = 32
        self.cooldown = 0  # initial cooldown is zero
        self.attack_flag = True  # enemy can attack initially

    def move(self):
        # Calculate the distance to the player
        x_distance = self.player.x - self.x
        y_distance = self.player.y - self.y
        distance = math.sqrt(x_distance**2 + y_distance**2)

        # Check if the enemy is within the attack range
        if distance < self.attack_range:
            self.attack(player)
        else:
            # Move towards the player
            x_move = x_distance / distance
            y_move = y_distance / distance

            # Check for collisions with the walls
            original_x = self.x
            original_y = self.y
            self.x += x_move * self.speed
            self.y += y_move * self.speed
            for wall in self.walls:
                if wall.check_collision(self):
                    self.x = original_x
                    self.y = original_y

    def attack(self, other):
        if self.attack_flag:
            self.player.take_damage(10)
            self.cooldown = time.time()  # set the cooldown to the current time
            self.attack_flag = False  # set the attack flag to False

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.alive = False

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.rect = pygame.Rect(
            self.x, self.y, self.width + self.x, self.y + self.height
        )
        if time.time() - self.cooldown > 0.3:  # check if cooldown has expired
            self.attack_flag = True  # set attack flag to True



class HealItem:
    def __init__(self, x, y, heal_amount):
        self.heal_amount = heal_amount
        self.x = x
        self.y = y
        self.width = 5
        self.height = 5
        self.image = pygame.image.load("heal_texture.png")
        self.alive = True

    def collide_with_player(self, player):
        player.health += self.heal_amount
        self.alive = False
        self.x = -10000
        self.y = -10000
        print(player.health)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, player):
        if (
            player.x + player.width > self.x
            and player.x < self.x + self.width
            and player.y + player.height > self.y
            and player.y < self.y + self.height
        ):
            return True
        else:
            return False

    def update(self):
        self.rect = pygame.Rect(
            self.x, self.y, self.width + self.x, self.y + self.height
        )


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.target = None

    def update(self):
        if self.target:
            x = -self.target.rect.x + int(WIDTH / 2)
            y = -self.target.rect.y + int(HEIGHT / 2)
            self.camera = pygame.Rect(x, y, self.width, self.height)


class Door:
    global walls
    global heal_items_list
    global enemy_list
    def __init__(self, x, y, width, height, image_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.alive = False
        

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, player):
        if (
            player.x + player.width > self.x
            and player.x < self.x + self.width
            and player.y + player.height > self.y
            and player.y < self.y + self.height
        ):
            return True
        else:
            return False

    def update(self):
        self.rect = pygame.Rect(
            self.x, self.y, self.width + self.x, self.y + self.height
        )
    
    def exit(self, player):
        player.x = 150
        player.y = 150

    
def game_over():
    while True:
        background = pygame.image.load("background.jpg")
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                create_start_screen(screen)
                player.alive = True
                return
        game_over_text = pygame.font.Font(None, 30).render("Game Over", False, (255, 255, 255))
        screen.blit(game_over_text,(200,250))
        pygame.display.update()
        




# Initialize Pygame and set the window size
cycle_flag = False
while True:
    WIDTH, HEIGHT = 800, 600
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    # создание стартового экрана
    def create_start_screen(screen):
        # загрузка фонового изображения
        background = pygame.image.load("background.jpg")
    
        # отображение фонового изображения
        screen.blit(background, (0, 0))
    
        # создание кнопки "Начать"
        start_button = pygame.draw.rect(screen, WHITE, (WIDTH//2-50, HEIGHT//2-25, 100, 50))
        start_button_text = pygame.font.Font(None, 30).render("Start", True, BLACK)
        screen.blit(start_button_text, (WIDTH//2-30, HEIGHT//2-10))
    
        # создание кнопки "Выйти"
        exit_button = pygame.draw.rect(screen, WHITE, (WIDTH//2-50, HEIGHT//2+50, 100, 50))
        exit_button_text = pygame.font.Font(None, 30).render("Exit", True, BLACK)
        screen.blit(exit_button_text, (WIDTH//2-30, HEIGHT//2+65))
        
    
        # обновление экрана
        pygame.display.update()
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x > WIDTH//2-50 and mouse_y > HEIGHT//2-25 and mouse_x < WIDTH//2-50 + 100 and mouse_y < HEIGHT//2-25 + 50:
                        return
                    elif mouse_x > WIDTH//2-50 and mouse_y > HEIGHT//2+50 and mouse_x < WIDTH//2-50 + 100 and mouse_y < HEIGHT//2+50 + 50:
                        pygame.quit()
                        sys.exit()
            pygame.display.flip()
    
    
    
    
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    player = Player()
    camera = Camera(WIDTH, HEIGHT)
    camera.target = player
    points = 0
    with open('highscore.txt') as f:
        best_score = int(f.readline())
    # Run the game loop
    create_start_screen(screen)
    running = True
    walls_templates = [[
        Wall(50, 50, 48, 39, "wall.png"),
        Wall(96, 50, 48, 39, "wall.png"),
        Wall(142, 50, 48, 39, "wall.png"),
        Wall(188, 50, 48, 39, "wall.png"),
        Wall(188 + 46, 50, 48, 39, "wall.png"),
        Wall(188 + 46 * 2, 50, 48, 39, "wall.png"),
        Wall(50, 87, 16, 39, "vertical_wall.png"),
        Wall(50, 87 + 39, 16, 39, "vertical_wall.png"),
        Wall(50, 87 + 39 * 2, 16, 39, "vertical_wall.png"),
        Wall(50, 87 + 39 * 3, 16, 39, "vertical_wall.png"),
        Wall(50, 87 + 39 * 4, 16, 39, "vertical_wall.png"),
        Wall(188 + 46 * 3, 50, 48, 39, "wall.png"),
        Wall(188 + 46 * 4, 50, 48, 39, "wall.png"),
        Wall(188 + 46 * 5, 87 + 39 * 4, 16, 39, "vertical_wall.png"),
        Wall(188 + 46 * 5, 87 + 39 * 3, 16, 39, "vertical_wall.png"),
        Wall(188 + 46 * 5, 87 + 39 * 2, 16, 39, "vertical_wall.png"),
        Wall(188 + 46 * 5, 87 + 39 * 1, 16, 39, "vertical_wall.png"),
        Wall(188 + 46 * 5, 87, 16, 39, "vertical_wall.png"),
        Wall(188 + 46 * 5, 87 - 39 * 1 + 1, 16, 39, "vertical_wall.png"),
        Wall(188 + 46 * 5, 87 + 39 * 5, 16, 39, "vertical_wall.png"),
        Wall(50, 87 + 39 * 5, 48, 39, "wall.png"),
        Wall(96, 87 + 39 * 5, 48, 39, "wall.png"),
        Wall(142, 87 + 39 * 5, 48, 39, "wall.png"),
        Wall(188, 87 + 39 * 5, 48, 39, "wall.png"),
        Wall(188 + 46, 87 + 39 * 5, 48, 39, "wall.png"),
        Wall(188 + 46 * 2, 87 + 39 * 5, 48, 39, "wall.png"),
        Wall(188 + 46 * 3, 87 + 39 * 5, 48, 39, "wall.png"),
        Wall(188 + 46 * 4, 87 + 39 * 5, 48, 39, "wall.png")
    ], [Wall(188 + 46 * 4, 87 + 39 * 5, 48, 39, "wall.png")]]
    door = Door(198 + 46 * 3, 90, 16, 16, "door.png")
    update_flag = True
    walls = random.choice(walls_templates)
    heal_items_templates = [[HealItem(250, 250, 20)], []]
    heal_items_list = random.choice(heal_items_templates)
    enemy_templates = [[Enemy(100, 100, 0.1, player, walls, "enemy.png", 50, 100)]]
    enemy_list = random.choice(enemy_templates)
    all_sprites = [player, door]
    all_sprites.extend(walls)
    all_sprites.extend(heal_items_list)
    all_sprites.extend(enemy_list)
    exit_flag = False
    font = pygame.font.Font(None, 30)
    points_text = font.render(f"Points: {points}", True, (255, 255, 255))
    best_score_text = font.render(f"Best Score: {best_score}", True, (255, 255, 255))
    health_text = font.render(f"Health: {player.health}", True, (255, 255, 255))
    while running:
        # Handle events
    
        if update_flag:
            walls = []
            heal_items_list = []
            enemy_list = []
            all_sprites = []
            walls_templates = [[
            Wall(50, 50, 48, 39, "wall.png"),
            Wall(96, 50, 48, 39, "wall.png"),
            Wall(142, 50, 48, 39, "wall.png"),
            Wall(188, 50, 48, 39, "wall.png"),
            Wall(188 + 46, 50, 48, 39, "wall.png"),
            Wall(188 + 46 * 2, 50, 48, 39, "wall.png"),
            Wall(50, 87, 16, 39, "vertical_wall.png"),
            Wall(50, 87 + 39, 16, 39, "vertical_wall.png"),
            Wall(50, 87 + 39 * 2, 16, 39, "vertical_wall.png"),
            Wall(50, 87 + 39 * 3, 16, 39, "vertical_wall.png"),
            Wall(50, 87 + 39 * 4, 16, 39, "vertical_wall.png"),
            Wall(188 + 46 * 3, 50, 48, 39, "wall.png"),
            Wall(188 + 46 * 4, 50, 48, 39, "wall.png"),
            Wall(188 + 46 * 5, 87 + 39 * 4, 16, 39, "vertical_wall.png"),
            Wall(188 + 46 * 5, 87 + 39 * 3, 16, 39, "vertical_wall.png"),
            Wall(188 + 46 * 5, 87 + 39 * 2, 16, 39, "vertical_wall.png"),
            Wall(188 + 46 * 5, 87 + 39 * 1, 16, 39, "vertical_wall.png"),
            Wall(188 + 46 * 5, 87, 16, 39, "vertical_wall.png"),
            Wall(188 + 46 * 5, 87 - 39 * 1 + 1, 16, 39, "vertical_wall.png"),
            Wall(188 + 46 * 5, 87 + 39 * 5, 16, 39, "vertical_wall.png"),
            Wall(50, 87 + 39 * 5, 48, 39, "wall.png"),
            Wall(96, 87 + 39 * 5, 48, 39, "wall.png"),
            Wall(142, 87 + 39 * 5, 48, 39, "wall.png"),
            Wall(188, 87 + 39 * 5, 48, 39, "wall.png"),
            Wall(188 + 46, 87 + 39 * 5, 48, 39, "wall.png"),
            Wall(188 + 46 * 2, 87 + 39 * 5, 48, 39, "wall.png"),
            Wall(188 + 46 * 3, 87 + 39 * 5, 48, 39, "wall.png"),
            Wall(188 + 46 * 4, 87 + 39 * 5, 48, 39, "wall.png")
            ]]
            door = Door(198 + 46 * 3, 90, 16, 16, "door.png")
            walls = random.choice(walls_templates)
            heal_items_templates = [[HealItem(250, 250, 20)], [], [], []]
            heal_items_list = random.choice(heal_items_templates)
            enemy_templates = [[Enemy(100, 100, 0.1, player, walls, "enemy.png", 50, 100)], [Enemy(100, 150, 0.1, player, walls, "enemy.png", 50, 100), Enemy(100, 100, 0.1, player, walls, "enemy.png", 50, 100)], [Enemy(100, 200, 0.1, player, walls, "enemy.png", 50, 100)], []]
            enemy_list = random.choice(enemy_templates)
            all_sprites = [player, door]
            all_sprites.extend(walls)
            all_sprites.extend(heal_items_list)
            all_sprites.extend(enemy_list)
            update_flag = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
    
                # Check if the mouse is within the attack range of the enemy
                for enemy in enemy_list:
                    x_distance = mouse_x - enemy.x
                    y_distance = mouse_y - enemy.y
                    distance = math.sqrt((player.x - enemy.x) ** 2 + (player.y - enemy.y) ** 2)
                    if distance**2 < player.attack_range**2:
                        # Attack the enemy
                        print("atack")
                        enemy.take_damage(player.attack_damage)
    
        # Clear the screen
        screen.fill((0, 0, 0))
    
        # Move and draw the player
        player.move(walls)
        # draw the wall and check collision
        for wall in walls:
            if wall.check_collision(player):
                print("Collision detected")
                player.speed = 0
        for heal_item in heal_items_list:
            if heal_item.check_collision(player):
                heal_item.collide_with_player(player)
        for enemy in enemy_list:
            if enemy.alive:
                enemy.move()
        for i in all_sprites:
            i.update()
        camera.update()
        for i in all_sprites:
            if i.alive:
                screen.blit(i.image, i.rect.move(camera.camera.topleft))
        screen.blit(points_text, (10, 10))
        screen.blit(best_score_text, (10, 40))
        screen.blit(health_text, (10, 70))
        health_text = font.render(f"Health: {player.health}", True, (255, 255, 255))
        res = 0
        for enemy in enemy_list:
            if not enemy.alive:
                res+=1
        if res == len(enemy_list):
            exit_flag = True
        if not player.alive:
            game_over()
            with open('highscore.txt', 'w') as f:
                f.truncate(0)
                f.write(str(best_score))
            break
        if exit_flag:
            door.alive = True
            if door.check_collision(player):
                door.exit(player)
                update_flag = True
                points += 1
                best_score = max(best_score, points)
                points_text = font.render(f"Points: {points}", True, (255, 255, 255))
                best_score_text = font.render(f"Best Score: {best_score}", True, (255, 255, 255))
                door.alive = False
                exit_flag = False
                pygame.display.update()
    
    
                
    
        # Update the display
        pygame.display.update()
    
    # Clean up and exit
