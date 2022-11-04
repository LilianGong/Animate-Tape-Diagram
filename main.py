import re

import animateByType

storePath = r'''animations/{}'''


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # questionDict = {'type1': ['x+2=6', '2+x=7', '7=4+x'],
    #                 'type2': ['2*x+1=5', '4*x+1=13', '20=8+2*x'],
    #                 'type3':  ['6*x=2*x+8', '7*x=4*x+9', '9*x=7*x+14'],  # ['5*x=2*x+15', 'x+9=4*x', '8*x=2*x+12'] +
    #                 'type4': ['5*x+4=2*x+19', 'x+10=4*x+1', '8*x+1=2*x+13']}

    questionDict = {'type1': ['n+14=25', 'p+8=18', 'm+108=243', 'q+18=22', 'r+10=22', 'r+5=15', 'x+9=16',
                              'x+3=9',  '3+x=9'],
                    'type3': ['5*x=35', '4*x=28', '3*x=9', '9=3*x', 'x + x + x = 9'],
                    'type5': ['m-7=17', 'g-62=14', 'p-21=34', 'r-15=5', 'r-18=14', 'x=9-3'],
                    'type6': ['x = 9 / 3']}

    # questionDict = {'type1': ['x+2=6']}

    for quesType in questionDict.keys():
        if quesType in ["type1", "type3"]:
            for question in questionDict[quesType]:
                print("now animating {}...".format(question))
                quesSymbol = re.findall(r"[a-zA-Z]", question)
                assert len(set(quesSymbol)) == 1, print("no symbol or multiple symbols found!", quesSymbol)
                animator = animateByType.AnimateThreeHints(question, quesType, quesSymbol[0])
                animator.animate_hints()


