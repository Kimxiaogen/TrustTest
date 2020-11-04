from model.RoleModel import Role, Role_A, Role_B, Role_C, Role_D, Role_E
from model.RuleModel import Rule
import tensorflow as tf
import os

if __name__ == '__main__':  # 主函数入口 #
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"
    gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
    strategy = tf.distribute.MirroredStrategy()
    with strategy.scope():
        reward = [[[0, 0], [3, -1]], [[-1, 3], [2, 2]]]  # 报酬收益表，2*2数组，数组内容为长度为2的一维数组 #
        players_num = [50, 50, 50, 50, 50]  # 5种玩家组成，长度为5的一维数组 #
        # players_num = [10, 10, 10, 10, 10]  # 5种玩家组成，长度为5的一维数组 #
        epoch = 10  # 每一轮进行比赛局数 #
        max_turns = 50  # 最大轮数 #
        replace = 5  # 每一轮比赛结束后，淘汰replace个最低分玩家，引入replace个最高分玩家 #
        mistake_rate = [0.00, 0.05, 0.10, 0.20, 0.30, 0.50]  # 错误率，范围在0至0.5之间（错误率达到0.5时等同于随机做出选择） #
        for i in range(0, 100):
            for mr in mistake_rate:
                rule = Rule(reward, players_num, epoch, max_turns, replace, mr, sign=i)
                rule.start()
