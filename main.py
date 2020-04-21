from inference import *


T_VAR_1 = TVar()
T_VAR_2 = TVar()
T_VAR_3 = TVar()


DEFAULT_ENV = Env({
    Var('add_int'): Scheme(set(), TArrow(TInt, TArrow(TInt, TInt))),
    Var('sub_int'): Scheme(set(), TArrow(TInt, TArrow(TInt, TInt))),
    Var('div_int'): Scheme(set(), TArrow(TInt, TArrow(TInt, TInt))),
    Var('mul_int'): Scheme(set(), TArrow(TInt, TArrow(TInt, TInt))),
    Var('mod_int'): Scheme(set(), TArrow(TInt, TArrow(TInt, TInt))),
    Var('print_int'): Scheme(set(), TArrow(TInt, TVoid)),
    Var('print_string'): Scheme(set(), TArrow(TString, TVoid)),
    Var('true'): Scheme(set(), TBool),
    Var('false'): Scheme(set(), TBool)
})


def main():
    e1, t1 = infer(
        DEFAULT_ENV,
        App(
            Lambda(
                Var('x'),
                Var('x')
            ),
            IntLit(1)
        )
    )

    e2, t2 = infer(
        DEFAULT_ENV,
        Let(
            Var('x'),
            Lambda(
                Var('y'),
                Var('y')
            ),
            App(
                Var('x'),
                StringLit('Types')
            )
        )
    )

    e3, t3 = infer(
        DEFAULT_ENV,
        Lambda(
            Var('y'),
            App(
                App(
                    Var('add_int'),
                    Var('y')
                ),
                Var('y')
            )
        ),
    )

    e4, t4 = infer(
        DEFAULT_ENV,
        App(
            Var('print_string'),
            StringLit('hello, world!')
        )
    )

    print(t1)
    print(t2)
    print(t3)
    print(t4)


if __name__ == '__main__':
    main()
