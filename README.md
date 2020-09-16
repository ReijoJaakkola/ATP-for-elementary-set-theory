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
 For example, the following is a proof of x=x.
 ```
{} => {(x=x)}
{} => {((xSx)&(xSx))}
First subcase:
        {} => {(xSx)}
        {} => {(!(x_0€x)|(x_0€x))}
        {} => {!(x_0€x), (x_0€x)}
        {(x_0€x)} => {(x_0€x)}
Second subcase:
        {} => {(xSx)}
        {} => {(!(x_0€x)|(x_0€x))}
        {} => {!(x_0€x), (x_0€x)}
        {(x_0€x)} => {(x_0€x)}
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
        Expanding with variables ['y', 'x_0']:
                {(x_0€x), (!(y€Cx)|(y€Cy)), (!(x_0€Cy)|(x_0€Cx))} => {(x_0€y)}
                First subcase:
                        {(x_0€x), (!(x_0€Cy)|(x_0€Cx)), !(y€Cx)} => {(x_0€y)}
                        {(x_0€x), (!(x_0€Cy)|(x_0€Cx)), !(y€Cx)} => {(x_0€y)}
                        {(x_0€x), (!(x_0€Cy)|(x_0€Cx))} => {(x_0€y), (y€Cx)}
                        First subcase:
                                {(x_0€x), !(x_0€Cy)} => {(x_0€y), (y€Cx)}
                                {(x_0€x), !(x_0€Cy)} => {(x_0€y), (y€Cx)}
                                {(x_0€x)} => {(x_0€y), (y€Cx), (x_0€Cy)}
                                {(x_0€x)} => {(x_0€y), (y€Cx), !(x_0€y)}
                                {(x_0€x), (x_0€y)} => {(x_0€y), (y€Cx)}
                        Second subcase:
                                {(x_0€x), (x_0€Cx)} => {(x_0€y), (y€Cx)}
                                {(x_0€x), (x_0€Cx)} => {(x_0€y), (y€Cx)}
                                {(x_0€x), (x_0€Cx)} => {(x_0€y), !(y€x)}
                                {(x_0€x), (x_0€Cx), (y€x)} => {(x_0€y)}
                                {(x_0€x), (y€x), !(x_0€x)} => {(x_0€y)}
                                {(x_0€x), (y€x)} => {(x_0€y), (x_0€x)}
                Second subcase:
                        {(x_0€x), (!(x_0€Cy)|(x_0€Cx)), (y€Cy)} => {(x_0€y)}
                        {(x_0€x), (!(x_0€Cy)|(x_0€Cx)), (y€Cy)} => {(x_0€y)}
                        First subcase:
                                {(x_0€x), (y€Cy), !(x_0€Cy)} => {(x_0€y)}
                                {(x_0€x), (y€Cy), !(x_0€Cy)} => {(x_0€y)}
                                {(x_0€x), (y€Cy)} => {(x_0€y), (x_0€Cy)}
                                {(x_0€x), (y€Cy)} => {(x_0€y), !(x_0€y)}
                                {(x_0€x), (y€Cy), (x_0€y)} => {(x_0€y)}
                        Second subcase:
                                {(x_0€x), (y€Cy), (x_0€Cx)} => {(x_0€y)}
                                {(x_0€x), (y€Cy), (x_0€Cx)} => {(x_0€y)}
                                {(x_0€x), (y€Cy), !(x_0€x)} => {(x_0€y)}
                                {(x_0€x), (y€Cy)} => {(x_0€y), (x_0€x)}
Second subcase:
        {(CxSCy), (CySCx)} => {(ySx)}
        {(CxSCy), (CySCx)} => {(!(x_0€y)|(x_0€x))}
        {(CxSCy), (CySCx)} => {!(x_0€y), (x_0€x)}
        {(CxSCy), (CySCx), (x_0€y)} => {(x_0€x)}
        Expanding with variables ['x_0', 'y']:
                {(x_0€y), (!(x_0€Cx)|(x_0€Cy)), (!(y€Cy)|(y€Cx))} => {(x_0€x)}
                First subcase:
                        {(x_0€y), (!(y€Cy)|(y€Cx)), !(x_0€Cx)} => {(x_0€x)}
                        {(x_0€y), (!(y€Cy)|(y€Cx)), !(x_0€Cx)} => {(x_0€x)}
                        {(x_0€y), (!(y€Cy)|(y€Cx))} => {(x_0€x), (x_0€Cx)}
                        First subcase:
                                {(x_0€y), !(y€Cy)} => {(x_0€x), (x_0€Cx)}
                                {(x_0€y), !(y€Cy)} => {(x_0€x), (x_0€Cx)}
                                {(x_0€y)} => {(x_0€x), (x_0€Cx), (y€Cy)}
                                {(x_0€y)} => {(x_0€x), (x_0€Cx), !(y€y)}
                                {(x_0€y), (y€y)} => {(x_0€x), (x_0€Cx)}
                                {(x_0€y), (y€y)} => {(x_0€x), !(x_0€x)}
                                {(x_0€y), (y€y), (x_0€x)} => {(x_0€x)}
                        Second subcase:
                                {(x_0€y), (y€Cx)} => {(x_0€x), (x_0€Cx)}
                                {(x_0€y), (y€Cx)} => {(x_0€x), (x_0€Cx)}
                Second subcase:
                        {(x_0€y), (!(y€Cy)|(y€Cx)), (x_0€Cy)} => {(x_0€x)}
                        {(x_0€y), (!(y€Cy)|(y€Cx)), (x_0€Cy)} => {(x_0€x)}
                        First subcase:
                                {(x_0€y), (x_0€Cy), !(y€Cy)} => {(x_0€x)}
                                {(x_0€y), (x_0€Cy), !(y€Cy)} => {(x_0€x)}
                                {(x_0€y), (x_0€Cy)} => {(x_0€x), (y€Cy)}
                                {(x_0€y), (x_0€Cy)} => {(x_0€x), !(y€y)}
                                {(x_0€y), (x_0€Cy), (y€y)} => {(x_0€x)}
                                {(x_0€y), (y€y), !(x_0€y)} => {(x_0€x)}
                                {(x_0€y), (y€y)} => {(x_0€x), (x_0€y)}
                        Second subcase:
                                {(x_0€y), (x_0€Cy), (y€Cx)} => {(x_0€x)}
                                {(x_0€y), (x_0€Cy), (y€Cx)} => {(x_0€x)}
                                {(x_0€y), (x_0€Cy), !(y€x)} => {(x_0€x)}
                                {(x_0€y), (x_0€Cy)} => {(x_0€x), (y€x)}
                                {(x_0€y), !(x_0€y)} => {(x_0€x), (y€x)}
                                {(x_0€y)} => {(x_0€x), (y€x), (x_0€y)}
 ```
 For clearness, the above proof does not show the backtracking that ATPEST had to do.
