import keyboard
import pyautogui
import pyperclip
import time
import loguru
import os
from src.voice_generation import main as voice_generation

os.environ["DISPLAY"] = ":0"

logger = loguru.logger


def save_to_file():
    """
    Saves the selected text to a file by performing the following steps:
    1. Copies the selected text to the clipboard.
    2. Logs the selected text.
    3. Generates voice using the selected text.
    4. Logs a message indicating that the request was made.

    This function does not take any parameters.

    This function does not return any values.
    """
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.5)

    selected_text = pyperclip.paste()
    logger.info(f"selected text: {selected_text}")
    voice_generation(voice_id_input="XrExE9yKIg1WjnnlVkGX", text_input=selected_text)
    logger.info("request made")
    exit()


def main():
    """
    Adds a hotkey to save the highlighted text to a file when 'Ctrl+Alt+S' is pressed.

    Parameters:
        None

    Return:
        None
    """
    keyboard.add_hotkey("ctrl+alt+s", save_to_file)
    logger.info("Waiting for 'Ctrl+Alt+S' to save highlighted text to file...")
    keyboard.wait()


if __name__ == "__main__":
    main()
