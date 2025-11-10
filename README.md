# Dino Jump Bot

This is a Python bot that plays the Chrome Dino game automatically.

## How it Works

The bot takes screenshots of the game area, analyzes the pixels to detect obstacles (cacti and birds), and presses the spacebar to jump over them.

## Configuration

The bot's behavior is controlled by the `config.py` file. You can adjust the following parameters:

### Game Coordinates

*   `GAME_X`, `GAME_Y`: The top-left corner of the game area on your screen.
*   `GAME_WIDTH`, `GAME_HEIGHT`: The width and height of the game area.

### Detection Boxes

The bot uses two detection boxes to look for obstacles:

*   `DETECT_X`, `DETECT_Y`: The top-left corner of the near detection box.
*   `DETECT_WIDTH`, `DETECT_HEIGHT`: The size of the near detection box.
*   `DETECT2_X`, `DETECT2_Y`: The top-left corner of the far detection box.
*   `DETECT2_WIDTH`, `DETECT2_HEIGHT`: The size of the far detection box.

### Detection Logic

*   `DARK_THRESHOLD`: A value between 0 and 255. Pixels darker than this value are considered part of an obstacle.
*   `OBSTACLE_PIXEL_COUNT`: The minimum number of dark pixels in a detection box to trigger a jump.

### Performance

*   `JUMP_COOLDOWN`: The minimum time in seconds between jumps.
*   `SCAN_INTERVAL`: The time in seconds between each scan of the game area.

### Debugging

*   `SAVE_DEBUG_IMAGES`: If `True`, the bot will save screenshots of the game with the detection boxes drawn on them. This is useful for debugging the detection logic.
*   `DEBUG_FOLDER`: The folder where the debug images will be saved.

## How to Use

1.  **Install Dependencies:**
    ```
    pip install pyautogui numpy pillow
    ```
2.  **Calibrate Coordinates:**
    *   Open the Chrome Dino game.
    *   Take a screenshot of your entire screen.
    *   Open the screenshot in an image editor and find the coordinates of the top-left corner of the game area.
    *   Update the `GAME_X` and `GAME_Y` values in `config.py`.
3.  **Run the Bot:**
    ```
    python main.py
    ```

## Disclaimer

This bot is for educational purposes only.
