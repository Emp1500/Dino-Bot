# ==================== CONFIGURATION ====================

# Your game coordinates
GAME_X = 593
GAME_Y = 246
GAME_WIDTH = 729
GAME_HEIGHT = 162

# Detection box 1 (near)
DETECT_X = GAME_X + 150  # 150 pixels from left edge
DETECT_Y = GAME_Y + 120   # Ground level area
DETECT_WIDTH = 50
DETECT_HEIGHT = 60

# Detection box 2 (far)
DETECT2_X = DETECT_X + 80 
DETECT2_Y = GAME_Y + 120
DETECT2_WIDTH = 50
DETECT2_HEIGHT = 60

DARK_THRESHOLD = 150  # Pixels darker than this are considered "obstacle"
OBSTACLE_PIXEL_COUNT = 300  # Minimum dark pixels to trigger jump

# Performance tracking
JUMP_COOLDOWN = 0.3  # Seconds between jumps
SCAN_INTERVAL = 0.01  # How often to check (10ms)

# Debug settings
SAVE_DEBUG_IMAGES = True
DEBUG_FOLDER = "dino_debug"
