from os import cpu_count
import pygame
from humanoid import *
from tile import *
from bullet import *
import random

class game_handle():
    def __init__(self, window_name, height, width):
        self.window_name = window_name
        self.height = height
        self.width = width
        self.gravity = 10
        self.map = []
        self.entities = []
        self.app_is_runing = True
        self.tiles_Size = 64
        self.tiles = {
            "dirt" : pygame.transform.scale(pygame.image.load("assets/dirt.png"),(self.tiles_Size, self.tiles_Size)),
            "grass" : pygame.transform.scale(pygame.image.load("assets/grass.png"),(self.tiles_Size, self.tiles_Size)),
            #"bush" : pygame.transform.scale(pygame.image.load("assets/bush.png"),(self.tiles_Size, self.tiles_Size)),
            "endline" : pygame.transform.scale(pygame.image.load("assets/endline.png"), (self.tiles_Size, self.tiles_Size))
        }
        self.gui_img = {
            "heart" : pygame.transform.scale(pygame.image.load("assets/heart.png"),(self.tiles_Size, self.tiles_Size)),
            "play" : pygame.transform.scale(pygame.image.load("assets/Play.png"),(self.tiles_Size, 32)),
            "quit" : pygame.transform.scale(pygame.image.load("assets/quit.png"),(self.tiles_Size, self.tiles_Size))
        }
        self.enemy_quantity = 0
        self.tiles_quantity = 0
        self.player_won = False
        self.map_index = 1
        self.bullets = []
        self.shoot_time = 0.5 * 60
        self.actual_shoot_time = 0
        self.game_over = True
        self.can_click_play = False
        self.can_click_quit = False
        self.global_player_life = 5

    def load_map(self):
        self.map.clear()
        file = open("map.txt", "r")
        lines = file.readlines()
        num_of_lines = 17
        if self.map_index != 0:
            x = 0 + (num_of_lines * (self.map_index - 1)) + (self.map_index - 1)
            y = (num_of_lines * self.map_index) + self.map_index 
        else:
            x = 0 + (num_of_lines * (self.map_index - 1))
            y = num_of_lines * self.map_index

        while x < y:
            dat = []
            for lin in lines[x]:
                splited_line = lin.split()
                for value in splited_line:
                    if value != "-":
                        dat.append(int(value))
            self.map.append(dat)
            x +=1
            

    def get_objects_from_map(self):
        line_index = 0
        for line in self.map:
            col_index = 0
            for col in line:
                if col == 4:
                    obj = humanoid(col_index*self.tiles_Size, line_index*self.tiles_Size, 64,32,4,13,"assets/player.png", self.global_player_life, 1)
                    self.entities.append(obj)
                col_index += 1
            line_index+=1
        line_index = 0
        for line in self.map:
            col_index = 0
            for col in line:
                if col == 5:
                    obj = humanoid(col_index*self.tiles_Size, line_index*self.tiles_Size, 64,32,random.randrange(2,6),8,"assets/enemy.png", random.randrange(5,11), 1)
                    self.entities.append(obj)
                    self.enemy_quantity +=1 
                col_index += 1
            line_index+=1
        line_index = 0
        for line in self.map:
            col_index = 0
            for col in line:
                if col < 4 and col != 0:
                    obj = tile(col_index*self.tiles_Size, line_index*self.tiles_Size, self.tiles_Size, self.tiles_Size)
                    self.entities.append(obj)
                    self.tiles_quantity +=1
                col_index += 1
            line_index+=1
        line_index = 0
        for line in self.map:
            col_index = 0
            for col in line:
                if col == 6:
                    self.finish_line = tile(col_index*self.tiles_Size, line_index*self.tiles_Size, self.tiles_Size, self.tiles_Size)
                col_index += 1
            line_index+=1

    def draw_map(self):
        line_index = 0
        for line in self.map:
            col_index = 0
            for colum in line:
                if colum == 1:
                    self.screen.blit(self.tiles["dirt"], (col_index * self.tiles_Size, line_index * self.tiles_Size))
                if colum == 2:
                    self.screen.blit(self.tiles["grass"], (col_index * self.tiles_Size, line_index * self.tiles_Size))
                if colum == 3:
                    self.screen.blit(self.tiles["bush"], (col_index * self.tiles_Size, line_index * self.tiles_Size))
                if colum == 6 and self.enemy_quantity <= 0:
                    self.screen.blit(self.tiles["endline"], (col_index*self.tiles_Size, line_index*self.tiles_Size))
                col_index +=1
            line_index +=1

    def create_window(self):
        pygame.init()
        self.dis_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.dis_info.current_w, self.dis_info.current_h), pygame.FULLSCREEN)
    def handle_events(self):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                self.app_is_runing = False
            if events.type == pygame.MOUSEBUTTONDOWN and self.can_click_play:
                self.game_over = False
                self.entities.clear()
                self.enemy_quantity = 0
                self.tiles_quantity = 0
                self.global_player_life = 5
                self.map_index = 1
                self.load_map()
                self.get_objects_from_map()
                
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:
            if self.entities[0].dir_x == 1:
                img = self.entities[0].img
                img_fliped = pygame.transform.flip(img, True, False)
                self.entities[0].img = img_fliped
            self.entities[0].change_speed("x", -1)
        elif keys_pressed[pygame.K_d]:
            if self.entities[0].dir_x == -1:
                img = self.entities[0].img
                img_fliped = pygame.transform.flip(img, True, False)
                self.entities[0].img = img_fliped
            self.entities[0].change_speed("x", 1)
        else:
            self.entities[0].change_speed("x", 0)
        if keys_pressed[pygame.K_w] and self.entities[0].is_grounded:
            self.entities[0].change_speed("y", -1)
            self.entities[0].is_grounded = False
        self.actual_shoot_time -= 1
        if keys_pressed[pygame.K_SPACE] and self.actual_shoot_time <= 0:
            self.bullets.append(bullet(10,10,5,self.entities[0],15,"assets/bullet.png"))
            self.actual_shoot_time = self.shoot_time

    def update(self):
        i=0
        for en in self.entities:
            if en == self.entities[0]:
                en.move(self.entities[1:])
                if en.speed[1] <= self.gravity:
                    en.speed[1] += 0.5
                if en.player_won(self.finish_line) and self.enemy_quantity <= 0:
                    self.global_player_life = self.entities[0].life
                    self.entities.clear()
                    self.enemy_quantity = 0
                    self.tiles_quantity = 0
                    self.map_index +=1
                    self.load_map()
                    self.get_objects_from_map()
                if self.entities[0].game_over():
                    self.game_over = True
            elif i < self.enemy_quantity:
                arr = self.entities.copy()
                arr.remove(en)
                en.artificial_inteligence(self.entities[0], self.entities[self.enemy_quantity+1:])

                en.move(arr)
                
                colb = en.collided_with(self.bullets)
                if en.speed[1] <= self.gravity:
                    en.speed[1] += 0.5
                if colb != None:
                    en.life -= colb.dmg
                    self.bullets.remove(colb)
                if en.life <= 0:
                    self.entities.remove(en)
                    self.enemy_quantity -= 1
                i+=1
            
        for b in self.bullets:
            b.move()
            col = b.bullet_colided(self.entities[self.enemy_quantity+1:])
            if col != None:
                self.bullets.remove(b)
            if b.xpos > self.dis_info.current_w:
                self.bullets.remove(b)
            elif b.xpos < 0:
                self.bullets.remove(b)
    
    def render_gui(self):
        if self.game_over:
            self.screen.blit(self.gui_img["play"], ((self.dis_info.current_w/2) - (self.tiles_Size*3)/2, (self.dis_info.current_h/2)))
            if (self.dis_info.current_w/2) - self.tiles_Size/2 * 3 <= pygame.mouse.get_pos()[0] and self.dis_info.current_w/2 + self.tiles_Size/2 * 3 >= pygame.mouse.get_pos()[0] and (self.dis_info.current_h/2) <= pygame.mouse.get_pos()[1] and self.dis_info.current_h/2 + (32*3) >= pygame.mouse.get_pos()[1]:
                    self.gui_img["play"] = pygame.transform.scale(pygame.image.load("assets/play_red.png"),(self.tiles_Size*3, 32*3))
                    self.can_click_play = True
            else:
                self.gui_img["play"] = pygame.transform.scale(pygame.image.load("assets/Play.png"),(self.tiles_Size*3, 32*3))
                self.can_click_play = False
        else:
            lifex = 20
            lifey = 20
            x = 0
            for i in range(self.entities[0].life):
                self.screen.blit(self.gui_img["heart"], (lifex + (x * pygame.Surface.get_width(self.gui_img["heart"])), lifey))
                x += 1

    def render_game(self):
        if not self.game_over:
            for en in self.entities[0:self.enemy_quantity+1]:
                self.screen.blit(en.img, (en.xpos, en.ypos))
            for b in self.bullets:
                self.screen.blit(b.img, (b.xpos, b.ypos))
            self.screen.blit(self.entities[0].img, (self.entities[0].xpos, self.entities[0].ypos))
            self.draw_map()
    def render(self):
        self.screen.fill((0,255,255))
        self.render_gui()
        self.render_game()
        pygame.display.set_caption(self.window_name)
        pygame.display.flip()
