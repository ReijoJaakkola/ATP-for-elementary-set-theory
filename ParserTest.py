from SetTheorySentences import SetParser, SetTheoryParser
from Deducer import substituteVariable

parser = SetParser('x')
print(parser.parseExpression())
parser = SetParser('(xUy)')
print(parser.parseExpression())
parser = SetParser('xUy')
print(parser.parseExpression())
parser = SetParser('(xIy)')
print(parser.parseExpression())
parser = SetParser('(xI(yUz))')
print(parser.parseExpression())
parser = SetParser('((xUy)I(zUw))')
print(parser.parseExpression())
parser = SetParser('xUyUz')
print(parser.parseExpression())
parser = SetParser('CCx')
print(parser.parseExpression())
parser = SetParser('(CxUy)')
print(parser.parseExpression())
parser = SetParser('(CxUCy)')
print(parser.parseExpression())
parser = SetParser('C(xUy)')
print(parser.parseExpression())
parser = SetParser('(CxICy)')
print(parser.parseExpression())
parser = SetParser('(xUy)Uz')
print(parser.parseExpression())
parser = SetParser('Px')
print(parser.parseExpression())
parser = SetParser('(PxUy)')
print(parser.parseExpression())
parser = SetParser('PPx')
print(parser.parseExpression())
parser = SetParser('x\\y')
print(parser.parseExpression())
parser = SetParser('(xUy)\\z')
print(parser.parseExpression())
print()

parser = SetTheoryParser('x')
print(parser.parseExpression())
parser = SetTheoryParser('x=y')
print(parser.parseExpression())
parser = SetTheoryParser('CCx=x')
print(parser.parseExpression())
parser = SetTheoryParser('xS(xUy)')
print(parser.parseExpression())
parser = SetTheoryParser('x=x&x=x')
print(parser.parseExpression())
parser = SetTheoryParser('[x=y]|[!x=y]')
print(parser.parseExpression())
parser = SetTheoryParser('x=x->x=x')
print(parser.parseExpression())
parser = SetTheoryParser('[x=x]->[x=x]')
print(parser.parseExpression())
parser = SetTheoryParser('x=y->y=x')
print(parser.parseExpression())
parser = SetTheoryParser('PxSPy')
print(parser.parseExpression())

parser = SetTheoryParser('Ax[x=x]')
print(parser.parseExpression())
parser = SetTheoryParser('Ex[x=x->y=y]')
print(parser.parseExpression())
parser = SetTheoryParser('[Az[z€X->z=x]&x€X&y€Y]->x=y')
print(parser.parseExpression())

parser = SetTheoryParser('[x=x->(xUy)=y]')
print(substituteVariable('x','z',parser.parseExpression()))
parser = SetTheoryParser('Ax[x€x]')
print(substituteVariable('x','z',parser.parseExpression()))
parser = SetTheoryParser('Ay[x€x]')
print(substituteVariable('x','z',parser.parseExpression()))