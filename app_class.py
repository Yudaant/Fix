import pygame
pygame.init()
import sys
from settings import *
from player import *
import pygame.math as m
from enemy import *
import copy




class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.run = True
        self.state = "start"
        self.intermission = False
        self.cells = []
        self.cell_width = 20
        self.cell_height = 20
        self.player = Player(self , m.Vector2(13 , 29))
        self.walls = []
        self.coins = []
        self.pellets = []
        self.enemies = []
        self.high = self.get_high_score()
        self.enemy_position = []
        self.load()
        self.draw_enemies()
        self.start_music()
        self.blinking = 0
    def running(self):

        while self.run == True:
            self.clock.tick(FPS)
            if self.state == "start":
                self.start_events()
                self.start_redraw()
            if self.state == "play":
                self.play_events()
                self.play_redraw()
            if self.state == "over":
                self.game_over_event()
                self.game_over_redraw()
        pygame.quit()
        sys.exit()

    def draw_text(self , text , screen , font_type , font_size , font_color , pos , centered = False):
        font = pygame.font.SysFont(font_type , font_size)
        text = font.render(text , False , font_color)
        if centered:
            pos[0] = pos[0] - text.get_size()[0] // 2
            pos[1] = pos[1] - text.get_size()[1] // 2

        screen.blit(text , pos)
    def load(self):
        self.background = pygame.image.load("maze.png")
        with open("walls.txt") as file:
            lines = file.readlines()
            for line in lines:
                self.cells.append(line)
            for i in range(ROW):
                for j in range(COL):
                    if self.cells[i][j] == "1":
                        self.walls.append(m.Vector2(j, i))
                    if self.cells[i][j] == "C":
                        self.coins.append(m.Vector2(j, i))
                    if self.cells[i][j] == "B":
                        pygame.draw.rect(self.background , black , (j * self.cell_width , i * self.cell_height , self.cell_width , self.cell_height) , 0)
                    if self.cells[i][j] in ["2" , "3" , "4" , "5"]:
                        self.enemy_position.append(m.Vector2(j , i ))
                    if self.cells[i][j] == "I":
                        self.pellets.append(m.Vector2(j , i))


    def start_music(self):
        pygame.mixer.music.load("pacman_beginning.wav")
        pygame.mixer.music.play(-1)
    def play_music(self):
        pygame.mixer.music.load("Pac_Man_Ghost_Noises.mp3")
        pygame.mixer.music.play(-1)


    def draw_grid(self):
        pass
        # for i in range(SCREEN_WIDTH//self.cell_width):
        #     pygame.draw.line(self.background , red , (i * self.cell_width , 0) , (i * self.cell_width , MAZE_HEIGHT) , 1)
        # for i in range(SCREEN_WIDTH//self.cell_width):
        #     pygame.draw.line(self.background , red , (0 , self.cell_height*i) , (MAZE_WIDTH , self.cell_height*i) , 1)
        #
        # for wall in self.walls:
        #     pygame.draw.rect(self.background, GREEN, (wall.x * self.cell_width, wall.y * self.cell_height, self.cell_width, self.cell_height), 0)


    def draw_enemies(self):
        for idx  , pos in enumerate(self.enemy_position):
            new_enemy = Enemy(self , copy.deepcopy(pos) , idx)
            self.enemies.append(new_enemy)

    def reset_enemies(self):
        self.enemies = []
        self.draw_enemies()

    def reset(self):
        self.player.score = 0
        self.player.lives = 3
        self.player.grid_pos = m.Vector2(13 , 29)
        self.player.pix_pos = self.player.get_pix_pos()

        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction - m.Vector2(0 , 0)
        self.player.stored_direction = m.Vector2(0, 0)
        for enemy in self.enemies:
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction = m.Vector2(0 , 0)
        self.coins = []
        for row in range(ROW):
            for col in range(COL):
                if self.cells[row][col] == 'C':
                    self.coins.append(m.Vector2(col, row))

        self.reset_enemies()

    # start screen
    def get_high_score(self):
        # connection = sqlite3.connect('high_score.db')
        # cursor = connection.cursor()
        # cursor.execute('CREATE TABLE IF NOT EXISTS HIGHSCORE (Number REAL)')
        # cursor.execute('')
        with open("High Score") as file:
            high = int(file.readline().split(" ")[2])
        return high

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = "play"
                    self.play_music()

    def start_redraw(self):
        self.screen.fill(black)
        self.draw_text("HIGH SCORE: " + str(self.high) , self.screen , default_font , default_size , white , [0 , 0])
        self.draw_text("PUSH SPACE BAR" , self.screen , default_font , default_size , red , [SCREEN_WIDTH//2 , SCREEN_HEIGHT//3 + 50] , centered=True)
        self.draw_text("1 PLAYER ONLY" , self.screen , default_font , default_size , blue , [SCREEN_WIDTH//2 , 2*SCREEN_HEIGHT//3 - 50] , True)
        pygame.display.update()

    def sart_music(self):
        pygame.mixer.music.load("pacman_beginning.wav")
        pygame.mixer.music.play(-1)

# play screen

    def play_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False


        self.keys_pressed =  pygame.key.get_pressed()
        if self.keys_pressed[pygame.K_UP] == True:
            self.player.move(m.Vector2(0 , -1))
        if self.keys_pressed[pygame.K_LEFT] == True:
            self.player.move(m.Vector2(-1 , 0))
        if self.keys_pressed[pygame.K_DOWN] == True:
            self.player.move(m.Vector2(0 , 1))
        if self.keys_pressed[pygame.K_RIGHT] == True:
            self.player.move(m.Vector2(1 , 0))

    def draw_coins(self):
        if len(self.coins) == 0:
            self.state = "over"
            return
        for coin in self.coins:
            pygame.draw.circle(self.screen, WHITE, (TOP_BOTTOM//2 + coin.x * self.cell_width + self.cell_width // 2, TOP_BOTTOM//2 +coin.y * self.cell_height + self.cell_height // 2),self.cell_width // 2 - 8, 0)
    def draw_pellets(self):
        self.blinking += 1
        if self.blinking % 2 == 0:
            for coin in self.pellets:
                pygame.draw.circle(self.screen, WHITE, (TOP_BOTTOM//2 + coin.x * self.cell_width + self.cell_width // 2, TOP_BOTTOM//2 +coin.y * self.cell_height + self.cell_height // 2),self.cell_width // 2 - 2, 0)

    def play_redraw(self):
        self.screen.fill(black)
        self.screen.blit(self.background , (TOP_BOTTOM//2 , TOP_BOTTOM//2))
        self.draw_text("CURRENT SCORE: " + str(self.player.score), self.screen, default_font, default_size, white, [60 , 0])
        self.draw_text("HIGH SCORE:" + str(self.high), self.screen, default_font, default_size, white, [SCREEN_WIDTH//2 + 50 , 0])
        self.draw_grid()
        self.draw_coins()
        self.draw_pellets()
        self.player.draw()
        # print(self.enemies)
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def game_over_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
        if pygame.key.get_pressed()[pygame.K_ESCAPE] == True:
            self.run = False
        if pygame.key.get_pressed()[pygame.K_SPACE] == True:
            self.state = "play"
            self.reset()

    def game_over_redraw(self):
        self.screen.fill(black)
        self.draw_text("GAME OVER", self.screen, default_font, default_size, red , [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], centered=True)
        self.draw_text("PRESS ESCAPE TO QUIT" , self.screen, default_font , default_size - 5 , white , [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50]  , centered=True )
        self.draw_text("PRESS SPACE TO RESTART" , self.screen, default_font , default_size - 5 , white , [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50]   , True)

        pygame.display.update()





