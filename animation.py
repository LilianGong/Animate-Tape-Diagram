import matplotlib.animation as ani
import matplotlib.pyplot as plt
from solveEquation import equationSolver, arrayGenerator
import utils

fig = plt.figure(figsize=(20, 5))
plt.ylim(0, 3)


class BarChartAnimatorHint:

    def __init__(self, equation_str: str, symbol="x"):
        self.equationStr = equation_str.replace(" ", "")

        self.solver = equationSolver(symbol)
        self.solver.solve_equation(self.equationStr)

        self.x = self.solver.x
        self.xValue = self.solver.xValue
        self.equation = self.solver.equation

        self.generator = arrayGenerator()
        self.generator.get_data_matrix(self.equationStr, self.xValue, symbol)
        self.leftMatrix = self.generator.leftMatrix
        self.rightMatrix = self.generator.rightMatrix

        # for frame 3 to 5
        self.leftTemp = None
        self.rightTemp = None

        self.patches = []
        self.xMax = float(sum([tup[0] for tup in self.leftMatrix])) + 1

        self.frameDurations = [10, 10, 10, 10, 10, 10, 10]

    def plot_one_frame(self, left, right):
        self.patches = []
        self.patches += utils.plot_bar(left, 0.3)
        self.patches += utils.plot_bar(right, 0.1)
        self.patches += utils.plot_labels(self.patches, left, right)

    '''
    # frame 0
    '''

    def init_frame(self):
        initial_animator = BarChartAnimatorHint(self.equationStr)
        return initial_animator.leftMatrix, initial_animator.rightMatrix

    '''
    # frame 1
    '''

    def simplify_components(self):
        simplified_equation_str = str(self.equation.lhs) + "=" + str(self.equation.rhs)
        simplify_animator = BarChartAnimatorHint(simplified_equation_str)
        self.leftMatrix = simplify_animator.leftMatrix
        self.rightMatrix = simplify_animator.rightMatrix

    '''
    # frame 2 - 6 
    # if mode = compare, frame 3 data returned
    # if mode = subtract, frame 4 data returned
    '''

    def get_components_to_subtract(self, mode=0):

        assert mode in [0, 1, 2, 3, 4, 5, 6], "invalid mode!"

        left_unknown = utils.get_specific_type_tuple(self.leftTemp, 0)
        right_unknown = utils.get_specific_type_tuple(self.rightTemp, 0)
        left_numeric = utils.get_specific_type_tuple(self.leftTemp, 1)
        right_numeric = utils.get_specific_type_tuple(self.rightTemp, 1)

        if mode == 0:  # split numeric subtraction part
            number_l, number_r = utils.compare_or_subtract_num_parts(self.xValue, left_numeric[0], right_numeric[0], 0)
            left_unknown = [tup for tup in left_unknown if tup[1] != '0x']
            right_unknown = [tup for tup in right_unknown if tup[1] != '0x']
            return left_unknown + number_l, right_unknown + number_r

        elif mode == 1:  # white out numeric subtraction part
            number_l, number_r = utils.compare_or_subtract_num_parts(self.xValue, left_numeric[0], right_numeric[0], 1)
            left_unknown = [tup for tup in left_unknown if tup[1] != '0x']
            right_unknown = [tup for tup in right_unknown if tup[1] != '0x']
            return left_unknown + number_l, right_unknown + number_r

        elif mode == 2:  # remove numeric subtraction part
            number_l, number_r = utils.compare_or_subtract_num_parts(self.xValue, left_numeric[0], right_numeric[0], 1)
            number_l = [tup for tup in number_l if tup[2] != 2]
            number_r = [tup for tup in number_r if tup[2] != 2]
            left_unknown = [tup for tup in left_unknown if tup[1] != '0x']
            right_unknown = [tup for tup in right_unknown if tup[1] != '0x']
            return left_unknown + number_l, right_unknown + number_r

        elif mode == 3:  # split unknown subtraction part
            unknown_l, unknown_r = utils.compare_or_subtract_x_parts(self.xValue, left_unknown[0], right_unknown[0], 0)
            number_l, number_r = utils.compare_or_subtract_num_parts(self.xValue, left_numeric[0], right_numeric[0], 1)
            number_l = [tup for tup in number_l if tup[2] != 2]
            number_r = [tup for tup in number_r if tup[2] != 2]
            return unknown_l + number_l, unknown_r + number_r

        elif mode == 4:  # white out unknown subtraction part
            unknown_l, unknown_r = utils.compare_or_subtract_x_parts(self.xValue, left_unknown[0], right_unknown[0], 1)
            number_l, number_r = utils.compare_or_subtract_num_parts(self.xValue, left_numeric[0], right_numeric[0], 1)
            number_l = [tup for tup in number_l if tup[2] != 2]
            number_r = [tup for tup in number_r if tup[2] != 2]
            return unknown_l + number_l, unknown_r + number_r

        elif mode == 5:  # remove unknown subtraction part - unstacked to the left part
            unknown_l, unknown_r = utils.compare_or_subtract_x_parts(self.xValue, left_unknown[0], right_unknown[0], 1)
            number_l, number_r = utils.compare_or_subtract_num_parts(self.xValue, left_numeric[0], right_numeric[0], 1)
            unknown_l = [tup if tup[2] != 2 else (tup[0], tup[1], 3) for tup in unknown_l]
            unknown_r = [tup if tup[2] != 2 else (tup[0], tup[1], 3) for tup in unknown_r]
            number_l = [tup for tup in number_l if tup[2] != 2]
            number_r = [tup for tup in number_r if tup[2] != 2]
            return unknown_l + number_l, unknown_r + number_r

        elif mode == 6:  # n*x=m stacked to the left part
            unknown_l, unknown_r = utils.compare_or_subtract_x_parts(self.xValue, left_unknown[0], right_unknown[0], 1)
            number_l, number_r = utils.compare_or_subtract_num_parts(self.xValue, left_numeric[0], right_numeric[0], 1)
            unknown_l = [tup for tup in unknown_l if tup[2] != 2]
            unknown_r = [tup for tup in unknown_r if tup[2] != 2]
            number_l = [tup for tup in number_l if tup[2] != 2]
            number_r = [tup for tup in number_r if tup[2] != 2]
            return unknown_l + number_l, unknown_r + number_r

    '''
    # frame 7
    '''

    def get_split_blocks(self):
        coef_str = [i[1] for i in self.leftMatrix + self.rightMatrix if i[2] == 0][0].split("x")[0]
        coef = utils.label_to_number(coef_str)
        return utils.split_unknowns(self.leftMatrix, coef, self.xValue), \
               utils.split_unknowns(self.rightMatrix, coef, self.xValue)

    '''
    # frame 8
    '''

    def get_single_block(self, sym_type):
        return utils.keep_single_block(self.leftMatrix, sym_type), utils.keep_single_block(self.rightMatrix, sym_type)
