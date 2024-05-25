# executor.py

# Constitute a simple command-line application for searching through a collection of words loaded from a file.
# Match results from the search operation are printed to the console, giving the user immediate feedback on their query.

# You can use it as a debugging codes in the CLI (without the UI) to check your codes.

#---------------------------- Split line ----------------------------#


# Targets: Run the CLI and test all the given testing usages here. You are suggested to generate your own testing data to make sure all the functionalities work correctly.

from data_handling import load_words_from_file, search
from hyperpara import TEST_DATA_01, TEST_DATA_02

FILE_PATH = TEST_DATA_01

def main():

    root, entries = load_words_from_file(FILE_PATH)     # You are allowed to change returned variables here. Still, you need to change correspondingly the unit test by yourself.

    # Example interaction
    while True:
        keywords = input("Enter your search (type 'quit' to exit): ")
        if keywords.lower() == 'quit':
            break
        results = search(root,keywords, entries, )       # You are allowed to change returned variables here. Still, you need to change correspondingly the unit test by yourself.
        print(results)

if __name__ == '__main__':
    main()