#!/usr/bin/env python

import sys

if len(sys.argv) == 1:
    print('''usage: parse_file.py <filename> ...
   Example: parse_file.py path/to/file.script ''')
    sys.exit(1)

from mocha.parser import MochaParser

parser = MochaParser()
for _file in sys.argv[1:]:
    print(parser.parse_file(_file))
