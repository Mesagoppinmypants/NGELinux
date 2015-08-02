#!/usr/bin/env python

import sys

if len(sys.argv) == 1:
    print('''usage: tokenizer.py <filename> ...
   Example: tokenizer.py '/path/to/file.script' ''')
    sys.exit(1)

from mocha.parser import MochaParser

parser = MochaParser()
for filename in sys.argv[1:]:
    print(parser.tokenize_file(filename))
