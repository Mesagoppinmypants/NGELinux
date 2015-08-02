#!/usr/bin/env python

import sys

if len(sys.argv) == 1:
    print('''usage: test_script.py <filename> ...
   Example: test_script.py '/path/to/file.script' ''')
    sys.exit(1)

from mocha.parser import MochaParser

parser = MochaParser()
parser.parse_file(sys.argv[1])
