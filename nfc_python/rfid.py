from pirc522 import RFID
import recipes
import sys
import signal


# Only call this class from one thread at a time
class rfid:
	authKey = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]  # card authkey
	rdr = RFID()
	util = rdr.util()

	""" Initializes rfid connection """
	def start(self):
		self.rdr.wait_for_tag()

		(error, data) = self.rdr.request()
		if not error:
			print("\nDetected: " + format(data, "02x"))

		(error, uid) = self.rdr.anticoll()

		if not error:
			self.util.set_tag(uid)
			self.util.auth(self.rdr.auth_b, self.authKey)

			return False
		return True

	# TODO: create this function
	def writerecipe(self, recipe):
		print("writing recipe to card")
		self.write(0, 0)

	""" Writes byte array with a maximum length of 16 to given block """
	def write(self, block, data):
		if not self.start():
			er = self.util.rewrite(block, data)

			print("\nDe-authorizing")
			self.util.deauth()

			return er
		else:
			print("Unknown error occurred while initializing card in start()")

	""" Reads byte array with length of 16 from block """
	def read(self, block):
		if not self.start():
			(error, data) = self.rdr.read(block)
			if not error:
				print(str(data))
				self.util.deauth()
				return data
			else:
				print("Unknown error occurred while initializing card in start()")

			self.util.deauth()
