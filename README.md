Chrome Dinosaur Game Automation 🦖
An automated Python bot that plays the Chrome Dinosaur game using computer vision and keyboard automation.
🎮 Demo
The bot automatically detects obstacles (cacti and birds) and makes the dinosaur jump or duck to avoid them, achieving high scores without human intervention.
🔧 How It Works
The automation uses:

Screenshot capture to monitor the game area in real-time
Image processing to detect obstacles by analyzing pixel patterns
Keyboard automation to send jump/duck commands

The bot continuously scans a specific region of the screen, identifies approaching obstacles based on color/shape changes, and triggers appropriate actions.
📋 Prerequisites

Python 3.7 or higher
Chrome browser
Windows/Mac/Linux OS

🚀 Installation

Clone this repository:

bashgit clone https://github.com/Emp1500/Dino-Bot.git
cd chrome-dino-automation

Install required dependencies:

bashpip install -r requirements.txt
Dependencies:

pyautogui - For keyboard control and screenshots
Pillow - For image processing
opencv-python - For computer vision (if using advanced detection)
numpy - For numerical operations

🎯 Usage

Open Chrome browser and navigate to the dinosaur game:

Disconnect internet, or
Visit chrome://dino directly


Position the game window appropriately on your screen
Run the automation script:

bashpython dino_bot.py

The bot will automatically start playing. Press Ctrl+C to stop.

🏗️ Technical Approach
Detection Algorithm:

Captures screenshots of the game region at regular intervals
Analyzes pixel values in the obstacle detection zone
Identifies obstacles by detecting color changes (dark pixels on light background)
Calculates obstacle distance and decides action timing

Action Logic:

Jump: When cacti detected in lower region
Duck: When birds (pterodactyls) detected in upper region
Timing: Actions triggered based on obstacle proximity thresholds

📁 Project Structure
chrome-dino-automation/
├── main.py              # Main automation script
├── requirements.txt     # Project dependencies
├── README.md            # Project documentation    
⚠️ Limitations

Screen Resolution: Detection coordinates may need adjustment for different screen sizes
Performance: Requires consistent frame rate; may struggle on slow systems
Browser Compatibility: Optimized for Chrome; may not work with other browsers
Game Speed: Effectiveness decreases as game speed increases significantly

🔮 Future Improvements

 Add machine learning for better obstacle recognition
 Implement adaptive timing based on game speed
 Create GUI for easy configuration
 Add support for different screen resolutions automatically
 Implement score tracking and statistics
 Add replay recording feature

🐛 Troubleshooting
Bot not detecting obstacles:

Ensure game window is fully visible
Check if detection coordinates match your screen resolution
Adjust threshold values in configuration

Bot reacting too late/early:

Modify timing parameters in the script
Ensure no other applications are causing lag

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

Inspired by various automation tutorials and computer vision projects
Chrome Dinosaur Game created by Google

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
