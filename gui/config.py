WINDOW_TITLE = "Project 02 - Wumpus World Agent"
# lưu tên file, thông số
SCALE = 0.45  # Scale factor for the game window and images
FONT_SIZE_SCALE = 0.85  # Scale factor for font sizes
WIDTH, HEIGHT = 1920 * SCALE, 1920 * SCALE  # Full HD resolution
ROWS, COLS = 6, 6
TILE_SIZE = 880 / 6 * SCALE  # Size of each tile in pixels
OFFSET_X, OFFSET_Y = 520 * SCALE, 520 * SCALE  # Offset for the grid position

# Font settings
FONT_NAME = 'comicsans'
FONT_SIZE = int(20 * FONT_SIZE_SCALE)  # Base font size
FONT_SIZE_LARGE = int(30 * FONT_SIZE_SCALE)  # Large font size
# FONT_SIZE_LARGE = 40


# Resource paths
BACKGROUND_IMAGE = 'gui/assets/background.png'
DESCRIPTION_BACKGROUND_IMAGE = 'gui/assets/description_background.png'
GAME_BACKGROUND_IMAGE = 'gui/assets/game_background.png'
#AGENT
AGENT_IMAGE = 'gui/assets/agent.png'
AGENT_VICTORY_IMAGE = 'gui/assets/agent_victory.png'
AGENT_SIDE_IMAGE = 'gui/assets/agent_side.png'
WUMPUS_IMAGE = 'gui/assets/wumpus.png'
ARROW_IMAGE = 'gui/assets/arrow.png'
GOLD_IMAGE = 'gui/assets/gold.png'
PIT_IMAGE = 'gui/assets/pit.png'
STENCH_IMAGE = 'gui/assets/cell_stench.png'
BREEZE_IMAGE = 'gui/assets/cell_breeze.png'
BREEZE_STENCH_IMAGE = 'gui/assets/cell_breeze_stench.png'
