from .dropdown import Dropdown
from .button import Button
from .config import *

class SelectionScreen:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.font = self.game_manager.fonts['normal']
        self.normal = Button((450, 600), 200, 50, "Normal", COLOR_MODE_NORMAL, font=self.font, border_radius=5)
        self.advanced = Button((450, 670), 200, 50, "Advanced", COLOR_MODE_ADVANCED, font=self.font, border_radius=5)
        self.game_started = False
    def draw(self, surface):
        # Draw background
        surface.blit(self.game_manager.get_image('background'), (0, 0))
        # Draw UI elements
        self.normal.draw(surface)
        self.advanced.draw(surface)

    def handle_event(self, event):
        # Check if start button clicked
        if self.normal.handle_event(event):
            self.game_started = True
            self.game_manager.current_state = "normal"
            return True
        if self.advanced.handle_event(event):
            self.game_started = True
            self.game_manager.current_state = "advanced"
            return True
        return False