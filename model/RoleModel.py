class Role:  # 定义游戏角色 #
    def __init__(self, coins):
        self.init_coins = coins
        self.coins = coins
        self.last = None
        self.sort = 0  # 排序 #

    def choose(self):  # 决策方式 #
        pass

    def feedback(self, oppo_choice, coins_change):  # 反馈函数 #
        self.last = oppo_choice  # 记录对手决策 #
        self.coins += coins_change  # 结算硬币收益 #

    def clean(self):  # 清除角色历史数据 #
        self.coins = self.init_coins

    def reset(self):  # 重置角色行为 #
        self.last = None

    def __str__(self):
        return "coins : " + str(self.coins)

    def __repr__(self):
        return "coins : " + str(self.coins)


class Role_A(Role):  # 永远合作 #
    def __init__(self, coins):
        Role.__init__(self, coins)
        self.sort = 1

    def choose(self):
        return 1


class Role_B(Role):  # 永远欺骗 #
    def __init__(self, coins):
        Role.__init__(self, coins)
        self.sort = 2

    def choose(self):
        return 0


class Role_C(Role):  # 首次合作，之后会做出跟对手前一轮一样的选择 #
    def __init__(self, coins):
        Role.__init__(self, coins)
        self.sort = 3

    def choose(self):
        if self.last is None:  # 首次合作 #
            return 1
        else:
            return self.last



class Role_D(Role):  # 永远合作，直到对面欺骗一次后，改为永远欺骗 #
    def __init__(self, coins):
        Role.__init__(self, coins)
        self.sort = 4
        self.corp = True

    def choose(self):
        if self.corp:
            return 1
        else:
            return 0

    def feedback(self, oppo_choice, coins_change):
        Role.feedback(self, oppo_choice, coins_change)
        if self.corp and self.last == 0:
            self.corp = False

    def reset(self):  # 重置角色行为 #
        Role.reset(self)
        self.corp = True

class Role_E(Role):  # 前四次分别合作、欺骗、合作、合作，观察前四次行为，如果存在欺骗，采取角色C行为；反之，采取角色B行为 #
    def __init__(self, coins):
        Role.__init__(self, coins)
        self.corp = True
        self.sort = 5
        self.times = 1

    def choose(self):
        if self.times <= 4:
            if self.times == 2:
                return 0
            else:
                return 1
        elif self.corp:  # 如果不存在欺骗，采取角色B行为 #
            return 0
        else:  # 如果存在欺骗，采取角色C行为 #
            return self.last

    def feedback(self, oppo_choice, coins_change):
        Role.feedback(self, oppo_choice, coins_change)
        if self.times <= 4:
            self.times += 1
            if self.corp:
                self.corp = True if self.last == 1 else False

    def reset(self):  # 重置角色行为 #
        Role.reset(self)
        self.corp = True
        self.times = 1
