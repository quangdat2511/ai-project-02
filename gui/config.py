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
BACKGROUND_IMAGE = 'gui/assets/background.jpg'
TARGET_CAR_IMAGE = 'gui/assets/car_player.png'
CAR_IMAGE_FORMAT = 'gui/assets/cars/car_{}.png'
TRUCK_IMAGE_FORMAT = 'gui/assets/trucks/truck_{}.png'