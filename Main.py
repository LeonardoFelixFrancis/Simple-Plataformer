import pygame
from game_handle import *

game = game_handle("Game", 900,1280)
game.load_map()
game.get_objects_from_map()
clock = pygame.time.Clock()
def main():
    clock.tick(60)
    game.create_window()
    game.handle_events()
    game.update()
    game.render()
    
if __name__ == "__main__":
    try:
        while game.app_is_runing:
            main()
    except:
        print("game overdd")
