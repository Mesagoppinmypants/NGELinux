
class SourceElement(object):

    def __init__(self):
        super(SourceElement, self).__init__()
        self._fields = []

    def __repr__(self):
        equals = ("{0}={1!r}".format(k, getattr(self, k))
                for k in self._fields)
        args = ", ".join(equals)
        return "{0}({1})".format(self.__class__.__name__, args)

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self == other

    def accept(self, visitor):
        s = visitor.visit(self)
        return s


class ArrayAccess(SourceElement):
    def __init__(self, index, target):
        super(ArrayAccess, self).__init__()
        self._fields = ['index', 'target']
        self.index = index
        self.target = target


class ArrayInitializer(SourceElement):

    def __init__(self, elements=None):
        super(ArrayInitializer, self).__init__()
        self._fields = ['elements']
        if elements is None:
            elements = []
        self.elements = elements


class Catch(SourceElement):

    def __init__(self, variable, modifiers=None, _type=None, block=None):
        super(Catch, self).__init__()
        self._fields = ['variable', 'modifiers', 'type', 'block']
        if modifiers is None:
            modifiers = []
        self.variable = variable
        self.modifiers = modifiers
        self.type = _type
        self.block = block


class CompilationUnit(SourceElement):

    def __init__(self, includes=None, inherits=None, statements=None):
        super(CompilationUnit, self).__init__()
        self._fields = ['includes', 'statements']
        if includes is None:
            includes = []
        if statements is None:
            statements = []
        self.includes = includes
        self.inherits = inherits
        self.statements = statements


class CrcString(SourceElement):

    def __init__(self, string):
        super(CrcString, self).__init__()
        self._fields = ['string']
        self.string = string


class Expression(SourceElement):

    def __init__(self):
        super(Expression, self).__init__()
        self._fields = []


class FieldDeclaration(SourceElement):

    def __init__(self, type, variable_declarators, modifiers=None):
        super(FieldDeclaration, self).__init__()
        self._fields = ['type', 'variable_declarators', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.type = type
        self.variable_declarators = variable_declarators
        self.modifiers = modifiers


class FormalParameter(SourceElement):

    def __init__(self, variable, type, modifiers=None):
        super(FormalParameter, self).__init__()
        self._fields = ['variable', 'type', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.variable = variable
        self.type = type
        self.modifiers = modifiers


class FunctionDeclaration(SourceElement):

    def __init__(self, name, modifiers=None, parameters=None, return_type='void', body=None):
        super(FunctionDeclaration, self).__init__()
        self._fields = ['name', 'modifiers', 'parameters', 'return_type', 'body']
        if modifiers is None:
            modifiers = []
        if parameters is None:
            parameters = []
        self.name = name
        self.modifiers = modifiers
        self.parameters = parameters
        self.return_type = return_type
        self.body = body


class IncludeDeclaration(SourceElement):

    def __init__(self, name, on_demand=False):
        super(IncludeDeclaration, self).__init__()
        self._fields = ['name', 'on_demand']
        self.name = name
        self.on_demand = on_demand


class InheritsDeclaration(SourceElement):

    def __init__(self, name):
        super(InheritsDeclaration, self).__init__()
        self._fields = ['name']
        self.name = name


class Literal(SourceElement):

    def __init__(self, literal):
        super(Literal, self).__init__()
        self._fields = ['literal']
        self.literal = literal


class Name(SourceElement):

    def __init__(self, value):
        super(Name, self).__init__()
        self._fields = ['value']
        self.value = value

    def append_name(self, name):
        try:
            self.value = self.value + '.' + name.value
        except:
            self.value = self.value + '.' + name


class Precidence(SourceElement):

    def __init__(self, expression):
        super(Precidence, self).__init__()
        self._field = ['expression']
        self.expression = expression


class Statement(SourceElement):
    pass


class SwitchCase(SourceElement):

    def __init__(self, cases, body=None):
        super(SwitchCase, self).__init__()
        self._fields = ['cases', 'body']
        if body is None:
            body = []
        self.cases = cases
        self.body = body


class Type(SourceElement):

    def __init__(self, name, enclosed_in=None, dimensions=0):
        super(Type, self).__init__()
        self._fields = ['name', 'enclosed_in', 'dimensions']

        self.name = name
        self.enclosed_in = enclosed_in
        self.dimensions = dimensions


class Variable(SourceElement):

    def __init__(self, name, dimensions=0):
        super(Variable, self).__init__()
        self._fields = ['name', 'dimensions']
        self.name = name
        self.dimensions = dimensions


class VariableDeclarator(SourceElement):

    def __init__(self, variable, initializer=None):
        super(VariableDeclarator, self).__init__()
        self._fields = ['variable', 'initializer']
        self.variable = variable
        self.initializer = initializer


class VariableDeclaration(Statement, FieldDeclaration):
    pass


class ArrayCreation(Expression):

    def __init__(self, type, dimensions=None, initializer=None):
        super(ArrayCreation, self).__init__()
        self._fields = ['type', 'dimensions', 'initializer']
        if dimensions is None:
            dimensions = []
        self.type = type
        self.dimensions = dimensions
        self.initializer = initializer


class BinaryExpression(Expression):

    def __init__(self, operator, lhs, rhs):
        super(BinaryExpression, self).__init__()
        self._fields = ['operator', 'lhs', 'rhs']
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs


class Cast(Expression):

    def __init__(self, target, expression, modifiers=None):
        super(Cast, self).__init__()
        self._fields = ['target', 'expression', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.target = target
        self.expression = expression
        self.modifiers = modifiers


class Conditional(Expression):

    def __init__(self, predicate, if_true, if_false):
        super(self.__class__, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false']
        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false


class FieldAccess(Expression):

    def __init__(self, name, target):
        super(FieldAccess, self).__init__()
        self._fields = ['name', 'target']
        self.name = name
        self.target = target


class InstanceCreation(Expression):

    def __init__(self, type, arguments=None):
        super(InstanceCreation, self).__init__()
        self._fields = ['type', 'arguments']
        if arguments is None:
            arguments = []
        self.type = type
        self.arguments = arguments


class MethodInvocation(Expression):

    def __init__(self, name, arguments=None, target=None):
        super(MethodInvocation, self).__init__()
        self._fields = ['name', 'arguments', 'target']
        if arguments is None:
            arguments = []
        self.name = name
        self.arguments = arguments
        self.target = target


class Unary(Expression):

    def __init__(self, sign, expression):
        super(Unary, self).__init__()
        self._fields = ['sign', 'expression']
        self.sign = sign
        self.expression = expression


class Assignment(BinaryExpression):
    pass


class ConditionalOr(BinaryExpression):
    pass


class ConditionalAnd(BinaryExpression):
    pass


class Or(BinaryExpression):
    pass


class Xor(BinaryExpression):
    pass


class And(BinaryExpression):
    pass


class Equality(BinaryExpression):
    pass


class InstanceOf(BinaryExpression):
    pass


class Relational(BinaryExpression):
    pass


class Shift(BinaryExpression):
    pass


class Additive(BinaryExpression):
    pass


class Multiplicative(BinaryExpression):
    pass


class Block(Statement):

    def __init__(self, statements=None, wrap=True):
        super(Block, self).__init__()
        self._fields = ['statements', 'wrap']
        if statements is None:
            statements = []
        self.statements = statements
        self.wrap = wrap

    def __iter__(self):
        for s in self.statements:
            yield s


class BlockStatement(Statement):

    def __init__(self, statement):
        super(BlockStatement, self).__init__()
        self._fields = ['statement']
        self.statement = statement


class Break(Statement):

    def __init__(self, label=None):
        super(Break, self).__init__()
        self._fields = ['label']
        self.label = label


class Continue(Statement):

    def __init__(self, label=None):
        super(Continue, self).__init__()
        self._fields = ['label']
        self.label = label


class DoWhile(Statement):

    def __init__(self, predicate, body=None):
        super(DoWhile, self).__init__()
        self._fields = ['predicate', 'body']
        self.predicate = predicate
        self.body = body


class Empty(Statement):
    pass


class For(Statement):

    def __init__(self, init, predicate, update, body):
        super(For, self).__init__()
        self._fields = ['init', 'predicate', 'update', 'body']
        self.init = init
        self.predicate = predicate
        self.update = update
        self.body = body


class IfThenElse(Statement):

    def __init__(self, predicate, if_true=None, if_false=None):
        super(IfThenElse, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false']
        self.predicate = predicate

        if if_true is not None and type(if_true) is not Block:
            if_true = Block([BlockStatement(if_true)])

        self.if_true = if_true
        self.if_false = if_false


class Return(Statement):

    def __init__(self, result=None):
        super(Return, self).__init__()
        self._fields = ['result']
        self.result = result


class StatementExpression(Statement):

    def __init__(self, expression):
        super(StatementExpression, self).__init__()
        self._fields = ['expression']
        self.expression = expression


class Switch(Statement):

    def __init__(self, expression, switch_cases):
        super(Switch, self).__init__()
        self._fields = ['expression', 'switch_cases']
        self.expression = expression
        self.switch_cases = switch_cases


class Throw(Statement):

    def __init__(self, expression):
        super(Throw, self).__init__()
        self._fields = ['expression']
        self.expression = expression


class Try(Statement):

    def __init__(self, block, catches=None, _finally=None):
        super(Try, self).__init__()
        self._fields = ['block', 'catches', '_finally']
        if catches is None:
            catches = []
        self.block = block
        self.catches = catches
        self._finally = _finally


class VariableDeclarationStatement(Statement):

    def __init__(self, statement):
        super(VariableDeclarationStatement, self).__init__()
        self._fields = ['statement']
        self.statement = statement


class While(Statement):

    def __init__(self, predicate, body=None):
        super(While, self).__init__()
        self._fields = ['predicate', 'body']
        self.predicate = predicate
        self.body = body

