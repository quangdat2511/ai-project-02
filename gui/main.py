# main.py (bên trong thư mục gui)
import pygame
import sys

from core import *                     # file này nằm ở thư mục gốc
from gui.config import *                     # sử dụng absolute import
from gui.game_manager import GameManager
from gui.selection_screen import SelectionScreen
from gui.gameplay_screen import GameplayScreen


# # Luồng game chính
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

            if self.game_manager.current_state == "normal" or self.game_manager.current_state == "advanced":
                self.gameplay_screen.update(dt)
            # print(self.game_manager.selected_agent)
            self.draw()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            
            if self.game_manager.current_state == "selecting":
                if self.selection_screen.handle_event(event):
                    if self.selection_screen.game_started:
                        self.gameplay_screen.initialize(
                            advanced_mode=self.game_manager.current_state == "advanced",
                            selected_map=self.game_manager.selected_map,
                            selected_agent= self.game_manager.selected_agent
                        )
            elif self.game_manager.current_state == "normal" or self.game_manager.current_state == "advanced":
                self.gameplay_screen.handle_event(event)
    
    def draw(self):
        # Dòng này để test xem giao diện có hoạt động không
        self.window.fill((50, 50, 50))  # tô nền xám để test
        if self.game_manager.current_state == "selecting":
            self.selection_screen.draw(self.window)
        elif self.game_manager.current_state == "normal" or self.game_manager.current_state == "advanced":
            self.gameplay_screen.draw(self.window, self.game_manager.current_state == "advanced", selected_map=self.game_manager.selected_map)
        
        pygame.display.flip()
    
    def quit(self):
        self.game_manager.is_running = False

        pygame.quit()
        sys.exit()

def main():
    app = App()
    app.run()
# if __name__ == "__main__":
#     main()