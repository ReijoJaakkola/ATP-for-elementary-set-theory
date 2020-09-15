from PropositionalSentences import CONNECTIVES, PropVariable, PropNegation, PropConjunction, PropDisjunction
from SetTheorySentences import SETOPERATIONS, Set, SetMember, SetSubset, SetComplement, SetUnion, SetIntersection, SetEquality, SetPowerset, SetDifference

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
	def __init__(self, assumptions, conclusions):
		self.assumptions = assumptions
		self.conclusions = conclusions
		
		variables = set()
		for assumption in self.assumptions:
			variables = variables.union(calculateVariables(assumption))
		for conclusion in self.conclusions:
			variables = variables.union(calculateVariables(conclusion))
		self.variables = variables

	def freshVariable(self):
		variableSuggestion = 'x0'
		index = 0
		while variableSuggestion in self.variables:
			variableSuggestion += '_' + str(index)
			index += 1
		return variableSuggestion

	def expandSetTheoreticalDefinition(self):
		for assumption in self.assumptions:
			if assumption.type == SETOPERATIONS.MEMBER:
				# Expansion depends on what is the type of the set.
				if assumption.set.type == SETOPERATIONS.COMPLEMENT:
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
				elif assumption.set.type == SETOPERATIONS.DIFFERENCE:
					self.assumptions.remove(assumption)
					self.assumptions.append(PropConjunction(SetMember(assumption.element, assumption.set.set1),PropNegation(SetMember(assumption.element, assumption.set.set2))))
					return True
			elif assumption.type == SETOPERATIONS.SUBSET:
				self.assumptions.remove(assumption)
				variable = self.freshVariable()
				self.assumptions.append(PropDisjunction(PropNegation(SetMember(Set(variable), assumption.set1)),SetMember(Set(variable), assumption.set2)))
				return True
			elif assumption.type == SETOPERATIONS.EQUALITY:
				self.assumptions.remove(assumption)
				self.assumptions.append(PropConjunction(SetSubset(assumption.set1,assumption.set2),SetSubset(assumption.set2, assumption.set1)))
				return True

		for conclusion in self.conclusions:
			if conclusion.type == SETOPERATIONS.MEMBER:
				# Expansion depends on what is the type of the set.
				if conclusion.set.type == SETOPERATIONS.COMPLEMENT:
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
				elif conclusion.set.type == SETOPERATIONS.DIFFERENCE:
					self.conclusions.remove(conclusion)
					self.conclusions.append(PropConjunction(SetMember(conclusion.element, conclusion.set.set1),PropNegation(SetMember(conclusion.element, conclusion.set.set2))))
					return True
			elif conclusion.type == SETOPERATIONS.SUBSET:
				self.conclusions.remove(conclusion)
				variable = self.freshVariable()
				self.conclusions.append(PropDisjunction(PropNegation(SetMember(Set(variable), conclusion.set1)),SetMember(Set(variable), conclusion.set2)))
				return True
			elif conclusion.type == SETOPERATIONS.EQUALITY:
				self.conclusions.remove(conclusion)
				self.conclusions.append(PropConjunction(SetSubset(conclusion.set1,conclusion.set2),SetSubset(conclusion.set2, conclusion.set1)))
				return True

		return False

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
				deducer1 = Deducer(assumptions1, self.conclusions.copy())
				deducer2 = Deducer(assumptions2, self.conclusions.copy())

				# Run the deducers.
				result1 = deducer1.prove()
				result2 = deducer2.prove()
				return result1 and result2

		# Next, try to find a conlcusion that could be expanded.
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
				deducer1 = Deducer(self.assumptions.copy(), conclusions1)
				deducer2 = Deducer(self.assumptions.copy(), conclusions2)

				# Run the deducer.
				result1 = deducer1.prove()
				result2 = deducer2.prove()
				return result1 and result2

		# No cases left to consider.
		return False

	def prove(self):
		valid = False
		done = False
		while not done:
			# Start by checking whether the claim has already been proven.
			for assumption in self.assumptions:
				for conclusion in self.conclusions:
					if assumption == conclusion:
						valid = True
						break

			# Then try to expand the set-theoretical definitions.
			result1 = self.expandSetTheoreticalDefinition()

			# And try to also expand at least one logical definition.
			result2 = self.expandLogicalDefinition()

			if result1 == False and result2 == False:
				# No more expanding left to do.
				done = True

		if valid == True:
			# The proof was finished by expanding definitions.
			return True

		# The claim has not been proven, but we also have
		# no definitions left to expand. Try to find if we can
		# begin considering cases.
		valid = self.considerCases()

		if valid == True:
			# The claim was proved by studying cases.
			return True

		# Nothing left to do, and the claim has not been proven.
		# Thus the claim is false.
		return False