#!/usr/bin/env python

import codecs
import os
import sys
import mocha

from mocha.parser import MochaParser
from mocha.generator import JavaClassGenerator, JavaStaticClassGenerator
from mocha.model import FunctionDeclaration

def main():
	sys.setrecursionlimit(5000)

	ifilename, ofilename = mocha.parse_input(sys.argv[1:])

	ibase = mocha.get_script_base(ifilename)
	package_name = mocha.build_package_name(ifilename)
	class_name = mocha.build_class_name(ifilename)

	parser = MochaParser()

	if ifilename[-9:] == "scriptlib":
		generator = JavaStaticClassGenerator()
	else:
		generator = JavaClassGenerator()

	ast = parser.parse_file(ifilename)

	functions = dict()

	#for inc in ast.includes:
	#	name = inc.name.value
	#	if len(name) >= 6 and name[:5] == "java.":
	#		continue

	#	fname = "%s/script/%s.scriptlib" % (ibase, name.replace(".", "/"))

	#	if not os.path.isfile(fname):
	#		continue

	#	alias = name.split(".")[-1]
	#	dast = parser.parse_file(fname)

	#	for stmt in dast.statements:
	#		if type(stmt) is FunctionDeclaration:
	#			func_name = "%s.%s" % (alias, stmt.name)
	#			functions[func_name] = {"return_type": stmt.return_type, "resizeable": True if "resizeable" in stmt.modifiers else False}

	if ofilename is "":
	    print generator.generate(package_name, class_name, ast, functions)
	else:
	    with open(ofilename, "w") as java_file:
	        java_file.write(generator.generate(package_name, class_name, ast, functions))
	    #with codecs.open(ofilename, "w", "utf-8") as java_file:
	    #    java_file.write(generator.generate(package_name, class_name, ast, functions).decode("utf8"))

if __name__ == "__main__":
	main()

