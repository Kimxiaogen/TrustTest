import matplotlib.pyplot as plot
import numpy as np
import loadData as ld
if __name__ == '__main__':
    mistake_rate = [0.00, 0.05, 0.10, 0.20, 0.30, 0.50]
    linestyles = ['-', '--', '-.', ':', '-']
    labels = ['A', 'B', 'C', 'D', 'E']
    x = np.arange(0, 50, 1)  # 横坐标 #
    for mr in mistake_rate:
        path = './result/mistake_rate_' + str(mr) + '.csv'
        data = ld.load(path)
        y_arr = np.asmatrix(data, dtype=np.float32).T  # 转置数据 #
        for y, l, s in zip(y_arr, labels, linestyles):
            plot.plot(x, y.T, label=l, linestyle=s)
        plot.title(str(mr))
        plot.legend()
        plot.show()
