import operator
import re


def to_list(s: str) -> list:

    # separate numbers from operations and make list   '1+1' -> ['1', '+', '1']

    nums = re.findall(r'\d*\.\d*|\d+', s)
    ops = re.findall(r'[+\-*/]', s)
    lst = []

    op = 0
    if s[0] in ['-', '+']:
        op = ops.pop(0)

    for i in range(len(ops)):
        lst.append(nums.pop(0))
        lst.append(ops.pop(0))

    lst.append(nums.pop())
    for i in lst:
        if i.isdigit() or ('.' in i):
            try:
                lst[lst.index(i)] = int(i)
            except ValueError:
                lst[lst.index(i)] = float(i)

    if op == '-':
        lst[0] = -lst[0]

    return lst


def polska(lst: list) -> list:
    # make Reverse Polish Notation

    priority = {"*": 1, "/": 1, "+": 0, "-": 0}
    pol = []
    ops = []
    for i in lst:
        try:
            int(i)

        except ValueError:
            if ops and (priority[ops[-1]] >= priority[i]):
                pol.append(ops.pop())

            ops.append(i)

        else:
            pol.append(i)

    while ops:
        pol.append(ops.pop())

    return pol


def solution(expression: str) -> float:
    # find a solution

    lst = to_list(expression)
    polka = polska(lst)
    operations = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}

    sol = []

    for i in polka:
        try:

            int(i)

        except ValueError:
            sol.append(operations[i](sol.pop(-2), sol.pop()))

        else:
            sol.append(i)

    return sol.pop()

