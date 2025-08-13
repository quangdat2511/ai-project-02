WINDOW_TITLE = "Project 02 - Wumpus World Agent"
# lưu tên file, thông số
SCALE = 0.45  # Scale factor for the game window and images
FONT_SIZE_SCALE = 0.85  # Scale factor for font sizes
WIDTH, HEIGHT = 2560 * SCALE, 1800* SCALE  # Widened window (e.g., 2560x1920)
ROWS, COLS = 6, 6
TILE_SIZE = 880 / 6 * SCALE  # Size of each tile in pixels
OFFSET_X, OFFSET_Y = 100 * SCALE, 30 * SCALE  # Offset for centering the grid in the window
CELL_SIZE = 48  # Size of each cell in pixels
# Font settings
FONT_NAME = 'comicsans'
FONT_SIZE = int(20 * FONT_SIZE_SCALE)  # Base font size
FONT_SIZE_LARGE = int(30 * FONT_SIZE_SCALE)  # Large font size
CELL_COLOR = (230, 230, 230)   # Nền ô: xám nhạt
GRID_COLOR = (100, 100, 100)   # Viền ô: xám đậm
# Màu sắc
COLOR_MODE_NORMAL = (0, 200, 255)      # xanh cyan
COLOR_MODE_ADVANCED = (255, 100, 0)    # cam
COLOR_SCORE = (255, 215, 0)            # vàng gold
COLOR_ACTION_COUNT = (144, 238, 144)   # xanh lá nhạt
COLOR_PERCEPT_TITLE = (255, 255, 0)    # vàng
COLOR_PERCEPT_NONE = (200, 200, 200)   # xám nhạt
COLOR_LAST_ACTION = (255, 105, 180)    # hồng
# Resource paths
BACKGROUND_IMAGE = 'gui/assets/background.png'
DESCRIPTION_BACKGROUND_IMAGE = 'gui/assets/description-bg.png'
GAME_BACKGROUND_IMAGE = 'gui/assets/game-bg-2.png'
#AGENT

AGENT_VICTORY = 'gui/assets/agent_victory_2.png'
AGENT_LOST = 'gui/assets/agent_lost.png'
AGENT_SIDE_IMAGE = 'gui/assets/agent_side.png'

AGENT_LEFT = 'gui/assets/agent_left.png'
AGENT_RIGHT = 'gui/assets/agent_right.png'
AGENT_UP = 'gui/assets/agent_up_2.png'
AGENT_DOWN = 'gui/assets/agent_down.png'
CELL_WUMPUS = 'gui/assets/wumpus.png'
ARROW_IMAGE = 'gui/assets/arrow.png'
GLITTER = 'gui/assets/gold.png'
BUMP = 'gui/assets/bump.png'
SCREAM = 'gui/assets/scream.png'
CELL_GOLD = 'gui/assets/cell_gold.png'
CELL_PIT = 'gui/assets/cell_pit.png'
CELL_STENCH = 'gui/assets/cell_stench.png'
CELL_BREEZE = 'gui/assets/cell_breeze.png'
CELL_BREEZE_GOLD = 'gui/assets/breeze_gold.png'
CELL_STENCH_GOLD = 'gui/assets/stench_gold.png'
CELL_BREEZE_STENCH = 'gui/assets/cell_breeze-stench.png'
CELL_BREEZE_STENCH_GOLD = 'gui/assets/breeze_stench_gold.png'
# Dropdowns với dữ liệu riêng
# Màu sắc
BG_COLOR = (240, 240, 240)  # xám nhạt
TEXT_COLOR = (0, 0, 0)      # đen
HOVER_COLOR = (200, 200, 255)  # xanh nhạt khi hover
COLOR_SAFE_ONLY = (0, 200, 0)       # Xanh lá đậm – an toàn
COLOR_VISITED_ONLY = (0, 102, 204)  # Xanh dương đậm – đã đi qua
COLOR_SAFE_AND_VISITED = (255, 165, 0)  # Cam – vừa an toàn vừa đã đi qua

