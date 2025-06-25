# Virtual Keyboard with Hand Tracking

This project is a virtual keyboard that uses your webcam and hand tracking to simulate key presses and interact with web search buttons (Google, YouTube, etc.). Built with OpenCV, cvzone, and MediaPipe.

<img width="1274" alt="Screenshot 2025-06-25 at 1 34 50 PM" src="https://github.com/user-attachments/assets/983bd1e1-48d8-4620-b777-0771d4d57f07" />

## Features
- Hand tracking using your webcam
- Virtual keyboard with clickable keys
- Special buttons for Google, YouTube, Clear, Backspace, and Exit
- Opens browser tabs for Google and YouTube searches
- Customizable keyboard layout

## Setup
1. **Install Python 3.10** (required for MediaPipe compatibility)
2. **Clone this repository**
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the app:**
   ```sh
   python main.py
   ```

## Usage
- Use your hand to hover over keys. Touch your thumb and index finger to "click" a key.
- Use the text box to see your input.
- Click `GGL` or `YTB` to search Google or YouTube for the current text.
- `CLR` clears the text box, `BSP` deletes the last character, and `EXT` exits the program.

## Dependencies
- opencv-python
- cvzone
- numpy
- pynput
- mediapipe (must use Python 3.10)

## Notes
- The app requires a webcam.
- For best results, use in a well-lit environment.
