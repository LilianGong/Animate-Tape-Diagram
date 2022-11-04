from builtins import str
import sympy
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import re
from itertools import zip_longest


class equationSolver:

    def __init__(self, symbol):
        self.x = symbols(symbol)
        self.equation = None
        self.xValue = None

    def get_equation(self, equation_str: str):
        assert re.search(r"-|/", equation_str) is None, "unsupported subtraction and division found"
        left_exp = parse_expr(equation_str.split("=")[0])
        right_exp = parse_expr(equation_str.split("=")[1])
        self.equation = Eq(left_exp, right_exp)

    def solve_equation(self, equation_str: str):
        self.get_equation(equation_str)
        self.xValue = solve(self.equation)[0]
        assert type(self.xValue) is sympy.core.numbers.Float or sympy.core.numbers.Integer, \
            "multiple unknown symbols found, please check your spelling"

        assert self.xValue >= 0, "x value is a negative number. please try the model with a positive x value"
        # return float or int object, not sympy.core object
        if type(self.xValue) is sympy.core.numbers.Float:
            self.xValue = round(float(self.xValue), 2)

        if type(self.xValue) is sympy.core.numbers.Integer:
            self.xValue = int(self.xValue)


class arrayGenerator:

    def __init__(self):
        self.xValue = None

        self.leftStrArray = None
        self.rightStrArray = None

        self.leftMatrix = None
        self.rightMatrix = None

    def get_str_array(self, equation_str, symbol):

        # make sure when coef. = 1, the label is the symbol
        equation_str = equation_str.replace("1*{}".format(symbol), symbol)

        left_str = equation_str.split("=")[0]
        right_str = equation_str.split("=")[1]

        self.leftStrArray = re.split(r'\+|- ', left_str)
        self.rightStrArray = re.split(r'\+|- ', right_str)

        str_array = list(zip_longest(self.leftStrArray, self.rightStrArray))
        self.leftStrArray, self.rightStrArray = map(list, zip(*str_array))

    @staticmethod
    def get_ordered_matrix(array, x_value, symbol):

        data_ls = []
        for i in array:
            if not i:
                data_ls.append(0)
            elif symbol in i:
                if i == symbol:
                    coef = 1
                else:
                    coef = float(i.split("*")[0])
                val = round(x_value * coef, 2)
                if type(val) is float and val.is_integer():
                    val = int(val)
                    data_ls.append(val)
                else:
                    data_ls.append(round(val, 2))
            else:
                val = round(float(i), 2)
                if val.is_integer():
                    val = int(val)
                data_ls.append(val)

        label_ls = ["" if not i
                    else i.replace("*", "")
                    for i in array]

        type_ls = [1 if not i
                   else
                   (0 if symbol in i
                    else 1)
                   for i in array]

        matrix_with_keys = list(zip(data_ls, label_ls, type_ls))
        matrix_with_keys = sorted(matrix_with_keys, key=lambda item: item[2])

        return matrix_with_keys

    def get_data_matrix(self, equation_str, x_value, symbol):
        self.get_str_array(equation_str, symbol)
        self.leftMatrix = self.get_ordered_matrix(self.leftStrArray, x_value, symbol)
        self.rightMatrix = self.get_ordered_matrix(self.rightStrArray, x_value, symbol)


if __name__ == "__main__":
    equation = '''2*x + 7 = 21'''
    solver = equationSolver()
    solver.solve_equation(equation)
    print("{}, x = {}".format(equation, solver.xValue))
