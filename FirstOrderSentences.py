from enum import Enum

class QUANTIFIERS(Enum):
    EXISTENTIAL = 6
    UNIVERSAL = 7

class ExistentialQuantifier:
	def __init__(self, variable, formula):
		self.type = QUANTIFIERS.EXISTENTIAL
		self.variable = variable
		self.formula = formula

	def __str__(self):
		return f'E{self.variable}{self.formula}'

	def __eq__(self, other):
		return str(self) == str(other)

class UniversalQuantifier:
	def __init__(self, variable, formula):
		self.type = QUANTIFIERS.UNIVERSAL
		self.variable = variable
		self.formula = formula

	def __str__(self):
		return f'A{self.variable}{self.formula}'

	def __eq__(self, other):
		return str(self) == str(other)