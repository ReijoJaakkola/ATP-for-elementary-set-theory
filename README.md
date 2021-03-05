# ATP for elementary set theory
 Automated theorem prover for elementary set theory (ATPEST).
 
 The goal for ATPEST is to be able to prove first-order statements about sets. The prover is not complete, since it uses essentially a version of
 sequent calculus without contraction rule. This means that each assumption of the form QxD, where Q is a quantifier and D is a formula of set-theory,
 can be used only once. The following formula is an example of a statement which this prover can't prove.
 ```
 AzEx[[x € z] -> Ay[y € z]]
 ```
 
 We have two kinds of formulas, the first being the set-formulas.
 B ::= x | CB | B U B | B I B | PB | B \ B
 Here x is a set, C denotes "complement", U denotes "union", I denotes "intersection", P denotes "power set", and \ denotes "set-difference".
 
 Besides set-formulas, we have logic-formulas.
 D ::= x € B | B S C | B = C | !D | D & D | D | D | D -> D | D <-> D | AxD | ExD
 Here x is a set, B,C are set-formulas, S denotes subset, = denotes equality, ! denotes negation, & denotes conjunction,
 | denotes disjunction, -> denotes implication, <-> denotes equivalence, A denotes universal quantifier and E denotes existential quantifier.
 
 At the core of ATPEST is that it relies on expanding definitions of set-operators and applying rules of sequential calculus.
 For example, the following is a proof of x S (x U y).
 ```
 {} => {(xS(xUy))}
 {} => {((x_0€x)->(x_0€(xUy)))}
 {(x_0€x)} => {(x_0€(xUy))}
 {(x_0€x)} => {((x_0€x)|(x_0€y))}
 {(x_0€x)} => {(x_0€x), (x_0€y)}
 ```
 Note that the prover stopped in both of the subcases because it encountered a clear tautology: if x_0 is a member of x, then x_0 is a member of x.

 However, the ATPEST is also able to handle variables by considering different ways of expanding the definition of a subset.
 As an example, here is a proof of Cx=Cy -> x=y.
 ```
 {} => {((Cx=Cy)->(x=y))}
 {(Cx=Cy)} => {(x=y)}
 {((CxSCy)&(CySCx))} => {(x=y)}
 {((CxSCy)&(CySCx))} => {((xSy)&(ySx))}
 {(CxSCy), (CySCx)} => {((xSy)&(ySx))}
 First subcase:
        {(CxSCy), (CySCx)} => {(xSy)}
        {(CxSCy), (CySCx)} => {((x_0€x)->(x_0€y))}
        {(CxSCy), (CySCx), (x_0€x)} => {(x_0€y)}
        Expanding with variables ['x', 'x_0']:
                {(x_0€x), ((x€Cx)->(x€Cy)), ((x_0€Cy)->(x_0€Cx))} => {(x_0€y)}
                First subcase:
                        {(x_0€x), ((x_0€Cy)->(x_0€Cx))} => {(x_0€y), (x€Cx)}
                        {(x_0€x), ((x_0€Cy)->(x_0€Cx))} => {(x_0€y), (x€Cx)}
                        First subcase:
                                {(x_0€x)} => {(x_0€y), (x€Cx), (x_0€Cy)}
                                {(x_0€x)} => {(x_0€y), (x€Cx), (x_0€Cy)}
                                {(x_0€x)} => {(x_0€y), (x€Cx), !(x_0€y)}
                                {(x_0€x), (x_0€y)} => {(x_0€y), (x€Cx)}
                        Second subcase:
                                {(x_0€x), (x_0€Cx)} => {(x_0€y), (x€Cx)}
                                {(x_0€x), (x_0€Cx)} => {(x_0€y), (x€Cx)}
                                {(x_0€x), (x_0€Cx)} => {(x_0€y), !(x€x)}
                                {(x_0€x), (x_0€Cx), (x€x)} => {(x_0€y)}
                                {(x_0€x), (x€x), !(x_0€x)} => {(x_0€y)}
                                {(x_0€x), (x€x)} => {(x_0€y), (x_0€x)}
                Second subcase:
                        {(x_0€x), ((x_0€Cy)->(x_0€Cx)), (x€Cy)} => {(x_0€y)}
                        {(x_0€x), ((x_0€Cy)->(x_0€Cx)), (x€Cy)} => {(x_0€y)}
                        First subcase:
                                {(x_0€x), (x€Cy)} => {(x_0€y), (x_0€Cy)}
                                {(x_0€x), (x€Cy)} => {(x_0€y), (x_0€Cy)}
                                {(x_0€x), (x€Cy)} => {(x_0€y), !(x_0€y)}
                                {(x_0€x), (x€Cy), (x_0€y)} => {(x_0€y)}
                        Second subcase:
                                {(x_0€x), (x€Cy), (x_0€Cx)} => {(x_0€y)}
                                {(x_0€x), (x€Cy), (x_0€Cx)} => {(x_0€y)}
                                {(x_0€x), (x€Cy), !(x_0€x)} => {(x_0€y)}
                                {(x_0€x), (x€Cy)} => {(x_0€y), (x_0€x)}
 Second subcase:
        {(CxSCy), (CySCx)} => {(ySx)}
        {(CxSCy), (CySCx)} => {((x_0€y)->(x_0€x))}
        {(CxSCy), (CySCx), (x_0€y)} => {(x_0€x)}
        Expanding with variables ['x_0', 'x']:
                {(x_0€y), ((x_0€Cx)->(x_0€Cy)), ((x€Cy)->(x€Cx))} => {(x_0€x)}
                First subcase:
                        {(x_0€y), ((x€Cy)->(x€Cx))} => {(x_0€x), (x_0€Cx)}
                        {(x_0€y), ((x€Cy)->(x€Cx))} => {(x_0€x), (x_0€Cx)}
                        First subcase:
                                {(x_0€y)} => {(x_0€x), (x_0€Cx), (x€Cy)}
                                {(x_0€y)} => {(x_0€x), (x_0€Cx), (x€Cy)}
                                {(x_0€y)} => {(x_0€x), (x_0€Cx), !(x€y)}
                                {(x_0€y), (x€y)} => {(x_0€x), (x_0€Cx)}
                                {(x_0€y), (x€y)} => {(x_0€x), !(x_0€x)}
                                {(x_0€y), (x€y), (x_0€x)} => {(x_0€x)}
                        Second subcase:
                                {(x_0€y), (x€Cx)} => {(x_0€x), (x_0€Cx)}
                                {(x_0€y), (x€Cx)} => {(x_0€x), (x_0€Cx)}
                                {(x_0€y), (x€Cx)} => {(x_0€x), !(x_0€x)}
                                {(x_0€y), (x€Cx), (x_0€x)} => {(x_0€x)}
                Second subcase:
                        {(x_0€y), ((x€Cy)->(x€Cx)), (x_0€Cy)} => {(x_0€x)}
                        {(x_0€y), ((x€Cy)->(x€Cx)), (x_0€Cy)} => {(x_0€x)}
                        First subcase:
                                {(x_0€y), (x_0€Cy)} => {(x_0€x), (x€Cy)}
                                {(x_0€y), (x_0€Cy)} => {(x_0€x), (x€Cy)}
                                {(x_0€y), (x_0€Cy)} => {(x_0€x), !(x€y)}
                                {(x_0€y), (x_0€Cy), (x€y)} => {(x_0€x)}
                                {(x_0€y), (x€y), !(x_0€y)} => {(x_0€x)}
                                {(x_0€y), (x€y)} => {(x_0€x), (x_0€y)}
                        Second subcase:
                                {(x_0€y), (x_0€Cy), (x€Cx)} => {(x_0€x)}
                                {(x_0€y), (x_0€Cy), (x€Cx)} => {(x_0€x)}
                                {(x_0€y), (x_0€Cy), !(x€x)} => {(x_0€x)}
                                {(x_0€y), (x_0€Cy)} => {(x_0€x), (x€x)}
                                {(x_0€y), !(x_0€y)} => {(x_0€x), (x€x)}
                                {(x_0€y)} => {(x_0€x), (x€x), (x_0€y)}
 ```
 For clearness, the above proof does not show the backtracking that ATPEST had to do.

 As the next example, consider the following proof of x = y -> Px = Py.
 ```
 {} => {((x=y)->(Px=Py))}
 {(x=y)} => {(Px=Py)}
 {((xSy)&(ySx))} => {(Px=Py)}
 {((xSy)&(ySx))} => {((PxSPy)&(PySPx))}
 {(xSy), (ySx)} => {((PxSPy)&(PySPx))}
 First subcase:
        {(xSy), (ySx)} => {(PxSPy)}
        {(xSy), (ySx)} => {((x_0€Px)->(x_0€Py))}
        {(xSy), (ySx), (x_0€Px)} => {(x_0€Py)}
        {(xSy), (ySx), (x_0€Px)} => {(x_0Sy)}
        {(xSy), (ySx), (x_0Sx)} => {(x_0Sy)}
 Second subcase:
        {(xSy), (ySx)} => {(PySPx)}
        {(xSy), (ySx)} => {((x_0€Py)->(x_0€Px))}
        {(xSy), (ySx), (x_0€Py)} => {(x_0€Px)}
        {(xSy), (ySx), (x_0€Py)} => {(x_0Sx)}
        {(xSy), (ySx), (x_0Sy)} => {(x_0Sx)}
 ```
 The prover stopped in the first subcase, because it realized that since x_0 is a subset of x, and x is a subset of y, it can conclude that x_0 is a subset of y, which is
 what it had to prove. On the other hand, the prover stopped in the second subcase, because it realized that if x_0 is a subset of y, and y is a subset of x, then x_0
 is also a subset of x, which it what it had to prove.
 
 As an example on how quantifiers are handled, consider the following proof of [Az[z€X->z=x] & x€X & Aw[w€Y->w=y] & y€Y & X=Y] -> x=y, which states that if two singelton sets
 are identical, then so are the elements contained in the two sets. Since (at the moment) singelton set is not a primitive concept in ATPEST, we had to axiomatize it using
 universal quantification. The resulting proof is relatively short.
 ```
 {} => {((Az((z€X)->(z=x))&((x€X)&(Aw((w€Y)->(w=y))&((y€Y)&(X=Y)))))->(x=y))}
 {(Az((z€X)->(z=x))&((x€X)&(Aw((w€Y)->(w=y))&((y€Y)&(X=Y)))))} => {(x=y)}
 {Az((z€X)->(z=x)), ((x€X)&(Aw((w€Y)->(w=y))&((y€Y)&(X=Y))))} => {(x=y)}
 {Az((z€X)->(z=x)), (x€X), (Aw((w€Y)->(w=y))&((y€Y)&(X=Y)))} => {(x=y)}
 {Az((z€X)->(z=x)), (x€X), Aw((w€Y)->(w=y)), ((y€Y)&(X=Y))} => {(x=y)}
 {Az((z€X)->(z=x)), (x€X), Aw((w€Y)->(w=y)), (y€Y), (X=Y)} => {(x=y)}
 {Az((z€X)->(z=x)), (x€X), Aw((w€Y)->(w=y)), (y€Y), ((XSY)&(YSX))} => {(x=y)}
 {Az((z€X)->(z=x)), (x€X), Aw((w€Y)->(w=y)), (y€Y), ((XSY)&(YSX))} => {((xSy)&(ySx))}
 {Az((z€X)->(z=x)), (x€X), Aw((w€Y)->(w=y)), (y€Y), (XSY), (YSX)} => {((xSy)&(ySx))}
 First subcase:
        {Az((z€X)->(z=x)), (x€X), Aw((w€Y)->(w=y)), (y€Y), (XSY), (YSX)} => {(xSy)}
        Expanding universal quantifiers with variables ['x', 'x']:
                {(x€X), (y€Y), (XSY), (YSX), ((x€X)->(x=x)), ((x€Y)->(x=y))} => {(xSy)}
                First subcase:
                        {(x€X), (y€Y), (XSY), (YSX), ((x€Y)->(x=y))} => {(xSy), (x€X)}
                        {(x€X), (y€Y), (XSY), (YSX), ((x€Y)->(x=y))} => {(xSy), (x€X)}
                Second subcase:
                        {(x€X), (y€Y), (XSY), (YSX), ((x€Y)->(x=y)), (x=x)} => {(xSy)}
                        {(x€X), (y€Y), (XSY), (YSX), ((x€Y)->(x=y)), (x=x)} => {(xSy)}
                        {(x€X), (y€Y), (XSY), (YSX), ((x€Y)->(x=y)), ((xSx)&(xSx))} => {(xSy)}
                        {(x€X), (y€Y), (XSY), (YSX), ((x€Y)->(x=y)), (xSx), (xSx)} => {(xSy)}
                        First subcase:
                                {(x€X), (y€Y), (XSY), (YSX), (xSx), (xSx)} => {(xSy), (x€Y)}
                                {(x€X), (y€Y), (XSY), (YSX), (xSx), (xSx)} => {(xSy), (x€Y)}
                        Second subcase:
                                {(x€X), (y€Y), (XSY), (YSX), (xSx), (xSx), (x=y)} => {(xSy)}
                                {(x€X), (y€Y), (XSY), (YSX), (xSx), (xSx), (x=y)} => {(xSy)}
                                {(x€X), (y€Y), (XSY), (YSX), (xSx), (xSx), ((xSy)&(ySx))} => {(xSy)}
                                {(x€X), (y€Y), (XSY), (YSX), (xSx), (xSx), (xSy), (ySx)} => {(xSy)}
 Second subcase:
        {Az((z€X)->(z=x)), (x€X), Aw((w€Y)->(w=y)), (y€Y), (XSY), (YSX)} => {(ySx)}
        Expanding universal quantifiers with variables ['x', 'x']:
                {(x€X), (y€Y), (XSY), (YSX), ((x€X)->(x=x)), ((x€Y)->(x=y))} => {(ySx)}
                First subcase:
                        {(x€X), (y€Y), (XSY), (YSX), ((x€Y)->(x=y))} => {(ySx), (x€X)}
                        {(x€X), (y€Y), (XSY), (YSX), ((x€Y)->(x=y))} => {(ySx), (x€X)}
                Second subcase:
                        {(x€X), (y€Y), (XSY), (YSX), ((x€Y)->(x=y)), (x=x)} => {(ySx)}
                        {(x€X), (y€Y), (XSY), (YSX), ((x€Y)->(x=y)), (x=x)} => {(ySx)}
                        {(x€X), (y€Y), (XSY), (YSX), ((x€Y)->(x=y)), ((xSx)&(xSx))} => {(ySx)}
                        {(x€X), (y€Y), (XSY), (YSX), ((x€Y)->(x=y)), (xSx), (xSx)} => {(ySx)}
                        First subcase:
                                {(x€X), (y€Y), (XSY), (YSX), (xSx), (xSx)} => {(ySx), (x€Y)}
                                {(x€X), (y€Y), (XSY), (YSX), (xSx), (xSx)} => {(ySx), (x€Y)}
                        Second subcase:
                                {(x€X), (y€Y), (XSY), (YSX), (xSx), (xSx), (x=y)} => {(ySx)}
                                {(x€X), (y€Y), (XSY), (YSX), (xSx), (xSx), (x=y)} => {(ySx)}
                                {(x€X), (y€Y), (XSY), (YSX), (xSx), (xSx), ((xSy)&(ySx))} => {(ySx)}
                                {(x€X), (y€Y), (XSY), (YSX), (xSx), (xSx), (xSy), (ySx)} => {(ySx)}
```
Perhaps the most non-trivial theorem proved by ATPEST is the following
```
[AxAyEzAw[w€z <-> [w = x | w = y]] & AxEyAz[Ey[y€x]->[y€x & [z€x->!z€y]]]]->!Ex[x€x]
```
which essentially states that from the ZFC axioms Foundation & Pairing it follows that there does not exists a set x which is a member of itself.
