import timeit
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

		print('Proving the formula...\n')
		start = timeit.default_timer()
		deducer = Deducer([],[parsedFormula])
		result = deducer.prove()
		stop = timeit.default_timer()
		print(f'Provers result: {result}')
		print(f'Time required by the prover: {stop - start}\n')