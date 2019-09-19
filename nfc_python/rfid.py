from pirc522 import RFID
from recipes import recipe
from recipes import part


# Only call this class from one thread at a time
class nfc:

	def __init__(self):
		self.authKey = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]  # card authkey
		# self.authKey = [0x74, 0x00, 0x52, 0x35, 0x00, 0xFF]  # blue drop
		self.rdr = RFID()
		self.util = self.rdr.util()
		self.recipeBlock = 4

	""" Initializes rfid connection """
	def start(self):
		self.rdr.wait_for_tag()

		(error, data) = self.rdr.request()
		if not error:
			print("\nDetected: " + format(data, "02x"))
		else:
			print("\nFalse detection")
			return True

		(error, uid) = self.rdr.anticoll()

		if not error:
			self.util.set_tag(uid)
			self.util.auth(self.rdr.auth_b, self.authKey)

			return False
		print("Error: " + str(error))
		return True

	""" Writes recipe from "recipes" class to card """
	def writerecipe(self, ticket):
		try:
			print("writing ticket to card")
			if len(ticket) == 4:
				res = self.write(self.recipeBlock, ticket)
				if res:
					print("Error while writing to card")
					return True
				return False
			print("Incorrect recipe length: " + str(len(ticket)))
			return True
		except (AttributeError, TypeError):
			print("Error: wrong ticket type")
			exit()

	""" Writes byte array with a maximum length of 16 to given block """
	def write(self, block, data):
		if not self.start():
			er = self.util.rewrite(block, data)

			print("\nDe-authorizing")
			self.util.deauth()

			return er
		else:
			print("Unknown error occurred while initializing card in start()")
			self.util.deauth()
			return 2

	""" Reads byte array with length of 16 from block """
	def read(self, block):
		print("waiting for nfc chip")
		res = self.start()
		if not res:
			error = self.util.do_auth(block)
			if not error:
				(error, data) = self.rdr.read(block)
				print(self.util.sector_string(block) + ": " + str(data))
				return data
			else:
				print("Error on " + self.util.sector_string(block))

		self.util.deauth()

	""" Reads recipe into recipe instance """
	def read_recipe(self):
		data = self.read(self.recipeBlock)
		return recipe(drink=data[part.drink.value], strength=data[part.strength.value],
					  sugar=data[part.sugar.value], milk=data[part.milk.value])
