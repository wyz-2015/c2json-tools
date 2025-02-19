import sys
import json

MINE_TEMPLATE = {"xscale": 100}


def num_is_int(n):
    return n == int(n)


def gen_mine_key(x, y):
    x = (int(x) if (num_is_int(x)) else x)
    y = (int(y) if (num_is_int(y)) else y)

    return "enemy06>{0}>{1}".format(x, y)


def main():
    print("线性地雷生成器\n=======================")

    (x_start, x_end) = tuple(int(i)
                             for i in input("x方向的 起点 终点 (空格分割，单位像素)：").split())
    (y_start, y_end) = tuple(int(i)
                             for i in input("y方向的 起点 终点 (空格分割，单位像素)：").split())
    n_mines = int(input("地雷数："))

    if (n_mines > 1):
        dx = (x_end - x_start) / (n_mines - 1)
        dy = (y_end - y_start) / (n_mines - 1)

        (x, y) = (x_start, y_start)

        minesDict = dict()
        while (x <= x_end and y <= y_end):
            minesDict[gen_mine_key(x, y)] = MINE_TEMPLATE

            x += dx
            y += dy

        print(json.dumps(minesDict, ensure_ascii=False,
              indent='\t', sort_keys=False))

    elif (n_mines == 1):
        mineDict = {gen_mine_key(
            ((x_start + x_end) / 2), ((y_start + y_end) / 2)): MINE_TEMPLATE}
        print(json.dumps(mineDict, ensure_ascii=False, indent='\t', sort_keys=False))
    
    else:
        sys.exit("指定的地雷数不合理")


if (__name__ == "__main__"):
    sys.exit(main())
