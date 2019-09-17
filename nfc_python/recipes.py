from enum import Enum


class recipe:
	parts = Enum(
		'drink',
		'strength',
		'sugar',
		'milk'
	)

	drink = {{'Hot water': 0},
			{'Coffee': 1},
			{'Espresso': 2},
			{'Hot Chocolate': 3},
			{'Latte macchiato': 4}}

	maxStrength = 10
	ticket = [0] * 4

	def __init__(self, drink=0, strength=0, sugar=0, milk=0):
		self.ticket[self.parts['drink']] = drink
		self.ticket[self.parts['strength']] = strength
		self.ticket[self.parts['sugar']] = sugar
		self.ticket[self.parts['milk']] = milk

	""" Makes sure all values are nominal, returns a tuple as {error, array} """
	def finalize(self):
		if not 0 <= self.ticket[self.parts.drink] <= len(self.drink):
			print("Error: Invalid " + self.parts['drink'].name)
			return {0, None}

		for i in range(1, 4):
			if not 0 <= self.ticket[i] <= self.maxStrength:
				return {i, None}

		return {None, self.ticket}


