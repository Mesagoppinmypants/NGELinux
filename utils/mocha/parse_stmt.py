#!/usr/bin/env python

import sys

if len(sys.argv) == 1:
    print('''usage: parse_stmt.py <statement> ...
   Example: parse_expr.py 'int a = 5;' ''')
    sys.exit(1)

from mocha.parser import MochaParser

parser = MochaParser()
for stmt in sys.argv[1:]:
    print(parser.parse_statement(stmt))
