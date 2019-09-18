import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.OUT) #Blue
GPIO.setup(17,GPIO.OUT) #Green
GPIO.setup(27,GPIO.OUT) #RED

GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)


CHOOSE = False
Hold = False
EXIT = False

drink = 0

while True:

    ENTER_BUTTON = GPIO.input(5)
    EXIT_BUTTON = GPIO.input(6)
    LEFT_BUTTON = GPIO.input(12)
    RIGHT_BUTTON = GPIO.input(13)

    if(CHOOSE == False):
        if(EXIT_BUTTON == False):
            GPIO.output(27,GPIO.HIGH)
            GPIO.output(4,GPIO.LOW)
            GPIO.output(17,GPIO.LOW)
            CHOOSE = True
            EXIT = True

 
    if(ENTER_BUTTON == False):
        GPIO.output(17,GPIO.HIGH)
        GPIO.output(4,GPIO.LOW)
        GPIO.output(27,GPIO.LOW)
        CHOOSE = False

    if(CHOOSE == True):
        GPIO.output(4,GPIO.HIGH)
        GPIO.output(17,GPIO.LOW)
        GPIO.output(27,GPIO.LOW)

        if(EXIT_BUTTON == True):
            EXIT = False
        if((LEFT_BUTTON == True) and (RIGHT_BUTTON == True)):
            Hold = False
        if((LEFT_BUTTON == False) and (Hold == False)):
            if(drink > 0):
                drink -= 1
                print switcher.get("You Choose:", drink)
                Hold = True
            else:
                drink = 4
        if((RIGHT_BUTTON == False) and (Hold == False)):
            if(drink < 4):
                drink += 1
                print switcher.get("You Choose:", drink)
                Hold = True
            else:
                drink = 0
        if((EXIT_BUTTON == False) and (EXIT == False)):
            print("So long Gay Boys")
            break

