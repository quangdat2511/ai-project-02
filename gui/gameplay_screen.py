import pygame
from typing import List, Tuple, Optional, Union
from gui.config import *
from .button import Button
from .inputbox import InputBox
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
        self.agent: Optional[Union[Agent, RandomAgent]] = None
        self.environment: Optional[Environment] = None 
        self.action_count = 0
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
        self.speed_up_button = Button(
            (indent, button_y - 70), button_width * 1.8, button_height,
            "Speed up", (100, 100, 100), font=self.font, border_radius=5
        )
        
        self.speed_down_button = Button(
            (indent + button_spacing * 2, button_y - 70), button_width * 1.8, button_height,
            "Speed down", (100, 100, 100), font=self.font, border_radius=5
        )
        # InputBox cho N, K, P
        input_y = button_y - 140
        self.input_box_N = InputBox(indent, input_y, 80, 30, text='', font=self.small_font)
        self.input_box_K = InputBox(indent + 100, input_y, 80, 30, text='', font=self.small_font)
        self.input_box_P = InputBox(indent + 200, input_y, 80, 30, text='', font=self.small_font)

        
    def initialize(self, advanced_mode: bool = True, selected_map: str = "Random", selected_agent: str = "Smart"):
        # Lấy giá trị người dùng nhập (nếu có)
        def get_input_value(input_box, default):
            try:
                return float(input_box.text) if '.' in input_box.text else int(input_box.text)
            except ValueError:
                return default

        env_configs = [
            (8, 2, 0.2, advanced_mode, None),
            (11, 2, 0.2, advanced_mode, None),
            (14, 2, 0.2, advanced_mode, None)
        ]

        print("Selected map:" + selected_map)

        if selected_map == "Random":
            # Lấy giá trị từ input box
            N = get_input_value(self.input_box_N, None)
            K = get_input_value(self.input_box_K, None)
            P = get_input_value(self.input_box_P, None)

            if N is not None and K is not None and P is not None:
                # Dùng giá trị người dùng nhập
                self.environment = Environment(N, K, P, advanced_mode, None)
            else:
                # Chọn ngẫu nhiên như cũ
                config = random.choice(env_configs)
                self.environment = Environment(*config)

        elif selected_map == "1":
            self.environment = Environment(map_id=1, advanced_mode=advanced_mode)
        elif selected_map == "2":
            self.environment = Environment(map_id=2, advanced_mode=advanced_mode)
        elif selected_map == "3":
            self.environment = Environment(map_id=3, advanced_mode=advanced_mode)
        elif selected_map == "4":
            self.environment = Environment(map_id=4, advanced_mode=advanced_mode)
        elif selected_map == "5":
            self.environment = Environment(map_id=5, advanced_mode=advanced_mode)
        else:
            raise ValueError(f"Invalid selected_map value: {selected_map}")

        # Khởi tạo Agent
        if selected_agent == "Smart":
            self.agent = Agent(K=self.environment.K, is_moving_wumpus=self.environment.advanced_mode)
        elif selected_agent == "Random":
            self.agent = RandomAgent()

                
    def start_animation(self):
        if not self.is_animating:
            self.is_animating = True
            self.is_paused = False
            self.animation_timer = 0.0
            
    def pause_animation(self):
        if self.is_animating:
            self.is_paused = not self.is_paused
            
    def reset_animation(self):
        # N = self.input_box_N.get_value(default=8)
        # K = self.input_box_K.get_value(default=2)
        # P = self.input_box_P.get_value(default=0.2)

        self.initialize(
            self.environment.advanced_mode,
            selected_map=self.game_manager.selected_map,
            selected_agent="Smart" if isinstance(self.agent, Agent) else "Random"
        )
        self.is_animating = False
        self.is_paused = False
        self.animation_timer = 0.0
        self.current_action = None  # Reset current action
        
    def update(self, dt: float):
        if self.agent and self.environment and self.is_animating and not self.is_paused and self.agent.is_alive and not self.agent.climbed_out:
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
            
        if self.speed_up_button.handle_event(event):
            self.animation_speed = min(self.animation_speed * 1.5, 10.0)
            return True
            
        if self.speed_down_button.handle_event(event):
            self.animation_speed = max(self.animation_speed / 1.5, 0.1)
            return True
        # InputBox events
        self.input_box_N.handle_event(event)
        self.input_box_K.handle_event(event)
        self.input_box_P.handle_event(event)
            
        return False    
    def draw(self, surface: pygame.Surface, advanced_mode: bool = False, selected_map: str = "Random"):
        # Draw background
        bg = self.game_manager.get_image('gamebackground')
        if bg is not None:
            surface.blit(bg, (0, 0))
        else:
            surface.fill((60, 60, 60))  # fallback background color
        self.menu_button.draw(surface)
        self.reset_button.draw(surface)
        if self.agent.climbed_out:
            self.game_manager.drawAgentClimbout(surface, self.agent.score)
        elif not self.agent.is_alive:
            self.game_manager.drawAgentDead(surface, self.agent.score)
        else:

            self.game_manager.draw_environment(surface, self.environment, self.agent, self.current_action)
            # Draw UI buttons
            self.play_button.draw(surface)
            self.pause_button.draw(surface)
            
            self.speed_up_button.draw(surface)
            self.speed_down_button.draw(surface)
            # Draw InputBox + label chỉ khi map là Random
            if self.game_manager.selected_map == "Random":
                self.input_box_N.draw(surface)
                self.input_box_K.draw(surface)
                self.input_box_P.draw(surface)

                # Label N, K, P
                label_font = self.game_manager.fonts['normal']
                surface.blit(label_font.render("N(max 16)", True, (255, 255, 255)),
                            (self.input_box_N.rect.x, self.input_box_N.rect.y - 20))
                surface.blit(label_font.render("K", True, (255, 255, 255)),
                            (self.input_box_K.rect.x, self.input_box_K.rect.y - 20))
                surface.blit(label_font.render("P(float)", True, (255, 255, 255)),
                            (self.input_box_P.rect.x, self.input_box_P.rect.y - 20))