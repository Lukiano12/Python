from pynput.mouse import Button, Controller
from pynput import keyboard
import time
import threading

# Initialize mouse controller
mouse = Controller()

# Settings
clicking = False  # Start with clicking disabled
delay = 0.01  # Delay between clicks (in seconds)

# Clicker function
def clicker():
    while True:
        if clicking:
            mouse.click(Button.left)
        time.sleep(delay)

# Keyboard listener functions
def on_press(key):
    global clicking
    try:
        if key.char == 's':  # Toggle clicking with 's'
            clicking = not clicking  # Flip the state
        elif key.char == 'q':  # Quit program with 'q'
            return False
    except AttributeError:
        pass

# Start clicker thread
clicker_thread = threading.Thread(target=clicker)
clicker_thread.daemon = True  # Ensure thread exits when main program exits
clicker_thread.start()

# Start listening for keyboard input
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
