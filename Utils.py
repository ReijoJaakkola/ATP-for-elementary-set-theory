def subtuplesUtil(subtupleLength, subtuples, tuple, index, subtuple):
	if len(subtuple) == subtupleLength:
		subtuples.append(subtuple.copy())

	if index == len(tuple):
		return

	for i in range(len(tuple)):
		subtuple.append(tuple[i])

		subtuplesUtil(subtupleLength,subtuples,tuple,index + 1,subtuple)

		subtuple.pop(-1)

def subtuples(subtupleLength, tuple):
	subtuples = []
	
	index = 0
	subtuple = []
	subtuplesUtil(subtupleLength, subtuples, tuple, index, subtuple)

	return subtuples

def combinationsUtils(depth, tuple, combination, combinations):
	if depth == 0:
		combinations.append(combination.copy())
		return
	else:
		for i in range(len(tuple)):
			combination.append(tuple[i])
			combinationsUtils(depth - 1, tuple, combination, combinations)
			combination.pop(-1)

def combinations(length, tuple):
	combination = []
	combinations = []
	combinationsUtils(length, tuple, combination, combinations)
	return combinations