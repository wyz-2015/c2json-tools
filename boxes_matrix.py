import sys
import json
import ast
import copy


class Box():
    """
    父类
    """

    def __init__(self):
        self.defaultSize = [None, None]
        self.defaultCenter = [None, None]
        self.defaultXRange = [None, None]
        self.defaultYRange = [None, None]
        self.objName = None  # 在游戏中的内部名字，比如“object01”。

        self.dictAttrs = {"ammo": 0, "boss": 0, "dsize": 1, "food": 0, "vars": [
            {"key": "inAir", "value": 0}], "xscale": 100}

        ############################
        # 可变的数值
        self.pos = [None, None]
        self.dsize = None
        self.xscale = None
        self.ammoAndFood = None
        self.inAir = None
        self.red = None

    def init_fastSet(self, objMetaData):
        """
        快速设定对象的元参数，应在继承类后紧接使用。
        objMetaData: 可迭代对象，格式为：
        [
            "object04", # objName
            [a, b], # defaultSize
            [c, d], # defaultCenter
            [e, f], # defaultXRange
            [g, h]  # defaultYRange
        ]
        """
        # objMetaData = copy.deepcopy(objMetaData)

        self.defaultSize = objMetaData[1]
        self.defaultCenter = objMetaData[2]
        self.defaultXRange = objMetaData[3]
        self.defaultYRange = objMetaData[4]
        self.objName = objMetaData[0]

    def set_pos(self, x, y):
        self.pos = [x, y]

    def set_dsize(self, dsize):
        self.dsize = dsize
        self.dictAttrs["dsize"] = self.dsize

    def set_xscale(self, xscale):
        """
        这个调了也没用，对于几个盒子对象
        """
        self.xscale = xscale
        self.dictAttrs["xscale"] = self.xscale

    def set_red(self, red):
        self.red = red
        self.dictAttrs["boss"] = self.red

    def set_inAir(self, inAir):
        self.inAir = inAir
        self.dictAttrs["vars"][0]["value"] = self.inAir

    def set_ammoAndFood(self, af: int):
        """
        af: 二进制数。2位，左边一位代表ammo，右边1位代表food。
        """
        self.ammoAndFood = af
        self.dictAttrs["ammo"] = int(bool(self.ammoAndFood & 0b10))
        self.dictAttrs["food"] = int(bool(self.ammoAndFood & 0b01))

    def get_size(self):
        """
        计算当前盒子的大小
        """
        return [abs(self.dsize * i) for i in self.defaultSize]

    def get_xRange(self):
        """
        计算当前盒子的x坐标范围
        """
        x0 = self.pos[0]
        dl = abs(self.dsize * (self.defaultCenter[0] - self.defaultXRange[0]))
        dr = abs(self.dsize * (self.defaultCenter[0] - self.defaultXRange[-1]))

        return [x0 - dl, x0 + dr]

    def get_yRange(self):
        """
        计算当前盒子的y坐标范围
        """
        y0 = self.pos[-1]
        du = abs(self.dsize * (self.defaultCenter[-1] - self.defaultYRange[0]))
        dd = abs(self.dsize *
                 (self.defaultCenter[-1] - self.defaultYRange[-1]))

        return [y0 - dd, y0 + du]

    def __num_is_int__(self, n):
        return n == int(n)

    def __gen_obj_key__(self):
        (x, y) = self.pos
        x = (int(x) if (self.__num_is_int__(x)) else x)
        y = (int(y) if (self.__num_is_int__(y)) else y)

        return "{2:s}>{0}>{1}".format(x, y, self.objName)

    def get_dict(self):
        _d = dict()
        keyName = self.__gen_obj_key__()
        _d[keyName] = self.dictAttrs

        return _d

    def get_pos(self) -> list:
        return self.pos


class WoodenBox(Box):
    """
    木盒子类
    """

    def __init__(self):
        super(WoodenBox, self).__init__()

        self.init_fastSet(
            [
                "object04",
                [40, 30],
                [21, 29],
                [-20, 19],
                [-29, 1]
            ]
        )


class Cursor():
    """
    虚拟光标系统，但是光标位于左上角。
    """

    def __init__(self):
        (self.x, self.y) = (0, 0)
        (self.step_x, self.step_y) = (None, None)
        (self.range_x, self.range_y) = ([None, None], [None, None])

    def set_pos(self, x, y):
        (self.x, self.y) = (x, y)

    def set_step(self, dx, dy):
        (self.step_x, self.step_y) = (dx, dy)

    def set_range(self, Rx: list, Ry: list):
        (self.range_x, self.range_y) = (Rx, Ry)

    def is_final_char(self):
        """
        当前虚拟光标是否到了本行的最后。
        """
        return self.x + self.step_x >= self.range_x[-1]

    def is_final_line(self):
        return self.y + self.step_y >= self.range_y[-1]

    def CR(self):
        self.x = self.range_x[0]

    def LF(self):
        self.y += self.step_y
        self.CR()  # Unix怎么你了

    def next_char(self):
        self.x += self.step_x

    def get_pos(self):
        return (self.x, self.y)


def calc_plant_pos(c: Cursor, templateObj) -> tuple:
    dl = abs(templateObj.defaultCenter[0] * templateObj.dsize)
    du = abs(templateObj.defaultCenter[1] * templateObj.dsize)

    (x, y) = c.get_pos()

    return (x+dl, y+du)


def matrix_draw(templateObj, Rx, Ry) -> list:
    c = Cursor()
    c.set_range(Rx, Ry)
    c.set_pos(Rx[0], Ry[0])
    (dx, dy) = templateObj.get_size()
    c.set_step(dx, dy)
    c.CR()

    matrix = []
    line = []
    while (True):
        obj = copy.deepcopy(templateObj)
        (x, y) = calc_plant_pos(c, templateObj)
        obj.set_pos(x, y)
        line.append(obj)

        if (c.is_final_char()):
            if (c.is_final_line()):
                matrix.append(line.copy())
                break
            else:
                matrix.append(line.copy())
                line.clear()
                c.LF()
        else:
            c.next_char()

    return matrix


def main():
    print("盒子矩阵计算器\n=======================\n\n提示：\n1. 本程序有意不使用命令行传参。如不想手动输入参数，可以考虑利用管道向stdin传值。\n2. 由于游戏实际对于小数的处理很微妙，这里的模拟计算仅仅作估计参考，不代表实际情况。\n")

    (x1, x2) = tuple(ast.literal_eval(i)
                     for i in input("x方向的 起点 终点 (空格分割，单位像素)：").split())
    (y1, y2) = tuple(ast.literal_eval(i)
                     for i in input("y方向的 起点 终点 (空格分割，单位像素)：").split())
    objCode = int(input("填充对象[1(木盒子), ...]："))
    (dsize, inAir, red, af) = tuple(ast.literal_eval(i)
                                    for i in input("盒子长宽放大系数 是否浮空(0/1) 是否变红(0/1) 弹药、食物掉落设定(0/1/2/3)：").split())

    [x_start, x_end] = sorted((x1, x2), reverse=False)
    [y_start, y_end] = sorted((y1, y2), reverse=False)

    match objCode:
        case 1:
            Obj = WoodenBox
        case _:
            sys.exit("(暂)不支持此对象")

    templateObj = Obj()
    templateObj.set_red(red)
    templateObj.set_dsize(dsize)
    templateObj.set_inAir(inAir)
    templateObj.set_ammoAndFood(af)

    objMatrix = matrix_draw(templateObj, [x_start, x_end], [y_start, y_end])
    # print('\n',objMatrix)

    objMatrixDict = dict()
    for line in objMatrix:
        for item in line:
            objMatrixDict.update(item.get_dict())

    print("\n{0}".format(json.dumps(objMatrixDict,
          ensure_ascii=False, indent='\t', sort_keys=False)))


if (__name__ == "__main__"):
    sys.exit(main())
