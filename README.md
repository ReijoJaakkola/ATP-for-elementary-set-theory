# ATP for elementary set theory
 Automated theorem prover for elementary set theory (ATPEST).
 
 The goal for ATPEST is to be able to prove statements of the form
 "For all x1,...,xn, A(x1,...,xn) holds"
 where A(x1,...,xn) is a quantifier-free first-order formula over the vocabulary {€}, where € denotes the membership relation for sets.
 
 We have two kinds of formulas, the first being the set-formulas.
 B ::= x | CB | B U B | B I B
 Here x is a set, C denotes "complement", U denotes "union" and "I" denotes intersection.
 
 Besides set-formulas, we have logic-formulas.
 A ::= x € B | B S C | B = C | !A | A & A | A | A | A -> A | A <-> A
 Here x is a set, B,C are set-formulas, S denotes subset, = denotes equality, ! denotes negation, & denotes conjunction,
 | denotes disjunction, -> denotes implication and <-> denotes equivalence.
 
 At the core of ATPEST is that it relies on expanding definitions of set-operators and applying rules of sequential calculus.
 For example, the following is a proof of x=x.
 
     |- x=x            
     |- (xSx) & (xSx)  : Use the definition of =.
 
 Case 1.               : Prove both subgoals.
     |- (xSx)          : First subgoal
     |- (!y€x | y€x)   : Use the definition of S.
     |- !y€x, y€x      : Rule for |
 y€x |- y€x            : Rule for !
 
 This is clearly a tautology, which proves the first subgoal.
 Proof for the second subgoal is similar.
