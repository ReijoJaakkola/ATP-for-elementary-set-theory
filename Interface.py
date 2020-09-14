from Deducer import Deducer
from SetTheorySentences import SetTheoryParser

if __name__ == "__main__":
	print('Welcome to ATPEST!\n')

	while True:
		formula = input('Write down the formula: ').replace(' ','')
		if formula == 'quit':
			break

		print('Parsing the formula...')
		parser = SetTheoryParser(formula)
		parsedFormula = parser.parseExpression()

		print('Proving the formula...')
		deducer = Deducer([],[parsedFormula])
		result = deducer.prove()
		print(f'Provers result: {result}\n')