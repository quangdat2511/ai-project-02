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

# Resource paths
BACKGROUND_IMAGE = 'gui/assets/background.png'
DESCRIPTION_BACKGROUND_IMAGE = 'gui/assets/description-bg.png'
GAME_BACKGROUND_IMAGE = 'gui/assets/game-bg-2.png'
#AGENT
AGENT_IMAGE = 'gui/assets/agent.png'
AGENT_VICTORY_IMAGE = 'gui/assets/agent_victory.png'
AGENT_SIDE_IMAGE = 'gui/assets/agent_side.png'
WUMPUS_IMAGE = 'gui/assets/wumpus.png'
ARROW_IMAGE = 'gui/assets/arrow.png'
GOLD_IMAGE = 'gui/assets/cell_gold.png'
PIT_IMAGE = 'gui/assets/cell_pit.png'
STENCH_IMAGE = 'gui/assets/cell_stench.png'
BREEZE_IMAGE = 'gui/assets/cell_breeze.png'
BREEZE_STENCH_IMAGE = 'gui/assets/cell_breeze-stench.png'
BREEZE_STENCH_IMAGE_GOLD = 'gui/assets/breeze_stench_gold.png'
