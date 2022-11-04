import numpy as np
import matplotlib.pyplot as plt

colorMap = {0: "#6E85B2",
            1: "#FDE49C",
            2: "#ffffff",
            3: "#ffffff"}

lineStyleMap = {0: "-",
                1: "-",
                2: "--",
                3: "--"}

lineWidthMap = {0: 2,
                1: 2,
                2: 1,
                3: 0}


# plot blocks for one side of the equation (one data matrix)
def plot_bar(matrix, bar_index):
    left_width = 0
    patches = []
    for tup in matrix:
        dat, label, sym_type = tup
        recs = plt.barh(bar_index, dat,
                        left=left_width, height=0.1,
                        color=colorMap[sym_type],
                        linestyle=lineStyleMap[sym_type],
                        linewidth=lineWidthMap[sym_type],
                        edgecolor="#334756")
        left_width += dat
        patches += recs
    return patches


# plot labels for each block in the patch list
def plot_labels(patches, left, right):
    merged_matrix = left + right
    annotations = []

    if len(merged_matrix) == 0:
        print("no bar plotted")
        return None

    # For each bar: Place a label
    for rect, tup in zip(patches, merged_matrix):
        label = tup[1]

        x_value = rect.get_x() + rect.get_width() / 2
        y_value = rect.get_y() + rect.get_height() / 2
        # Number of points between bar and label
        space = 0
        # Vertical alignment for positive values
        ha = 'left'
        # Create annotation
        anno = plt.annotate(
            label,
            (x_value, y_value),
            xytext=(space, 0),  # Horizontally shift label by `space`
            textcoords="offset points",  # Interpret `xytext` as offset in points
            va='center',  # Vertically center label
            ha=ha,  # Horizontally align label differently for
            fontsize=32)
        annotations.append(anno)

    return annotations


# compare if left and right matrix is the same
def compare_equation_matrices(prev, current):
    pass


# to keep all float as %2f, all int as int
# from float or int to str label
def number_to_label(n):
    if n == 0:
        return ''
    if type(n) is int:
        return str(int(n))
    elif type(n) is float:
        if n.is_integer():
            return str(int(n))
    return str(round(n, 2))


# to keep all float as %2f, all int as int
# from label to float or int
def label_to_number(l):
    if l == '':
        return 0
    n = float(l)
    if n.is_integer():
        return int(n)
    return round(n, 2)


# frame 2, 3 and 4
# extract one type of symbols in the data matrix
def get_specific_type_tuple(matrix, symType):
    unknown = [tup for tup in matrix if tup[2] == symType and tup[0] != 0]
    # assert len(unknown) <= 1, print("there are multiple unknown/numeric symbols in one side of the equation.")
    if len(unknown) == 0:
        if symType == 0:
            unknown = [(0, "0x", 0)]
        if symType == 1:
            unknown = [(0, "0", 1)]
    return unknown


def subtract_part(value_tup):
    max_index = np.argmax(value_tup)
    subtract_val = value_tup[1 - max_index]
    remain_val = value_tup[max_index] - subtract_val
    return max_index, subtract_val, remain_val


def get_unknown_labels(subtract_val, remain_val, x_value):
    coef_subtract = number_to_label(subtract_val / x_value)
    coef_remain = number_to_label(remain_val / x_value)
    # there is no unknown to subtract
    if coef_subtract == "":
        subtract_label = ""

    else:
        # subtract if == 1x
        if coef_subtract == "1":
            coef_subtract = ""

        subtract_label = coef_subtract + "x"

    # ramin if == 1x
    if coef_remain == "1":
        coef_remain = ""
    remain_label = coef_remain + "x"

    if subtract_label == "0x":
        subtract_label == ""

    return subtract_label, remain_label


def return_tuples(subtract_val, subtract_label, remain_val, remain_label, sym_type, max_index, mode):
    assert mode in [0, 1], "invalid mode passed"

    if mode == 0:
        return_tup_left = [(remain_val, remain_label, sym_type), (subtract_val, subtract_label, sym_type)]
        return_tup_right = [(subtract_val, subtract_label, sym_type)]

    if mode == 1:
        return_tup_left = [(remain_val, remain_label, sym_type), (subtract_val, "", 2)]
        return_tup_right = [(subtract_val, "", 2)]

    if max_index == 1:
        return_tup_left, return_tup_right = return_tup_right, return_tup_left

    return return_tup_left, return_tup_right


# frame 2, 3 and 4
# mode == 0 : split
# mode == 1 : subtract
def compare_or_subtract_num_parts(x_value, left_num_part, right_num_part, mode):
    value_tup = [left_num_part[0], right_num_part[0]]  # numeric values of each side's number part
    sym_type = 1  # symbol type : number
    max_index, subtract_val, remain_val = subtract_part(value_tup)  # get the value to subtract, and value to remain
    subtract_label = number_to_label(subtract_val)
    remain_label = number_to_label(remain_val)

    returnTupLeft, returnTupRight = return_tuples(subtract_val, subtract_label,
                                                  remain_val, remain_label,
                                                  sym_type, max_index, mode)

    return returnTupLeft, returnTupRight


def compare_or_subtract_x_parts(x_value, left_unknown_part, right_unknown_part, mode):
    valueTup = [left_unknown_part[0], right_unknown_part[0]]  # numeric values of each side's number part
    symType = 0  # symbol type : number
    maxIndex, subtractVal, remainVal = subtract_part(valueTup)  # get the value to subtract, and value to remain
    subtractLabel, remainLabel = get_unknown_labels(subtractVal, remainVal, x_value)

    returnTupLeft, returnTupRight = return_tuples(subtractVal, subtractLabel,
                                                  remainVal, remainLabel,
                                                  symType, maxIndex, mode)

    returnTupLeft.reverse()
    returnTupRight.reverse()

    return returnTupLeft, returnTupRight


# frame 5
# split n*x into x, x, ..., x
def split_unknowns(matrix, coef, x_value):
    assert type(coef) is int, "split by decimal coefficient not yet enabled"
    updated = []
    for tup in matrix:
        if tup[2] == 2:
            updated.append(tup)
        # unknown
        elif tup[2] == 0:
            for i in range(coef):
                updated.append((x_value, 'x', 0))
        # number
        elif tup[2] == 1:
            for i in range(coef):
                updated.append((x_value, str(x_value), 1))
    return updated


# frame 6
# keep one block each for unknowns and numbers
def keep_single_block(matrix, sym_type=2):
    updated = []
    blockEncountered = None
    for tup in matrix:
        if tup[2] == 2:
            if sym_type == 2 and sym_type == 2:
                updated.append(tup)
        if tup[2] == 0 or tup[2] == 1:
            if not blockEncountered:
                updated.append(tup)
                blockEncountered = 1
            else:
                updated.append((tup[0], '', sym_type))
    return updated


def pass_matrix_value(animator, animator_hint_two):
    animator_hint_two.leftMatrix, animator_hint_two.rightMatrix = animator.leftMatrix, animator.rightMatrix
    animator_hint_two.leftTemp, animator_hint_two.rightTemp = animator.leftTemp, animator.rightTemp
