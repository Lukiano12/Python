from pynput import keyboard
from pynput.keyboard import Controller
import time

# Initialize the keyboard controller
keyboard_controller = Controller()

# The alphabet to type
alphabet = "bcdefghijklmnopqrstuvwxyz"

# Function to type the alphabet
def type_alphabet():
    for letter in alphabet:
        keyboard_controller.type(letter)  # Simulate typing the letter
        time.sleep(0.1)  # Small delay to simulate typing speed

# Listener function for key press
def on_press(key):
    try:
        # Start typing when "a" is pressed
        if key.char == "a":
            print("Starting to type the alphabet...")
            type_alphabet()
            print("Alphabet typed successfully!")
            # Stop the listener after completing the task
            return False
    except AttributeError:
        # Ignore special keys
        pass

# Start listening for the key press
print("Press 'a' to start typing the alphabet automatically.")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
