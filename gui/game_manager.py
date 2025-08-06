import pygame
from typing import Dict, List
from gui.config import *


class GameManager:
    def __init__(self):
        # asset manager
        self.images: Dict[str, pygame.Surface] = {}
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.load_assets()

        # game state
        self.current_state = "selecting"
        self.is_running = True
    

    def load_assets(self):
        # background image
        try:
            self.images['background'] = pygame.image.load(BACKGROUND_IMAGE)
            self.images['background'] = pygame.transform.scale(self.images['background'], (WIDTH, HEIGHT))
        except Exception as e:
            print("Lỗi khi load background:", e)

        # fonts
        self.fonts['normal'] = pygame.font.SysFont(FONT_NAME, FONT_SIZE, True)
        self.fonts['large'] = pygame.font.SysFont(FONT_NAME, FONT_SIZE_LARGE, True)
    

    def get_image(self, name: str) -> pygame.Surface:
        return self.images.get(name)
    
    def get_font(self, size: str = 'normal') -> pygame.font.Font:
        return self.fonts.get(size, self.fonts['normal'])
