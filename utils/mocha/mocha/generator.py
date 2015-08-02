
import sys

from .model import *

import crc
import visit as v


class ScopeStack(object):
	def __init__(self):
		self._stack = [{"functions": dict(), "variables": dict()}]
		self._last_function = dict()

	def push_scope(self):
		self._stack.append({"functions": dict(), "variables": dict()})

	def pop_scope(self):
		assert len(self._stack) >= 1
		self._stack.pop()

	def depth(self):
		return len(self._stack) - 1

	def add_function(self, name, return_type, resizeable=False):
		self._stack[-1]["functions"][name] = {"return_type": return_type, "resizeable": resizeable}

	def add_variable(self, name, _type, resizeable=False):
		self._stack[-1]["variables"][name] = {"type": _type, "resizeable": resizeable}

	def get_function_data(self, func_name):
		for s in reversed(self._stack):
			if func_name in s["functions"].keys():
				return s["functions"][func_name]

		return None

	def get_enclosing_function(self):
		return self._last_function

	def get_variable_data(self, var_name):
		for s in reversed(self._stack):
			if var_name in s["variables"].keys():
				return s["variables"][var_name]

		return None


class JavaClassGenerator(object):
	def __init__(self):
		self._scope_stack = ScopeStack()

	def generate(self, package_name, class_name, ast, functions):
		if type(ast) is not CompilationUnit:
			return ""

		self._scope_stack._stack[-1]["functions"] = functions
		self.package_name = package_name
		self.class_name = class_name

		if class_name == "base_script":
			self.inherits = "script.base_class"
		else:
			self.inherits = "script.base_script"

		self.indention = 4

		self._add_global_scope_functions(ast)

		s = ast.accept(self)

		self._scope_stack.pop_scope()

		s += self._generate_class_footer()

		return s

	@v.on('model')
	def visit(self, model):
		return "%s" % model

	@v.when(Additive)
	def visit(self, model):
		return "%s %s %s" % (self.visit(model.lhs), model.operator, self.visit(model.rhs))

	@v.when(ArrayAccess)
	def visit(self, model):
		varname = self.visit(model.target)
		vspec = self._scope_stack.get_variable_data(varname)

		if vspec is not None and vspec["resizeable"]:
			_type = self.visit(vspec["type"].name)

			if _type == "int":
				return "((Integer)%s.get(%s)).intValue()" % (varname, self.visit(model.index))
			elif _type == "float":
				return "((Float)%s.get(%s)).floatValue()" % (varname, self.visit(model.index))
			elif _type == "boolean":
				return "((Boolean)%s.get(%s)).booleanValue()" % (varname, self.visit(model.index))
			else:
				return "((%s)%s.get(%s))" % (_type, varname, self.visit(model.index))
		else:
			return "%s[%s]" % (self.visit(model.target), self.visit(model.index))

	@v.when(ArrayCreation)
	def visit(self, model):
		if type(model.type) is str:
			s = "new %s" % model.type
		else:
			s = "new %s" % self.visit(model.type.name)

		for d in model.dimensions:
			if d is None:
				s += "[]"
			else:
				s += "[%s]" % self.visit(d)

		if model.initializer is not None:
			s += "%s" % self.visit(model.initializer)

		return s

	@v.when(ArrayInitializer)
	def visit(self, model):
		s = "\n"
		s += self._indent() + "{\n"

		self._scope_stack.push_scope()

		for i, e in enumerate(model.elements):
			s += self._indent() + self.visit(e)

			if i + 1 < len(model.elements):
				s += ","

			s += "\n"

		self._scope_stack.pop_scope()

		s += self._indent() + "}"

		return "%s" % s

	@v.when(Assignment)
	def visit(self, model):
		s = ""

		if type(model.lhs) is Name and type(model.rhs) is Name:
			if self._is_resizeable(model.rhs.value) and not self._is_resizeable(model.lhs.value):
				to_spec = self._scope_stack.get_variable_data(model.lhs.value)
				to_type = self.visit(to_spec["type"].name)

				s = "if (%s != null)\n" % model.rhs.value
				s += self._indent() + "{\n"

				self._scope_stack.push_scope()

				s += self._indent() + "%s = new %s[%s.size()];\n" % (model.lhs.value, to_type, model.rhs.value)

				if to_type == "int":
					s += self._indent() + "for (int _i = 0; _i < %s.size(); ++_i)\n" % model.rhs.value
					s += self._indent() + "{\n"

					self._scope_stack.push_scope()

					s += self._indent() + "%s[_i] = ((Integer)%s.get(_i)).intValue();\n" % (model.lhs.value, model.rhs.value)

					self._scope_stack.pop_scope()

					s += self._indent() + "}\n"

				else:
					s += self._indent() + "%s.toArray(%s);\n" % (model.rhs.value, model.lhs.value)

				self._scope_stack.pop_scope()

				s += "\n"
				s += self._indent() + "}"

			if self._is_resizeable(model.lhs.value) and not self._is_resizeable(model.rhs.value):
				s = "%s = new Vector(Arrays.asList(%s))" % (model.lhs.value, model.rhs.value)

		if type(model.lhs) is ArrayAccess and self._is_resizeable(self.visit(model.lhs.target)):
			#print "%s" % model.lhs.target
			to_spec = self._scope_stack.get_variable_data(self.visit(model.lhs.target))
			to_type = self.visit(to_spec["type"].name)

			if to_type == "int":
				s = "%s.set(%s, new Integer(%s))" % (self.visit(model.lhs.target), self.visit(model.lhs.index), self.visit(model.rhs))
			elif to_type == "float":
				s = "%s.set(%s, new Float(%s))" % (self.visit(model.lhs.target), self.visit(model.lhs.index), self.visit(model.rhs))
			else:
				s = "%s.set(%s, %s)" % (self.visit(model.lhs.target), self.visit(model.lhs.index), self.visit(model.rhs))

		if s == "":
			s = "%s %s %s" % (self.visit(model.lhs), model.operator, self.visit(model.rhs))

		return s

	@v.when(BinaryExpression)
	def visit(self, model):
		return "%s %s %s" % (self.visit(model.lhs), model.operator, self.visit(model.rhs))

	@v.when(Block)
	def visit(self, model):
		s = "\n"

		if model.wrap:
			s += self._indent() + "{\n"

			self._scope_stack.push_scope()

		for stmt in model.statements:
			s += "%s" % self.visit(stmt)

		if model.wrap:
			self._scope_stack.pop_scope()

			s += self._indent() + "}"

		return s

	@v.when(BlockStatement)
	def visit(self, model):
		return self._indent() + "%s\n" % self.visit(model.statement)

	@v.when(Break)
	def visit(self, model):
		return "break;"

	@v.when(Cast)
	def visit(self, model):
		if "resizeable" in model.modifiers:
			return "(Vector)%s" % self.visit(model.expression)
		else:
			return "(%s)%s" % (self.visit(model.target), self.visit(model.expression))

	@v.when(Catch)
	def visit(self, model):
		s = "\n%scatch(" % self._indent()

		for m in model.modifiers:
			s += self._build_modifier(m)

		s += "%s " % self.visit(model.type)

		s += model.variable.name

		s += ")"
		s += "%s" % self.visit(model.block)

		return s

	@v.when(CompilationUnit)
	def visit(self, model):
		s  = "package %s;\n\n" % self.package_name
		s += "import script.*;\n"
		s += "import script.base_class.*;\n"
		s += "import script.combat_engine.*;\n"
		s += "import java.util.Arrays;\n"
		s += "import java.util.Hashtable;\n"
		s += "import java.util.Vector;\n"
		s += "import script.base_script;\n\n"

		self.include_count = len(model.includes)

		if model.inherits is not None:
			self.inherits = "script." + model.inherits.name.value

		if self.include_count is 0:
			s += self._generate_class_header()

		for include in model.includes:
			s += self.visit(include)

		for statement in model.statements:
			s += self.visit(statement)

		return s

	@v.when(Conditional)
	def visit(self, model):
		return "%s ? %s : %s" % (self.visit(model.predicate), self.visit(model.if_true), self.visit(model.if_false))

	@v.when(Continue)
	def visit(self, model):
		return "continue;"

	@v.when(CrcString)
	def visit(self, model):
		return "(%s)" % crc.calculate(model.string.lower().replace('"', ''))

	@v.when(DoWhile)
	def visit(self, model):
		s = "do"

		s += self.visit(model.body)
		s += " while (%s);" % self.visit(model.predicate)

		return s

	@v.when(Empty)
	def visit(self, model):
		return ""

	@v.when(Equality)
	def visit(self, model):
		s = ""
		if type(model.lhs) is Name:
			vspec = self._scope_stack.get_variable_data(model.lhs.value)
			if vspec is not None:
				_type = self.visit(vspec["type"].name)
				rhs = self.visit(model.rhs)

				if (_type == "String" or _type == "dictionary" or _type == "string_id" or _type == "location") and rhs != "null":
					s = ""
					if model.operator == "!=":
						s += "!"

					s += "%s.equals(%s)" % (self.visit(model.lhs), self.visit(model.rhs))

		if type(model.lhs) is ArrayAccess:
			vspec = self._scope_stack.get_variable_data(self.visit(model.lhs.target))
			if vspec is not None:
				_type = self.visit(vspec["type"].name)
				rhs = self.visit(model.rhs)

				if (_type == "String" or _type == "dictionary" or _type == "string_id" or _type == "location") and rhs != "null":
					s = ""
					if model.operator == "!=":
						s += "!"

					s += "%s.equals(%s)" % (self.visit(model.lhs), self.visit(model.rhs))


		if s == "":
			s = "%s %s %s" % (self.visit(model.lhs), model.operator, self.visit(model.rhs))

		return s

	@v.when(FieldAccess)
	def visit(self, model):
		return "%s.%s" % (self.visit(model.target), model.name)

	@v.when(For)
	def visit(self, model):
		init = ""
		predicate = ""
		update = ""

		if model.init is not None:
			if type(model.init) is list:
				for i, _init in enumerate(model.init):
					init += "%s" % self.visit(_init)

					if i + 1 < len(model.init):
						init += ", "
			else:
				init = "%s" % self.visit(model.init)
		if model.predicate is not None:
			predicate = "%s" % self.visit(model.predicate)
		if model.update is not None:
			for i, u in enumerate(model.update):
				update += "%s" % self.visit(u)

				if i + 1 < len(model.update):
					update += ", "

		s  = "for (%s; %s; %s)" % (init, predicate, update)

		if type(model.body) is Block:
			s += self.visit(model.body)
		else:
			s += "\n"
			s += self._indent() + "{\n"

			self._scope_stack.push_scope()

			s += self._indent() + "%s" % self.visit(model.body)

			self._scope_stack.pop_scope()

			s += "\n"
			s += self._indent() + "}"

		return s

	@v.when(FormalParameter)
	def visit(self, model):
		s = ""

		for m in model.modifiers:
			s += self._build_modifier(m)

		if "resizeable" in model.modifiers:
			s += "Vector "
		else:
			s += "%s " % self.visit(model.type)

		s += model.variable.name
		s += self._build_dimensions(model.variable.dimensions)
		return s

	@v.when(FunctionDeclaration)
	def visit(self, model):
		return_type = self.visit(model.return_type)
		if return_type == "commandHandler":
			model = self._build_commandHandler_declaration(model)
		elif return_type == "messageHandler":
			model = self._build_messageHandler_declaration(model)
		elif return_type == "trigger":
			model = self._build_trigger_declaration(model)

		return self._build_function_declaration(model)


	@v.when(IfThenElse)
	def visit(self, model):
		s = "if (%s)" % self.visit(model.predicate)

		if model.if_true is not None:
			s += "%s" % self.visit(model.if_true)

		if model.if_false is not None:
			s += "\n"
			s += self._indent() + "else "
			if type(model.if_false) is not IfThenElse and type(model.if_false) is not Block:
				s += "\n"
				s += self._indent() + "{\n"

				self._scope_stack.push_scope()

				s += self._indent() + "%s" % self.visit(model.if_false)

				self._scope_stack.pop_scope()

				s += "\n"
				s += self._indent() + "}"

			else:
				s += "%s" % self.visit(model.if_false)

		return s

	@v.when(IncludeDeclaration)
	def visit(self, model):
		on_demand = ".*" if model.on_demand else ""

		if model.name.value[:4] == "java":
			s = "import %s%s;\n" % (model.name.value, on_demand)
		else:
			s = "import script.%s%s;\n" % (model.name.value, on_demand)

		self.include_count -= 1

		if self.include_count is 0:
			s += "\n"
			s += self._generate_class_header()

		return s

	@v.when(InstanceCreation)
	def visit(self, model):
		s = "new %s(" % self.visit(model.type)

		for i, a in enumerate(model.arguments):
			s += "%s" % self.visit(a)

			if i + 1 < len(model.arguments):
				s += ", "

		s += ")"

		return s

	@v.when(InstanceOf)
	def visit(self, model):
		_type = self.visit(model.rhs)
		if _type == "int":
			return "%s instanceof Integer" % self.visit(model.lhs)
		elif _type == "float":
			return "%s instanceof Float" % self.visit(model.lhs)
		else:
			return "%s instanceof %s" % (self.visit(model.lhs), _type)

	@v.when(Literal)
	def visit(self, model):
		return model.literal

	@v.when(MethodInvocation)
	def visit(self, model):
		if model.target is not None:
			if type(model.target) is not Name and type(model.target) is not ArrayAccess and type(model.target) is not str:
				s = "(%s).%s" % (self.visit(model.target), model.name)
			else:
				s = "%s.%s" % (self.visit(model.target), model.name)
		else:
			s = model.name

		s += "("

		for i, a in enumerate(model.arguments):
			s += "%s" % self.visit(a)

			if i + 1 < len(model.arguments):
				s += ", "

		s += ")"

		return s

	@v.when(Name)
	def visit(self, model):
		if model.value == "string":
			model.value = "String"

		if "." in model.value:
			tmp = model.value.split(".")

			if self._is_resizeable(tmp[0]) and tmp[1] == "length":
				return "%s.size()" % tmp[0]

		return model.value

	@v.when(Precidence)
	def visit(self, model):
		return "(%s)" % self.visit(model.expression)

	@v.when(Return)
	def visit(self, model):
		s = ""
		if model.result is not None:
			enclosing_func = self._scope_stack.get_enclosing_function()

			if type(model.result) is Name and self._is_resizeable(model.result.value) and not enclosing_func["resizeable"] and not self.visit(enclosing_func["return_type"].name) == "Vector":
				varname = model.result.value
				s = self._build_resizeable_conversion_to_type("_%s" % varname, self.visit(enclosing_func["return_type"].name), varname)
				s += "\n"
				s += self._indent() + "return _%s;" % varname
			else:
				s = "return %s;" % self.visit(model.result)
		else:
			s += "return;"

		return s

	@v.when(StatementExpression)
	def visit(self, model):
		s = "%s" % self.visit(model.expression)
		if not ";\n" in s:
			s += ";"

		return s

	@v.when(Switch)
	def visit(self, model):
		s  = "switch (%s)\n" % self.visit(model.expression)
		s += self._indent() + "{\n"

		self._scope_stack.push_scope()

		for c in model.switch_cases:
			s += "%s" % self.visit(c)

		self._scope_stack.pop_scope()

		s += self._indent() + "}"
		return s

	@v.when(SwitchCase)
	def visit(self, model):
		s = ""

		for c in model.cases:
			if c == "default":
				s += self._indent() + "default:\n"
			else:
				s += self._indent() + "case %s:\n" % self.visit(c)

		for stmt in model.body:
			s += "%s" % self.visit(stmt)

		return s

	@v.when(Throw)
	def visit(self, model):
		return "throw %s;" % self.visit(model.expression)

	@v.when(Try)
	def visit(self, model):
		s = "try"

		s += "%s" % self.visit(model.block)

		for c in model.catches:
			s += "%s" % self.visit(c)

		return s

	@v.when(Type)
	def visit(self, model):
		s = ""

		if type(model.name) is str:
			s += "%s" % model.name
		else:
			name = self.visit(model.name)

			if name == "unknown":
				name = "Object"

			s += "%s" % name

		s += "%s" % self._build_dimensions(model.dimensions)

		return s

	@v.when(Unary)
	def visit(self, model):
		if model.sign == "x++":
			return "%s%s" % (self.visit(model.expression), "++")
		elif model.sign == "x--":
			return "%s%s" % (self.visit(model.expression), "--")
		elif model.sign == "++x":
			return "%s%s" % ("++", self.visit(model.expression))
		elif model.sign == "--x":
			return "%s%s" % ("--", self.visit(model.expression))
		else:
			#return "%s" % model.sign
			return "%s%s" % (model.sign, self.visit(model.expression))

	@v.when(VariableDeclarator)
	def visit(self, model):
		variable = model.variable.name
		dimensions = self._build_dimensions(model.variable.dimensions)
		initializer = ""
		if model.initializer is not None:
			initializer = " = %s" % self.visit(model.initializer)

		return "%s%s%s" % (variable, dimensions, initializer)

	@v.when(VariableDeclaration)
	def visit(self, model):
		if "resizeable" in model.modifiers or (len(model.variable_declarators) == 1 and type(model.variable_declarators[0].initializer) is Name and self._is_resizeable(model.variable_declarators[0].initializer.value)):
			return self._visit_resizeable_declaration(model)

		s = ""

		if self._scope_stack.depth() == 1:
			s += "public static "


		for m in model.modifiers:
			s += self._build_modifier(m)

		s += "%s " % self.visit(model.type)

		for i, d in enumerate(model.variable_declarators):
			self._scope_stack.add_variable(d.variable.name, model.type, True if "resizeable" in model.modifiers else False)

			s += self.visit(d)

			if i + 1 < len(model.variable_declarators):
				s += ", "

		return "%s" % s

	@v.when(VariableDeclarationStatement)
	def visit(self, model):
		s = "%s" % self.visit(model.statement)
		if not ";\n" in s:
			s += ";"

		return s

	@v.when(While)
	def visit(self, model):
		s  = "while (%s)" % self.visit(model.predicate)

		if model.body is not None:
			s += self.visit(model.body)
		else:
			s += ";"

		return s

	def _build_dimensions(self, count):
		dimensions = ""
		while count > 0:
			dimensions += "[]"
			count -= 1
		return dimensions

	def _build_modifier(self, modifier):
		if modifier == "const":
			modifier = "final"

		if modifier == "resizeable":
			return ""

		return "%s " % modifier

	def _build_commandHandler_declaration(self, model):
		model.return_type = Type(name=Name(value='int'), enclosed_in=None, dimensions=0)

		prepend = [
			FormalParameter(variable=Variable(name='self', dimensions=0), type=Type(name=Name(value='obj_id'), enclosed_in=None, dimensions=0), modifiers=[]),
			FormalParameter(variable=Variable(name='target', dimensions=0), type=Type(name=Name(value='obj_id'), enclosed_in=None, dimensions=0), modifiers=[]),
			FormalParameter(variable=Variable(name='params', dimensions=0), type=Type(name=Name(value='string'), enclosed_in=None, dimensions=0), modifiers=[]),
			FormalParameter(variable=Variable(name='defaultTime', dimensions=0), type=Type(name=Name(value='float'), enclosed_in=None, dimensions=0), modifiers=[])
		]

		model.parameters = prepend + model.parameters

		return model

	def _build_messageHandler_declaration(self, model):
		model.return_type = Type(name=Name(value='int'), enclosed_in=None, dimensions=0)

		prepend = [
			FormalParameter(variable=Variable(name='self', dimensions=0), type=Type(name=Name(value='obj_id'), enclosed_in=None, dimensions=0), modifiers=[]),
			FormalParameter(variable=Variable(name='params', dimensions=0), type=Type(name=Name(value='dictionary'), enclosed_in=None, dimensions=0), modifiers=[])
		]

		model.parameters = prepend + model.parameters

		return model

	def _build_trigger_declaration(self, model):
		model.return_type = Type(name=Name(value='int'), enclosed_in=None, dimensions=0)

		prepend = [
			FormalParameter(variable=Variable(name='self', dimensions=0), type=Type(name=Name(value='obj_id'), enclosed_in=None, dimensions=0), modifiers=[])
		]

		model.parameters = prepend + model.parameters

		return model

	def _build_function_pre_declaration(self):
		return self._indent() + "public "

	def _build_function_declaration(self, model):
		self._scope_stack._last_function["name"] = model.name
		self._scope_stack._last_function["return_type"] = model.return_type
		self._scope_stack._last_function["resizeable"] = True if "resizeable" in model.modifiers else False

		s = self._build_function_pre_declaration()

		if "resizeable" in model.modifiers:
			s += "Vector %s(" % model.name
		else:
			for m in model.modifiers:
				s += self._build_modifier(m)

			s += "%s %s(" % (self.visit(model.return_type), model.name)

		append_stack = dict()

		for i, p in enumerate(model.parameters):
			append_stack[p.variable.name] = {
				"type": p.type,
				"resizeable": True if "resizeable" in p.modifiers else False
			}

			s += "%s" % self.visit(p)

			if i + 1 < len(model.parameters):
				s += ", "

		s += ") throws InterruptedException\n"

		s += self._indent() + "{\n"

		self._scope_stack.push_scope()
		self._scope_stack._stack[-1]["variables"].update(append_stack)


		for stmt in model.body:
			s += "%s" % self.visit(stmt)

		self._scope_stack.pop_scope()

		s += self._indent() + "}\n"

		return s

	def _generate_class_header(self):
		s  = self._indent() + "public class %s extends %s\n" % (self.class_name, self.inherits)
		s += self._indent() + "{\n"

		self._scope_stack.push_scope()

		s += self._indent() + "public %s()\n" % self.class_name
		s += self._indent() + "{\n"
		s += self._indent() + "}\n"

		return s

	def _generate_class_footer(self):
		s = "}\n"

		return s

	def _indent(self):
		return " " * (self.indention * self._scope_stack.depth())

	def _add_global_scope_functions(self, ast):
		for stmt in ast.statements:
			if type(stmt) is FunctionDeclaration:
				self._scope_stack.add_function(stmt.name, stmt.return_type, True if "resizeable" in stmt.modifiers else False)


	### Resizeable handling ###

	def _visit_resizeable_declaration(self, model):
		self._scope_stack.add_variable(model.variable_declarators[0].variable.name, model.type, True if "resizeable" in model.modifiers else False)

		if len(model.variable_declarators) > 1:
			raise Exception("Too many declarators in resizeable declaration")

		decl = model.variable_declarators[0]

		if type(decl.initializer) is Name and self._is_resizeable(decl.initializer.value) and not self._is_resizeable(decl.variable.name):
			#vdata = self._scope_stack.get_variable_data(decl.variable.name)
			#return "%s t %s" % (decl.variable.name, vdata["type"])
			return self._build_resizeable_conversion_to_type(decl.variable.name, self.visit(model.type.name), decl.initializer.value)

		if type(model.variable_declarators[0].initializer) is ArrayCreation:
			return self._handle_resizeable_ArrayCreation(model)
		if type(model.variable_declarators[0].initializer) is Cast:
			return self._handle_resizeable_Cast(model)
		if type(model.variable_declarators[0].initializer) is Conditional:
			return self._handle_resizeable_Conditional(model)
		if type(model.variable_declarators[0].initializer) is InstanceCreation:
			return self._handle_resizeable_InstanceCreation(model)
		if type(model.variable_declarators[0].initializer) is Literal:
			return self._handle_resizeable_Literal(model)
		if type(model.variable_declarators[0].initializer) is MethodInvocation:
			return self._handle_resizeable_MethodInvocation(model)
		if type(model.variable_declarators[0].initializer) is Name:
			return self._handle_resizeable_Name(model)
		if model.variable_declarators[0].initializer is None:
			return self._handle_resizeable_Init(model)
		return "%s" % model

	def _handle_resizeable_ArrayCreation(self, model):
		name = model.variable_declarators[0].variable.name
		length = self.visit(model.variable_declarators[0].initializer.dimensions[0])

		if length is None:
			length = 0

		s = "Vector %s = new Vector();\n" % name
		s += self._indent() + "%s.setSize(%s);" % (name, length)

		return s

	def _handle_resizeable_Cast(self, model):
		name = model.variable_declarators[0].variable.name
		cast = model.variable_declarators[0].initializer

		if self._is_resizeable(name):
			if "resizeable" in cast.modifiers:
				return "Vector %s = new Vector(Arrays.asList((%s)%s))" % (name, self.visit(cast.target), self.visit(cast.expression))
			else:
				return "Vector %s = %s" % (name, self.visit(cast))

		return "%s" % model

	def _handle_resizeable_Conditional(self, model):
		name = model.variable_declarators[0].variable.name
		return "Vector %s = %s" % (name, self.visit(model.variable_declarators[0].initializer))

	def _handle_resizeable_InstanceCreation(self, model):
		name = model.variable_declarators[0].variable.name
		_type = model.variable_declarators[0].initializer.type.name.value

		if _type == "Vector":
			return "Vector %s = new Vector()" % name
		else:
			return "%s" % model

	def _handle_resizeable_Literal(self, model):
		name = model.variable_declarators[0].variable.name
		literal = model.variable_declarators[0].initializer.literal

		if literal == "null":
			return "Vector %s = null" % name
		else:
			return "%s" % model

	def _handle_resizeable_MethodInvocation(self, model):
		name = model.variable_declarators[0].variable.name
		method_invocation = model.variable_declarators[0].initializer

		s = ""

		fspec = self._scope_stack.get_function_data(method_invocation.name)

		if fspec is None:
			s += "Vector %s = %s" % (name, self.visit(method_invocation))
		else:
			if fspec["resizeable"] is True or (type(fspec["return_type"]) is Type and fspec["return_type"].name.value == "Vector"):
				s += "Vector %s = %s" % (name, self.visit(method_invocation))
			else:
				s += "%s" % model

		return s

	def _handle_resizeable_Name(self, model):
		name = model.variable_declarators[0].variable.name
		varname = model.variable_declarators[0].initializer.value

		vspec = self._scope_stack.get_variable_data(varname)

		if vspec["resizeable"] is True or vspec["type"].name.value == "Vector":
			s = "Vector %s = %s" % (name, varname)
		else:
			to_type = self.visit(vspec["type"].name)

			if to_type == "int":
				s = "Vector %s = new Vector();\n" % (name)
				s += self._indent() + "if (%s != null)\n" % (name)
				s += self._indent() + "{\n"
			
				self._scope_stack.push_scope()

				s += self._indent() + "%s.setSize(%s.length);\n" % (name, varname)
				s += self._indent() + "for (int _i = 0; _i < %s.length; ++_i)\n" % (varname)

				s += self._indent() + "{\n"
			
				self._scope_stack.push_scope()

				s += self._indent() + "%s.set(_i, new Integer(%s[_i]));\n" % (name, varname)

				self._scope_stack.pop_scope()
			
				s += self._indent() + "}\n"

				self._scope_stack.pop_scope()
			
				s += self._indent() + "}"

			elif to_type == "float":
				s = "Vector %s = new Vector();\n" % (name)
				s += self._indent() + "if (%s != null)\n" % (name)
				s += self._indent() + "{\n"
			
				self._scope_stack.push_scope()

				s += self._indent() + "%s.setSize(%s.length);\n" % (name, varname)
				s += self._indent() + "for (int _i = 0; _i < %s.length; ++_i)\n" % (varname)

				s += self._indent() + "{\n"
			
				self._scope_stack.push_scope()

				s += self._indent() + "%s.set(_i, new Float(%s[_i]));\n" % (name, varname)

				self._scope_stack.pop_scope()
			
				s += self._indent() + "}\n"

				self._scope_stack.pop_scope()
			
				s += self._indent() + "}"

			else:
				s = "Vector %s = new Vector(Arrays.asList(%s))" % (name, varname)

		return s

	def _handle_resizeable_Init(self, model):
		name = model.variable_declarators[0].variable.name
		return "Vector %s" % name

	def _build_resizeable_conversion_to_type(self, to_name, to_type, from_name):
		s = "%s[] %s = new %s[0];\n" % (to_type, to_name, to_type)
		s += self._indent() + "if (%s != null)\n" % from_name
		s += self._indent() + "{\n"

		self._scope_stack.push_scope()

		s += self._indent() + "%s = new %s[%s.size()];\n" % (to_name, to_type, from_name)

		if to_type == "int":
			s += self._indent() + "for (int _i = 0; _i < %s.size(); ++_i)\n" % from_name
			s += self._indent() + "{\n"

			self._scope_stack.push_scope()

			s += self._indent() + "%s[_i] = ((Integer)%s.get(_i)).intValue();\n" % (to_name, from_name)

			self._scope_stack.pop_scope()

			s += self._indent() + "}\n"
		elif to_type == "float":
			s += self._indent() + "for (int _i = 0; _i < %s.size(); ++_i)\n" % from_name
			s += self._indent() + "{\n"

			self._scope_stack.push_scope()

			s += self._indent() + "%s[_i] = ((Float)%s.get(_i)).floatValue();\n" % (to_name, from_name)

			self._scope_stack.pop_scope()

			s += self._indent() + "}\n"
		else:
			s += self._indent() + "%s.toArray(%s);\n" % (from_name, to_name)

		self._scope_stack.pop_scope()

		s += self._indent() + "}"

		return s

	def _is_resizeable(self, name):
		data = self._scope_stack.get_variable_data(name)

		if data is not None:
			return True if data["resizeable"] is True or data["type"].name.value == "Vector" else False
		else:
			return False

	def _is_resizeable_function(self, name):
		data = self._scope_stack.get_function_data(name)

		if data is not None:
			return True if data["resizeable"] is True or data["return_type"].name.value == "Vector" else False
		else:
			return False

class JavaStaticClassGenerator(JavaClassGenerator):
	def _build_function_pre_declaration(self):
		return self._indent() + "public static "

