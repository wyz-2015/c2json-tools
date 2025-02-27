import sys
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class Shadow_Door():
    def __init__(self):

        self.defaultBreakableArea_X = [-18, 102]
        self.defaultBreakableArea_Y = [-244, 21]

        self.defaultShadowArea_X = [8, 321]
        self.defaultShadowArea_Y = [-244, 41]

        self.pos = [None, None]
        self.dsize = None
        self.xscale = None

    def __sgn__(self, n):
        return (-1 if (n < 0) else 1)

    def set_pos(self, x, y):
        self.pos = [x, y]

    def set_dsize(self, n):
        self.dsize = n

    def set_xscale(self, n):
        self.xscale = n

    def get_breakableAreaRange(self) -> list:
        """
        返回的格式：
        [
        [x1, x2],
        [y1, y2]
        ]
        """
        (xp, yp) = self.pos

        deltaX = [(self.dsize * self.__sgn__(self.xscale) * x)
                  for x in self.defaultBreakableArea_X]
        deltaY = [(self.dsize * y) for y in self.defaultBreakableArea_Y]

        deltaX.sort()
        deltaY.sort()

        return [
            [(x + xp) for x in deltaX],
            [(y + yp) for y in deltaY]
        ]

    def get_shadowAreaRange(self) -> list:
        """
        返回的格式：
        [
        [x1, x2],
        [y1, y2]
        ]
        """
        (xp, yp) = self.pos

        deltaX = [(self.dsize * self.__sgn__(self.xscale) * x)
                  for x in self.defaultShadowArea_X]
        deltaY = [(self.dsize * y) for y in self.defaultShadowArea_Y]

        deltaX.sort()
        deltaY.sort()

        return [
            [(x + xp) for x in deltaX],
            [(y + yp) for y in deltaY]
        ]


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.shadowDoor = Shadow_Door()

        ##################################
        # 标题，兼状态标识
        self.lb1 = QLabel("阴影之门计算器")
        self.setWindowTitle(self.lb1.text())

        ###################################
        # 数据输入
        self.lb_pos1 = QLabel("放置坐标：(")
        self.lineEdit_xp = QLineEdit()
        self.lb_pos2 = QLabel(",")
        self.lineEdit_yp = QLineEdit()
        self.lb_pos3 = QLabel(")")
        layout_pos = QHBoxLayout()
        for widget in (self.lb_pos1, self.lineEdit_xp, self.lb_pos2, self.lineEdit_yp, self.lb_pos3):
            layout_pos.addWidget(widget)

        self.lb_xscale1 = QLabel("xscale：")
        self.lineEdit_xscale = QLineEdit()
        layout_xscale = QHBoxLayout()
        for widget in (self.lb_xscale1, self.lineEdit_xscale):
            layout_xscale.addWidget(widget)

        self.lb_dsize1 = QLabel("dsize：")
        self.lineEdit_dsize = QLineEdit()
        layout_dsize = QHBoxLayout()
        for widget in (self.lb_dsize1, self.lineEdit_dsize):
            layout_dsize.addWidget(widget)

        layout_input = QHBoxLayout()
        for l in (layout_pos, layout_dsize, layout_xscale):
            layout_input.addLayout(l)

        ###################################
        # 结果
        self.lb_separationLine = QLabel(32 * '=')
        self.lb2 = QLabel("格式：\n[x1, x2]\n[y1, y2]\n即：x范围[x1, x2]，y范围[y1, y2]")
        self.lb_breakableResult = QLabel("受击判定区域：")
        self.textEdit_breakableResult = QTextEdit()
        self.lb_shadowResult = QLabel("纯阴影区域：")
        self.textEdit_shadowResult = QTextEdit()

        for te in (self.textEdit_shadowResult, self.textEdit_breakableResult):
            te.setReadOnly(True)

        layout_breakable = QVBoxLayout()
        for widget in (self.lb_breakableResult, self.textEdit_breakableResult):
            layout_breakable.addWidget(widget)
        layout_shadow = QVBoxLayout()
        for widget in (self.lb_shadowResult, self.textEdit_shadowResult):
            layout_shadow.addWidget(widget)

        layout_result = QHBoxLayout()
        for l in (layout_breakable, layout_shadow):
            layout_result.addLayout(l)

        ##################################
        # 控件槽函连接
        for widget in (self.lineEdit_xp, self.lineEdit_yp, self.lineEdit_dsize, self.lineEdit_xscale):
            widget.textChanged.connect(self.calc)

        #################################
        # 控件排布
        layout = QVBoxLayout()
        layout.addWidget(self.lb1)
        layout.addLayout(layout_input)
        layout.addWidget(self.lb_separationLine)
        layout.addWidget(self.lb2)
        layout.addLayout(layout_result)

        self.setLayout(layout)

    ###################################
    # 槽函数区

    def calc(self):
        (xp, yp) = (self.lineEdit_xp.text(), self.lineEdit_yp.text())
        dsize = self.lineEdit_dsize.text()
        xscale = self.lineEdit_xscale.text()
        if (self.__is_int__(xp) and self.__is_int__(yp) and self.__is_float__(dsize) and self.__is_int__(xscale)):
            self.shadowDoor.set_pos(int(xp), int(yp))
            self.shadowDoor.set_dsize(float(dsize))
            self.shadowDoor.set_xscale(int(xscale))

            (bX, bY) = self.shadowDoor.get_breakableAreaRange()
            (sX, sY) = self.shadowDoor.get_shadowAreaRange()

            self.textEdit_breakableResult.setPlainText(
                "{0}\n{1}".format(bX, bY))
            self.textEdit_shadowResult.setPlainText("{0}\n{1}".format(sX, sY))

            self.lb1.setText('<span style="color: green">计算成功</span>')
        else:
            self.lb1.setText(
                '<span style="color: red">无法计算：各输入区域必须输入整数才可计算。(dsize要求为实数即可)</span>')

    def __is_int__(self, n):
        try:
            int(n)
            return True
        except:
            return False

    def __is_float__(self, n):
        try:
            float(n)
            return True
        except:
            return False


if (__name__ == "__main__"):
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
