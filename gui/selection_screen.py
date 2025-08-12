from .button import Button
from .config import *
from .dropdown import Dropdown

class SelectionScreen:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.font = self.game_manager.fonts['normal']
        
        # Buttons
        self.normal = Button((450, 600), 200, 50, "Normal", COLOR_MODE_NORMAL, font=self.font, border_radius=5)
        self.advanced = Button((450, 670), 200, 50, "Advanced", COLOR_MODE_ADVANCED, font=self.font, border_radius=5)
        
        self.game_started = False
    
        self.map_dropdown = Dropdown(
            "Select Map:",
            self.game_manager.maps,
            (50, 415),
            self.font,
            200,
            40
        )

        self.agent_dropdown = Dropdown(
            "Agent:",
            self.game_manager.agents,
            (900, 415),
            self.font,
            200,
            40
        )


    def draw(self, surface):
        # Draw background
        surface.blit(self.game_manager.get_image('background'), (0, 0))
        
        # Draw UI elements
        self.normal.draw(surface)
        self.advanced.draw(surface)
        self.map_dropdown.draw(surface)
        self.agent_dropdown.draw(surface)
        
    def handle_event(self, event):
        # Kiểm tra nút Normal
        if self.normal.handle_event(event):
            self.game_started = True
            self.game_manager.current_state = "normal"
            return True
        
        # Kiểm tra nút Advanced
        if self.advanced.handle_event(event):
            self.game_started = True
            self.game_manager.current_state = "advanced"
            return True
        
        # Kiểm tra dropdown
        if self.map_dropdown.handle_event(event):
            self.game_manager.selected_map = self.map_dropdown.get_value()
        if self.agent_dropdown.handle_event(event):
            self.game_manager.selected_agent = self.agent_dropdown.get_value()
        return False
