#!/usr/bin/env python

import signal
import time
import sys

from pirc522 import RFID

rdr = RFID()
util = rdr.util()
# Set util debug to true - it will print what's going on
util.debug = True

run = True


def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()


signal.signal(signal.SIGINT, end_read)

# valid sections white card: S1B0, S1B2
# valid sections blue drop:

while run:
    rdr.wait_for_tag()

    (error, data) = rdr.request()
    if not error:
        print("\nDetected: " + format(data, "02x"))

    (error, uid) = rdr.anticoll()
    if not error:
        print("Card read UID:")
        for a in uid:
            print(" " + str(a))

        print("Setting tag")
        util.set_tag(uid)
        print("\nAuthorizing")
        # util.auth(rdr.auth_a, [0x12, 0x34, 0x56, 0x78, 0x96, 0x92])
        # util.auth(rdr.auth_b, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]) # White card S1B0
        # util.auth(rdr.auth_b, [0x74, 0x00, 0x52, 0x35, 0x00, 0xFF]) # Blue drop S1B0
        print("\nReading")
        util.read_out(4)
        print("\nDeauthorizing")
        util.deauth()

        time.sleep(1)