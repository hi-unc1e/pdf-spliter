# PDF Splitter

一个强大的命令行工具，用于智能分割大型 PDF 文件。
## 需求
- 分割 PDF 文件：将一个大的 PDF 文件分割成多个小文件。
- 自定义每部分的最大页数：允许用户指定每个分割后文件的最大
页数，默认为 250 页。
- 自定义每部分的最大文件大小：允许用户指定每个分割后文件的
最大大小，默认为 9MB。
-确保每个拆分后的文件既不超过指定的页数也不超过指定的大
小：即每个文件的页数不能超过用户指定的最大页数，同时文件大
小也不能超过用户指定的最大文件大小。
- 命令行界面（CLI）：程序应接受命令行参数，包括输入文件路
径、输出目录、输出文件前缀、每部分的最大页数和最大文件大
小。
- 使用常见 PDF 库：使用一个较为成熟的 PDF 库来处理 PDF 
文件。

## 功能特点

- 将大型 PDF 文件分割成多个较小的文件
- 支持自定义每个分割文件的最大页数和最大文件大小
- 智能拆分：确保每个输出文件既不超过指定页数，也不超过指定大小
- 多进程处理，提高分割速度
- 简单易用的命令行界面

## 使用方法

```bash
python splitor.py <input_file> [options]
```

### 选项

- `--output-dir <dir>`: 指定输出目录（默认：'splited'）
- `--output-prefix <prefix>`: 指定输出文件前缀（默认：'s'）
- `--max-pages <num>`: 设置每个输出文件的最大页数（默认：250）
- `--max-size <size>`: 设置每个输出文件的最大大小，单位为字节（默认：9MB）

### 示例

```bash
python splitor.py large_document.pdf --max-pages 100 --max-size 5000000
```

## 依赖

- Python 3.6+
- pymupdf

## 安装

1. 克隆此仓库
2. 安装依赖：`pip install pymupdf`

## 注意事项

- 处理大型 PDF 文件时可能需要较长时间
- 确保有足够的磁盘空间存储输出文件

## 贡献

欢迎提交问题和拉取请求！

## 许可

[Apache License 2.0](LICENSE)
