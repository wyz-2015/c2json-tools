from svg.path import parse_path
import sys
import xml.etree.ElementTree as ET
import pathlib
import pprint
import argparse


class SVG_Analyser():
    def __init__(self):
        self.rawData = []
        self.svgFile = None

        self.tree = None
        self.root = None

    def set_svgFile(self, svgFilePath: str):
        self.svgFile = pathlib.Path(svgFilePath).absolute()
        self.tree = ET.parse(self.svgFile)
        self.root = self.tree.getroot()

    def group_by_color(self):
        group = self.root.findall('.//{http://www.w3.org/2000/svg}path')
        for path in group:
            pathRawData = {"rawData": None, "color": None}
            pathRawData["color"] = path.get("fill")
            pathRawData["rawData"] = path.get("d")
            self.rawData.append(pathRawData)
            # print(i.items())

    def extract_path_points(self):
        for path in self.rawData:
            ###############
            # 分割表达式
            subPathStrs = path["rawData"].split('M')
            subPathStrs = [("M" + subPathStr)
                           for subPathStr in subPathStrs if (subPathStr)]
            ##############
            # 正式分析
            # print(subPathStrs)
            path["pathData"] = []
            oData = [parse_path(subPathStr) for subPathStr in subPathStrs]
            for o in oData:
                pathPoints = []
                for segment in o:
                    if hasattr(segment, 'start'):
                        pathPoints.append(
                            (segment.start.real, segment.start.imag))
                    if hasattr(segment, 'end'):
                        pathPoints.append((segment.end.real, segment.end.imag))
                # path["pathData"].append(pathPoints)
                path["pathData"].append(sorted(set(pathPoints)))

    def generate(self) -> list:
        self.group_by_color()
        self.extract_path_points()

        return self.rawData


def main():
    cmdParser = argparse.ArgumentParser(
        description="自动分析应用了path的svg矢量图文件中，各个多边形的顶点。")
    cmdParser.add_argument("svgFiles", nargs='*')
    args = cmdParser.parse_args()

    # svgFiles = sys.argv[1:]
    svgFiles = args.svgFiles
    outText = []

    pp = pprint.PrettyPrinter(sort_dicts=False)
    for svgFile in svgFiles:
        svg = SVG_Analyser()
        svg.set_svgFile(svgFile)

        resultStr = "\n传入文件：{0}\n======================\n{1:s}".format(
            svg.svgFile, pp.pformat(svg.generate()))
        outText.append(resultStr)

    print('\n'.join(outText))


if (__name__ == "__main__"):
    sys.exit(main())
