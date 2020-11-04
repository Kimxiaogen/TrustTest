from model.RoleModel import Role, Role_A, Role_B, Role_C, Role_D, Role_E
import random as rd
import copy
import writeToCSV


def getSort(role):  # 返回排序字段sort #
    return role.sort


def getCoins(role):  # 返回排序字段coins #
    return role.coins


class Rule:  # 定义游戏规则 #
    def __init__(self, reward, players_num, epoch, max_turns, replace, mistake_rate, sign):
        self.reward = reward  # 报酬收益表，2*2数组，数组内容为长度为2的一维数组 #
        self.players_num = players_num  # 5种玩家组成，长度为5的一维数组 #
        self.epoch = epoch  # 每一局进行比赛轮数 #
        self.max_turns = max_turns  # 最大局数 #
        self.replace = replace  # 每一局比赛结束后，淘汰replace个最低分玩家，引入replace个最高分玩家 #
        self.mistake_rate = mistake_rate  # 错误率，范围在0至1之间 #
        self.roles = []  # 参与的角色集合 #
        self.total_num = sum(players_num)  # 参与总人数 #
        self.data = []  # 输出数据 #
        self.sign = sign

    def compute(self, choice_a, choice_b):  # 计算决策结果 #
        reward_array = self.reward[choice_a][choice_b]  # 得到奖励数组 #
        coin_a = reward_array[0]
        coin_b = reward_array[1]
        return coin_a, coin_b

    def play(self, a, b):  # 角色a与角色b进行一轮游戏 #
        choose_a = self.mistake(a.choose())
        choose_b = self.mistake(b.choose())
        coin_a, coin_b = self.compute(choose_a, choose_b)
        a.feedback(choose_b, coin_a)
        b.feedback(choose_a, coin_b)

    def playForNum(self, a, b, num):  # 角色a与角色b进行N轮游戏 #
        for i in range(num):
            self.play(a, b)

    def mistake(self, choice):  # 按照错误率，随机改变角色选择 #
        rand = rd.random()
        if rand < self.mistake_rate:  # 发生错误时，改变choice #
            choice = 1 if choice == 0 else 0
        return choice

    def show(self):  # 打印角色情况 #
        print("角色A\t角色B\t角色C\t角色D\t角色E\n")
        arr = []
        for num in self.players_num:
            arr.append(num)
            print(str(num) + "\t\t", end='')
        print()
        self.data.append(arr)

    def updatePlayersNum(self):  # 更新角色数量 #
        self.players_num = [0, 0, 0, 0, 0]
        for r in self.roles:
            self.players_num[r.sort - 1] += 1

    def addPlayers(self):  # 构造参与玩家 #
        coins = 0  # 初始硬币数 #
        for n in range(self.players_num[0]):
            r = Role_A(coins)
            self.roles.append(r)
        for n in range(self.players_num[1]):
            r = Role_B(coins)
            self.roles.append(r)
        for n in range(self.players_num[2]):
            r = Role_C(coins)
            self.roles.append(r)
        for n in range(self.players_num[3]):
            r = Role_D(coins)
            self.roles.append(r)
        for n in range(self.players_num[4]):
            r = Role_E(coins)
            self.roles.append(r)

    def initPlayers(self):  # 重置所有玩家 #
        for r in self.roles:
            r.clean()
        self.roles.sort(key=getSort)  # 排序 #

    def replaceFailers(self):  # 用最高分玩家替换最低分玩家 #
        self.roles.sort(key=getCoins)  # 按照硬币数排序 #
        winner = self.roles[self.total_num - 1]  # 找到硬币最多的玩家 #
        loser = self.roles[0].coins  # 最低分 #
        # 移除5名最低分玩家（若有多余5名最低分玩家，随机挑选5位移除） #
        if loser == self.roles[self.replace - 1].coins:  # 多余5位 #
            remove_list = []
            for i in range(len(self.roles)):
                if loser == self.roles[i].coins:
                    remove_list.append(i)
            max = len(remove_list)
            for n in range(self.replace):
                rand = rd.randrange(0, max, 1)
                self.roles[remove_list[rand]] = copy.deepcopy(winner)
        else:  # 少于或等于5位 #
            for r in range(self.replace):
                self.roles[r] = copy.deepcopy(winner)

    def start(self):  # 游戏开始 #
        self.addPlayers()
        path = './result/mistake_rate_' + str(self.mistake_rate) + '_' + str(self.sign) + '.csv'
        for m in range(self.max_turns):  # 每一局，每个玩家与其他所有玩家都要进行比赛 #
            self.initPlayers()
            self.show()
            for gap in range(1, self.total_num):  # 每个玩家之间进行epoch轮比赛 #
                index = 0
                curr = self.total_num - gap
                while index + curr < self.total_num:
                    a = self.roles[index]
                    b = self.roles[index + curr]
                    self.playForNum(a, b, self.epoch)
                    index += 1
                    a.reset()
                    b.reset()
            self.replaceFailers()
            self.updatePlayersNum()
        writeToCSV.writecsvByName(self.data, path)
