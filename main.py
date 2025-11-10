import pyautogui
import time
import numpy as np
from PIL import Image, ImageDraw, ImageGrab
import os
from datetime import datetime

try:
    from config import *
except ImportError:
    print("ERROR: config.py not found. Please create it based on config.py.example")
    exit()

# ==================== SETUP ====================
if SAVE_DEBUG_IMAGES and not os.path.exists(DEBUG_FOLDER):
    os.makedirs(DEBUG_FOLDER)

# ==================== CAPTURE & ANALYSIS ====================

class ObstacleDetector:
    def __init__(self):
        self.frame_count = 0
        self.jump_count = 0
        self.last_jump_time = 0
        self.detection_history = []
        
    def capture_full_game(self):
        """Capture entire game area"""
        screenshot = ImageGrab.grab(bbox=(GAME_X, GAME_Y, 
                                          GAME_X + GAME_WIDTH, 
                                          GAME_Y + GAME_HEIGHT))
        return screenshot
    
    def capture_detection_regions(self):
        """Capture both near and far detection box areas"""
        near_screenshot = ImageGrab.grab(bbox=(DETECT_X, DETECT_Y, 
                                              DETECT_X + DETECT_WIDTH, 
                                              DETECT_Y + DETECT_HEIGHT))
        far_screenshot = ImageGrab.grab(bbox=(DETECT2_X, DETECT2_Y, 
                                             DETECT2_X + DETECT2_WIDTH, 
                                             DETECT2_Y + DETECT2_HEIGHT))
        return near_screenshot, far_screenshot
    
    def analyze_regions(self, near_image, far_image):
        """
        Detailed pixel analysis of two detection regions (near and far)
        Returns: dict with combined analysis results
        """
        def analyze_single_region(image):
            gray = np.array(image.convert('L'))
            dark_pixels = np.sum(gray < DARK_THRESHOLD)
            return {
                'dark_pixels': dark_pixels,
                'obstacle_detected': dark_pixels > OBSTACLE_PIXEL_COUNT
            }

        near_analysis = analyze_single_region(near_image)
        far_analysis = analyze_single_region(far_image)

        # Combine analysis
        total_dark_pixels = near_analysis['dark_pixels'] + far_analysis['dark_pixels']
        obstacle_detected = near_analysis['obstacle_detected'] or far_analysis['obstacle_detected']

        analysis = {
            'near_dark_pixels': near_analysis['dark_pixels'],
            'far_dark_pixels': far_analysis['dark_pixels'],
            'total_dark_pixels': total_dark_pixels,
            'obstacle_detected': obstacle_detected,
            'threshold_used': DARK_THRESHOLD,
            'trigger_count': OBSTACLE_PIXEL_COUNT
        }
        
        return analysis
    
    def create_visualization(self, full_game_img, near_detection_img, far_detection_img, analysis):
        """
        Create a detailed visualization showing:
        - Full game view with both detection boxes highlighted
        - Zoomed-in views of both detection regions
        - Pixel analysis overlay
        - Statistics
        """
        # Create canvas
        canvas_width = GAME_WIDTH + 400  # Extra space for info
        canvas_height = GAME_HEIGHT + 300  # Extra space for detection zoom
        canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 255
        
        # Place full game image
        game_array = np.array(full_game_img)
        canvas[0:GAME_HEIGHT, 0:GAME_WIDTH] = game_array
        
        # Draw detection boxes on full game view
        full_game_draw = full_game_img.copy()
        draw = ImageDraw.Draw(full_game_draw)
        # Near box
        box_coords1 = (
            DETECT_X - GAME_X,
            DETECT_Y - GAME_Y,
            DETECT_X - GAME_X + DETECT_WIDTH,
            DETECT_Y - GAME_Y + DETECT_HEIGHT
        )
        color1 = "red" if analysis['obstacle_detected'] else "green"
        draw.rectangle(box_coords1, outline=color1, width=3)
        # Far box
        box_coords2 = (
            DETECT2_X - GAME_X,
            DETECT2_Y - GAME_Y,
            DETECT2_X - GAME_X + DETECT2_WIDTH,
            DETECT2_Y - GAME_Y + DETECT2_HEIGHT
        )
        color2 = "red" if analysis['obstacle_detected'] else "green"
        draw.rectangle(box_coords2, outline=color2, width=3)

        canvas[0:GAME_HEIGHT, 0:GAME_WIDTH] = np.array(full_game_draw)
        
        # Place zoomed detection regions
        near_zoomed = near_detection_img.resize((200, 240), resample=0)  # 4x zoom
        near_array = np.array(near_zoomed)
        canvas[GAME_HEIGHT + 10:GAME_HEIGHT + 10 + 240, 0:200] = near_array

        far_zoomed = far_detection_img.resize((200, 240), resample=0)  # 4x zoom
        far_array = np.array(far_zoomed)
        canvas[GAME_HEIGHT + 10:GAME_HEIGHT + 10 + 240, 220:420] = far_array

        # Add text information
        canvas_img = Image.fromarray(canvas)
        draw = ImageDraw.Draw(canvas_img)
        
        # Statistics text
        info_x = GAME_WIDTH + 10
        info_y = 10
        line_height = 20
        
        info_lines = [
            f"Frame: {self.frame_count}",
            f"Jumps: {self.jump_count}",
            f"",
            f"PIXEL ANALYSIS:",
            f"Near Dark Pixels: {analysis['near_dark_pixels']}",
            f"Far Dark Pixels: {analysis['far_dark_pixels']}",
            f"Total Dark Pixels: {analysis['total_dark_pixels']}",
            f"",
            f"THRESHOLDS:",
            f"Dark Threshold: < {DARK_THRESHOLD}",
            f"Trigger Count: > {OBSTACLE_PIXEL_COUNT}",
            f"",
            f"STATUS:",
            f"Obstacle: {'YES - JUMP!' if analysis['obstacle_detected'] else 'NO - Safe'}",
        ]
        
        for i, line in enumerate(info_lines):
            color = "red" if "JUMP" in line else "black"
            draw.text((info_x, info_y + i * line_height), line, fill=color)
        
        # Labels for visualizations
        draw.text((10, GAME_HEIGHT + 250), "Near Detection (4x zoom)", fill="black")
        draw.text((220, GAME_HEIGHT + 250), "Far Detection (4x zoom)", fill="black")
        
        return canvas_img
    
    def save_debug_frame(self, visualization, analysis):
        """Save debug frame to disk"""
        if SAVE_DEBUG_IMAGES and self.frame_count % 50 == 0:  # Save every 50th frame
            timestamp = datetime.now().strftime("%H%M%S")
            status = "JUMP" if analysis['obstacle_detected'] else "safe"
            filename = f"{DEBUG_FOLDER}/frame_{self.frame_count:05d}_{timestamp}_{status}.png"
            visualization.save(filename)
            print(f"  💾 Saved: {filename}")
    
    def print_analysis(self, analysis):
        """Print detailed analysis to console"""
        print(f"\n{'='*60}")
        print(f"Frame #{self.frame_count} | Jumps: {self.jump_count}")
        print(f"{'='*60}")
        print(f"📊 PIXEL BREAKDOWN:")
        print(f"   Near Dark Pixels: {analysis['near_dark_pixels']}")
        print(f"   Far Dark Pixels: {analysis['far_dark_pixels']}")
        print(f"   Total Dark Pixels (obstacle): {analysis['total_dark_pixels']}")
        print(f"\n⚙️  DETECTION LOGIC:")
        print(f"   Threshold: Pixels < {analysis['threshold_used']} = Obstacle")
        print(f"   Trigger: Dark pixels > {analysis['trigger_count']}")
        print(f"   Current: {analysis['total_dark_pixels']} dark pixels")
        
        if analysis['obstacle_detected']:
            print(f"\n🚨 OBSTACLE DETECTED! JUMPING!")
        else:
            print(f"\n✅ Clear - No obstacle")
        
        print(f"{'='*60}\n")
    
    def jump(self):
        """Execute jump command"""
        current_time = time.time()
        if current_time - self.last_jump_time >= JUMP_COOLDOWN:
            pyautogui.press('space')
            self.jump_count += 1
            self.last_jump_time = current_time
            return True
        return False

# ==================== MAIN BOT LOOP ====================

def main():
    print("=" * 70)
    print("🦖 DETAILED DINO GAME BOT MVP")
    print("=" * 70)
    print("\n📋 CONFIGURATION:")
    print(f"   Game Region: ({GAME_X}, {GAME_Y}) to ({GAME_X + GAME_WIDTH}, {GAME_Y + GAME_HEIGHT})")
    print(f"   Detection Box 1 (Near): ({DETECT_X}, {DETECT_Y}) - {DETECT_WIDTH}x{DETECT_HEIGHT} pixels")
    print(f"   Detection Box 2 (Far): ({DETECT2_X}, {DETECT2_Y}) - {DETECT2_WIDTH}x{DETECT2_HEIGHT} pixels")
    print(f"   Dark Threshold: < {DARK_THRESHOLD}")
    print(f"   Obstacle Trigger: > {OBSTACLE_PIXEL_COUNT} dark pixels")
    print(f"   Scan Interval: {SCAN_INTERVAL * 1000}ms")
    print(f"   Debug Images: {'Enabled' if SAVE_DEBUG_IMAGES else 'Disabled'}")
    
    print("\n⏳ Starting in 5 seconds...")
    print("   1. Make sure Chrome Dino game is visible")
    print("   2. Position it where you calibrated")
    print("   3. Game will auto-start!")
    print("\n🛑 Press Ctrl+C to stop\n")
    
    time.sleep(5)
    
    # Initialize detector
    detector = ObstacleDetector()
    
    # Start the game
    print("🎮 Starting game...")
    detector.jump()
    time.sleep(0.5)
    
    print("🤖 Bot is running with detailed analysis...\n")
    
    try:
        while True:
            detector.frame_count += 1
            
            # Capture images
            full_game = detector.capture_full_game()
            near_region, far_region = detector.capture_detection_regions()
            
            # Analyze pixels
            analysis = detector.analyze_regions(near_region, far_region)
            
            # Print analysis every 100 frames or when obstacle detected
            if detector.frame_count % 100 == 0 or analysis['obstacle_detected']:
                detector.print_analysis(analysis)
            
            # Create and save visualization
            if SAVE_DEBUG_IMAGES and (detector.frame_count % 50 == 0 or analysis['obstacle_detected']):
                visualization = detector.create_visualization(full_game, near_region, far_region, analysis)
                detector.save_debug_frame(visualization, analysis)
            
            # Take action
            if analysis['obstacle_detected']:
                if detector.jump():
                    print(f"⬆️  JUMP #{detector.jump_count} executed!")
            
            # Small delay before next scan
            time.sleep(SCAN_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("🛑 BOT STOPPED")
        print("=" * 70)
        print(f"📊 FINAL STATS:")
        print(f"   Total Frames Processed: {detector.frame_count}")
        print(f"   Total Jumps: {detector.jump_count}")
        print(f"   Runtime: {detector.frame_count * SCAN_INTERVAL:.1f} seconds")
        if SAVE_DEBUG_IMAGES:
            print(f"   Debug images saved in: {DEBUG_FOLDER}/")
        print("=" * 70)

if __name__ == "__main__":
    main()