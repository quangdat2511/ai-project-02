import pygame
from typing import List, Tuple, Optional
from gui.config import *
from .button import Button
from state.environment import *
from state.agent import *
import copy
import random
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
        self.current_action = None
        # UI Components
        self.create_ui_components()

    def create_ui_components(self):
        button_y = HEIGHT - 70
        button_spacing = 80 
        button_width = 80 
        button_height = 30
        indent = (100 * SCALE) + 780  
        
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
        # self.speed_up_button = Button(
        #     (WIDTH - 140, button_y), 50, button_height,
        #     ">>", (0, 150, 150), font=self.font, border_radius=5
        # )
        
        # self.speed_down_button = Button(
        #     (WIDTH - 320, button_y), 50, button_height,
        #     "<<", (0, 150, 150), font=self.font, border_radius=5
        # )
        
    def initialize(self):
        # Danh sách các cấu hình Environment
        env_configs = [
            # (8, 2, 0.2, False, None),
            # (12, 2, 0.2, False, None),
            # (16, 2, 0.2, False, None),
            # (2, 2, 0.2, False, None)
            (8, 10, 0.5, False, None),
            (12, 10, 0.5, False, None),
            (16, 10, 0.5, False, None),
            (2, 2, 0.2, False, None)
        ]

        # Chọn ngẫu nhiên một cấu hình
        config = random.choice(env_configs)

        # Tạo Environment và Agent
        self.environment = Environment(*config)
        self.agent = Agent(2) 
                
    def start_animation(self):
        if not self.is_animating:
            self.is_animating = True
            self.is_paused = False
            self.animation_timer = 0.0
            
    def pause_animation(self):
        if self.is_animating:
            self.is_paused = not self.is_paused
            
    def reset_animation(self):
        self.initialize()  # Reset environment and agent
        self.is_animating = False
        self.is_paused = False
        self.animation_timer = 0.0
        self.current_action = None  # Reset current action
        
    def update(self, dt: float):
        if self.agent and self.environment and self.is_animating and not self.is_paused and self.agent.is_alive and not self.agent.winning:
            self.animation_timer += dt
            if self.animation_timer >= 1.0 / self.animation_speed:
                self.animation_timer = 0.0
                self.current_action = self.agent.play_one_action(self.environment)
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
            
        # if self.speed_up_button.handle_event(event):
        #     self.animation_speed = min(self.animation_speed * 1.5, 10.0)
        #     return True
            
        # if self.speed_down_button.handle_event(event):
        #     self.animation_speed = max(self.animation_speed / 1.5, 0.1)
        #     return True
            
        return False    
    def draw(self, surface: pygame.Surface):
        # Draw background
        bg = self.game_manager.get_image('gamebackground')
        if bg is not None:
            surface.blit(bg, (0, 0))
        else:
            surface.fill((60, 60, 60))  # fallback background color
        self.menu_button.draw(surface)
        self.reset_button.draw(surface)
        if self.agent.winning:
            self.game_manager.drawAgentWinning(surface, self.agent.score)
        elif not self.agent.is_alive:
            self.game_manager.drawAgentLost(surface, self.agent.score)
        else:

            self.game_manager.draw_environment(surface, self.environment, self.agent, self.current_action)
            # Draw UI buttons
            self.play_button.draw(surface)
            self.pause_button.draw(surface)

            # self.speed_up_button.draw(surface)
            # self.speed_down_button.draw(surface)

    def draw_info_text(self, surface: pygame.Surface):
        pass
