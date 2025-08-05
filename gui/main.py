import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from definition import *
import pygame
import sys
from config import *
from game_manager import GameManager
from selection_screen import SelectionScreen
from gameplay_screen import GameplayScreen
# Luồng game chính
class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        
        self.game_manager = GameManager()
        self.selection_screen = SelectionScreen(self.game_manager)
        self.gameplay_screen = GameplayScreen(self.game_manager)
        
    def run(self):
        while self.game_manager.is_running:
            dt = self.clock.tick(60) / 1000.0  # 60 FPS
            
            self.handle_events()

            self.draw()

            if self.game_manager.current_state == "playing":
                self.gameplay_screen.update(dt)
                
            self.draw()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            
            if self.game_manager.current_state == "selecting":
                if self.selection_screen.handle_event(event):
                    if self.selection_screen.game_started:
                        self.game_manager.current_state = "playing"
                        self.gameplay_screen.initialize(self.game_manager.selected_map, self.game_manager.selected_algorithm)
                        
            elif self.game_manager.current_state == "playing":
                self.gameplay_screen.handle_event(event)
    
    def draw(self):
        if self.game_manager.current_state == "selecting":
            self.selection_screen.draw(self.window)
        elif self.game_manager.current_state == "playing":
            self.gameplay_screen.draw(self.window)
        
        pygame.display.flip()
    
    def quit(self):
        self.game_manager.is_running = False

        pygame.quit()
        sys.exit()

def main():
    app = App()
    app.run()
# def main():
#     Dang = Agent(8)
#     Dang.add_percept(Percept(False, False), 0, 0)
#     Dang.add_percept(Percept(False, False), 1, 0)
#     Dang.add_percept(Percept(False, False), 2, 0)
#     Dang.add_percept(Percept(False, True), 3, 0)
#     x = 4
#     y = 0
#     query_1 = Literal("Wumpus", x, y, True)
#     query_2 = Literal("Pit", x, y, True)

#     if Dang.kb.infer(query_1) and Dang.kb.infer(query_2):
#         print("(" + str(x) + ", " + str(y) + ") is safe")
#     else:
#         print("(" + str(x) + ", " + str(y) + ") is not safe")

# main()