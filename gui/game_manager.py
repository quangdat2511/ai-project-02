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
                'cell_breeze_stench': BREEZE_STENCH_IMAGE,
                'cell_breeze_stench_gold': BREEZE_STENCH_IMAGE_GOLD,
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

        offset_x = OFFSET_X
        offset_y = OFFSET_Y

        # Vẽ lưới và các vật thể
        for y in range(N):
            for x in range(N):
                rect = pygame.Rect(
                    offset_x + x * CELL_SIZE,
                    offset_y + (N - 1 - y) * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )

                pygame.draw.rect(surface, GRID_COLOR, rect, 3)

                cell = env.grid[x][y]
                percept = env.get_percept_in_cell((x, y))

                is_wumpus = cell.has_wumpus
                is_pit = cell.has_pit
                is_gold = cell.has_gold
                has_stench = percept.stench
                has_breeze = percept.breeze

                if is_wumpus:
                    img = self.get_image('wumpus')
                    if img: surface.blit(img, rect.topleft)
                elif is_pit:
                    img = self.get_image('pit')
                    if img: surface.blit(img, rect.topleft)
                else:
                    if is_gold and has_stench and has_breeze:
                        img = self.get_image('cell_breeze_stench_gold')
                        if img: surface.blit(img, rect.topleft)
                    else:
                        if has_stench and has_breeze:
                            img = self.get_image('cell_breeze_stench')
                            if img: surface.blit(img, rect.topleft)
                        elif has_stench:
                            img = self.get_image('cell_stench')
                            if img: surface.blit(img, rect.topleft)
                        elif has_breeze:
                            img = self.get_image('cell_breeze')
                            if img: surface.blit(img, rect.topleft)

                        if is_gold:
                            img = self.get_image('gold')
                            if img: surface.blit(img, rect.topleft)

                if agent is not None and agent.position == (x, y):
                    img = self.get_image('agent')
                    if img: surface.blit(img, rect.topleft)

        # === Vẽ score & percept bên phải lưới ===
        if agent is not None:
            font_large = self.get_font('large')

            score_x = OFFSET_X + grid_width + 20
            score_y = OFFSET_Y

            # Hiển thị Score
            score_text = font_large.render(f"Score: {agent.score}", True, (255, 255, 255))
            surface.blit(score_text, (score_x, score_y))

            # Lấy percept hiện tại
            percept = env.get_percept_in_cell(agent.position)
            percept_images = []
            if percept.stench:
                percept_images.append(self.get_image('cell_stench'))
            if percept.breeze:
                percept_images.append(self.get_image('cell_breeze'))
            if getattr(percept, "glitter", False):
                percept_images.append(self.get_image('cell_glitter'))
            if getattr(percept, "bump", False):
                percept_images.append(self.get_image('cell_bump'))
            if getattr(percept, "scream", False):
                percept_images.append(self.get_image('cell_scream'))

            # Nếu không có percept nào thì hiện "None"
            if not percept_images:
                none_text = self.get_font('normal').render("None", True, (255, 255, 255))
                surface.blit(none_text, (score_x, score_y + 50))
            else:
                # Hiển thị các hình percept ngay dưới Score
                for i, img in enumerate(percept_images):
                    if img:
                        surface.blit(img, (score_x, score_y + 50 + i * (CELL_SIZE + 5)))


