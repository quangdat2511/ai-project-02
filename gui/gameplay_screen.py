import pygame
from typing import List, Tuple, Optional
from gui.config import *
from .button import Button
# from state.agent import *
# from state.environment import *
import copy
class GameplayScreen:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.font = self.game_manager.fonts['large']
        self.small_font = self.game_manager.fonts['normal']

        # Game state
        #This blongs to project 01
        # self.game: Optional[Game] = None
        # self.game_loader = GameLoader()
        # self.current_state: Optional[GameState] = None
        # self.initial_state: Optional[GameState] = None

        self.current_state = None  # Current game state
        self.initial_state = None  # Initial game state
        # Solution data

        
        # Animation state
        self.is_animating = False
        self.animation_speed = 1.0  # moves per second
        self.animation_timer = 0.0
        self.is_paused = False
        
        # Search results
        
        # UI Components
        self.create_ui_components()

    def create_ui_components(self):
        button_y = HEIGHT - 70
        button_spacing = 110 
        button_width = 100 
        button_height = 40
        indent = 100 * SCALE
        
        # Control buttons
        self.play_button = Button(
            (indent, button_y), button_width, button_height,
            "Play", (0, 100, 200), font=self.font, border_radius=5
        )
        
        self.pause_button = Button(
            (indent + button_spacing, button_y), button_width, button_height,
            "Pause", (200, 100, 0), font=self.font, border_radius=5
        )
        
        self.reset_button = Button(
            (indent + button_spacing * 2, button_y), button_width, button_height,
            "Reset", (150, 0, 0), font=self.font, border_radius=5
        )
        
        self.menu_button = Button(
            (indent + button_spacing * 3, button_y), button_width, button_height,
            "Menu", (100, 100, 100), font=self.font, border_radius=5
        )
        
        # Speed control buttons
        self.speed_up_button = Button(
            (WIDTH - 140, button_y), 50, button_height,
            ">>", (0, 150, 150), font=self.font, border_radius=5
        )
        
        self.speed_down_button = Button(
            (WIDTH - 320, button_y), 50, button_height,
            "<<", (0, 150, 150), font=self.font, border_radius=5
        )
        
    def initialize(self):
        self.game = None
        self.initial_state = None
                
    def start_animation(self):
        if self.solution_path and not self.is_animating:
            self.is_animating = True
            self.is_paused = False
            self.animation_timer = 0.0
            
    def pause_animation(self):
        if self.is_animating:
            self.is_paused = not self.is_paused
            
    def reset_animation(self):
        self.current_state = copy.deepcopy(self.initial_state)
        self.current_step = 0
        self.is_animating = False
        self.is_paused = False
        self.animation_timer = 0.0
        
    def update(self, dt: float):
        if self.search_result is None or not self.search_completed:
            self.solve_game()
            return

        if self.is_animating and not self.is_paused:
            self.animation_timer += dt
            
            # Check if it's time for the next move
            if self.animation_timer >= 1.0 / self.animation_speed:
                self.animation_timer = 0.0
                
                if self.current_step < self.total_steps:
                    # Move to the next state
                    self.current_step += 1
                    self.current_state = copy.deepcopy(self.solution_states[self.current_step])
                else:
                    # Animation complete
                    self.is_animating = False
                    
    def handle_event(self, event):
        if self.play_button.handle_event(event):
            self.start_animation()
            return True
            
        if self.pause_button.handle_event(event):
            self.pause_animation()
            return True
            
        if self.reset_button.handle_event(event):
            self.reset_animation()
            return True
            
        if self.menu_button.handle_event(event):
            # Return to selection screen
            self.game_manager.current_state = "selecting"
            return True
            
        if self.speed_up_button.handle_event(event):
            self.animation_speed = min(self.animation_speed * 1.5, 10.0)
            return True
            
        if self.speed_down_button.handle_event(event):
            self.animation_speed = max(self.animation_speed / 1.5, 0.1)
            return True
            
        return False
        
    def draw(self, surface: pygame.Surface):
        # Draw background
        surface.blit(self.game_manager.get_image('background'), (0, 0))
        
        # Draw the current game state
            
        # Draw UI buttons
        
    def draw_info_text(self, surface: pygame.Surface):
        pass
            