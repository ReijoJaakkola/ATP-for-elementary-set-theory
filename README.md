# ATP for elementary set theory
 Automated theorem prover for elementary set theory (ATPEST).
 
 The goal for ATPEST is to be able to prove statements of the form
 "For all x1,...,xn, A(x1,...,xn) holds"
 where A(x1,...,xn) is a quantifier-free first-order formula over the vocabulary {€}, where € denotes the membership relation for sets.
 
 We have two kinds of formulas, the first being the set-formulas.
 B ::= x | CB | B U B | B I B | PB | B \ B
 Here x is a set, C denotes "complement", U denotes "union", I denotes "intersection", P denotes "power set", and \ denotes "set-difference".
 
 Besides set-formulas, we have logic-formulas.
 A ::= x € B | B S C | B = C | !A | A & A | A | A | A -> A | A <-> A
 Here x is a set, B,C are set-formulas, S denotes subset, = denotes equality, ! denotes negation, & denotes conjunction,
 | denotes disjunction, -> denotes implication and <-> denotes equivalence.
 
 At the core of ATPEST is that it relies on expanding definitions of set-operators and applying rules of sequential calculus.
 For example, the following is a proof of x S (x U y).
 ```
 {} => {(xS(xUy))}
 {} => {(!(x_0€x)|(x_0€(xUy)))}
 {} => {!(x_0€x), (x_0€(xUy))}
 {(x_0€x)} => {(x_0€(xUy))}
 {(x_0€x)} => {((x_0€x)|(x_0€y))}
 {(x_0€x)} => {(x_0€x), (x_0€y)}
 ```
 Note that the prover stopped in both of the subcases because it encountered a clear tautology: if x_0 is a member of x, then x_0 is a member of x.

 However, the ATPEST is also able to handle variables by considering different ways of expanding the definition of a subset.
 As an example, here is a proof of Cx=Cy -> x=y.
 ```
 {} => {(!(Cx=Cy)|(x=y))}
 {} => {!(Cx=Cy), (x=y)}
 {(Cx=Cy)} => {(x=y)}
 {((CxSCy)&(CySCx))} => {(x=y)}
 {((CxSCy)&(CySCx))} => {((xSy)&(ySx))}
 {(CxSCy), (CySCx)} => {((xSy)&(ySx))}
 First subcase:
        {(CxSCy), (CySCx)} => {(xSy)}
        {(CxSCy), (CySCx)} => {(!(x_0€x)|(x_0€y))}
        {(CxSCy), (CySCx)} => {!(x_0€x), (x_0€y)}
        {(CxSCy), (CySCx), (x_0€x)} => {(x_0€y)}
        Expanding with variables ['x_0', 'x_0']:
                {(x_0€x), (!(x_0€Cx)|(x_0€Cy)), (!(x_0€Cy)|(x_0€Cx))} => {(x_0€y)}
                First subcase:
                        {(x_0€x), (!(x_0€Cy)|(x_0€Cx)), !(x_0€Cx)} => {(x_0€y)}
                        {(x_0€x), (!(x_0€Cy)|(x_0€Cx)), !(x_0€Cx)} => {(x_0€y)}
                        {(x_0€x), (!(x_0€Cy)|(x_0€Cx))} => {(x_0€y), (x_0€Cx)}
                        First subcase:
                                {(x_0€x), !(x_0€Cy)} => {(x_0€y), (x_0€Cx)}
                                {(x_0€x), !(x_0€Cy)} => {(x_0€y), (x_0€Cx)}
                                {(x_0€x)} => {(x_0€y), (x_0€Cx), (x_0€Cy)}
                                {(x_0€x)} => {(x_0€y), (x_0€Cx), !(x_0€y)}
                                {(x_0€x), (x_0€y)} => {(x_0€y), (x_0€Cx)}
                        Second subcase:
                                {(x_0€x), (x_0€Cx)} => {(x_0€y), (x_0€Cx)}
                                {(x_0€x), (x_0€Cx)} => {(x_0€y), (x_0€Cx)}
                Second subcase:
                        {(x_0€x), (!(x_0€Cy)|(x_0€Cx)), (x_0€Cy)} => {(x_0€y)}
                        {(x_0€x), (!(x_0€Cy)|(x_0€Cx)), (x_0€Cy)} => {(x_0€y)}
                        First subcase:
                                {(x_0€x), (x_0€Cy), !(x_0€Cy)} => {(x_0€y)}
                                {(x_0€x), (x_0€Cy), !(x_0€Cy)} => {(x_0€y)}
                                {(x_0€x), (x_0€Cy)} => {(x_0€y), (x_0€Cy)}
                        Second subcase:
                                {(x_0€x), (x_0€Cy), (x_0€Cx)} => {(x_0€y)}
                                {(x_0€x), (x_0€Cy), (x_0€Cx)} => {(x_0€y)}
                                {(x_0€x), (x_0€Cy), !(x_0€x)} => {(x_0€y)}
                                {(x_0€x), (x_0€Cy)} => {(x_0€y), (x_0€x)}
 Second subcase:
        {(CxSCy), (CySCx)} => {(ySx)}
        {(CxSCy), (CySCx)} => {(!(x_0€y)|(x_0€x))}
        {(CxSCy), (CySCx)} => {!(x_0€y), (x_0€x)}
        {(CxSCy), (CySCx), (x_0€y)} => {(x_0€x)}
        Expanding with variables ['x_0', 'x_0']:
                {(x_0€y), (!(x_0€Cx)|(x_0€Cy)), (!(x_0€Cy)|(x_0€Cx))} => {(x_0€x)}
                First subcase:
                        {(x_0€y), (!(x_0€Cy)|(x_0€Cx)), !(x_0€Cx)} => {(x_0€x)}
                        {(x_0€y), (!(x_0€Cy)|(x_0€Cx)), !(x_0€Cx)} => {(x_0€x)}
                        {(x_0€y), (!(x_0€Cy)|(x_0€Cx))} => {(x_0€x), (x_0€Cx)}
                        First subcase:
                                {(x_0€y), !(x_0€Cy)} => {(x_0€x), (x_0€Cx)}
                                {(x_0€y), !(x_0€Cy)} => {(x_0€x), (x_0€Cx)}
                                {(x_0€y)} => {(x_0€x), (x_0€Cx), (x_0€Cy)}
                                {(x_0€y)} => {(x_0€x), (x_0€Cx), !(x_0€y)}
                                {(x_0€y), (x_0€y)} => {(x_0€x), (x_0€Cx)}
                                {(x_0€y), (x_0€y)} => {(x_0€x), !(x_0€x)}
                                {(x_0€y), (x_0€y), (x_0€x)} => {(x_0€x)}
                        Second subcase:
                                {(x_0€y), (x_0€Cx)} => {(x_0€x), (x_0€Cx)}
                                {(x_0€y), (x_0€Cx)} => {(x_0€x), (x_0€Cx)}
                Second subcase:
                        {(x_0€y), (!(x_0€Cy)|(x_0€Cx)), (x_0€Cy)} => {(x_0€x)}
                        {(x_0€y), (!(x_0€Cy)|(x_0€Cx)), (x_0€Cy)} => {(x_0€x)}
                        First subcase:
                                {(x_0€y), (x_0€Cy), !(x_0€Cy)} => {(x_0€x)}
                                {(x_0€y), (x_0€Cy), !(x_0€Cy)} => {(x_0€x)}
                                {(x_0€y), (x_0€Cy)} => {(x_0€x), (x_0€Cy)}
                        Second subcase:
                                {(x_0€y), (x_0€Cy), (x_0€Cx)} => {(x_0€x)}
                                {(x_0€y), (x_0€Cy), (x_0€Cx)} => {(x_0€x)}
                                {(x_0€y), (x_0€Cy), !(x_0€x)} => {(x_0€x)}
                                {(x_0€y), (x_0€Cy)} => {(x_0€x), (x_0€x)}
                                {(x_0€y), !(x_0€y)} => {(x_0€x), (x_0€x)}
                                {(x_0€y)} => {(x_0€x), (x_0€x), (x_0€y)}
 ```
 For clearness, the above proof does not show the backtracking that ATPEST had to do.

 As a final example, consider the following proof of x = y -> Px = Py.
 ```
 {} => {(!(x=y)|(Px=Py))}
 {} => {!(x=y), (Px=Py)}
 {(x=y)} => {(Px=Py)}
 {((xSy)&(ySx))} => {(Px=Py)}
 {((xSy)&(ySx))} => {((PxSPy)&(PySPx))}
 {(xSy), (ySx)} => {((PxSPy)&(PySPx))}
 First subcase:
        {(xSy), (ySx)} => {(PxSPy)}
        {(xSy), (ySx)} => {(!(x_0€Px)|(x_0€Py))}
        {(xSy), (ySx)} => {!(x_0€Px), (x_0€Py)}
        {(xSy), (ySx), (x_0€Px)} => {(x_0€Py)}
        {(xSy), (ySx), (x_0€Px)} => {(x_0Sy)}
        {(xSy), (ySx), (x_0Sx)} => {(x_0Sy)}
 Second subcase:
        {(xSy), (ySx)} => {(PySPx)}
        {(xSy), (ySx)} => {(!(x_0€Py)|(x_0€Px))}
        {(xSy), (ySx)} => {!(x_0€Py), (x_0€Px)}
        {(xSy), (ySx), (x_0€Py)} => {(x_0€Px)}
        {(xSy), (ySx), (x_0€Py)} => {(x_0Sx)}
        {(xSy), (ySx), (x_0Sy)} => {(x_0Sx)}
 ```
 The prover stopped in the first subcase, because it realized that since x_0 is a subset of x, and x is a subset of y, it can conclude that x_0 is a subset of y, which is
 what it had to prove. On the other hand, the prover stopped in the second subcase, because it realized that if x_0 is a subset of y, and y is a subset of x, then x_0
 is also a subset of x, which it what it had to prove.
