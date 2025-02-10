import pyautogui
import time
import keyboard


# Movement settings
step = 50 # Pixels to move up and down
delay = 0.5 # Seconds to wait between moves
running = True # Controls the loop

# Define an exit funciton 
def stop_script():
    global running
    running = False
    print("\nExit command received. Stopping script.")

# Set 'q' as the exit key
keyboard.add_hotkey("q", stop_script)

print("Mouse movement started. Press 'q' to exit.")

# Continuous loop to move the mouse up and down
while running:
    pyautogui.moveRel(0, -step, duration=0.2) # Move up relative to current position
    time.sleep(delay)

    pyautogui.moveRel(0, step, duration=0.2) # Move downq relative to current position
    time.sleep(delay)

print("Script exited successfully.")