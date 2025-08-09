import pygame
from typing import List, Tuple, Optional
from gui.config import *
from .button import Button
from state.environment import *
from state.agent import *
import copy
class GameplayScreen:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.font = self.game_manager.fonts['large']
        self.small_font = self.game_manager.fonts['normal']


        # State variables
        self.agent: Optional[Agent] = None  # Current agent state
        self.environment: Optional[Environment] = None 
        
        # Animation state
        self.is_animating = False
        self.animation_speed = 1.0  # moves per second
        self.animation_timer = 0.0
        self.is_paused = False
        
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
        self.environment = Environment(16)  
        self.agent = Agent()   
                
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
        
    def draw(self, surface: pygame.Surface):
        # Draw background
        bg = self.game_manager.get_image('gamebackground')
        if bg is not None:
            surface.blit(bg, (0, 0))
        else:
            surface.fill((60, 60, 60))  # fallback background color
        # Draw the current game state
        if self.environment is not None and self.agent is not None:
            self.game_manager.draw_environment(surface, self.environment, self.agent)
        # Draw UI buttons   
        
    def draw_info_text(self, surface: pygame.Surface):
        pass
            