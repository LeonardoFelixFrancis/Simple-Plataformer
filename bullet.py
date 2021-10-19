import pygame

class bullet():
    def __init__(self, height, width, dmg, player_obj,bullet_speed,img):
        if player_obj.dir_x == 1:
            self.offsetx = 64
        elif player_obj.dir_x == -1:
            self.offsetx = -5
        
        self.offsety = 30
        self.xpos = player_obj.xpos + self.offsetx
        self.ypos = player_obj.ypos + self.offsety
        self.height = height
        self.width = width
        self.dmg = dmg 
        self.img = pygame.transform.scale(pygame.image.load(img),(self.height, self.width))
        self.bullet_speed = bullet_speed
        self.dir = player_obj.dir_x
        self.player_speed_atshot = player_obj.speed[0]
    
    def move(self):
        self.xpos += self.dir * (self.bullet_speed + self.player_speed_atshot)
    
    def bullet_colided(self, coliders):
        col_info = [0,0]
        for col in coliders:
            if self.xpos + self.width > col.xpos and self.xpos <= col.xpos + col.width or self.xpos < col.xpos + col.width and self.xpos + self.width >= col.xpos:
                if self.ypos + self.height > col.ypos and self.ypos <= col.ypos + col.height or self.ypos < col.ypos + col.height and self.ypos + self.height >= col.ypos:
                    col_info[0] = True
                    col_info[1] = col
                    return col_info
