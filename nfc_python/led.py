import RPi.GPIO as GPIO
import time
import datetime
import sys
import signal
from recipes import recipe
from recipes import part
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

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

red = 13
green = 11
blue = 7

enter = 29
right = 31
left = 32
exit = 33

GPIO.setup(blue, GPIO.OUT)  # Blue
GPIO.setup(green, GPIO.OUT)  # Green
GPIO.setup(red, GPIO.OUT)  # RED

GPIO.output(blue, GPIO.LOW)
GPIO.output(red, GPIO.LOW)
GPIO.output(green, GPIO.LOW)

GPIO.setup(enter, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(exit, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(left, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(right, GPIO.IN, pull_up_down=GPIO.PUD_UP)

printed = False
printed_choice = False

CHOOSE = False
Hold = False
EXIT = False
ENTER_PRESSED = False
ORDERING = False
OVERWRITE = False
bef = 0
stren = 1
sugar = 2
milk = 3
drink = 0
value = 0
choice = 0

old_recipe = recipe()
millis = int(round(time.time() * 1000))

while run:
	GPIO.output(red, GPIO.HIGH)
	GPIO.output(green, GPIO.HIGH)
	recipe_ = reader.read_recipe()
	GPIO.output(green, GPIO.LOW)
	# recipe_ = recipe(bef, stren, sugar, milk)
	print(recipe_)

	while run:
		ENTER_BUTTON = GPIO.input(enter)
		EXIT_BUTTON = GPIO.input(exit)
		LEFT_BUTTON = GPIO.input(left)
		RIGHT_BUTTON = GPIO.input(right)

		if not CHOOSE and not EXIT_BUTTON:
			GPIO.output(blue, GPIO.HIGH)
			GPIO.output(green, GPIO.LOW)
			GPIO.output(red, GPIO.LOW)
			CHOOSE = True
			EXIT = True
			ORDERING = True

		if not ENTER_BUTTON and not ENTER_PRESSED and not ORDERING:
			GPIO.output(blue, GPIO.HIGH)
			GPIO.output(green, GPIO.LOW)
			GPIO.output(red, GPIO.HIGH)
			CHOOSE = False
			print("pouring: " + recipe_.drink[recipe_.ticket[part.drink.value]])
			ENTER_PRESSED = True
			time.sleep(2)
			GPIO.output(blue, GPIO.LOW)
			GPIO.output(red, GPIO.LOW)
			break

		if ENTER_BUTTON:
			ENTER_PRESSED = False

		if EXIT_BUTTON:
			EXIT = False

		if CHOOSE:
			GPIO.output(blue, GPIO.HIGH)
			GPIO.output(red, GPIO.LOW)
			GPIO.output(green, GPIO.LOW)

			if not ENTER_BUTTON and not ENTER_PRESSED:
				choice += 1
				value = 0
				printed_choice = False
				ENTER_PRESSED = True
			if not EXIT_BUTTON and not EXIT and choice > 0:
				print("gaat fout")
				choice -= 1
				value = 0
				printed_choice = False
				EXIT = True
			if not EXIT_BUTTON and not EXIT and choice == 0:
				print("So long Gay Boys")
				GPIO.output(blue, GPIO.LOW)
				break
			if LEFT_BUTTON and RIGHT_BUTTON:
				Hold = False
			if not LEFT_BUTTON and not Hold:
				if value > 0:
					value -= 1
				else:
					value = recipe_.maxStrength
				printed = False
				Hold = True
			if not RIGHT_BUTTON and not Hold:
				if value < recipe_.maxStrength:
					value += 1
				else:
					value = 0
				printed = False
				Hold = True
			if choice == 0:
				bef = value
				if not printed_choice:
					print 'selecteer uw drankje'
					printed_choice = True
				if not printed:
					print 'beverage = ', recipe_.drink[bef]
					printed = True

			# order_number[part.drink.value] = value
			if choice == 1:
				if not printed_choice:
					print 'hoe sterk  wilt u uw drankje'
					print 'strenght = ', value
					printed_choice = True
				if not printed:
					print 'strenght = ', value
					printed = True
				stren = value
			# order_number[part.strenght.value] = value
			if choice == 2:
				if not printed_choice:
					print('hoeveel suiker wilt u')
					print 'sugar = ', value
					printed_choice = True
				if not printed:
					print 'sugar = ', value
					printed = True
				sugar = value
			# order_number[part.sugar.value] = value
			if choice == 3:
				if not printed_choice:
					print 'hoeveel melk wilt u'
					print 'milk = ', value
					printed_choice = True
				if not printed:
					print 'milk = ', value
					printed = True

				milk = value
			# order_number[part.milk.value] = value
			if choice == 4:
				GPIO.output(blue, GPIO.LOW)
				GPIO.output(green, GPIO.HIGH)
				recipe_.__init__(drink=bef, strength=stren, sugar=sugar, milk=milk)
				# recipe_.ticket[part.drink.value] = bef
				old_recipe = recipe_
				print("pouring: " + recipe_.drink[recipe_.ticket[part.drink.value]])
				time.sleep(2)
				millis = int(round(time.time() * 1000))
				GPIO.output(green, GPIO.LOW)
				choice = 0
				break
