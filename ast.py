from type_ast import *


class Expr:
    def __init__(self):
        self.type = Hole()


class Var(Expr):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f'Var({self.name}) : {self.type}'

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Var):
            return self.name == other.name

        return False


class Literal(Expr):
    TYPE = Hole()

    def __init__(self, value):
        super().__init__()
        self.value = value
        self.type = type(self).TYPE

    def __str__(self):
        return f'{self.value} : {self.type}'

    def __eq__(self, other):
        return isinstance(other, Literal) and self.value == other.value


class BoolLit(Literal):
    TYPE = TBool


class StringLit(Literal):
    TYPE = TString


class IntLit(Literal):
    TYPE = TInt


class FloatLit(Literal):
    TYPE = TFloat


class Lambda(Expr):
    def __init__(self, var: Var, body: Expr):
        super().__init__()
        assert isinstance(var, Var)

        self.var = var
        self.body = body

    def __str__(self):
        return f'(\\({self.var}) -> ({self.body})) : {self.type}'

    def __eq__(self, other):
        return isinstance(other, Lambda) and self.var == other.var and self.body == other.body


class Let(Expr):
    def __init__(self, var, body, expr):
        super().__init__()
        self.var = var
        self.body = body
        self.expr = expr

    def __str__(self):
        return f'let {self.var} = {self.body} in {self.expr}'


class App(Expr):
    def __init__(self, e1, e2):
        super().__init__()
        self.e1 = e1
        self.e2 = e2

    def __str__(self):
        return f'App({self.e1}, {self.e2}) : {self.type}'


class IfThenElse(Expr):
    def __init__(self, cond, succ, fail):
        super().__init__()
        self.cond = cond
        self.succ = succ
        self.fail = fail

    def __str__(self):
        return f"if {self.cond} then {self.succ} else {self.fail}"

    def __repr__(self):
        return str(self)
