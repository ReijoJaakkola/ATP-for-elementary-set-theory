from Utils import combinations, transitiveClosure
from PropositionalSentences import CONNECTIVES, PropVariable, PropNegation, PropConjunction, PropDisjunction
from SetTheorySentences import SETOPERATIONS, Set, SetMember, SetSubset, SetComplement, SetUnion, SetIntersection, SetEquality, SetPowerset, SetDifference

def suggestFreshVariable(suggestion, reserved):
	variableSuggestion = suggestion
	index = 0
	while variableSuggestion in reserved:
		variableSuggestion += '_' + str(index)
		index += 1
	return variableSuggestion

def calculateVariables(claim):
	if claim.type == SETOPERATIONS.SET:
		return {claim.set}
	elif claim.type == SETOPERATIONS.MEMBER:
		return calculateVariables(claim.element).union(calculateVariables(claim.set))
	elif claim.type == SETOPERATIONS.SUBSET:
		return calculateVariables(claim.set1).union(calculateVariables(claim.set2))
	elif claim.type == SETOPERATIONS.COMPLEMENT:
		return calculateVariables(claim.set)
	elif claim.type == SETOPERATIONS.UNION:
		return calculateVariables(claim.set1).union(calculateVariables(claim.set2))
	elif claim.type == SETOPERATIONS.INTERSECTION:
		return calculateVariables(claim.set1).union(calculateVariables(claim.set2))
	elif claim.type == SETOPERATIONS.EQUALITY:
		return calculateVariables(claim.set1).union(calculateVariables(claim.set2))
	elif claim.type == SETOPERATIONS.POWERSET:
		return calculateVariables(claim.set)
	elif claim.type == SETOPERATIONS.DIFFERENCE:
		return calculateVariables(claim.set1).union(calculateVariables(claim.set2))
	elif claim.type == CONNECTIVES.NEG:
		return calculateVariables(claim.subformula)
	elif claim.type == CONNECTIVES.AND:
		return calculateVariables(claim.subformula1).union(calculateVariables(claim.subformula2))
	elif claim.type == CONNECTIVES.OR:
		return calculateVariables(claim.subformula1).union(calculateVariables(claim.subformula2))
	else:
		raise Exception('Error: Unrecognized claim type.')

class Deducer:
	def __init__(self, assumptions, conclusions, depth = 0):
		self.assumptions = assumptions
		self.conclusions = conclusions
		self.depth = depth

	def printStatus(self):
		assumptions = '{'
		for i in range(len(self.assumptions)):
			if i > 0:
				assumptions += ', '
			assumptions += str(self.assumptions[i])
		assumptions += '}'
		
		conclusions = '{'
		for i in range(len(self.conclusions)):
			if i > 0:
				conclusions += ', '
			conclusions += str(self.conclusions[i])
		conclusions += '}'

		print(self.depth * '\t' + f'{assumptions} => {conclusions}')

	def calculateTransitiveClosureForSubsets(self):
		# First collect the relevant assumptions.
		relevantAssumptions = []
		for assumption in self.assumptions:
			if assumption.type == SETOPERATIONS.SUBSET:
				relevantAssumptions.append(assumption)

		# Create an adjacency matrix.
		matrix = []
		for i in range(len(relevantAssumptions)):
			array = []
			for j in range(len(relevantAssumptions)):
				if relevantAssumptions[i].set2 == relevantAssumptions[j].set1:
					array.append(True)
				else:
					array.append(False)
			matrix.append(array)

		# Calculate its transitive closure.
		matrix = transitiveClosure(len(relevantAssumptions), matrix)

		# Check whether any of the memberships appear in the conclusions.
		for i in range(len(relevantAssumptions)):
			for j in range(len(relevantAssumptions)):
				if matrix[i][j] == True:
					if SetSubset(relevantAssumptions[i].set1,relevantAssumptions[j].set2) in self.conclusions:
						return True

		# Check whether we have a chain of the form
		# x \in A_1 \subseteq A_2 \subseteq ... \subseteq A_n,
		# and x \in A_n as a conclusion.
		for assumption in self.assumptions:
			if assumption.type == SETOPERATIONS.MEMBER:
				for i in range(len(relevantAssumptions)):
					for j in range(len(relevantAssumptions)):
						if matrix[i][j] == True and assumption.set == relevantAssumptions[i].set1:
							if SetMember(assumption.element, relevantAssumptions[j].set2) in self.conclusions:
								return True
		
		return False

	def isProofFinished(self):
		for assumption in self.assumptions:
				for conclusion in self.conclusions:
					if assumption == conclusion:
						return True

		if self.calculateTransitiveClosureForSubsets() == True:
			return True

		for conclusion in self.conclusions:
			if conclusion.type == SETOPERATIONS.SUBSET:
				if conclusion.set1 == conclusion.set2:
					return True
			elif conclusion.type == SETOPERATIONS.EQUALITY:
				if conclusion.set1 == conclusion.set2:
					return True

		return False

	def expandSetTheoreticalMembershipInAssumptions(self, assumption):
		if assumption.type == SETOPERATIONS.MEMBER:
			if assumption.set.type == SETOPERATIONS.SET:
				return False
			elif assumption.set.type == SETOPERATIONS.COMPLEMENT:
				self.assumptions.remove(assumption)
				self.assumptions.append(PropNegation(SetMember(assumption.element, assumption.set.set)))
				return True
			elif assumption.set.type == SETOPERATIONS.UNION:
				self.assumptions.remove(assumption)
				self.assumptions.append(PropDisjunction(SetMember(assumption.element, assumption.set.set1),SetMember(assumption.element, assumption.set.set2)))
				return True
			elif assumption.set.type == SETOPERATIONS.INTERSECTION:
				self.assumptions.remove(assumption)
				self.assumptions.append(PropConjunction(SetMember(assumption.element, assumption.set.set1),SetMember(assumption.element, assumption.set.set2)))
				return True
			elif assumption.set.type == SETOPERATIONS.POWERSET:
				self.assumptions.remove(assumption)
				self.assumptions.append(SetSubset(assumption.element, assumption.set.set))
				return True
			elif assumption.set.type == SETOPERATIONS.DIFFERENCE:
				self.assumptions.remove(assumption)
				self.assumptions.append(PropConjunction(SetMember(assumption.element, assumption.set.set1),PropNegation(SetMember(assumption.element, assumption.set.set2))))
				return True
		else:
			return False

	def expandSetTheoreticalMembershipInConclusions(self, conclusion):
		if conclusion.type == SETOPERATIONS.MEMBER:
			if conclusion.set.type == SETOPERATIONS.SET:
				return False
			elif conclusion.set.type == SETOPERATIONS.COMPLEMENT:
				self.conclusions.remove(conclusion)
				self.conclusions.append(PropNegation(SetMember(conclusion.element, conclusion.set.set)))
				return True
			elif conclusion.set.type == SETOPERATIONS.UNION:
				self.conclusions.remove(conclusion)
				self.conclusions.append(PropDisjunction(SetMember(conclusion.element, conclusion.set.set1),SetMember(conclusion.element, conclusion.set.set2)))
				return True
			elif conclusion.set.type == SETOPERATIONS.INTERSECTION:
				self.conclusions.remove(conclusion)
				self.conclusions.append(PropConjunction(SetMember(conclusion.element, conclusion.set.set1),SetMember(conclusion.element, conclusion.set.set2)))
				return True
			elif conclusion.set.type == SETOPERATIONS.POWERSET:
				self.conclusions.remove(conclusion)
				self.conclusions.append(SetSubset(conclusion.element, conclusion.set.set))
				return True
			elif conclusion.set.type == SETOPERATIONS.DIFFERENCE:
				self.conclusions.remove(conclusion)
				self.conclusions.append(PropConjunction(SetMember(conclusion.element, conclusion.set.set1),PropNegation(SetMember(conclusion.element, conclusion.set.set2))))
				return True
		else:
			return False

	def complexity(self, claim):
		if claim.type == SETOPERATIONS.SET:
			return 1
		elif claim.type == SETOPERATIONS.MEMBER:
			return self.complexity(claim.element) + self.complexity(claim.set) + 1
		elif claim.type == SETOPERATIONS.SUBSET:
			return self.complexity(claim.set1) + self.complexity(claim.set2)
		elif claim.type == SETOPERATIONS.COMPLEMENT:
			return self.complexity(claim.set) + 1
		elif claim.type == SETOPERATIONS.UNION:
			return self.complexity(claim.set1) + self.complexity(claim.set2) + 1
		elif claim.type == SETOPERATIONS.INTERSECTION:
			return self.complexity(claim.set1) + self.complexity(claim.set2) + 1
		elif claim.type == SETOPERATIONS.EQUALITY:
			return self.complexity(claim.set1) + self.complexity(claim.set2)
		elif claim.type == SETOPERATIONS.POWERSET:
			return self.complexity(claim.set) + 1
		elif claim.type == SETOPERATIONS.DIFFERENCE:
			return self.complexity(claim.set1) + self.complexity(claim.set2) + 1
		elif claim.type == CONNECTIVES.NEG:
			return self.complexity(claim.subformula)
		elif claim.type == CONNECTIVES.AND:
			return self.complexity(claim.subformula1) + self.complexity(claim.subformula2)
		elif claim.type == CONNECTIVES.OR:
			return self.complexity(claim.subformula1) + self.complexity(claim.subformula2)
		else:
			raise Exception('Error: Unrecognized claim type.')

	def expandSetTheoreticalMembership(self):
		assumptionsCopy = self.assumptions.copy()
		conclusionsCopy = self.conclusions.copy()
		definitions = []
		for assumption in assumptionsCopy:
			definitions.append([1,assumption])
		for conclusion in conclusionsCopy:
			definitions.append([2,conclusion])

		definitions.sort(key = lambda claim : self.complexity(claim[1]))
		if definitions[-1][0] == 1:
			result = self.expandSetTheoreticalMembershipInAssumptions(definitions[-1][1])
		else:
			result = self.expandSetTheoreticalMembershipInConclusions(definitions[-1][1])
		return result

	def expandEquality(self):
		for assumption in self.assumptions:
			if assumption.type == SETOPERATIONS.EQUALITY:
				self.assumptions.remove(assumption)
				self.assumptions.append(PropConjunction(SetSubset(assumption.set1,assumption.set2),SetSubset(assumption.set2, assumption.set1)))
				return True
		for conclusion in self.conclusions:
			if conclusion.type == SETOPERATIONS.EQUALITY:
				self.conclusions.remove(conclusion)
				self.conclusions.append(PropConjunction(SetSubset(conclusion.set1,conclusion.set2),SetSubset(conclusion.set2, conclusion.set1)))
				return True
		return False

	def expandSubsetIntersection(self):
		for assumption in self.assumptions:
			if assumption.type == SETOPERATIONS.SUBSET:
				if assumption.set2.type == SETOPERATIONS.INTERSECTION:
					self.assumptions.remove(assumption)
					self.assumptions.append(SetSubset(assumption.set1, assumption.set2.set1))
					self.assumptions.append(SetSubset(assumption.set1, assumption.set2.set2))
					return True

		for conclusion in self.conclusions:
			if conclusion.type == SETOPERATIONS.SUBSET:
				if conclusion.set2.type == SETOPERATIONS.INTERSECTION:
					self.conclusions.remove(conclusion)
					self.conclusions.append(SetSubset(conclusion.set1, conclusion.set2.set1))
					self.conclusions.append(SetSubset(conclusion.set1, conclusion.set2.set2))
					return True

	def expandLogicalDefinition(self):
		for assumption in self.assumptions:
			if assumption.type == CONNECTIVES.NEG:
				# Add the immediate subformula to conclusions.
				self.conclusions.append(assumption.subformula)
				self.assumptions.remove(assumption)
				# Return True to indicate success.
				return True
			elif assumption.type == CONNECTIVES.AND:
				# Add the immediate subformulas to assumptions.
				self.assumptions.append(assumption.subformula1)
				self.assumptions.append(assumption.subformula2)
				self.assumptions.remove(assumption)
				# Return True to indicate success.
				return True

		for conclusion in self.conclusions:
			if conclusion.type == CONNECTIVES.NEG:
				# Add the immediate subformula to assumptions.
				self.assumptions.append(conclusion.subformula)
				self.conclusions.remove(conclusion)
				# Return true to indicate success.
				return True
			elif conclusion.type == CONNECTIVES.OR:
				# Add the immediate subformulas to conclusions.
				self.conclusions.append(conclusion.subformula1)
				self.conclusions.append(conclusion.subformula2)
				self.conclusions.remove(conclusion)
				# Return true to indicate success.
				return True

		# Failed to expand definitions, return false to indicate this.
		return False

	def considerCases(self):
		# First try to expand a conclusion.
		for conclusion in self.conclusions:
			if conclusion.type == CONNECTIVES.AND:
				# We have to deal with two cases based corresponding to the two subformulas.
				conclusions1 = self.conclusions.copy()
				conclusions1.remove(conclusion)
				conclusions1.append(conclusion.subformula1)
				conclusions2 = self.conclusions.copy()
				conclusions2.remove(conclusion)
				conclusions2.append(conclusion.subformula2)

				# Initialize two deducers for the different cases.
				deducer1 = Deducer(self.assumptions.copy(), conclusions1, self.depth + 1)
				deducer2 = Deducer(self.assumptions.copy(), conclusions2, self.depth + 1)

				# Run the deducer.
				print(self.depth * '\t' + f'First subcase:')
				result1 = deducer1.prove()
				print(self.depth * '\t' + f'Second subcase:')
				result2 = deducer2.prove()
				return result1 and result2

		# Next, try to find an assumption that could be expanded.
		for assumption in self.assumptions:
			if assumption.type == CONNECTIVES.OR:
				# We have to deal with two cases based corresponding to the two subformulas.
				assumptions1 = self.assumptions.copy()
				assumptions1.remove(assumption)
				assumptions1.append(assumption.subformula1)
				assumptions2 = self.assumptions.copy()
				assumptions2.remove(assumption)
				assumptions2.append(assumption.subformula2)

				# Initialize two deducers for the different cases.
				deducer1 = Deducer(assumptions1, self.conclusions.copy(), self.depth + 1)
				deducer2 = Deducer(assumptions2, self.conclusions.copy(), self.depth + 1)

				# Run the deducers.
				print(self.depth * '\t' + f'First subcase:')
				deducer1.printStatus()
				result1 = deducer1.prove()
				print(self.depth * '\t' + f'Second subcase:')
				deducer2.printStatus()
				result2 = deducer2.prove()
				return result1 and result2

		# No cases left to consider.
		return False

	def expandSubsetRelationsInConclusions(self):
		# First calculate what variables already appear in the conclusions and in the assumptions.
		reservedVariables = set()
		for assumption in self.assumptions:
			reservedVariables = reservedVariables.union(calculateVariables(assumption))
		for conclusion in self.conclusions:
			reservedVariables = reservedVariables.union(calculateVariables(conclusion))

		# Collect all the relevant conclusions.
		relevantConclusions = []
		for conclusion in self.conclusions:
			if conclusion.type == SETOPERATIONS.SUBSET:
				relevantConclusions.append(conclusion)
		
		if len(relevantConclusions) == 0:
			# No subset relations to expand.
			return False

		for conclusion in relevantConclusions:
			freshVariable = suggestFreshVariable('x', reservedVariables)
			reservedVariables = reservedVariables.union({freshVariable})

			self.conclusions.remove(conclusion)
			self.conclusions.append(PropDisjunction(PropNegation(SetMember(Set(freshVariable), conclusion.set1)),SetMember(Set(freshVariable), conclusion.set2)))

		return True

	def doWeHaveSubsetRelationsInAssumptions(self):
		for assumption in self.assumptions:
			if assumption.type == SETOPERATIONS.SUBSET:
				return True
		return False

	def considerDifferentVariables(self):
		# First calculate what assumptions are subset relations.
		relevantAssumptions = []
		for assumption in self.assumptions:
			if assumption.type == SETOPERATIONS.SUBSET:
				relevantAssumptions.append(assumption)

		if len(relevantAssumptions) == 0:
			# No subset relations among the assumptions.
			return False

		# Calculate the variables occuring in the assumptions and in the conclusions.
		freeVariables = set()
		for assumption in self.assumptions:
			freeVariables = freeVariables.union(calculateVariables(assumption))
		for conclusion in self.conclusions:
			freeVariables = freeVariables.union(calculateVariables(conclusion))

		# Form all the combinations of freeVariables of length len(relevantAssumptions),
		# and check whether any of them works.
		combs = combinations(len(relevantAssumptions), list(freeVariables))
		valid = False
		for combination in combs:
			assumptionsCopy = self.assumptions.copy()
			
			for i in range(len(relevantAssumptions)):
				assumptionsCopy.remove(relevantAssumptions[i])
				assumptionsCopy.append(PropDisjunction(PropNegation(SetMember(Set(combination[i]), relevantAssumptions[i].set1)),SetMember(Set(combination[i]), relevantAssumptions[i].set2)))
			
			# Initialize a deducer for this case.
			deducer = Deducer(assumptionsCopy, self.conclusions.copy(), self.depth + 1)

			# Run the deducer.
			print(self.depth * '\t' + f'Expanding with variables {combination}:')
			valid = deducer.prove()

			if valid == True:
				# We found a valid combination, so no need to continue.
				return True

		# None of the combinations worked.
		return False

	def prove(self):
		self.printStatus()
		
		valid = False
		done = False
		while not done:
			if self.isProofFinished():
				valid = True
				break

			# Expand all logical definitions.
			result1 = False
			while True:
				if self.expandLogicalDefinition():
					self.printStatus()
					result1 = True
				else:
					break

			if result1 == True and self.isProofFinished():
				valid = True
				break

			# Expand all equalities.
			result2 = False
			while True:
				if self.expandEquality():
					self.printStatus()
					result2 = True
				else:
					break

			if result2 == True and self.isProofFinished():
				valid = True
				break

			# Expand all subset relations of the form x S y I z.
			result3 = False
			while True:
				if self.expandSubsetIntersection():
					self.printStatus()
					result3 = True
				else:
					break

			if result3 == True and self.isProofFinished():
				valid = True
				break

			# Expand a single set-theoretic membership.
			result4 = self.expandSetTheoreticalMembership()
			if result4 == True:
				self.printStatus()
				if self.isProofFinished():
					valid = True
					break

			if result1 == False and result2 == False and result3 == False and result4 == False:
				done = True

		if valid == True:
			# The proof was finished by expanding logical definitions and memberships.
			return True
		
		# There are no more logical definitions that can be expanded, nor are there
		# memberships between sets that could be expanded. Try to see if we can proceed
		# by considering different cases (i.e. check whether assumption contains something like A or B,
		# or that conclusion contains something like A and B.)
		valid = self.considerCases()
		if valid == True:
			# The claim was proved by studying cases.
			return True

		# Only thing that can be remaining now is subset relations between sets.
		# What we do now is that we will expand all the subset relations in the conclusions.
		# This will be done by using the definition of subset relation
		# x S y <=> For all z, z € x -> z € y.
		# Each time we expand a subset relation a fresh variable will be introduced. These will
		# be collected as the active variables.
		result = self.expandSubsetRelationsInConclusions()
		if result == True:
			# We have expanded subset relations in the definitions, 
			# so try to prove the claim now with the fresh conclusions.
			valid = self.prove()
			if valid == True:
				# We succeeded in proving the claim.
				return True
		else:
			if self.doWeHaveSubsetRelationsInAssumptions():
				# Go trough all the subset relations in the assumptions, and try to
				# expand them with all the possible combinations for freshVariables.
				valid = self.considerDifferentVariables()
				if valid == True:
					# We succeeded in proving the claim.
					return True

		# Nothing left to do, and the claim has not been proven.
		# Could not find a proof.
		return False