from enum import Enum
from PropositionalSentences import PropNegation, PropConjunction, PropDisjunction, PropImplication, PropEquivalence

class SETOPERATIONS(Enum):
	SET = 6
	MEMBER = 7
	SUBSET = 8
	COMPLEMENT = 9
	UNION = 10
	INTERSECTION = 11
	EQUALITY = 12
	POWERSET = 13

class Set:
	def __init__(self, set):
		self.type = SETOPERATIONS.SET
		self.set = set

	def __str__(self):
		return self.set

	def __eq__(self, other):
		return str(self) == str(other)

class SetMember:
	def __init__(self, element, set):
		self.type = SETOPERATIONS.MEMBER
		self.element = element
		self.set = set

	def __str__(self):
		return f'({self.element}€{self.set})'

	def __eq__(self, other):
		return str(self) == str(other)

class SetSubset:
	def __init__(self, set1, set2):
		self.type = SETOPERATIONS.SUBSET
		self.set1 = set1
		self.set2 = set2

	def __str__(self):
		return f'({self.set1}S{self.set2})'

	def __eq__(self, other):
		return str(self) == str(other)

class SetComplement:
	def __init__(self, set):
		self.type = SETOPERATIONS.COMPLEMENT
		self.set = set

	def __str__(self):
		return f'C{self.set}'

class SetUnion:
	def __init__(self, set1, set2):
		self.type = SETOPERATIONS.UNION
		self.set1 = set1
		self.set2 = set2

	def __str__(self):
		return f'({self.set1}U{self.set2})'

	def __eq__(self, other):
		return str(self) == str(other)

class SetIntersection:
	def __init__(self, set1, set2):
		self.type = SETOPERATIONS.INTERSECTION
		self.set1 = set1
		self.set2 = set2

	def __str__(self):
		return f'({self.set1}I{self.set2})'

	def __eq__(self, other):
		return str(self) == str(other)

class SetEquality:
	def __init__(self, set1, set2):
		self.type = SETOPERATIONS.EQUALITY
		self.set1 = set1
		self.set2 = set2

	def __str__(self):
		return f'({self.set1}={self.set2})'

	def __eq__(self, other):
		return str(self) == str(other)

class SetPowerset:
	def __init__(self, set):
		self.type = SETOPERATIONS.POWERSET
		self.set = set

	def __str__(self):
		return f'P{self.set}'

	def __eq__(self, other):
		return str(self) == str(other)

SETOPERATORS = ['C','U','I','P']

class SetParser:
	def __init__(self, input):
		self.input = list(input)
		self.input.reverse()
		self.output = []
		self.operators = []

	def precedenceForOperator(self, operator):
		if operator == 'C' or operator == 'P':
			return 0
		elif operator == 'U' or operator == 'I':
			return 1
		else:
			raise Exception('Error: Unrecognized operator.')

	def peekIsNextOperator(self):
		if len(self.input) == 0:
			return False
		if self.input[-1] in SETOPERATORS:
			return True
		else:
			return False

	def getNextAtom(self):
		atom = self.input.pop()
		while len(self.input) > 0:
			if self.peekIsNextOperator():
				break
			if self.input[-1] == '(' or self.input[-1] == ')':
				break
			else:
				atom += self.input.pop()
		return atom		

	def getNextOperator(self):
		if len(self.input) == 0:
			return None
		if self.input[-1] in SETOPERATORS:
			return self.input.pop()
		else:
			return None

	def addOperatorToOutput(self):
		if len(self.operators) == 0:
			return
		
		operator = self.operators.pop()
		if operator == 'C':
			self.output.append(SetComplement(self.output.pop()))
		elif operator == 'U':
			operand1 = self.output.pop()
			operand2 = self.output.pop()
			self.output.append(SetUnion(operand2, operand1))
		elif operator == 'I':
			operand1 = self.output.pop()
			operand2 = self.output.pop()
			self.output.append(SetIntersection(operand2, operand1))
		elif operator == 'P':
			self.output.append(SetPowerset(self.output.pop()))
		else:
			raise Exception('Error: When adding a new operator, unexpected operator occured.')

	def parseExpression(self):
		while len(self.input) > 0:
			if self.peekIsNextOperator():
				operator = self.getNextOperator()
				while len(self.operators) > 0 and self.operators[-1] != '(':
					if self.precedenceForOperator(operator) > self.precedenceForOperator(self.operators[-1]):
						self.addOperatorToOutput()
					else:
						break
				self.operators.append(operator)
			elif self.input[-1] == '(':
				self.operators.append(self.input.pop())
			elif self.input[-1] == ')':
				while len(self.operators) > 0 and self.operators[-1] != '(':
					self.addOperatorToOutput()
				if len(self.operators) > 0 and self.operators[-1] == '(':
					self.operators.pop()
					self.input.pop()
				else:
					raise Exception('Error: Missing left-bracket.')
			else:
				self.output.append(Set(self.getNextAtom()))
					
		while len(self.operators) > 0:
			self.addOperatorToOutput()

		return self.output.pop()

LOGICOPERATORS = ['€','S','=','!','|','&','-','<']

class SetTheoryParser:
	def __init__(self, input):
		self.input = list(input)
		self.input.reverse()
		self.output = []
		self.operators = []

	def precedenceForOperator(self, operator):
		if operator == '€' or operator == 'S' or operator == '=':
			return 0
		elif operator == '!':
			return 1
		elif operator == '|' or operator == '&':
			return 2
		elif operator == '-' or operator == '->':
			return 3
		elif operator == '<' or operator == '<->':
			return 4
		else:
			raise Exception('Error: Unrecognized operator.')

	def peekIsNextOperator(self):
		if len(self.input) == 0:
			return False
		if self.input[-1] in LOGICOPERATORS:
			return True
		else:
			return False

	def getNextAtom(self):
		atom = self.input.pop()
		while len(self.input) > 0:
			if self.peekIsNextOperator():
				break
			if self.input[-1] == '[' or self.input[-1] == ']':
				break
			else:
				atom += self.input.pop()
		return atom		

	def getNextOperator(self):
		if len(self.input) == 0:
			return None
		if self.peekIsNextOperator():
			if self.input[-1] == '-':
				if len(self.input) < 2:
					raise Exception('Error: Syntax error.')
				operator = self.input.pop()
				operator += self.input.pop()
				return operator
			elif self.input[-1] == '<':
				if len(self.input) < 3:
					raise Exception('Error: Syntax error.')
				operator = self.input.pop()
				operator += self.input.pop()
				operator += self.input.pop()
				return operator
			else:
				return self.input.pop()
		else:
			return None

	def addAtomToOutput(self, atom):
		atomParser = SetParser(atom)
		self.output.append(atomParser.parseExpression())

	def addOperatorToOutput(self):
		if len(self.operators) == 0:
			return
		
		operator = self.operators.pop()
		if operator == '€':
			operand1 = self.output.pop()
			operand2 = self.output.pop()
			self.output.append(SetMember(operand2, operand1))
		elif operator == 'S':
			operand1 = self.output.pop()
			operand2 = self.output.pop()
			self.output.append(SetSubset(operand2, operand1))
		elif operator == '=':
			operand1 = self.output.pop()
			operand2 = self.output.pop()
			self.output.append(SetEquality(operand2, operand1))
		elif operator == '!':
			self.output.append(PropNegation(self.output.pop()))
		elif operator == '&':
			operand1 = self.output.pop()
			operand2 = self.output.pop()
			self.output.append(PropConjunction(operand2, operand1))
		elif operator == '|':
			operand1 = self.output.pop()
			operand2 = self.output.pop()
			self.output.append(PropDisjunction(operand2, operand1))
		elif operator == '->':
			operand1 = self.output.pop()
			operand2 = self.output.pop()
			self.output.append(PropDisjunction(PropNegation(operand2), operand1))
		elif operator == '<->':
			operand1 = self.output.pop()
			operand2 = self.output.pop()
			self.output.append(PropConjunction(PropDisjunction(PropNegation(operand2), operand1),PropDisjunction(PropNegation(operand1), operand2)))
		else:
			raise Exception('Error: When adding a new operator, unexpected operator occured.')

	def parseExpression(self):
		while len(self.input) > 0:
			if self.peekIsNextOperator():
				operator = self.getNextOperator()
				while len(self.operators) > 0 and self.operators[-1] != '[':
					if self.precedenceForOperator(operator) > self.precedenceForOperator(self.operators[-1]):
						self.addOperatorToOutput()
					else:
						break
				self.operators.append(operator)
			elif self.input[-1] == '[':
				self.operators.append(self.input.pop())
			elif self.input[-1] == ']':
				while len(self.operators) > 0 and self.operators[-1] != '[':
					self.addOperatorToOutput()
				if len(self.operators) > 0 and self.operators[-1] == '[':
					self.operators.pop()
					self.input.pop()
				else:
					raise Exception('Error: Missing left-bracket.')
			else:
				self.addAtomToOutput(self.getNextAtom())
					
		while len(self.operators) > 0:
			self.addOperatorToOutput()

		return self.output.pop()