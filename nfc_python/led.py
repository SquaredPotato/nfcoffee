import RPi.GPIO as GPIO
import time
import sys
import signal
from recipes import recipe
from recipes import part
from rfid import nfc

run = True


def end_read(signal, frame):
	global run
	print("\nSIGINT captured, ending read.")
	run = False
	sys.exit()


# Set sigint catcher
signal.signal(signal.SIGINT, end_read)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

red = 7
green = 11
blue = 13

enter = 29
exit = 31
left = 32
right = 33

GPIO.setup(blue, GPIO.OUT)  # Blue
GPIO.setup(green, GPIO.OUT)  # Green
GPIO.setup(red, GPIO.OUT)  # RED

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

bef = 0
stren = 1
sugar = 2
milk = 3
drink = 0
value = 0
choice = 0

reader = nfc()

while run:

	# recipe_ = reader.read_recipe()
	# recipe_ = recipe(bef, stren, sugar, milk)
	recipe_ = recipe(drink=0, strength=0, sugar=0, milk=0)
	print(recipe_)

	while run:
		time.sleep(0.1)
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
			GPIO.output(red, GPIO.LOW)
			CHOOSE = False
			print(recipe_)
			ENTER_PRESSED = True
			time.sleep(2)
			GPIO.output(blue, GPIO.LOW)
			break

		if ENTER_BUTTON:
			ENTER_PRESSED = False

		if EXIT_BUTTON:
			EXIT = False

		if CHOOSE:
			GPIO.output(green, GPIO.HIGH)
			GPIO.output(red, GPIO.LOW)
			GPIO.output(blue, GPIO.LOW)

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
				break
			if LEFT_BUTTON and RIGHT_BUTTON:
				Hold = False
			if not LEFT_BUTTON and not Hold:
				if value > 0:
					printed = False
					value -= 1
					Hold = True
				else:
					value = 4
			if not RIGHT_BUTTON and not Hold:
				if value < 4:
					printed = False
					value += 1
					Hold = True
				else:
					value = 0
			if choice == 0:
				if not printed_choice:
					print 'selecteer uw drankje'
					printed_choice = True
				if not printed:
					print 'beverage = ', recipe_.drink.keys()[bef]
					printed = True
				bef = value
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
				GPIO.output(blue, GPIO.HIGH)
				recipe_.__init__(drink=bef, strength=stren, sugar=sugar, milk=milk)
				print(recipe_)
				time.sleep(2)
				GPIO.output(blue, GPIO.LOW)
				break
