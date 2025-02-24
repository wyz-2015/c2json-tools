import sys
import json
import ast
import copy

MINE_TEMPLATE = {"xscale": 100}  # 因为xscale修改无用，故写死


class Mine():
    """
    地雷类，用于模拟计算
    """

    def __init__(self, x=0, y=0, dsize=1):
        self.defaultSize = [41, 18]
        self.defaultCenter = [21, 14]
        self.defaultXRange = [-20, 20]
        self.defaultYRange = [-13, 4]
        self.MINE_TEMPLATE2 = copy.deepcopy(MINE_TEMPLATE)

        ############################
        # 可变的数值
        self.pos = [x, y]
        self.dsize = dsize

        self.MINE_TEMPLATE2["dsize"] = self.dsize

    def set_pos(self, x, y):
        self.pos = [x, y]

    def set_dsize(self, dsize):
        self.dsize = dsize
        self.MINE_TEMPLATE2["dsize"] = self.dsize

    def get_size(self):
        """
        计算当前地雷的大小
        """
        return [abs(dsize * i) for i in self.defaultSize]

    def get_xRange(self):
        """
        计算当前地雷的x坐标范围
        """
        x0 = self.pos[0]
        dl = abs(self.dsize * (self.defaultCenter[0] - self.defaultXRange[0]))
        dr = abs(self.dsize * (self.defaultCenter[0] - self.defaultXRange[-1]))

        return [x0 - dl, x0 + dr]

    def get_yRange(self):
        """
        计算当前地雷的y坐标范围
        """
        y0 = self.pos[-1]
        du = abs(self.dsize * (self.defaultCenter[-1] - self.defaultYRange[0]))
        dd = abs(self.dsize *
                 (self.defaultCenter[-1] - self.defaultYRange[-1]))

        return [y0 - dd, y0 + du]

    def __num_is_int__(self, n):
        return n == int(n)

    def __gen_mine_key__(self):
        (x, y) = self.pos
        x = (int(x) if (self.__num_is_int__(x)) else x)
        y = (int(y) if (self.__num_is_int__(y)) else y)

        return "enemy06>{0}>{1}".format(x, y)

    def get_dict(self):
        _d = dict()
        keyName = self.__gen_mine_key__()
        _d[keyName] = self.MINE_TEMPLATE2

        return _d


def domino_check(minesList: list) -> bool:
    (mine1, mine2) = minesList[: 1 + 1]

    (x1, x2) = mine1.get_xRange()
    (x3, x4) = mine2.get_xRange()

    cond_x = (x2 < x3) or (x4 < x1)

    (y1, y2) = mine1.get_yRange()
    (y3, y4) = mine2.get_yRange()

    cond_y = (y2 < y3) or (y4 < y1)

    return (not (cond_x or cond_y))


def main():
    print("线性地雷计算器\n=======================\n\n提示：\n1. 本程序有意不使用命令行传参。如不想手动输入参数，可以考虑利用管道向stdin传值。\n2. 由于游戏实际对于小数的处理很微妙，这里的模拟计算仅仅作估计参考，不代表实际情况。\n")

    (x_start, x_end) = tuple(ast.literal_eval(i)
                             for i in input("x方向的 起点 终点 (空格分割，单位像素)：").split())
    (y_start, y_end) = tuple(ast.literal_eval(i)
                             for i in input("y方向的 起点 终点 (空格分割，单位像素)：").split())
    dsize = ast.literal_eval(input("地雷长宽放大系数："))
    n_mines = int(input("地雷数："))

    if (n_mines > 1):
        dx = (x_end - x_start) / (n_mines - 1)
        dy = (y_end - y_start) / (n_mines - 1)

        (x, y) = (x_start, y_start)

        minesDict = dict()
        minesList = []
        while (x <= x_end and y <= y_end):
            # minesDict[gen_mine_key(x, y)] = MINE_TEMPLATE
            minesList.append(Mine(x, y, dsize))

            x += dx
            y += dy

        for mine in minesList:
            minesDict.update(mine.get_dict())

        outputText = ["\n提示："]
        if (domino_check(minesList)):
            outputText.append("这样的参数下，地雷可能 可以 连续引爆")
        else:
            outputText.append("这样的参数下，地雷可能 无法 连续引爆")

        print(
            json.dumps(minesDict, ensure_ascii=False,
                       indent='\t', sort_keys=False),
            '\n'.join(outputText)
        )

    elif (n_mines == 1):
        keyName = "enemy06>{0}>{1}".format(
            (x_start + x_end) / 2, (y_start + y_end) / 2)
        mineTemplate3 = copy.deepcopy(MINE_TEMPLATE)
        mineTemplate3["dsize"] = dsize

        mineDict = {keyName: mineTemplate3}
        print(json.dumps(mineDict, ensure_ascii=False, indent='\t', sort_keys=False),
              "\n提示：\n只放一个地雷有使用本程序的必要吗？(恼)"
              )

    else:
        sys.exit("指定的地雷数不合理")


if (__name__ == "__main__"):
    sys.exit(main())
