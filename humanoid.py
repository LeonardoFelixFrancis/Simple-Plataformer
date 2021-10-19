import pygame

class humanoid():
    def __init__(self, xpos,ypos,height,width,speed_value, jump_value,img, life, dmg):
        self.xpos = xpos
        self.ypos = ypos
        self.speed_value = speed_value
        self.life = life
        self.dmg = dmg
        self.speed = [0,0]
        self.width = width
        self.height = height
        self.img = pygame.transform.scale(pygame.image.load(img), (width, height))
        self.is_grounded = False
        self.jump_value = jump_value
        self.jump_force = self.jump_value
        self.dir_x = 1
        self.is_alert = False
        self.time_to_dmg = 1 * 60
        self.acutal_time_to_dmg = 0

    def change_speed(self, axis, dir):
        if axis == "x":
            self.speed[0] = dir * self.speed_value
            if dir != 0:
                self.dir_x = dir
        elif axis == "y":
            if dir > 0:
                self.speed[1] = dir * self.speed_value * 3
            else:
                self.speed[1] = dir * self.jump_force
        
        if not self.is_grounded:
            self.speed[0] = self.speed[0]/2

    def move(self, coliders):
        col_type = {"Left":False, "Right":False, "Top":False,"Bottom":False}
        for col in coliders:

            

            if self.xpos + self.speed[0]/2 <= col.xpos+col.width and self.ypos < col.ypos+col.height and self.ypos+self.height > col.ypos and self.xpos >= col.xpos:
                col_type["Left"] = True
            if self.xpos+self.width+self.speed[0]/2 >= col.xpos and self.ypos < col.ypos+col.height and self.ypos+self.height > col.ypos and self.xpos <= col.xpos:
                col_type["Right"] = True
            if self.ypos + self.speed[1]/2 <= col.ypos+col.height and self.xpos < col.xpos+col.width - self.jump_value and self.xpos+self.width > col.xpos + self.jump_value  and self.ypos >= col.ypos:
                col_type["Top"] = True
                self.change_speed("y", 1)
                if self.speed[1] < 0:
                    self.speed[1] = 0
            if self.ypos+self.height + self.speed[1]/2 >= col.ypos and self.xpos < col.xpos+col.width - self.jump_value and self.xpos+self.width > col.xpos + self.jump_value and self.ypos <= col.ypos:
                col_type["Bottom"] = True
                self.is_grounded = True
                self.speed[1] = 0
                self.ypos = col.ypos - self.height


        if not col_type["Bottom"] and self.speed[1] > 0:
            self.ypos += self.speed[1]            
        if not col_type["Top"] and self.speed[1] < 0:
            self.ypos += self.speed[1]        
        if not col_type["Left"] and self.speed[0] < 0:
            self.xpos += self.speed[0]
        if not col_type["Right"] and self.speed[0] > 0:
            self.xpos += self.speed[0]
    
    def artificial_inteligence(self, obj_to_follow, tiles):
        is_seeing_enemy = True

        if self.ypos < obj_to_follow.ypos + obj_to_follow.height and self.ypos + self.height > obj_to_follow.ypos:
            if self.xpos > obj_to_follow.xpos:
                for t in tiles:
                    if self.ypos < t.ypos + t.height and self.ypos + self.height >= t.ypos + 1:
                        if t.xpos + t.width < self.xpos and t.xpos + t.width > obj_to_follow.xpos:
                            is_seeing_enemy = False 


                if is_seeing_enemy:
                    if self.dir_x == 1:
                        img = self.img
                        img_fliped = pygame.transform.flip(img, True, False)
                        self.img = img_fliped
                    self.change_speed("x", -1)
            elif self.xpos < obj_to_follow.xpos:
                for t in tiles:
                    if self.ypos < t.ypos + obj_to_follow.height and self.ypos + self.height >= t.ypos + 1:
                        if t.xpos > self.xpos + self.width and t.xpos < obj_to_follow.xpos + obj_to_follow.width:
                            is_seeing_enemy = False

                if is_seeing_enemy:
                    if self.dir_x == -1:
                        img = self.img
                        img_fliped = pygame.transform.flip(img, True, False)
                        self.img = img_fliped
                    self.change_speed("x", 1)
            
            
            if self.xpos - 1 <= obj_to_follow.xpos + obj_to_follow.width and self.xpos + self.width >= obj_to_follow.xpos and self.acutal_time_to_dmg <=0:
                obj_to_follow.life -= self.dmg
                self.acutal_time_to_dmg = self.time_to_dmg
           
            elif self.xpos + 1 + self.width >= obj_to_follow.xpos - 1 and self.xpos <= obj_to_follow.xpos and self.acutal_time_to_dmg <=0:
                obj_to_follow.life -= self.dmg
                self.acutal_time_to_dmg = self.time_to_dmg
           
            self.acutal_time_to_dmg -=0.5


    def player_won(self, finish_line):
        if self.xpos + self.width > finish_line.xpos and self.xpos <= finish_line.xpos + finish_line.width or self.xpos < finish_line.xpos + finish_line.width and self.xpos + self.width >= finish_line.xpos:
            if self.ypos + self.height > finish_line.ypos and self.ypos <= finish_line.ypos + finish_line.height or self.ypos < finish_line.ypos + finish_line.height and self.ypos + self.height >= finish_line.ypos:
                return True

    def collided_with(self, colliders):
        try:
            for col in colliders:
                if self.xpos + self.width > col.xpos and self.xpos <= col.xpos + col.width or self.xpos < col.xpos + col.width and self.xpos + self.width >= col.xpos:
                    if self.ypos + self.height > col.ypos and self.ypos <= col.ypos + col.height or self.ypos < col.ypos + col.height and self.ypos + self.height >= col.ypos:
                        return col
        except:
            if self.xpos + self.width >= colliders.xpos and self.xpos <= colliders.xpos + colliders.width or self.xpos <= colliders.xpos + colliders.width and self.xpos + self.width >= colliders.xpos:
                    if self.ypos + self.height >= colliders.ypos and self.ypos <= colliders.ypos + colliders.height or self.ypos <= colliders.ypos + colliders.height and self.ypos + self.height >= colliders.ypos:
                        return colliders
    def game_over(self):
        if self.life <= 0:
            return True
