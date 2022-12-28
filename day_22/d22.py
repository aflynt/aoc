

class Expr:
    pass


class BinaryOp(Expr):
    def __init__(self, left, right, opchar='+') -> None:
        self.m_l = left
        self.m_r = right
        self.m_opchar = opchar
        super().__init__()

    def str_helper(self):
        return '(' + str(self.m_l) + self.m_opchar + str(self.m_r) + ')'

    def __str__(self) -> str:
        return self.str_helper()

    def eval(self, context):

        if self.m_opchar == '*':
            return self.m_l.eval(context) * self.m_r.eval(context)
        else:
            return self.m_l.eval(context) + self.m_r.eval(context)


class Multipy(BinaryOp):
    def __init__(self, left, right) -> None:
        super().__init__(left, right, '*')


class Add(BinaryOp):
    def __init__(self, left, right) -> None:
        super().__init__(left, right, '+')


class Var(Expr):
    def __init__(self, name) -> None:
        self.m_name = name
        super().__init__()

    def __str__(self) -> str:
        return self.m_name

    def eval(self, context):
        return context[self.m_name]


class Const(Expr):
    def __init__(self, value) -> None:
        self.m_value = value

    def __str__(self):
        return str(self.m_value)

    def eval(self, _):
        return self.m_value


e1 = Multipy(Var('x'), Add(Const(2), Var('y')))
e2 = Add(Multipy(Var('x'), Const(2)), Var('y'))

ctx = {
        'x': 3,
        'y': 4,
}

print(f'{e1}: { e1.eval(ctx)}')
print(f'{e2}: { e2.eval(ctx)}')




