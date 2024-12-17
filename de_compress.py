import json
import sys
import pathlib
import argparse
import zlib


def main():
    ######################
    # 命令行参数引入
    cmdParser = argparse.ArgumentParser(
        description="(解)压缩Commando 2 mod文件的简单工具。A tool for (de)compressing Commando 2 mod file.")
    cmdParser.add_argument("command",
                           help="命令：压缩(c)/解压缩(d)。command: (c)ompress/(d)ecompress")
    cmdParser.add_argument("inPath", help="传入的文件路径。Path to input file.")
    cmdParser.add_argument("-o", "--outpath", required=False, dest="outPath",
                           default=None, help="输出文件的路径。Path to output file.")
    cmdParser.add_argument("--raw_json", action="store_true",
                           help="输出不经美化的json文件，仅在解压缩模式有用。Output raw json file. Only available in \"d\" mode.")
    cmdParser.add_argument("--no_sort_keys", dest="no_sort_keys",
                           action="store_false", help="不对输出的json作各键排序，仅在解压缩模式有用。Don't sort keys. Only available in \"d\" mode.")

    ###################################
    # 变量们
    args = cmdParser.parse_args()
    inPath = pathlib.Path(args.inPath).absolute()
    inDir = inPath.parent
    inFileStem = inPath.stem
    command = args.command.lower()
    raw_json = args.raw_json
    no_sort_keys = args.no_sort_keys

    ##############################
    # 指定的命令不正确
    if (command != "c" and command != "d"):
        print("指定的命令“{0:s}”不正确。".format(command))
        cmdParser.print_help()
        return 1

    ################################
    # 打开文件指针
    match command:
        case "c":
            inFile = open(str(inPath), "rt")
        case "d":
            inFile = open(str(inPath), "rb")

    ##################################
    # 目录自动处理
    outPath = args.outPath
    if (not outPath):
        match command:
            case "c":
                outFileName = "{0:s}_compressed.bin".format(inFileStem)
            case "d":
                outFileName = "{0:s}_decompressed.json".format(inFileStem)

        outPath = inDir / outFileName

    #####################################
    # 处理
    match command:
        case "c":
            data = json.load(inFile)
            data = json.dumps(data, ensure_ascii="False")
            data = data.encode()
            data = zlib.compress(data)

            outFile = open(outPath, "wb")
            outFile.write(data)
        case "d":
            data = inFile.read()
            data = zlib.decompress(data)
            data = json.loads(data)

            outFile = open(outPath, "wt")
            jsonOption = None if (raw_json) else "\t"
            json.dump(data, outFile, ensure_ascii=False,
                      indent=jsonOption, sort_keys=no_sort_keys)

    inFile.close()
    outFile.close()


if (__name__ == "__main__"):
    sys.exit(main())
