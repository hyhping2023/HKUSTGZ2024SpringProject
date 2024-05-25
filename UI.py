# UI.py

# A main execution block that sets up the curses environment, creates two windows (input and result), and handles user input.

# The input window prompts the user to enter keywords, while the result window displays the search results.

# The program listens for various key presses, such as
#                                                      Enter to initiate a search,
#                                                      ESC to exit,
#                                                      Backspace to delete characters,
#                                                  and arrow keys to scroll through search results.

#---------------------------- Split line ----------------------------#


# Targets: Run the windows correctly and make sure all functionalities here can still work.


import curses
from data_handling import load_words_from_file, search
import re
import sys

def splitResultwithinWidth(result:str, width:int):
    return [result[i:i + width] for i in range(0, len(result), width)]


def main(stdscr):

    # The start command `python3 UI.py file_path`
    # Or you can just use the PATH in `hyperpara.py`

    # init
    if len(sys.argv) != 2:
        print("Error: Please supply the data file name\n")
        sys.exit(-1)
    else: 
        file_path = sys.argv[1]
        print(file_path)

    data, original_data = load_words_from_file(file_path)         # You are allowed to change returned variables here. Still, you need to change correspondingly the unit test by yourself.

    # for idx, sentence in enumerate(records):
    #     words = re.split('[^a-zA-Z0-9]+', sentence)
    #     for word in words:
    #         for i in range(len(word)):
    #             root.insert(word[i:], idx)


    # Clear screen
    stdscr.clear()

    # Define constants
    PROMPT_STR = "Enter keywords: "

    # Dimensions of the terminal
    height, width = stdscr.getmaxyx()

    # Create windows
    input_win_height = 3
    input_win = curses.newwin(input_win_height, width, 0, 0)
    result_win_height = height - input_win_height
    result_win = curses.newpad(500, width - 2)  # Large pad, can be adjusted based on expected content size

    # Box the input window to make it visible
    input_win.box()
    input_win.addstr(1, 1, PROMPT_STR)
    input_win.refresh()

    # Initialize keyword storage and result pad position
    keywords = ''
    pad_position = 0
    curses.curs_set(1)
    input_win.keypad(True)
    input_win.move(1, len(PROMPT_STR) + len(keywords) + 1)

    #I modified here to let the user be able to use arrow keys
    while True:
        # Get input
        #input_win.move(1, len(PROMPT_STR) + len(keywords) + 1)  # Position cursor correctly
        key = input_win.getkey()

        # Handle special keys
        if key in ['\n', '\r']:  # Enter key
            # Call the search function and display results
            if keywords == '':
                continue
            results = search(keywords, original_data, data)           # You are allowed to change returned variables here. Still, you need to change correspondingly the unit test by yourself.
            result_win.clear()
            i = 0
            for line in results.split('\n'):
                result = splitResultwithinWidth(line, width - 2)
                for fr in result:
                    result_win.addstr(i, 1, fr)
                    i+=1
            result_win.refresh(pad_position, 0, input_win_height, 1, height - 1, width - 2)
            pad_position = 0  # Reset scrolling position
        elif len(key)==1 and ord(key) == 27:  # ESC key
            break
        elif key in ['KEY_BACKSPACE', '\b', '\x7f']:  # Backspace key
            y,x = input_win.getyx()
            if x <= len(PROMPT_STR) + 1:
                continue
            keywords = keywords[:x - len(PROMPT_STR) - 2] + keywords[x - len(PROMPT_STR) - 1:]
            input_win.clear()
            input_win.box()
            input_win.addstr(1, 1, PROMPT_STR + keywords)
            input_win.move(y, x-1)
            input_win.refresh()
        elif key == "KEY_DOWN":
            pad_position += 1
            result_win.refresh(pad_position, 0, input_win_height, 1, height - 1, width - 2)
        elif key == "KEY_UP":
            pad_position = max(0, pad_position - 1)
            result_win.refresh(pad_position, 0, input_win_height, 1, height - 1, width - 2)
        elif key == "KEY_LEFT":  # Handle left and right arrows
            # Optionally, you can add code to move the cursor position if needed
            y,x = input_win.getyx()
            input_win.move(y,max(x-1, len(PROMPT_STR) + 1))
            input_win.refresh()           
        elif key == "KEY_RIGHT":
            y,x = input_win.getyx()
            input_win.move(y,min(x+1,len(PROMPT_STR) + len(keywords)+1))
            input_win.refresh()
        else:
            # Add the character to the input
            y,x = input_win.getyx()
            keywords = keywords[:x - len(PROMPT_STR) - 1] + key + keywords[x - len(PROMPT_STR) - 1:]
            input_win.addstr(1, 1, PROMPT_STR + keywords)
            input_win.move(y, x+1)
            input_win.refresh()


    # Clean up before exiting
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


if __name__ == '__main__':
    curses.wrapper(main)
