#!/usr/bin/env python

import signal
import sys
import recipes
import time
from rfid import nfc

run = True
reader = nfc()


def end_read(signal, frame):
    global run
    print("\nSIGINT captured, ending read.")
    run = False
    reader.rdr.cleanup()
    sys.exit()


# Set sigint catcher
signal.signal(signal.SIGINT, end_read)


def main():
    recipe_ = recipes.recipe(drink=2, strength=3, sugar=9, milk=3)

    while run:
        reader.writerecipe(recipe_.finalize()[1])

        card_data = reader.read_recipe()
        print(card_data)


        time.sleep(1)

    reader.rdr.cleanup()

    print(recipe_)


if __name__ == "__main__":
    main()
