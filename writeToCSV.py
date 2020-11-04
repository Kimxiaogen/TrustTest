import numpy as np
import os

# 指定分隔符写入csv文件 #
def writecsvByNameWithDelimiter(data, fileName, delimiter):
    # 保存为csv文件
    if os.path.exists(fileName):
        os.remove(fileName)
    np.savetxt(fileName, data, delimiter=delimiter, fmt='%s', encoding='utf-8-sig')

# 根据数据集和文件名写入csv文件 #
def writecsvByName(data, fileName):
    writecsvByNameWithDelimiter(data, fileName, ',')


# 根据数据集和源文件写入csv文件 #
def writecsvByFile(data, sourceFile):
    # 获取文件名
    start = sourceFile.rindex('\\')
    end = sourceFile.index('.', start)
    fileName = sourceFile[start + 1: end] + '.csv'

    writecsvByName(data, fileName)
