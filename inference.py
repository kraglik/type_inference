from typing import Set

from ast import *
from type_ast import *


def var_bind(u, t):
    if isinstance(u, TVar) and u == t:
        return Subst()

    if u in t.ftv:
        raise Exception("occur check fails")

    return Subst({u: t})


def mgu(t1, t2):
    if isinstance(t1, TVar):
        return var_bind(t1, t2)

    elif isinstance(t2, TVar):
        return var_bind(t2, t1)

    elif isinstance(t1, TCon) and isinstance(t2, TCon):
        return Subst()

    elif isinstance(t1, TArrow) and isinstance(t2, TArrow):
        s1 = mgu(t1.t1, t2.t1)
        s2 = mgu(t1.t2.apply(s1), t2.t2.apply(s1))

        return s1.compose(s2)

    raise Exception("Types does not unify")


def infer(env, expr):
    if isinstance(expr, Literal):
        if isinstance(expr, BoolLit):
            return Subst(), TBool

        elif isinstance(expr, FloatLit):
            return Subst(), TFloat

        elif isinstance(expr, StringLit):
            return Subst(), TString

        elif isinstance(expr, IntLit):
            return Subst(), TInt

    elif isinstance(expr, Var):
        if expr not in env:
            raise Exception("Unbound variable")

        e = env[expr]

        return Subst(), e.instantiate()

    elif isinstance(expr, Lambda):
        tv = TVar()
        env_ = env.remove(expr.var).union(Env({expr.var: Scheme(set(), tv)}))

        s, t = infer(env_, expr.body)

        return s, TArrow(tv.apply(s), t)

    elif isinstance(expr, App):
        tv = TVar()
        s1, t1 = infer(env, expr.e1)
        s2, t2 = infer(env.apply(s1), expr.e2)
        s3 = mgu(t1.apply(s2), TArrow(t2, tv))

        return s3.compose(s2).compose(s1), tv.apply(s3)

    elif isinstance(expr, Let):
        s1, t1 = infer(env, expr.body)
        env_ = env.remove(expr.var)
        t_ = env.apply(s1).generalize(t1)
        env_ = env_.insert(expr.var, t_)

        s2, t2 = infer(env_.apply(s1), expr.expr)

        return s1.compose(s2), t2

    elif isinstance(expr, IfThenElse):
        s_cond, t_cond = infer(env, expr.cond)
        s_succ, t_succ = infer(env.apply(s_cond), expr.succ)
        s_fail, t_fail = infer(env.apply(s_succ), expr.fail)

        s_body = mgu(t_succ.apply(s_fail), t_fail)

        t_succ = t_succ.apply(s_body)
        t_fail = t_fail.apply(s_body)

        assert t_succ == t_fail

        return s_body, t_succ


