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
                'cell_wumpus': CELL_WUMPUS,
                'cell_pit': CELL_PIT,
                'gold': CELL_GOLD,
                'glitter': GLITTER,
                'bump': BUMP,
                'scream': SCREAM,
                'agent_left': AGENT_LEFT,
                'agent_right': AGENT_RIGHT,
                'agent_up': AGENT_UP,
                'agent_down': AGENT_DOWN,
                'agent_victory': AGENT_VICTORY,
                'agent_lost': AGENT_LOST,
                'cell_stench': CELL_STENCH,
                'cell_breeze': CELL_BREEZE,
                'cell_breeze_stench': CELL_BREEZE_STENCH,
                'cell_breeze_stench_gold': CELL_BREEZE_STENCH_GOLD,
                'cell_breeze_gold': CELL_BREEZE_GOLD,
                'cell_stench_gold': CELL_STENCH_GOLD,
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
    def drawAgentWinning(self, surface: pygame.Surface, score: int = 0):
        img = self.get_image('agent_victory')
        if img:
            # Scale ảnh
            new_width = WIDTH // 3
            new_height = HEIGHT // 3
            img = pygame.transform.scale(img, (new_width, new_height))

            # Căn giữa
            x = (WIDTH - new_width) // 2
            y = (HEIGHT - new_height) // 2
            surface.blit(img, (x, y))

            # Thêm chữ "Agent Win"
            font = self.get_font('large')
            text_surface = font.render("Agent Win", True, (255, 255, 0))  # vàng
            text_x = (WIDTH - text_surface.get_width()) // 2
            text_y = y + new_height + 20  # cách ảnh 20px
            surface.blit(text_surface, (text_x, text_y))
            # Hiển thị điểm số
            score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))  # trắng
            score_x = (WIDTH - score_text.get_width()) // 2
            score_y = text_y + 40  # cách chữ "Agent Win" 20px
            surface.blit(score_text, (score_x, score_y))



    def drawAgentLost(self, surface: pygame.Surface, score: int = 0):
        img = self.get_image('agent_lost')
        if img:
            # Scale ảnh
            new_width = WIDTH // 3
            new_height = HEIGHT // 3
            img = pygame.transform.scale(img, (new_width, new_height))

            # Căn giữa
            x = (WIDTH - new_width) // 2
            y = (HEIGHT - new_height) // 2
            surface.blit(img, (x, y))

            # Thêm chữ "Agent Lost"
            font = self.get_font('large')
            text_surface = font.render("Agent Lost", True, (255, 0, 0))  # đỏ
            text_x = (WIDTH - text_surface.get_width()) // 2
            text_y = y + new_height + 20
            surface.blit(text_surface, (text_x, text_y))
            # Hiển thị điểm số
            score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
            score_x = (WIDTH - score_text.get_width()) // 2
            score_y = text_y + 40
            surface.blit(score_text, (score_x, score_y))
            



    def draw_environment(self, surface: pygame.Surface, env: Environment, agent: 'Agent' = None, current_action: Action = None):
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
                if agent is not None and agent.position == (x, y):
                    if agent.direction == Direction.NORTH:
                        img = self.get_image('agent_up')
                    elif agent.direction == Direction.EAST:
                        img = self.get_image('agent_right')
                    elif agent.direction == Direction.SOUTH:
                        img = self.get_image('agent_down')
                    elif agent.direction == Direction.WEST:
                        img = self.get_image('agent_left')
                    if img: surface.blit(img, rect.topleft)
                    continue  # Skip drawing the cell if agent is there
                pygame.draw.rect(surface, GRID_COLOR, rect, 3)

                cell = env.grid[x][y]
                percept = env.get_percept_in_cell((x, y))

                is_wumpus = cell.has_wumpus
                is_pit = cell.has_pit
                is_gold = cell.has_gold
                has_stench = percept.stench
                has_breeze = percept.breeze


                if is_wumpus:
                    img = self.get_image('cell_wumpus')
                    if img: surface.blit(img, rect.topleft)
                elif is_pit:
                    img = self.get_image('cell_pit')
                    if img: surface.blit(img, rect.topleft)
                else:
                    if is_gold and has_stench and has_breeze:
                        img = self.get_image('cell_breeze_stench_gold')
                        if img: surface.blit(img, rect.topleft)
                    else:
                        if has_stench and has_breeze:
                            img = self.get_image('cell_breeze_stench')
                            if img: surface.blit(img, rect.topleft)
                        elif has_breeze and is_gold:
                            img = self.get_image('cell_breeze_gold')
                            if img: surface.blit(img, rect.topleft)
                        elif has_stench and is_gold:
                            img = self.get_image('cell_stench_gold')
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


        # score, last action, last percept
        # === Vẽ score & percept bên phải lưới ===
        if agent is not None:
            font_large = self.get_font('large')

            score_x = OFFSET_X + grid_width + 20
            score_y = OFFSET_Y

            # Hiển thị Score
            # Draw mode
            mode_text = mode_text = font_large.render("Normal Mode", True, (255, 255, 255))
            if env.advanced_mode:
                mode_text = font_large.render("Advanced Mode", True, (255, 255, 255))
            # # Hiển thị số action đã thực hiện
            action_count_text = font_large.render(f"Action count: {agent.action_count}", True, (255, 255, 255))
            surface.blit(action_count_text, (score_x, score_y + 60))
            # Hiển thị điểm số
            score_text = font_large.render(f"Score: {agent.score}", True, (255, 255, 255))
            surface.blit(score_text, (score_x, score_y + 30))
            surface.blit(mode_text, (score_x, score_y))
            # Lấy percept hiện tại
            percept = env.get_percept_in_cell(agent.position)
                #             glitter = percept.glitter
                # bump = percept.bump
            percept_images = []
            if percept.stench:
                percept_images.append(self.get_image('cell_stench'))
            if percept.breeze:
                percept_images.append(self.get_image('cell_breeze'))
            if percept.glitter:
                percept_images.append(self.get_image('glitter'))
            if percept.bump:
                percept_images.append(self.get_image('bump'))
            if percept.scream:
                percept_images.append(self.get_image('scream'))
            # if getattr(percept, "bump", False):
            #     percept_images.append(self.get_image('cell_bump'))
            # if getattr(percept, "scream", False):
            #     percept_images.append(self.get_image('cell_scream'))
            # Thêm chữ "Current Percept" trước các ảnh percept
            title_text = self.get_font('normal').render("Current Percept:", True, (255, 255, 0))
            surface.blit(title_text, (score_x, score_y + 90))
            # Nếu không có percept nào thì hiện "None"
            if not percept_images:
                none_text = self.get_font('normal').render("None", True, (255, 255, 255))
                surface.blit(none_text, (score_x, score_y + 110))
            else:
                # Hiển thị các hình percept ngay dưới dòng chữ
                for i, img in enumerate(percept_images):
                    if img:
                        surface.blit(img, (score_x, score_y + 110 + i * (CELL_SIZE + 5)))
            # Hiển thị hành động hiện tại
            if current_action is not None:
                action_text = self.get_font('normal').render(f"Last Action: {current_action.value}", True, (255, 255, 255))
                surface.blit(action_text, (score_x, score_y + 110 + len(percept_images) * (CELL_SIZE + 5) + 20))


