# mocha - A .script to .java translator

This utility uses the [PLY (Python Lex-Yacc)](http://www.dabeaz.com/ply/) library to generate .java files from .script file inputs. To install this library on debian based systems run the following command:

    sudo apt-get install python-ply

# parse_expr.py - Parse debugging utility/example

This tool will parse any expression given to it and print out a string representation of the AST.

    ./parse_expr.py 'a + ++(++1 * 2++)'

# script_prep.py - Primary code generation tool

This translator will accept .script or .scriptlib filenames via the -i flag and generate the .java file via stdout.

    ./script_prep.py -i ./filename.script
    ./script_prep.py -i ./library.scriptlib

Alternatively an -o flag can be given to specify a custom output target.

    ./script_prep.py -i ./src/file.script -o ./built/file.java


# Design Goals

In addition to serving as an important tool for the SWGNext's scripting system, this script serves as a learning tool for the author in language parsing. With that in mind a few notes about the overall design and intent will be kept here for reference.


The first phase of translation is turning the .script or .scriptlib file into a series of "tokens" using the ScriptLexer class. Consider the following simple bit of code:

    int a = 5;

The output from the script lexer would be a list of 8 tokens:

    INT, 'int'
    WS, ' '
    ID, 'a'
    WS, ' '
    EQ, '='
    WS, ' '
    NUM, '5'
    SEMI, ';'

This stream of tokens is then fed into the ScriptParser class which builds a tree of logical constructs held in a ScriptAST.

@TODO: More information here about how ScriptParser generates an AST and what an AST is in laymens terms.

Finally, the generated AST is passed to the JavaGenerator class which turns it into .java code that can then be either dumped to stdout or a specied file target.
