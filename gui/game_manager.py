import pygame
from typing import Dict
from gui.config import *
from state.environment import *
from state.agent import *

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
        try:
            # Load background
            self.images['background'] = pygame.image.load(BACKGROUND_IMAGE)
            self.images['background'] = pygame.transform.scale(self.images['background'], (int(WIDTH), int(HEIGHT)))

            self.images['gamebackground'] = pygame.image.load(GAME_BACKGROUND_IMAGE)
            self.images['gamebackground'] = pygame.transform.scale(self.images['gamebackground'], (int(WIDTH), int(HEIGHT)))

            # Load game elements
            asset_paths = {
                'wumpus': WUMPUS_IMAGE,
                'pit': PIT_IMAGE,
                'gold': GOLD_IMAGE,
                'agent': AGENT_IMAGE,
                'cell_stench': STENCH_IMAGE,
                'cell_breeze': BREEZE_IMAGE,
                'cell_breeze_stench': BREEZE_STENCH_IMAGE
            }

            for key, path in asset_paths.items():
                image = pygame.image.load(path)
                self.images[key] = pygame.transform.scale(image, (CELL_SIZE * 0.98, CELL_SIZE * 0.98))

        except Exception as e:
            print("Lỗi khi load assets:", e)

        # fonts
        self.fonts['normal'] = pygame.font.SysFont(FONT_NAME, FONT_SIZE, True)
        self.fonts['large'] = pygame.font.SysFont(FONT_NAME, FONT_SIZE_LARGE, True)

    def get_image(self, name: str) -> pygame.Surface:
        return self.images.get(name)

    def get_font(self, size: str = 'normal') -> pygame.font.Font:
        return self.fonts.get(size, self.fonts['normal'])

    def draw_environment(self, surface: pygame.Surface, env: Environment, agent: 'Agent' = None):
        N = env.N  # Lưới NxN

        grid_width = CELL_SIZE * N
        grid_height = CELL_SIZE * N

        # Tính lề để căn giữa lưới
        # offset_x = (surface.get_width() - grid_width) // 2
        # offset_y = (surface.get_height() - grid_height) // 2
        offset_x = OFFSET_X
        offset_y = OFFSET_Y
        for y in range(N):
            for x in range(N):
                # Tính vị trí vẽ ô (gốc tọa độ ở trên cùng bên trái)
                rect = pygame.Rect(
                    offset_x + x * CELL_SIZE,
                    offset_y + (N - 1 - y) * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )

                # Chỉ vẽ viền ô, không fill màu nền
                pygame.draw.rect(surface, GRID_COLOR, rect, 3)  # Đường viền dày hơn

                cell = env.grid[x][y]
                percept = env.get_percept_in_cell((x, y))

                # # Vẽ percept
                # if percept.stench and percept.breeze:
                #     img = self.get_image('cell_breeze_stench')
                #     if img:
                #         surface.blit(img, rect.topleft)
                # elif percept.stench:
                #     img = self.get_image('cell_stench')
                #     if img:
                #         surface.blit(img, rect.topleft)
                # elif percept.breeze:
                #     img = self.get_image('cell_breeze')
                #     if img:
                #         surface.blit(img, rect.topleft)

                # Vẽ vật thể
                if cell.has_wumpus:
                    img = self.get_image('wumpus')
                    if img:
                        surface.blit(img, rect.topleft)
                elif cell.has_pit:
                    img = self.get_image('pit')
                    if img:
                        surface.blit(img, rect.topleft)
                elif cell.has_gold:
                    img = self.get_image('gold')
                    if img:
                        surface.blit(img, rect.topleft)

                # Vẽ agent nếu đang ở ô này
                if agent is not None and agent.position == (x, y):
                    img = self.get_image('agent')
                    if img:
                        surface.blit(img, rect.topleft)




