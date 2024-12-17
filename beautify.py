import json
import sys
import argparse
import pathlib


def __convert__(inFile, outFile, sk):
    data = json.load(inFile)
    json.dump(data, outFile, indent="\t", ensure_ascii=False, sort_keys=sk)


def main():
    cmdParser = argparse.ArgumentParser(
        description="美化Commando 2输出的json文件，使之更可读。Convert a json file from \"Commando 2\" to a readable json file.")
    cmdParser.add_argument("inPath")
    cmdParser.add_argument(
        "-o", "--outpath", dest="outPath", required=False, default=None)
    cmdParser.add_argument("--no_sort_keys", dest="no_sort_keys",
                           action="store_false", help="不对输出的json作键名排序。Don't sort keys.")

    args = cmdParser.parse_args()
    inPath = pathlib.Path(args.inPath).absolute()
    inDir = inPath.parent
    inFileStem = inPath.stem
    sk = args.no_sort_keys

    if (args.outPath):
        outPath = args.outPath
    else:  # 若未指定输出路径，则自动在与输入文件同一目录下创建 原文件名+“_readable”+“.json" 文件，并写入数据。
        outFileName = "{0:s}_readable.json".format(inFileStem)
        # outPath = "{0:s}/{1:s}".format(str(inDir), outFileName)
        outPath = inDir / outFileName

    inFile = open(inPath, "rt")
    outFile = open(outPath, "wt")

    __convert__(inFile, outFile, sk)

    inFile.close()
    outFile.close()


if (__name__ == "__main__"):
    sys.exit(main())
