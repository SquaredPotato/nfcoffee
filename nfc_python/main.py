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


def end_read(signal, frame):
    global run
    print("\nSIGINT captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()


# Set sigint catcher
signal.signal(signal.SIGINT, end_read)

while run:
    rdr.wait_for_tag()

    (error, data) = rdr.request()
    if not error:
        print("\nDetected: " + format(data, "02x"))

    (error, uid) = rdr.anticoll()
    if not error:
        print("Card read UID: "+str(uid[0])+", "+str(uid[1])+", "+str(uid[2])+", "+str(uid[3])+", "+str(uid[4])+"]")
        print("Select given card")
        util.set_tag(uid)
        print("\nAuthorizing")
        util.auth(rdr.auth_b, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]) # White card S1B0
        # util.auth(rdr.auth_b, [0x74, 0x00, 0x52, 0x35, 0x00, 0xFF])
        bank = 4

        print("writing: " + str(util.rewrite(bank, [250])))

        util.read_out(bank)

        print("\nDeauthorizing")
        util.deauth()

        time.sleep(1)
