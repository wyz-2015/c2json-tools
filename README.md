# c2json-tools

为方便修改steam版《二战前线2》的创意工坊mod的json文件，而编写的一些小工具。

## beautify.py

在创意工坊中直接导出的json文件，其中大量信息糊在一起，不便编辑。此工具用于美化之，方便编辑。同时美化后的文件仍然可以直接导入回创意工坊。

### 帮助信息

```
usage: beautify.py [-h] [-o OUTPATH] [--no_sort_keys] inPath

美化Commando 2输出的json文件，使之更可读。Convert a json file from "Commando 2" to a readable json file.

positional arguments:
  inPath                传入文件路径。Path to input file.

options:
  -h, --help            show this help message and exit
  -o OUTPATH, --outpath OUTPATH
                        输出文件路径。Path to output file.
  --no_sort_keys        不对输出的json作各键排序。Don't sort keys.
```

### 示例(Linux bash shell，Windows下则类比推理可得，下同)

`$ python3 ./beautify.py ~/C2/mod1.json #在本程序目录下调用美化程序，未指定输出路径，将自动在~/C2/下生成一份已美化且自动排序各键的mod1_readable.json文件。`

`$ python3 ./beautify.py ~/C2/mod1.json -o /tmp/114514.json --no_sort_keys #在本程序目录下调用美化程序，指定在/tmp/下生成一份仅作了换行与缩进美化的114514.json文件。`

## de\_compress.py

在`2024-12-16`悄悄放出的的预览版本里，新创建的mod由已压缩数据的形式存在，不能直接查看编辑。此工具用于针对之的压缩与解压缩。

注意：“MY WORKS”的mod数据存在于本地的steam目录下的`userdata/……/3059010/`下，被压缩而变成密文的是这里的文件。通过往常途径，从游戏内导出的json文件则仍然是明文文件，无需解压。

### 帮助信息

```
usage: de_compress.py [-h] [-o OUTPATH] [--raw_json] [--no_sort_keys] command inPath

(解)压缩Commando 2 mod文件的简单工具。A tool for (de)compress Commando 2 mod file.

positional arguments:
  command               命令：压缩(c)/解压缩(d)。command: (c)ompress/(d)ecompress
  inPath                传入的文件路径。Path to input file.

options:
  -h, --help            show this help message and exit
  -o OUTPATH, --outpath OUTPATH
                        输出文件的路径。Path to output file.
  --raw_json            输出不经美化的json文件，仅在解压缩模式有用。Output raw json file. Only available in "d" mode.
  --no_sort_keys        不对输出的json作各键排序，仅在解压缩模式有用。Don't sort keys. Only available in "d" mode.
```
### 示例

`$ python3 ./de_compress.py d ~/C2/mod2 #在本程序目录下调用程序，执行解压缩，未指定输出路径，将自动在~/C2/下生成一份已美化且自动排序各键的mod2_decompressed.json文件。`

`$ python3 ./de_compress.py c ~/C2/mod1.json -o /tmp/1919810.bin #在本程序目录下调用程序，执行压缩，指定在/tmp/下生成一份已压缩的1919810.bin文件。`
