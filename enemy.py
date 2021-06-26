import pygame
pygame.mixer.init()
from settings import *
import pygame.math as m
import random
import copy
import sqlite3

collision_sound = pygame.mixer.Sound("pacman_death.wav")
pink_enemy = pygame.image.load("pacman-pink-ghost.jpg")
orange_enemy = pygame.image.load("pacman-orange-ghost.jpg")
blue_enemy = pygame.image.load("pacman-blue-ghost.jpg")
red_enemy = pygame.image.load("pacman-red-ghost.jpg")

class Enemy:
    def __init__(self , app , pos , idx):
        self.app = app
        self.index = idx
        self.starting_pos = pos
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.personality = self.select_personality()
        self.image = self.select_image()
        self.image = pygame.transform.scale(self.image , (18 , 18))
        self.color = self.select_color()
        self.direction = m.Vector2(0 , 0 )
        self.first_run = True
        self.speed = self.select_speed()

    def get_pix_pos(self):
        self.x = TOP_BOTTOM//2 + self.grid_pos[0] * self.app.cell_width
        self.y = TOP_BOTTOM//2 + self.grid_pos[1] * self.app.cell_height

        return m.Vector2(self.x , self.y)

    def get_grid_pos(self):
        x = (self.pix_pos.x - TOP_BOTTOM // 2) \
            // self.app.cell_width
        y = (self.pix_pos.y - TOP_BOTTOM // 2) \
            // self.app.cell_height
        return m.Vector2(x, y)


    def draw(self):
        self.app.screen.blit(self.image,
        (TOP_BOTTOM // 2 + self.grid_pos.x * self.app.cell_width,
        TOP_BOTTOM // 2 + self.grid_pos.y * self.app.cell_height))
        # pygame.draw.circle(self.app.screen, self.color, self.pix_pos, self.app.cell_width // 2 - 2, 0)
        self.move()

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()

        elif self.personality == "scared":
            if self.first_run == True:
                self.grid_pos = m.Vector2(13 , 23)
                self.pix_pos = self.get_pix_pos()
                self.first_run= False
            self.direction = self.get_scared_direction()
        else:
            if self.app.intermission == False:
                print("HI")
                next_cell = self.get_next_cell()
                self.direction = next_cell - self.grid_pos
            else:
                print("hello")
                self.direction = self.get_scared_direction()
        if self.able_to_move() == True:
            self.pix_pos += self.direction * self.speed
            self.grid_pos = self.get_grid_pos()

        self.check_pos()
        # for i in range(100000):
        #     pass



    def get_random_direction(self):
        return random.choice([up, down, left, right])


    def get_next_cell(self):
        path = self.get_bfs_path()
        return m.Vector2(path[1]) if len(path) > 1 else m.Vector2(path[0])



    def get_bfs_path(self):
        # source is the enemy position
        src = self.grid_pos
        # target is the player position
        target = self.app.player.grid_pos
        # parent (parent of key is value)
        parent = {}
        # append the source into the queue
        queue = [src]
        # parent of source is [-1, -1]
        parent[tuple(src)] = m.Vector2(-1, -1)
        # neighbours are top, down, left, right
        neighbours = [up, down, left, right]

        # run this loop till queue becomes empty
        while len(queue) > 0:
            # first element is the current cell
            curr_cell = queue[0]
            # remove the current cell from the queue
            queue.remove(queue[0])
            # curr_cell becomes the target, then we have reached the destination, so break
            if curr_cell == target:
                break
            # otherwise, go to every neighbour of current cell
            for i in neighbours:
                neighbour_cell = curr_cell + i
                # if the nighbour is not a wall, is valid and is not visited
                if self.isSafe(neighbour_cell) == True and \
                tuple(neighbour_cell) not in parent:
                    # append the neighbour into the queue
                    queue.append(neighbour_cell)
                    # parent of neighbour cell would be current cell
                    parent[tuple(neighbour_cell)] = curr_cell

        # pth initilaization
        path = [target]
        # starting from target, travel back to the source using parent
        try:
            while parent[tuple(target)] != m.Vector2(-1, -1):
                # append the parent of the target
                path.append(parent[tuple(target)])
            # reassign the target to parent of target (travelling back)
                target = parent[tuple(target)]
        except:
            pass

        # reverse the path and return
        path.reverse()
        return path

    def isSafe(self, cell):
        # check for boundaries and check if cell is not a wall
        return (cell.x >= 0) and (cell.y >= 0) and (cell.x <= 27) and \
        (cell.y <= 30) and (cell not in self.app.walls)

    # def move(self):
    #     if self.personality == "random":
    #         self.direction = self.get_random_direction()
    #
    #     elif self.personality == "scared":
    #         if self.first_run == True:
    #             # print("hello")
    #             self.grid_pos = m.Vector2(13 , 23)
    #             self.first_run= False
    #         self.direction = self.get_scared_direction()
    #     else:
    #         next_cell = self.get_next_cell()
    #         self.direction = next_cell - self.grid_pos
    #     if self.able_to_move() == True:
    #         self.pix_pos += self.direction * self.speed
    #         self.grid_pos = self.get_grid_pos()
    #
    #     self.check_pos()
    #     # for i in range(100000):
    #     #     pass
    def get_scared_direction(self):
        path = self.get_bfs_path()
        neighbours = [up, down , left, right]
        for i in neighbours:
            curr_neighbour = self.grid_pos + i
            if self.isSafe(curr_neighbour) and \
                curr_neighbour not in path:
                return curr_neighbour - self.grid_pos
        return (path[1] - self.grid_pos) if len(path) > 1 \
        else (path[0] - self.grid_pos)


    def check_pos(self):
        if self.grid_pos == self.app.player.grid_pos:
            collision_sound.play()
            # print("collision")
            if self.app.intermission == False:
                self.app.player.lives -= 1
                self.app.player.grid_pos = m.Vector2(13, 29)
                print(self.app.player.grid_pos)
                self.app.player.pix_pos = self.app.player.get_pix_pos()
                self.app.player.direction = m.Vector2(0, 0)

                self.app.reset_enemies()
                self.app.player.draw()
                pygame.display.update()
                print(self.app.player.lives)
                if self.app.player.lives == 0:
                    self.app.state = "over"
                    self.app.start_music()
                pygame.time.delay(250)
            else:
                self.app.player.score += 100
                self.app.draw_text("100", self.app.screen, default_font, 10, WHITE, self.pix_pos - m.Vector2())
                self.grid_pos = copy.deepcopy(self.app.enemy_position[self.index])
                self.pix_pos = self.get_pix_pos()

                pygame.display.update()
                pygame.time.delay(500)


    def able_to_move(self):
        if m.Vector2(self.grid_pos + self.direction) in self.app.walls:
            return False
        return True
    def select_color(self):
        if self.index == 0:
            return  blue
        if self.index == 1:
            return RED
        if self.index == 2:
            return ORANGE
        if self.index == 3:
            return (255,192,203)

    def select_image(self):
        if self.index == 0:
            return  blue_enemy
        if self.index == 1:
            return red_enemy
        if self.index == 2:
            return orange_enemy
        if self.index == 3:
            return pink_enemy
    def select_personality(self):
        if self.index == 0:
            return "slow"
        if self.index == 1:
            return "random"
        if self.index == 2:
            return "scared"
        if self.index == 3:
            return "speedy"
    def select_speed(self):
        if self.index == 0:
            return 5
        if self.index == 1:
            return 10
        if self.index == 2:
            return 10
        if self.index == 3:
            return 20


