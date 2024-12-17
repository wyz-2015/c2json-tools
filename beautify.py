import json
import sys
import argparse
import pathlib


def __convert__(inFile, outFile):
    data = json.load(inFile)
    json.dump(data, outFile, indent="\t", ensure_ascii=False)


def main():
    cmdParser = argparse.ArgumentParser(
        description="Convert a json file from \"Commando 2\" to a readable json file.")
    cmdParser.add_argument("inPath")
    cmdParser.add_argument(
        "-o", "--outpath", dest="outPath", required=False, default=None)

    args = cmdParser.parse_args()
    inPath = pathlib.Path(args.inPath).absolute()
    inDir = inPath.parent
    inFileStem = inPath.stem

    if (args.outPath):
        outPath = args.outPath
    else:  # 若未指定输出路径，则自动在与输入文件同一目录下创建 原文件名+“_readable”+“.json" 文件，并写入数据。
        outFileName = "{0:s}_readable.json".format(inFileStem)
        outPath = "{0:s}/{1:s}".format(str(inDir), outFileName)

    inFile = open(inPath, "rt")
    outFile = open(outPath, "wt")

    __convert__(inFile, outFile)

    inFile.close()
    outFile.close()


if (__name__ == "__main__"):
    sys.exit(main())
