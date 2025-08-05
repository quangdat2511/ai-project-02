from .dropdown import Dropdown
from .button import Button
from .config import *

class SelectionScreen:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.font = self.game_manager.fonts['normal']
        self.map_dropdown = Dropdown("Select Map:", self.game_manager.map_names, (50, 50), self.font, 200, 40)
        self.start_button = Button((650, 70), 200, 50, "Solve", (0, 150, 0), font=self.font, border_radius=5)
        
        self.game_started = False
    def draw(self, surface):
    # Draw background
        surface.blit(self.game_manager.get_image('background'), (0, 0))
    def handle_event(self, event):
        # Check if start button clicked
        if self.start_button.handle_event(event):
            self.game_started = True
            return True

        return False