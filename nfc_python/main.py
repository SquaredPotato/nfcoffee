#!/usr/bin/env python

import signal
import sys
import recipes
import rfid

run = True
rfid_ = rfid.rfid


def end_read(signal, frame):
    global run
    print("\nSIGINT captured, ending read.")
    run = False
    rfid_.rdr.cleanup()
    sys.exit()


# Set sigint catcher
signal.signal(signal.SIGINT, end_read)


def main():
    
    recipe = recipes.recipe(drink=3, strength=8, sugar=0, milk=0)

    print(recipe)


if __name__ is "__main__":
    main()
