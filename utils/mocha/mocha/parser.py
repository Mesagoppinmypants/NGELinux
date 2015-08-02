#!/usr/bin/env python

import ply.lex as lex
import ply.yacc as yacc

from .model import *


class Coord(object):
    """ Coordinates of a syntatic element:
            - Filename
            - Line number
            - (optional) column number
    """
    def __init__(self, file, line, column=None):
        self.file = file
        self.line = line
        self.column = column

    def __str__(self):
        str = "%s:%s" % (self.file, self.line)
        if self.column: str += ":%s" % self.column
        return str


class ParseError(Exception): pass


class BaseParser(object):

    def _coord(self, lineno, column=None):
        return Coord(
                file=self.lexer.filename,
                line=lineno,
                column=column)

    def _parse_error(self, msg, coord):
        raise ParseError("%s: %s" % (coord, msg))


class MochaLexer(object):

    def __init__(self, error_func=None):
        self.error_func = error_func
        self.filename = ''

    def build(self, **kwargs):
        self.lexer = lex.lex(object=self, **kwargs)

    def reset_lineno(self):
        """ Resets the internal line number counter of the lexer.
        """
        self.lexer.lineno = 1

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        self.last_token = self.lexer.token()
        return self.last_token

    def find_tok_column(self, token):
        """ Find the column of the token in its line.
        """
        last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
        return token.lexpos - last_cr

    def _error(self, msg, token):
        location = self._make_tok_location(token)
        self.error_func(msg, location[0], location[1])
        self.lexer.skip(1)

    def _make_tok_location(self, token):
        return (token.lineno, self.find_tok_column(token))

    keywords = ('boolean', 'void', 'byte', 'short', 'int', 'long', 'char',
        'float', 'double', 'new', 'include', 'const', 'true', 'false',
        'null', 'if', 'else', 'while', 'for', 'do', 'break', 'continue',
        'return', 'switch', 'case', 'default', 'resizeable', 'inherits',
        'instanceof', 'throw', 'try', 'catch', 'finally', 'define',
        'ifdef', 'endif')

    tokens = [
        'NAME',

        'INT_CONST',
        'INT_CONST_HEX',
        'FLOAT_CONST',
        'CHAR_LITERAL',
        'STRING_LITERAL',

        # Operators (+,-,*,/,%,|,&,~,^,<<,>>, ||, &&, !, <, <=, >, >=, ==, !=)
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
        'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
        'LOR', 'LAND', 'LNOT',
        'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

        # Assignment (=, *=, /=, %=, +=, -=, <<=, >>=, &=, ^=, |=)
        'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
        'LSHIFTEQUAL','RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL', 'OREQUAL',

        # Ternary operator (?)
        'TERNARY',

        # Hash symbol
        'HASH',

        # Increment/decrement (++,--)
        'PLUSPLUS', 'MINUSMINUS',

        # Delimeters ( ) [ ] { } , . ; :
        'LPAREN', 'RPAREN',
        'LBRACKET', 'RBRACKET',
        'LBRACE', 'RBRACE',
        'COMMA', 'PERIOD', 'SEMI', 'COLON',

    ] + [ k.upper() for k in keywords ]

    hex_prefix = '0[xX]'
    hex_digits = '[0-9a-fA-F]+'

    integer_suffix_opt = r'(([uU]ll)|([uU]LL)|(ll[uU]?)|(LL[uU]?)|([uU][lL])|([lL][uU]?)|[uU])?'

    # literals
    t_INT_CONST = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'
    t_INT_CONST_HEX = hex_prefix + hex_digits + integer_suffix_opt
    t_FLOAT_CONST = r'([0-9]+[.]?[fF]|[0-9]*(\.[0-9]+))([fF])?'
    t_CHAR_LITERAL = r'\'([^\\\n]|(\\.))*?\''
    t_STRING_LITERAL = r'\"(\\.|[^"])*\"'

    # Comment (C++-Style)
    def t_CPPCOMMENT(self, t):
        r'//.*\n?'
        t.lexer.lineno += 1
        pass

    # Comment (C-Style)
    def t_COMMENT(self, t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')
        pass

    # Operators
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MOD = r'%'
    t_OR = r'\|'
    t_AND = r'&'
    t_NOT = r'~'
    t_XOR = r'\^'
    t_LSHIFT = r'<<'
    t_RSHIFT = r'>>'
    t_LOR = r'\|\|'
    t_LAND = r'&&'
    t_LNOT = r'!'
    t_LT = r'<'
    t_GT = r'>'
    t_LE = r'<='
    t_GE = r'>='
    t_EQ = r'=='
    t_NE = r'!='

    # Assignment operators
    t_EQUALS = r'='
    t_TIMESEQUAL = r'\*='
    t_DIVEQUAL = r'/='
    t_MODEQUAL = r'%='
    t_PLUSEQUAL = r'\+='
    t_MINUSEQUAL = r'-='
    t_LSHIFTEQUAL = r'<<='
    t_RSHIFTEQUAL = r'>>='
    t_ANDEQUAL = r'&='
    t_OREQUAL = r'\|='
    t_XOREQUAL = r'^='

    # Increment/decrement
    t_PLUSPLUS = r'\+\+'
    t_MINUSMINUS = r'--'

    # ?
    t_TERNARY = r'\?'

    # #
    t_HASH = r'\#'

    # Delimeters
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_COMMA = r','
    t_PERIOD = r'\.'
    t_SEMI = r';'
    t_COLON = r':'

    t_ignore = ' \t\f'

    def t_NAME(self, t):
        '[A-Za-z_$][A-Za-z0-9_$]*'
        if t.value in MochaLexer.keywords:
            t.type = t.value.upper()
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_newline2(self, t):
        r'(\r\n)+'
        t.lexer.lineno += len(t.value) / 2

    def t_error(self, t):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)


class ClassParser(BaseParser):

    def p_argument_list_opt_1(self, p):
        ''' argument_list_opt   : argument_list '''
        p[0] = p[1]

    def p_argument_list_opt_2(self, p):
        ''' argument_list_opt   : empty '''
        p[0] = []

    def p_argument_list(self, p):
        ''' argument_list   : expression
                            | argument_list COMMA expression
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]


class ExpressionParser(BaseParser):

    def p_expression(self, p):
        ''' expression  : assignment_expression '''
        p[0] = p[1]

    def p_expression_not_name(self, p):
        ''' expression_not_name : assignment_expression_not_name '''
        p[0] = p[1]

    def p_assignment_expression(self, p):
        ''' assignment_expression   : assignment
                                    | conditional_expression
        '''
        p[0] = p[1]

    def p_assignment_expression_not_name(self, p):
        ''' assignment_expression_not_name  : assignment
                                            | conditional_expression_not_name
        '''
        p[0] = p[1]

    def p_assignment(self, p):
        ''' assignment  : postfix_expression assignment_operator assignment_expression '''
        p[0] = Assignment(p[2], p[1], p[3])

    def p_assignment_operator(self, p):
        ''' assignment_operator : EQUALS
                                | XOREQUAL
                                | TIMESEQUAL
                                | DIVEQUAL
                                | MODEQUAL
                                | PLUSEQUAL
                                | MINUSEQUAL
                                | LSHIFTEQUAL
                                | RSHIFTEQUAL
                                | ANDEQUAL
                                | OREQUAL
        '''
        p[0] = p[1]

    def p_conditional_expression(self, p):
        ''' conditional_expression  : conditional_or_expression
                                    | conditional_or_expression TERNARY expression COLON conditional_expression
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Conditional(p[1], p[3], p[5])

    def p_conditional_expression_not_name(self, p):
        ''' conditional_expression_not_name : conditional_or_expression_not_name
                                            | conditional_or_expression_not_name TERNARY expression COLON conditional_expression
                                            | name TERNARY expression COLON conditional_expression
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Conditional(p[1], p[3], p[5])

    def binop(self, p, ctor):
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ctor(p[2], p[1], p[3])

    def p_conditional_or_expression(self, p):
        ''' conditional_or_expression   : conditional_and_expression
                                        | conditional_or_expression LOR conditional_and_expression
        '''
        self.binop(p, ConditionalOr)

    def p_conditional_or_expression_not_name(self, p):
        ''' conditional_or_expression_not_name  : conditional_and_expression_not_name
                                                | conditional_or_expression_not_name LOR conditional_and_expression
                                                | name LOR conditional_and_expression
        '''
        self.binop(p, ConditionalOr)

    def p_conditional_and_expression(self, p):
        ''' conditional_and_expression  : inclusive_or_expression
                                        | conditional_and_expression LAND inclusive_or_expression
        '''
        self.binop(p, ConditionalAnd)

    def p_conditional_and_expression_not_name(self, p):
        ''' conditional_and_expression_not_name : inclusive_or_expression_not_name
                                                | conditional_and_expression_not_name LAND inclusive_or_expression
                                                | name LAND inclusive_or_expression'''
        self.binop(p, ConditionalAnd)

    def p_inclusive_or_expression(self, p):
        '''inclusive_or_expression  : exclusive_or_expression
                                    | inclusive_or_expression OR exclusive_or_expression'''
        self.binop(p, Or)

    def p_inclusive_or_expression_not_name(self, p):
        '''inclusive_or_expression_not_name : exclusive_or_expression_not_name
                                            | inclusive_or_expression_not_name OR exclusive_or_expression
                                            | name OR exclusive_or_expression'''
        self.binop(p, Or)

    def p_exclusive_or_expression(self, p):
        '''exclusive_or_expression : and_expression
                                   | exclusive_or_expression XOR and_expression'''
        self.binop(p, Xor)

    def p_exclusive_or_expression_not_name(self, p):
        '''exclusive_or_expression_not_name : and_expression_not_name
                                            | exclusive_or_expression_not_name XOR and_expression
                                            | name XOR and_expression'''
        self.binop(p, Xor)

    def p_and_expression(self, p):
        '''and_expression : equality_expression
                          | and_expression AND equality_expression'''
        self.binop(p, And)

    def p_and_expression_not_name(self, p):
        '''and_expression_not_name : equality_expression_not_name
                                   | and_expression_not_name AND equality_expression
                                   | name AND equality_expression'''
        self.binop(p, And)

    def p_equality_expression(self, p):
        '''equality_expression : instanceof_expression
                               | equality_expression EQ instanceof_expression
                               | equality_expression NE instanceof_expression'''
        self.binop(p, Equality)

    def p_equality_expression_not_name(self, p):
        '''equality_expression_not_name : instanceof_expression_not_name
                                        | equality_expression_not_name EQ instanceof_expression
                                        | name EQ instanceof_expression
                                        | equality_expression_not_name NE instanceof_expression
                                        | name NE instanceof_expression'''
        self.binop(p, Equality)

    def p_instanceof_expression(self, p):
        '''instanceof_expression : relational_expression
                                 | instanceof_expression INSTANCEOF type'''
        self.binop(p, InstanceOf)

    def p_instanceof_expression_not_name(self, p):
        '''instanceof_expression_not_name : relational_expression_not_name
                                          | name INSTANCEOF reference_type
                                          | instanceof_expression_not_name INSTANCEOF type'''
        self.binop(p, InstanceOf)

    def p_relational_expression(self, p):
        '''relational_expression : shift_expression
                                 | relational_expression GT shift_expression
                                 | relational_expression LT shift_expression
                                 | relational_expression GE shift_expression
                                 | relational_expression LE shift_expression'''
        self.binop(p, Relational)

    def p_relational_expression_not_name(self, p):
        '''relational_expression_not_name : shift_expression_not_name
                                          | shift_expression_not_name LT shift_expression
                                          | name LT shift_expression
                                          | shift_expression_not_name GT shift_expression
                                          | name GT shift_expression
                                          | shift_expression_not_name GE shift_expression
                                          | name GE shift_expression
                                          | shift_expression_not_name LE shift_expression
                                          | name LE shift_expression'''
        self.binop(p, Relational)

    def p_shift_expression(self, p):
        '''shift_expression : additive_expression
                            | shift_expression LSHIFT additive_expression
                            | shift_expression RSHIFT additive_expression'''
        self.binop(p, Shift)

    def p_shift_expression_not_name(self, p):
        '''shift_expression_not_name : additive_expression_not_name
                                     | shift_expression_not_name LSHIFT additive_expression
                                     | name LSHIFT additive_expression
                                     | shift_expression_not_name RSHIFT additive_expression
                                     | name RSHIFT additive_expression'''
        self.binop(p, Shift)

    def p_additive_expression(self, p):
        '''additive_expression : multiplicative_expression
                               | additive_expression PLUS multiplicative_expression
                               | additive_expression MINUS multiplicative_expression'''
        self.binop(p, Additive)

    def p_additive_expression_not_name(self, p):
        '''additive_expression_not_name : multiplicative_expression_not_name
                                        | additive_expression_not_name PLUS multiplicative_expression
                                        | name PLUS multiplicative_expression
                                        | additive_expression_not_name MINUS multiplicative_expression
                                        | name MINUS multiplicative_expression'''
        self.binop(p, Additive)

    def p_multiplicative_expression(self, p):
        '''multiplicative_expression : unary_expression
                                     | multiplicative_expression TIMES unary_expression
                                     | multiplicative_expression DIVIDE unary_expression
                                     | multiplicative_expression MOD unary_expression'''
        self.binop(p, Multiplicative)

    def p_multiplicative_expression_not_name(self, p):
        '''multiplicative_expression_not_name : unary_expression_not_name
                                              | multiplicative_expression_not_name TIMES unary_expression
                                              | name TIMES unary_expression
                                              | multiplicative_expression_not_name DIVIDE unary_expression
                                              | name DIVIDE unary_expression
                                              | multiplicative_expression_not_name MOD unary_expression
                                              | name MOD unary_expression'''
        self.binop(p, Multiplicative)

    def p_unary_expression(self, p):
        '''unary_expression : pre_increment_expression
                            | pre_decrement_expression
                            | PLUS unary_expression
                            | MINUS unary_expression
                            | unary_expression_not_plus_minus'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Unary(p[1], p[2])

    def p_unary_expression_not_name(self, p):
        '''unary_expression_not_name : pre_increment_expression
                                     | pre_decrement_expression
                                     | PLUS unary_expression
                                     | MINUS unary_expression
                                     | unary_expression_not_plus_minus_not_name'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Unary(p[1], p[2])

    def p_pre_increment_expression(self, p):
        ''' pre_increment_expression : PLUSPLUS unary_expression'''
        p[0] = Unary('++x', p[2])

    def p_pre_decrement_expression(self, p):
        ''' pre_decrement_expression : MINUSMINUS unary_expression'''
        p[0] = Unary('--x', p[2])

    def p_unary_expression_not_plus_minus(self, p):
        '''unary_expression_not_plus_minus : postfix_expression
                                           | NOT unary_expression
                                           | LNOT expression
                                           | cast_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Unary(p[1], p[2])

    def p_unary_expression_not_plus_minus_not_name(self, p):
        '''unary_expression_not_plus_minus_not_name : postfix_expression_not_name
                                                    | NOT unary_expression
                                                    | LNOT expression
                                                    | cast_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Unary(p[1], p[2])

    def p_postfix_expression(self, p):
        ''' postfix_expression  : primary_expression
                                | name
                                | post_increment_expression
                                | post_decrement_expression
        '''
        p[0] = p[1]

    def p_postfix_expression_not_name(self, p):
        '''postfix_expression_not_name : primary_expression
                                       | post_increment_expression
                                       | post_decrement_expression'''
        p[0] = p[1]

    def p_post_increment_expression(self, p):
        ''' post_increment_expression   : postfix_expression PLUSPLUS '''
        p[0] = Unary('x++', p[1])

    def p_post_decrement_expression(self, p):
        ''' post_decrement_expression   : postfix_expression MINUSMINUS '''
        p[0] = Unary('x--', p[1])

    def p_primary_expression(self, p):
        ''' primary_expression  : primary_expression_no_new_array
                                | array_creation_with_array_initializer
                                | array_creation_without_array_initializer
        '''
        p[0] = p[1]

    def p_primary_expression_no_new_array_1(self, p):
        ''' primary_expression_no_new_array : literal
                                            | class_instance_creation_expression
                                            | field_access
                                            | method_invocation
                                            | array_access
                                            | crc_string
        '''
        p[0] = p[1]

    def p_primary_expression_no_new_array_2(self, p):
        ''' primary_expression_no_new_array : LPAREN name RPAREN
                                            | LPAREN expression_not_name RPAREN
        '''
        p[0] = Precidence(p[2])

    def p_dimensions_opt_1(self, p):
        ''' dimensions_opt  : dimensions '''
        p[0] = p[1]

    def p_dimensions_opt_2(self, p):
        ''' dimensions_opt  : empty '''
        p[0] = 0

    def p_dimensions(self, p):
        ''' dimensions  : dimension
                        | dimensions dimension
        '''
        if len(p) == 2:
            p[0] = 1
        else:
            p[0] = 1 + p[1]

    def p_dimension(self, p):
        ''' dimension   : LBRACKET RBRACKET '''
        pass

    def p_cast_expression_1(self, p):
        ''' cast_expression : LPAREN primitive_type dimensions_opt RPAREN unary_expression '''
        p[0] = Cast(Type(p[2], dimensions=p[3]), p[5])

    def p_cast_expression_2(self, p):
        ''' cast_expression : LPAREN modifiers primitive_type dimensions_opt RPAREN unary_expression '''
        p[0] = Cast(Type(p[3], dimensions=p[4]), p[6], p[2])

    def p_cast_expression_3(self, p):
        ''' cast_expression : LPAREN name RPAREN unary_expression_not_plus_minus '''
        p[0] = Cast(Type(p[2]), p[4])

    def p_cast_expression_4(self, p):
        ''' cast_expression : LPAREN modifiers name RPAREN unary_expression_not_plus_minus '''
        p[0] = Cast(Type(p[3]), p[5], p[2])

    def p_cast_expression_5(self, p):
        ''' cast_expression : LPAREN name dimensions RPAREN unary_expression_not_plus_minus '''
        p[0] = Cast(Type(p[2], dimensions=p[3]), p[5])

    def p_cast_expression_6(self, p):
        ''' cast_expression : LPAREN modifiers name dimensions RPAREN unary_expression_not_plus_minus '''
        p[0] = Cast(Type(p[3], dimensions=p[4]), p[6], p[2])


class FunctionParser(BaseParser):

    def p_formal_parameter_list_opt_1(self, p):
        ''' formal_parameter_list_opt   : formal_parameter_list '''
        p[0] = p[1]

    def p_formal_parameter_list_opt_2(self, p):
        ''' formal_parameter_list_opt   : formal_parameter_list COMMA '''
        p[0] = p[1]

    def p_formal_parameter_list_opt_3(self, p):
        ''' formal_parameter_list_opt   : empty '''
        p[0] = []

    def p_formal_parameter_list(self, p):
        ''' formal_parameter_list   : formal_parameter
                                    | formal_parameter_list COMMA formal_parameter
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_formal_parameter(self, p):
        ''' formal_parameter : modifiers_opt type variable_declarator_id '''
        p[0] = FormalParameter(p[3], p[2], modifiers=p[1])

    def p_function_body(self, p):
        ''' function_body   : LBRACE block_statements_opt RBRACE '''
        p[0] = p[2]

    def p_function_declaration(self, p):
        ''' function_declaration    : function_header function_body '''
        p[0] = FunctionDeclaration(
                p[1]['name'],
                modifiers=p[1]['modifiers'],
                parameters=p[1]['parameters'],
                return_type=p[1]['type'],
                body=p[2])

    def p_function_header(self, p):
        ''' function_header : function_header_name formal_parameter_list_opt RPAREN '''
        p[1]['parameters'] = p[2]
        p[0] = p[1]

    def p_function_header_name_1(self, p):
        ''' function_header_name  : type NAME LPAREN '''
        p[0] = {'modifiers': [], 'type': p[1], 'name': p[2] }

    def p_function_header_name_2(self, p):
        ''' function_header_name  : modifiers type NAME LPAREN '''
        p[0] = {'modifiers': p[1], 'type': p[2], 'name': p[3] }


class LiteralParser(BaseParser):

    def p_literal(self, p):
        ''' literal : INT_CONST
                    | INT_CONST_HEX
                    | FLOAT_CONST
                    | CHAR_LITERAL
                    | STRING_LITERAL
                    | TRUE
                    | FALSE
                    | NULL
        '''
        p[0] = Literal(p[1])

    def p_crc_string_literal(self, p):
        ''' crc_string  : HASH HASH STRING_LITERAL '''
        p[0] = CrcString(p[3])


class NameParser(BaseParser):

    def p_name(self, p):
        ''' name    : simple_name
                    | qualified_name
        '''
        p[0] = p[1]

    def p_simple_name(self, p):
        ''' simple_name : NAME '''
        p[0] = Name(p[1])

    def p_qualified_name(self, p):
        ''' qualified_name : name PERIOD simple_name '''
        p[1].append_name(p[3])
        p[0] = p[1]


class StatementParser(BaseParser):

    def p_block(self, p):
        ''' block   : LBRACE block_statements_opt RBRACE '''
        p[0] = Block(p[2])

    def p_block_statements_opt_1(self, p):
        ''' block_statements_opt    : block_statements '''
        p[0] = p[1]

    def p_block_statements_opt_2(self, p):
        ''' block_statements_opt    : empty '''
        p[0] = []

    def p_block_statements(self, p):
        ''' block_statements    : block_statement
                                | block_statements block_statement
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_block_statement_1(self, p):
        ''' block_statement : statement
                            | pp_define
                            | pp_ifdef
        '''
        p[0] = BlockStatement(p[1])

    def p_block_statement_2(self, p):
        ''' block_statement : function_declaration '''
        p[0] = p[1]

    def p_pp_define(self, p):
        ''' pp_define   : HASH DEFINE NAME INT_CONST '''
        self.defines[p[3]] = p[4]
        p[0] = Empty()

    def p_pp_ifdef_1(self, p):
        ''' pp_ifdef    : HASH IFDEF NAME block_statements HASH ENDIF '''
        if self.defines.get(p[3], False):
            p[0] = Block(p[4], False)
        else:
            p[0] = Empty()

    def p_local_variable_declaration_statement(self, p):
        ''' local_variable_declaration_statement    : local_variable_declaration SEMI '''
        p[0] = VariableDeclarationStatement(p[1])

    def p_local_variable_declaration_1(self, p):
        ''' local_variable_declaration  : type variable_declarators '''
        p[0] = VariableDeclaration(p[1], p[2])

    def p_local_variable_declaration_2(self, p):
        ''' local_variable_declaration  : modifiers type variable_declarators '''
        p[0] = VariableDeclaration(p[2], p[3], modifiers=p[1])

    def p_variable_declarators(self, p):
        '''variable_declarators : variable_declarator
                                | variable_declarators COMMA variable_declarator'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_variable_declarator(self, p):
        ''' variable_declarator : variable_declarator_id
                                | variable_declarator_id EQUALS variable_initializer
        '''
        if len(p) == 2:
            p[0] = VariableDeclarator(p[1])
        else:
            p[0] = VariableDeclarator(p[1], initializer=p[3])

    def p_variable_declarator_id(self, p):
        ''' variable_declarator_id  : NAME dimensions_opt '''
        p[0] = Variable(p[1], dimensions=p[2])

    def p_variable_initializer(self, p):
        ''' variable_initializer    : expression
                                    | array_initializer
        '''
        p[0] = p[1]

    def p_statement(self, p):
        ''' statement   : local_variable_declaration_statement
                        | statement_without_trailing_substatement
                        | if_then_statement
                        | if_then_else_statement
                        | while_statement
                        | for_statement
        '''
        p[0] = p[1]

    def p_statement_without_trailing_substatement(self, p):
        ''' statement_without_trailing_substatement : block
                                                    | expression_statement
                                                    | empty_statement
                                                    | switch_statement
                                                    | do_statement
                                                    | break_statement
                                                    | continue_statement
                                                    | return_statement
                                                    | throw_statement
                                                    | try_statement
        '''
        p[0] = p[1]

    def p_expression_statement(self, p):
        ''' expression_statement    : statement_expression SEMI
        '''
        p[0] = StatementExpression(p[1])

    def p_statement_expression(self, p):
        ''' statement_expression    : assignment
                                    | pre_increment_expression
                                    | pre_decrement_expression
                                    | post_increment_expression
                                    | post_decrement_expression
                                    | method_invocation
                                    | class_instance_creation_expression
        '''
        p[0] = p[1]

    def p_comma_opt(self, p):
        ''' comma_opt   : COMMA
                        | empty
        '''
        pass

    def p_array_initializer_1(self, p):
        ''' array_initializer : LBRACE comma_opt RBRACE '''
        p[0] = ArrayInitializer()

    def p_array_initializer_2(self, p):
        ''' array_initializer   : LBRACE variable_initializers RBRACE
                                | LBRACE variable_initializers COMMA RBRACE
        '''
        p[0] = ArrayInitializer(p[2])

    def p_variable_initializers(self, p):
        ''' variable_initializers   : variable_initializer
                                    | variable_initializers COMMA variable_initializer
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_method_invocation_1(self, p):
        ''' method_invocation   : NAME LPAREN argument_list_opt RPAREN '''
        p[0] = MethodInvocation(p[1], arguments=p[3])

    def p_method_invocation_2(self, p):
        ''' method_invocation   : name PERIOD NAME LPAREN argument_list_opt RPAREN
                                | primary_expression PERIOD NAME LPAREN argument_list_opt RPAREN
        '''
        p[0] = MethodInvocation(p[3], target=p[1], arguments=p[5])

    def p_if_then_statement(self, p):
        ''' if_then_statement   : IF LPAREN expression RPAREN statement %prec then'''
        p[0] = IfThenElse(p[3], p[5])

    def p_if_then_else_statement_1(self, p):
        ''' if_then_else_statement  : IF LPAREN expression RPAREN statement ELSE statement '''
        p[0] = IfThenElse(p[3], p[5], p[7])

    def p_while_statement_1(self, p):
        ''' while_statement : WHILE LPAREN expression RPAREN statement '''
        p[0] = While(p[3], p[5])

    def p_while_statement_2(self, p):
        ''' while_statement : WHILE LPAREN expression RPAREN SEMI '''
        p[0] = While(p[3])

    def p_for_statement(self, p):
        ''' for_statement : FOR LPAREN for_init_opt SEMI expression_opt SEMI for_update_opt RPAREN statement '''
        p[0] = For(p[3], p[5], p[7], p[9])

    def p_for_init_opt(self, p):
        ''' for_init_opt    : for_init
                            | empty
        '''
        p[0] = p[1]

    def p_for_init(self, p):
        ''' for_init    : statement_expression_list
                        | local_variable_declaration
        '''
        p[0] = p[1]

    def p_statement_expression_list(self, p):
        ''' statement_expression_list   : statement_expression
                                        | statement_expression_list COMMA statement_expression
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_expression_opt(self, p):
        ''' expression_opt  : expression
                            | empty
        '''
        p[0] = p[1]

    def p_for_update_opt(self, p):
        ''' for_update_opt  : for_update
                            | empty
        '''
        p[0] = p[1]

    def p_for_update(self, p):
        ''' for_update  : statement_expression_list '''
        p[0] = p[1]

    def p_empty_statement(self, p):
        '''empty_statement : SEMI '''
        p[0] = Empty()

    def p_switch_statement(self, p):
        ''' switch_statement    : SWITCH LPAREN expression RPAREN switch_block '''
        p[0] = Switch(p[3], p[5])

    def p_switch_block_1(self, p):
        ''' switch_block    : LBRACE RBRACE '''
        p[0] = []

    def p_switch_block_2(self, p):
        ''' switch_block    : LBRACE switch_block_statements RBRACE '''
        p[0] = p[2]

    def p_switch_block_3(self, p):
        ''' switch_block    : LBRACE switch_labels RBRACE '''
        p[0] = [SwitchCase(p[2])]

    def p_switch_block_4(self, p):
        ''' switch_block    : LBRACE switch_block_statements switch_labels RBRACE '''
        p[0] = p[2] + [SwitchCase(p[3])]

    def p_switch_block_statements(self, p):
        ''' switch_block_statements : switch_block_statement
                                    | switch_block_statements switch_block_statement
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_switch_block_statement(self, p):
        ''' switch_block_statement  : switch_labels block_statements '''
        p[0] = SwitchCase(p[1], body=p[2])

    def p_switch_labels(self, p):
        ''' switch_labels   : switch_label
                            | switch_labels switch_label
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_switch_label(self, p):
        ''' switch_label    : CASE constant_expression COLON
                            | DEFAULT COLON
        '''
        if len(p) == 3:
            p[0] = 'default'
        else:
            p[0] = p[2]

    def p_constant_expression(self, p):
        ''' constant_expression : expression '''
        p[0] = p[1]

    def p_do_statement(self, p):
        ''' do_statement    : DO statement WHILE LPAREN expression RPAREN SEMI '''
        p[0] = DoWhile(p[5], body=p[2])

    def p_break_statement(self, p):
        ''' break_statement : BREAK SEMI
                            | BREAK NAME SEMI
        '''
        if len(p) == 3:
            p[0] = Break()
        else:
            p[0] = Break(p[2])

    def p_continue_statement(self, p):
        ''' continue_statement  : CONTINUE SEMI
                                | CONTINUE NAME SEMI
        '''
        if len(p) == 3:
            p[0] = Continue()
        else:
            p[0] = Continue(p[2])

    def p_return_statement(self, p):
        ''' return_statement    : RETURN expression_opt SEMI '''
        p[0] = Return(p[2])

    def p_throw_statement(self, p):
        ''' throw_statement : THROW expression SEMI '''
        p[0] = Throw(p[2])

    def p_try_statement(self, p):
        ''' try_statement   : TRY try_block catches
                            | TRY try_block catches_opt finally
        '''
        if len(p) == 4:
            p[0] = Try(p[2], catches=p[3])
        else:
            p[0] = Try(p[2], catches=p[3], _finally=p[4])

    def p_try_block(self, p):
        ''' try_block   : block '''
        p[0] = p[1]

    def p_catches(self, p):
        ''' catches : catch_clause
                    | catches catch_clause
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_catches_opt_1(self, p):
        ''' catches_opt : catches '''
        p[0] = p[1]

    def p_catches_opt_2(self, p):
        ''' catches_opt : empty '''
        p[0] = []

    def p_catch_clause(self, p):
        ''' catch_clause    : CATCH LPAREN catch_formal_parameter RPAREN block '''
        p[0] = Catch(p[3]['variable'], _type=p[3]['type'], modifiers=p[3]['modifiers'], block=p[5])

    def p_catch_formal_parameter(self, p):
        ''' catch_formal_parameter  : modifiers_opt type variable_declarator_id '''
        p[0] = {'modifiers': p[1], 'type': p[2], 'variable': p[3]}

    def p_finally(self, p):
        ''' finally : FINALLY block '''
        p[0] = p[2]

    def p_class_instance_creation_expression_1(self, p):
        ''' class_instance_creation_expression : NEW class_type LPAREN argument_list_opt RPAREN '''
        p[0] = InstanceCreation(p[2], p[4])

    def p_field_access(self, p):
        ''' field_access    : primary_expression PERIOD NAME '''
        p[0] = FieldAccess(p[3], p[1])

    def p_array_access(self, p):
        ''' array_access    : name LBRACKET expression RBRACKET
                            | primary_expression_no_new_array LBRACKET expression RBRACKET
                            | array_creation_with_array_initializer LBRACKET expression RBRACKET
        '''
        p[0] = ArrayAccess(p[3], p[1])

    def p_array_creation_with_array_initializer_1(self, p):
        ''' array_creation_with_array_initializer   : NEW primitive_type dim_with_or_without_exprs array_initializer '''
        p[0] = ArrayCreation(Type(p[2]), dimensions=p[3], initializer=p[4])

    def p_array_creation_with_array_initializer_2(self, p):
        ''' array_creation_with_array_initializer   : NEW class_type dim_with_or_without_exprs array_initializer '''
        p[0] = ArrayCreation(p[2], dimensions=p[3], initializer=p[4])

    def p_dim_with_or_without_exprs(self, p):
        '''dim_with_or_without_exprs : dim_with_or_without_expr
                                     | dim_with_or_without_exprs dim_with_or_without_expr'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_dim_with_or_without_expr(self, p):
        '''dim_with_or_without_expr : LBRACKET expression RBRACKET
                                    | LBRACKET RBRACKET
        '''
        if len(p) == 3:
            p[0] = None
        else:
            p[0] = p[2]

    def p_array_creation_without_array_initializer_1(self, p):
        ''' array_creation_without_array_initializer    : NEW primitive_type dim_with_or_without_exprs '''
        p[0] = ArrayCreation(Type(p[2]), dimensions=p[3])

    def p_array_creation_without_array_initializer_2(self, p):
        ''' array_creation_without_array_initializer    : NEW class_type dim_with_or_without_exprs '''
        p[0] = ArrayCreation(p[2], dimensions=p[3])

class TypeParser(BaseParser):

    def p_modifiers_opt_1(self, p):
        ''' modifiers_opt   : modifiers '''
        p[0] = p[1]

    def p_modifiers_opt_2(self, p):
        ''' modifiers_opt   : empty '''
        p[0] = []

    def p_modifiers(self, p):
        ''' modifiers   : modifier
                        | modifiers modifier
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_modifier(self, p):
        ''' modifier    : CONST
                        | RESIZEABLE
        '''
        p[0] = p[1]

    def p_type_1(self, p):
        ''' type    :  reference_type '''
        p[0] = p[1]

    def p_type_2(self, p):
        ''' type    : primitive_type '''
        p[0] = Type(p[1])

    def p_primitive_type(self, p):
        ''' primitive_type  : BOOLEAN
                            | VOID
                            | BYTE
                            | SHORT
                            | INT
                            | LONG
                            | CHAR
                            | FLOAT
                            | DOUBLE
        '''
        p[0] = Name(p[1])

    def p_reference_type(self, p):
        ''' reference_type  : class_type
                            | array_type
        '''
        p[0] = p[1]

    def p_class_type(self, p):
        ''' class_type  : name '''
        p[0] = Type(p[1])

    def p_array_type(self, p):
        ''' array_type  : primitive_type dimensions
                        | name dimensions
        '''
        p[0] = Type(p[1], dimensions=p[2])


class CompilationParser(BaseParser):

    def p_pp_ifdef_compilation_unit_2(self, p):
        ''' pp_ifdef_compilation_unit   : HASH IFDEF NAME include_declarations block_statements HASH ENDIF '''
        if self.defines.get(p[3], False):
            p[0] = CompilationUnit(includes=p[4], statements=p[5])

    def p_compilation_unit_0(self, p):
        ''' compilation_unit    : pp_ifdef_compilation_unit '''
        p[0] = p[1]

    def p_compilation_unit_1(self, p):
        ''' compilation_unit    : include_declarations '''
        p[0] = CompilationUnit(includes=p[1])

    def p_compilation_unit_2(self, p):
        ''' compilation_unit    : inherits_declaration '''
        p[0] = CompilationUnit(inherits=p[1])

    def p_compilation_unit_3(self, p):
        ''' compilation_unit    : block_statements '''
        p[0] = CompilationUnit(statements=p[1])

    def p_compilation_unit_4(self, p):
        ''' compilation_unit    : include_declarations inherits_declaration '''
        p[0] = CompilationUnit(includes=p[1], inherits=p[2])

    def p_compilation_unit_5(self, p):
        ''' compilation_unit    : include_declarations block_statements '''
        p[0] = CompilationUnit(includes=p[1], statements=p[2])

    def p_compilation_unit_6(self, p):
        ''' compilation_unit    : inherits_declaration block_statements '''
        p[0] = CompilationUnit(inherits=p[1], statements=p[2])

    def p_compilation_unit_7(self, p):
        ''' compilation_unit    : include_declarations inherits_declaration block_statements '''
        p[0] = CompilationUnit(includes=p[1], inherits=p[2], statements=p[3])

    def p_compilation_unit_8(self, p):
        ''' compilation_unit    : inherits_declaration include_declarations block_statements '''
        p[0] = CompilationUnit(inherits=p[1], includes=p[2], statements=p[3])

    def p_compilation_unit_9(self, p):
        ''' compilation_unit    : empty '''
        p[0] = CompilationUnit()

    def p_inherits_declaration(self, p):
        ''' inherits_declaration    : INHERITS name semi_opt '''
        p[0] = InheritsDeclaration(p[2])

    def p_include_declarations(self, p):
        ''' include_declarations    : include_declaration
                                    | include_declarations include_declaration
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_include_declaration(self, p):
        ''' include_declaration : single_type_include_declaration
                                | type_include_on_demand_declaration
        '''
        p[0] = p[1]

    def p_single_type_include_declaration(self, p):
        ''' single_type_include_declaration : INCLUDE name semi_opt '''
        p[0] = IncludeDeclaration(p[2])

    def p_type_include_on_demand_declaration(self, p):
        ''' type_include_on_demand_declaration  : INCLUDE name PERIOD TIMES semi_opt '''
        p[0] = IncludeDeclaration(p[2], on_demand=True)

    def p_semi_opt(self, p):
        ''' semi_opt    : SEMI
                        | empty
        '''
        p[0] = p[1]


class MochaParser(ClassParser, CompilationParser, ExpressionParser, FunctionParser, LiteralParser, NameParser, StatementParser, TypeParser):

    tokens = MochaLexer.tokens

    precedence = (
        ('nonassoc', 'then'),
        ('nonassoc', 'ELSE'),
        ('left', 'LOR'),
        ('left', 'LAND'),
        ('left', 'OR'),
        ('left', 'XOR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NE'),
        ('left', 'GT', 'GE', 'LT', 'LE'),
        ('left', 'RSHIFT', 'LSHIFT'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MOD')
    )

    def __init__(self,
            optimize_lex=True,
            lextab='mocha.lextab',
            optimize_yacc=True,
            yacctab='mocha.yacctab',
            debug=False):
        super(MochaParser, self).__init__()
        self.lexer = MochaLexer(self._lex_error_func)
        self.lexer.build(optimize=optimize_lex, lextab=lextab, debug=debug)
        self.parser = yacc.yacc(module=self,
                    start='root',
                    debug=debug,
                    optimize=optimize_yacc,
                    tabmodule=yacctab)
        self.defines = { "DEBUG": True }

    def _lex_error_func(self, msg, line, column):
        self._parse_error(msg, self._coord(line, column))

    def tokenize_string(self, code):
        self.lexer.input(code)
        for token in self.lexer:
            print(token)

    def tokenize_file(self, _file):
        if type(_file) == str:
            _file = file(_file)
        content = ''
        for line in _file:
            content += line
        return self.tokenize_string(content)

    def parse_expression(self, code, debug=0, lineno=1):
        return self.parse_string(code, debug, lineno, prefix='--')

    def parse_statement(self, code, debug=0, lineno=1):
        return self.parse_string(code, debug, lineno, prefix='* ')

    def parse_string(self, code, debug=0, lineno=1, prefix='++'):
        self.lexer.lineno = lineno
        return self.parser.parse(prefix + code, lexer=self.lexer, debug=debug)

    def parse_file(self, _file, debug=0):
        if type(_file) == str:
            _file = file(_file)
        content = ''
        for line in _file:
            content += line
        self.lexer.filename = _file.name

        res = ()

        try:
            res = self.parse_string(content, debug=debug)
        except ParseError, e:
            if debug:
                raise
            else:
                print e

        return res

    def p_root_compilation_unit(self, p):
        ''' root    : PLUSPLUS compilation_unit '''
        p[0] = p[2]

    def p_root_expression(self, p):
        """ root    : MINUSMINUS expression
        """
        p[0] = p[2]

    def p_root_statement(self, p):
        """ root    : TIMES block_statement
        """
        p[0] = p[2]

    def p_empty(self, p):
        ''' empty : '''

    def p_error(self, p):
        # If error recovery is added here in the future, make sure
        # _get_yacc_lookahead_token still works!
        #
        if p:
            self._parse_error(
                'before: %s' % p.value,
                self._coord(lineno=p.lineno,
                            column=self.lexer.find_tok_column(p)))
        else:
            self._parse_error('At end of input', '')

