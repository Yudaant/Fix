import pygame
pygame.mixer.init()
from settings import *
import pygame.math as m
import time

chomp_sound = pygame.mixer.Sound("pacman_chomp.wav")
player_img = pygame.image.load("pacman-player.png")
player_shrink_img = pygame.transform.scale(player_img, (18 , 18))
play_scared = pygame.image.load("105-1056741_image-result-for-pacman-scared-ghost-pacman-dark.png")
collision_sound = pygame.mixer.Sound("pacman_death.wav")
pink_enemy = pygame.image.load("pacman-pink-ghost.jpg")
orange_enemy = pygame.image.load("pacman-orange-ghost.jpg")
blue_enemy = pygame.image.load("pacman-blue-ghost.jpg")
red_enemy = pygame.image.load("pacman-red-ghost.jpg")
class Player:
    def __init__(self, app , start_pos):
        self.app = app
        self.grid_pos = start_pos
        self.image = player_shrink_img
        self.pixel_pos = self.get_pix_pos()
        self.score = 1
        self.speed = 20
        self.start_time = None
        self.direction = m.Vector2(0, 0)
        self.lives = 3
        self.stored_direction = m.Vector2(0 , 0)
        self.intermission_start_time = None
    def get_pix_pos(self):
        self.x = TOP_BOTTOM//2 + self.grid_pos[0] * self.app.cell_width
        self.y = TOP_BOTTOM//2 + self.grid_pos[1] * self.app.cell_height

        return m.Vector2(self.x , self.y)

    def get_grid_pos(self):
        x = (self.pixel_pos.x - TOP_BOTTOM// 2) \
            // self.app.cell_width
        y = (self.pixel_pos.y - TOP_BOTTOM // 2) \
            // self.app.cell_height
        return m.Vector2(x, y)

    def draw(self):
        if self.time_to_move():
            self.direction = self.stored_direction
        if self.able_to_move():
           self.pixel_pos+= self.direction * self.speed
           self.grid_pos = self.get_grid_pos()

        self.on_coin()
        self.eat_pellet()
        if self.app.intermission == True:
            if (time.time() - self.intermission_start_time) >= 10:
                self.intermission_start_time = None
                print("end intermission")
                self.app.intermission = False
                self.change_back()


        # pygame.draw.circle(self.app.screen , YELLOW , self.pixel_pos , self.app.cell_width//2 - 2 , 0)
        self.app.screen.blit(self.image,(TOP_BOTTOM // 2 + self.grid_pos.x * self.app.cell_width,TOP_BOTTOM // 2 + self.grid_pos.y * self.app.cell_height))

        self.app.draw_text("Lives - ", self.app.screen, default_font, default_size, WHITE, [25, SCREEN_HEIGHT - 28])
        for x in range(self.lives):
            self.app.screen.blit(player_shrink_img , (100 + 22 * x, SCREEN_HEIGHT - 22))
        self.rotate()

    def time_to_move(self):
        if self.stored_direction == left:
            if self.grid_pos + left not in self.app.walls:
                return True
        if self.stored_direction == up:
            if self.grid_pos + up not in self.app.walls:
                return True
        if self.stored_direction == right:
            if self.grid_pos + right not in self.app.walls:
                return True
        if self.stored_direction == down:
            if self.grid_pos + down not in self.app.walls:
                return True
        return False

    def move(self , direction):
        self.stored_direction = direction

    def rotate(self):
        if self.direction == right:
            self.image = pygame.transform.rotate(player_shrink_img , 0)
        elif self.direction == left:
            self.image = pygame.transform.rotate(player_shrink_img , 180)
        elif self.direction == up:
            self.image = pygame.transform.rotate(player_shrink_img , 90)
        elif self.direction == down:
            self.image = pygame.transform.rotate(player_shrink_img , -90)
        else:
            self.image = pygame.transform.rotate(player_shrink_img, 0)

    def able_to_move(self): # direction is vel
        if m.Vector2(self.grid_pos + self.direction) in self.app.walls:
            return False
        else:
            return True
    def on_coin(self):
        if m.Vector2(self.grid_pos ) in self.app.coins:
            self.app.coins.remove(m.Vector2(self.grid_pos))
            self.score += 1
            chomp_sound.play(maxtime=50)
        if self.score > self.app.high:
            self.app.high = self.score
            with open('High Score', 'w') as file:
                file.write(f"HIGHSCORE = {self.app.high}")

        return

    def change_pictures(self):
        for enemy in self.app.enemies:
            enemy.image = play_scared
            enemy.image = pygame.transform.scale(enemy.image, (18, 18))
    def change_back(self):
        for enemy in self.app.enemies:
            if enemy.index == 0:
                enemy.image = blue_enemy
            if enemy.index == 1:
                enemy.image = pink_enemy
            if enemy.index == 2:
                enemy.image = orange_enemy
            if enemy.index == 3:
                enemy.image = red_enemy
            enemy.image = pygame.transform.scale(enemy.image, (18, 18))
    def eat_pellet(self):
        if m.Vector2(self.grid_pos ) in self.app.pellets:
            self.app.pellets.remove(m.Vector2(self.grid_pos))
            self.app.intermission = True
            print("start intermission")
            self.intermission_start_time = time.time()
            self.change_pictures()
            # self.change_back()


            # self.score += 1
            # chomp_sound.play(maxtime=50)

        return




