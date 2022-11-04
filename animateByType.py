from animation import BarChartAnimatorHint, fig
import matplotlib.animation as ani
import matplotlib.pyplot as plt
import os
import main

typeRef = {'type1': 'x+b=c',
           'type2': 'ax+b=c',
           'type3': 'ax+b=cx',
           'type4': 'ax+b=cx+d'}


# create the folders if not exist
def mk_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_save_path(equation_str):
    formatted_str = equation_str.replace("*", "")
    fpath = main.storePath.format(formatted_str)
    mk_path(fpath)
    return fpath


class TypedHintAnimator(BarChartAnimatorHint):

    def __init__(self, equation_str: str, equation_type: str, symbol):
        super(TypedHintAnimator, self).__init__(equation_str, symbol)

        self.type = equation_type

        self.hintOneSequence = []
        self.hintTwoSequence = []
        self.hintThreeSequence = []

        self.subtractFrameStep = 0

        self.keepBlockStep = 2

        self.get_hint_one_frames()
        self.get_hint_two_frames()
        self.get_hint_three_frames()

    def get_hint_one_frames(self):
        if self.type == 'type1':
            self.hintOneSequence = [(self.init_frame, None),
                                    (self.get_components_to_subtract, 0),
                                    (self.get_components_to_subtract, 0)]

        elif self.type == "type3":
            self.hintOneSequence = [(self.init_frame, None),
                                    (self.get_components_to_subtract, 3),
                                    (self.get_components_to_subtract, 4),
                                    (self.get_components_to_subtract, 5)]

        elif self.type in ["type2", "type4"]:
            self.hintOneSequence = [(self.init_frame, None),
                                    (self.get_components_to_subtract, 0),
                                    (self.get_components_to_subtract, 1),
                                    (self.get_components_to_subtract, 2)]

    def get_hint_two_frames(self):

        if self.type == "type1":
            self.hintTwoSequence = [(self.get_components_to_subtract, 0),
                                    (self.get_components_to_subtract, 1),
                                    (self.get_components_to_subtract, 2)]

        elif self.type in ["type2", "type3"]:
            self.hintTwoSequence = []

        elif self.type == "type4":
            self.hintTwoSequence = [(self.get_components_to_subtract, 2),
                                    (self.get_components_to_subtract, 3),
                                    (self.get_components_to_subtract, 4),
                                    (self.get_components_to_subtract, 5)]

    def get_hint_three_frames(self):
        if self.type == "type1":
            self.hintThreeSequence = []

        else:
            self.hintThreeSequence = [(self.get_components_to_subtract, 6),
                                      (self.get_split_blocks, None),
                                      (self.get_single_block, 2),
                                      (self.get_single_block, 3)]

    def animate(self, i, hint_sequence):

        assert hint_sequence != [], "empty sequence!"

        fig.clear()
        plt.axis('off')

        func, input = hint_sequence[i]

        # for the very first frame in hint 1
        if func == self.init_frame:
            self.leftTemp, self.rightTemp = self.leftMatrix, self.rightMatrix

        else:
            if not input:
                self.leftMatrix, self.rightMatrix = func()
            else:
                self.leftMatrix, self.rightMatrix = func(input)

        self.plot_one_frame(self.leftMatrix, self.rightMatrix)

        plt.xlim(-3, self.xMax)

        return self.patches


class AnimateThreeHints:

    def __init__(self, equation_str, equation_type, symbol):

        self.typeAnimator = TypedHintAnimator(equation_str, equation_type, symbol)
        self.savePath = get_save_path(equation_type + " " + equation_str)

    def animate_hints(self):

        for i, hintSequence in enumerate([self.typeAnimator.hintOneSequence,
                                          self.typeAnimator.hintTwoSequence,
                                          self.typeAnimator.hintThreeSequence]):
            if len(hintSequence) > 0:
                hint_length = len(hintSequence)
                try:
                    animated_hint = ani.FuncAnimation(fig, self.typeAnimator.animate,
                                                      fargs=(hintSequence,),
                                                      frames=hint_length, interval=1500, blit=True)
                    animated_hint.save(self.savePath + '/Hint{}.gif'.format(i + 1))

                except Exception as e:
                    print("unable to plot hint {}".format(i + 1))
                    print(e)


if __name__ == "__main__":
    equation = "4*x=4+2*x"
    equationType = 'type3'
    symbol = "x"

    animator = AnimateThreeHints(equation, equationType, symbol)
    animator.animate_hints()
