from functools import reduce
from typing import Set
from abc import abstractmethod, ABC


class Types:
    @property
    def ftv(self):
        raise NotImplementedError

    @abstractmethod
    def apply(self, subst):
        raise NotImplementedError


class Type(Types, ABC):
    pass


class TVar(Type):
    _next_id = 1

    def __init__(self):
        super().__init__()
        self.id = TVar._next_id
        TVar._next_id += 1

    def __str__(self):
        return f'τ{self.id}'

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return str(self)

    @property
    def ftv(self):
        return {self}

    def apply(self, subst: dict):
        return subst.get(self, self)

    def __eq__(self, other):
        return isinstance(other, TVar) and self.id == other.id


class TArrow(Type):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2

    def __str__(self):
        return f'{self.t1} -> {self.t2}'

    def __repr__(self):
        return str(self)

    @property
    def ftv(self):
        return self.t1.ftv | self.t2.ftv

    def apply(self, subst):
        return TArrow(self.t1.apply(subst), self.t2.apply(subst))


class Hole(Type):
    def __str__(self):
        return 'ø'

    def __eq__(self, other):
        return isinstance(other, Hole)

    @property
    def ftv(self):
        return set()

    def apply(self, subst):
        return self


class TCon(Type):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __eq__(self, other):
        return isinstance(other, TCon) and self.name == other.name

    def __str__(self):
        return self.name if len(self.args) == 0 else f"{self.name} {' '.join(self.args)}"

    def __repr__(self):
        return self.name

    @property
    def ftv(self):
        return set()

    def apply(self, subst):
        return self


TInt = TCon('Int', [])
TBool = TCon('Bool', [])
TString = TCon('String', [])
TFloat = TCon('Float', [])
TVoid = TCon('()', [])


class Scheme(Types):
    def __init__(self, xs: Set['TVar'], t: 'Type'):
        self.vars: Set[TVar] = xs
        self.type: Type = t

    def __str__(self):
        if len(self.vars) == 0:
            return str(self.type)

        return f'∀ {" ".join(str(v) for v in self.vars)} . {self.type}'

    @property
    def ftv(self):
        return self.type.ftv - set(self.vars)

    def apply(self, subst):
        return Scheme(self.vars, self.type.apply(subst))

    def instantiate(self):
        s = Subst({v: TVar() for v in self.vars})

        return self.type.apply(s)


class Constraint:
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2

    def __str__(self):
        return f'{self.t1} ≡ {self.t2}'


class TypesList(Types, list):
    def apply(self, subst):
        return [t.apply(subst) for t in self]

    @property
    def ftv(self):
        return reduce(lambda t1, t2: t1 | t2.ftv, self, set())


class Subst(dict):
    def compose(self, other):
        s2 = {k: v.apply(self) for k, v in other.items()}

        return Subst({**self, **s2})

    def __str__(self):
        return '{' + ', '.join(f'{k} -> {v}' for k, v in self.items()) + '}'

    def repr(self):
        return str(self)


class Env(Types, dict):
    def remove(self, var):
        return Env({k: v for k, v in self.items() if k != var})

    def insert(self, var, type):
        return Env({**self, **{var: type}})

    def apply(self, subst):
        return Env({k: v.apply(subst) for k, v in self.items()})

    def union(self, other):
        return Env({**self, **other})

    @property
    def ftv(self):
        return TypesList(self.values()).ftv

    def generalize(self, t: Type):
        return Scheme(t.ftv - self.ftv, t)

