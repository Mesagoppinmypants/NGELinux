#!/usr/bin/env python

import sys

if len(sys.argv) == 1:
    print('''usage: parse_expr.py <expression> ...
   Example: parse_expr.py '1+2' '3' 'j = (int) i + 3' ''')
    sys.exit(1)

from mocha.parser import MochaParser

parser = MochaParser()
for expr in sys.argv[1:]:
    print(parser.parse_expression(expr))
