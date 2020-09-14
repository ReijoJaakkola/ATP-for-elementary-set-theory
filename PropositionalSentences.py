from enum import Enum

class CONNECTIVES(Enum):
	ATOM = 0
	NEG = 1
	AND = 2
	OR = 3
	IMPLICATION = 4
	EQUIVALENCE = 5

class PropVariable:
	def __init__(self, variable):
		self.type = CONNECTIVES.ATOM
		self.variable = variable

	def __str__(self):
		return self.variable

	def __eq__(self, other):
		return str(self) == str(other)

class PropNegation:
	def __init__(self, formula):
		self.type = CONNECTIVES.NEG
		self.subformula = formula

	def __str__(self):
		return f'!{self.subformula}'

	def __eq__(self, other):
		return str(self) == str(other)

class PropConjunction:
	def __init__(self, formula1, formula2):
		self.type = CONNECTIVES.AND
		self.subformula1 = formula1
		self.subformula2 = formula2

	def __str__(self):
		return f'({self.subformula1}&{self.subformula2})'

	def __eq__(self, other):
		return str(self) == str(other)

class PropDisjunction:
	def __init__(self, formula1, formula2):
		self.type = CONNECTIVES.OR
		self.subformula1 = formula1
		self.subformula2 = formula2

	def __str__(self):
		return f'({self.subformula1}|{self.subformula2})'

	def __eq__(self, other):
		return str(self) == str(other)

class PropImplication:
	def __init__(self, formula1, formula2):
		self.type = CONNECTIVES.IMPLICATION
		self.subformula1 = formula1
		self.subformula2 = formula2

	def __str__(self):
		return f'({self.subformula1}->{self.subformula2})'

	def __eq__(self, other):
		return str(self) == str(other)

class PropEquivalence:
	def __init__(self, formula1, formula2):
		self.type = CONNECTIVES.EQUIVALENCE
		self.subformula1 = formula1
		self.subformula2 = formula2

	def __str__(self):
		return f'({self.subformula1}<->{self.subformula2})'

	def __eq__(self, other):
		return str(self) == str(other)