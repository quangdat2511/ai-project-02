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
        self.maps: List[str] = ["1", "2", "3", "4", "5", "Random"]
        self.agents: List[str] = ["Smart", "Random"]
        self.load_assets()
        # game state
        self.current_state = "selecting"
        self.is_running = True
        self.selected_agent = "Smart"
        self.selected_map = "1"
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
                self.images[key] = pygame.transform.scale(image, (CELL_SIZE * 0.90, CELL_SIZE * 0.90))

        except Exception as e:
            print("Lỗi khi load assets:", e)

        # fonts
        self.fonts['normal'] = pygame.font.SysFont(FONT_NAME, FONT_SIZE, True)
        self.fonts['large'] = pygame.font.SysFont(FONT_NAME, FONT_SIZE_LARGE, True)

    def get_image(self, name: str) -> pygame.Surface:
        return self.images.get(name)

    def get_font(self, size: str = 'normal') -> pygame.font.Font:
        return self.fonts.get(size, self.fonts['normal'])
    def drawAgentClimbout(self, surface: pygame.Surface, score: int = 0):
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
            text_surface = font.render("The agent has climbed out", True, (255, 255, 0))  # vàng
            text_x = (WIDTH - text_surface.get_width()) // 2
            text_y = y + new_height + 20  # cách ảnh 20px
            surface.blit(text_surface, (text_x, text_y))
            # Hiển thị điểm số
            score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))  # trắng
            score_x = (WIDTH - score_text.get_width()) // 2
            score_y = text_y + 40  # cách chữ "Agent Win" 20px
            surface.blit(score_text, (score_x, score_y))



    def drawAgentDead(self, surface: pygame.Surface, score: int = 0):
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
            text_surface = font.render("Agent is dead", True, (255, 0, 0))  # đỏ
            text_x = (WIDTH - text_surface.get_width()) // 2
            text_y = y + new_height + 20
            surface.blit(text_surface, (text_x, text_y))
            # Hiển thị điểm số
            score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
            score_x = (WIDTH - score_text.get_width()) // 2
            score_y = text_y + 40
            surface.blit(score_text, (score_x, score_y))
            


    def draw_cell_image(self, surface, img, rect, scale=0.4):
        # Thu nhỏ ảnh theo tỉ lệ
        new_w = int(rect.width * scale)
        new_h = int(rect.height * scale)
        img = pygame.transform.smoothscale(img, (new_w, new_h))

        # Căn giữa ảnh trong ô
        img_rect = img.get_rect(center=rect.center)
        surface.blit(img, img_rect.topleft)
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
                pygame.draw.rect(surface, GRID_COLOR, rect, 3)
                if agent is not None and agent.position == (x, y):
                    if agent.direction == Direction.NORTH:
                        img = self.get_image('agent_up')
                    elif agent.direction == Direction.EAST:
                        img = self.get_image('agent_right')
                    elif agent.direction == Direction.SOUTH:
                        img = self.get_image('agent_down')
                    elif agent.direction == Direction.WEST:
                        img = self.get_image('agent_left')
                    if img:
                        img_rect = img.get_rect(center=rect.center)
                        surface.blit(img, img_rect.topleft)
                    continue  # Skip drawing the cell if agent is there


                cell = env.grid[x][y]
                percept = env.get_percept_in_cell((x, y))

                is_wumpus = cell.has_wumpus
                is_pit = cell.has_pit
                is_gold = cell.has_gold
                has_stench = percept.stench
                has_breeze = percept.breeze


                if is_wumpus:
                    img = self.get_image('cell_wumpus')
                    if img:
                        img_rect = img.get_rect(center=rect.center)
                        surface.blit(img, img_rect.topleft)
                elif is_pit:
                    img = self.get_image('cell_pit')
                    if img:
                        img_rect = img.get_rect(center=rect.center)
                        surface.blit(img, img_rect.topleft)
                else:
                        if is_gold and has_stench and has_breeze:
                            img = self.get_image('cell_breeze_stench_gold')
                            if img:
                                img_rect = img.get_rect(center=rect.center)
                                surface.blit(img, img_rect.topleft)
                        else:
                            if has_stench and has_breeze:
                                img = self.get_image('cell_breeze_stench')
                                if img: self.draw_cell_image(surface, img, rect, 0.6)
                            elif has_breeze and is_gold:
                                img = self.get_image('cell_breeze_gold')
                                if img:
                                    img_rect = img.get_rect(center=rect.center)
                                    surface.blit(img, img_rect.topleft)
                            elif has_stench and is_gold:
                                img = self.get_image('cell_stench_gold')
                                if img:
                                    img_rect = img.get_rect(center=rect.center)
                                    surface.blit(img, img_rect.topleft)
                            elif has_stench:
                                img = self.get_image('cell_stench')
                                if img: self.draw_cell_image(surface, img, rect)
                            elif has_breeze:
                                img = self.get_image('cell_breeze')
                                if img: self.draw_cell_image(surface, img, rect)
                            elif is_gold:
                                img = self.get_image('gold')
                                if img:
                                    img_rect = img.get_rect(center=rect.center)
                                    surface.blit(img, img_rect.topleft)


        # score, last action, last percept
        # === Vẽ score & percept bên phải lưới ===
        if agent is not None:
            font_large = self.get_font('large')
            font_normal = self.get_font('normal')

            score_x = OFFSET_X + grid_width + 20
            score_y = OFFSET_Y

            # Thêm Selected Map & Agent
            selected_map_text = font_large.render(f"Map: {self.selected_map}", True, (200, 200, 200))
            selected_agent_text = font_large.render(f"Agent: {self.selected_agent}", True, (200, 200, 200))
            surface.blit(selected_map_text, (score_x, score_y))
            surface.blit(selected_agent_text, (score_x, score_y + 30))

            # Mode text
            if env.advanced_mode:
                mode_text = font_large.render("Advanced Mode", True, COLOR_MODE_ADVANCED)
            else:
                mode_text = font_large.render("Normal Mode", True, COLOR_MODE_NORMAL)

            action_count_text = font_large.render(
                f"Action count: {agent.action_count}",
                True,
                COLOR_ACTION_COUNT
            )

            score_text = font_large.render(
                f"Score: {agent.score}",
                True,
                COLOR_SCORE
            )

            # Vẽ các thông tin khác
            surface.blit(mode_text, (score_x, score_y + 60))
            surface.blit(score_text, (score_x, score_y + 90))
            surface.blit(action_count_text, (score_x, score_y + 120))

            # Percept
            if isinstance(agent, Agent):
                percept = agent.current_percept
                if percept:
                    percept_list = []
                    if percept.stench:
                        percept_list.append(("Stench", self.get_image('cell_stench')))
                    if percept.breeze:
                        percept_list.append(("Breeze", self.get_image('cell_breeze')))
                    if percept.glitter:
                        percept_list.append(("Glitter", self.get_image('glitter')))
                    if percept.bump:
                        percept_list.append(("Bump", self.get_image('bump')))
                    if percept.scream:
                        percept_list.append(("Scream", self.get_image('scream')))

                    title_text = font_normal.render("Current Percept:", True, COLOR_PERCEPT_TITLE)
                    surface.blit(title_text, (score_x, score_y + 150))

                    if not percept_list:
                        none_text = font_normal.render("None", True, COLOR_PERCEPT_NONE)
                        surface.blit(none_text, (score_x, score_y + 180))
                    else:
                        for i, (label, img) in enumerate(percept_list):
                            y_pos = score_y + 180 + i * (CELL_SIZE + 5)
                            if img:
                                surface.blit(img, (score_x, y_pos))
                            label_text = font_normal.render(label, True, (255, 255, 255))
                            surface.blit(label_text, (score_x + CELL_SIZE + 5, y_pos + CELL_SIZE // 4))

            # Last action
            if current_action is not None:
                action_text = font_normal.render(
                    f"Last Action: {current_action.value}",
                    True,
                    COLOR_LAST_ACTION
                )
                surface.blit(action_text, (score_x, score_y + 180 + len(percept_list) * (CELL_SIZE + 5) + 20))




