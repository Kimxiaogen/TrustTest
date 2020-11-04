import numpy as np
import loadData as ld
import writeToCSV as wc

if __name__ == '__main__':
    # path = './result/mistake_rate_0.0.csv'
    # data = ld.load(path)
    # matrix = np.asmatrix(data, dtype=float)
    # print(matrix)
    result_path = './result/mistake_rate_'
    mistake_rate = ['0.0', '0.05', '0.1', '0.2', '0.3', '0.5']
    for mr in mistake_rate:
        maxtrix = np.zeros([50, 5], dtype=float)
        max_iter = 100
        file = result_path + mr + '.csv'
        for i in range(0, max_iter):
            path = result_path + mr + '_' + str(i) + '.csv'
            data = ld.load(path)
            maxtrix += np.asmatrix(data, dtype=float)
        maxtrix /= max_iter
        wc.writecsvByName(maxtrix, file)
