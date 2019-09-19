from enum import Enum


class part(Enum):
	drink = 0
	strength = 1
	sugar = 2
	milk = 3


class recipe:

	drink = {'Cappuccino': 0, 'Coffee': 1, 'Espresso': 2, 'Hot Chocolate': 3, 'Latte macchiato': 4}

	maxStrength = 10
	ticket = [0] * 4

	def __init__(self, drink=0, strength=0, sugar=0, milk=0):
		self.ticket[part.drink.value] = drink
		self.ticket[part.strength.value] = strength
		self.ticket[part.sugar.value] = sugar
		self.ticket[part.milk.value] = milk

	def __repr__(self):
		return "recipe: [drink: " + self.getkeys(self.ticket[part.drink.value])[0] + ", strength: " \
			   + str(self.ticket[part.strength.value]) + ", sugar: " \
			   + str(self.ticket[part.sugar.value]) + ", milk: " \
			   + str(self.ticket[part.milk.value]) + "]"

	def getkeys(self, value):
		keys = list()
		items = self.drink.items()
		for item in items:
			if item[1] == value:
				keys.append(item[0])
		return keys

	""" Makes sure all values are nominal, returns a tuple as {error, array} """
	def finalize(self):
		if not 0 <= self.ticket[part.drink.value] <= len(self.drink):
			print("Error: Invalid drink type")
			return 0, None

		for i in range(1, 4):
			if not 0 <= self.ticket[i] <= self.maxStrength:
				return i, None

		return None, self.ticket


