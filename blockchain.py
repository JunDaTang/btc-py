"""
银行记帐
开帐号：记录个人信息，帐号为123
转帐：帐号123转给另帐号573，100块
记录到银行帐本系统中
区块链比特币
开帐号：func(私钥abc) -> 付款方地址123
转帐：sigh(交易信息,签名) -> 交易签名结果
交易信息：付款方地址123转给收款方地址573，100块
签名：私钥abc
广播给其他节点
节点验证：verity(交易签名结果,付款方地址)
"""
class Blockchain(object):
    def __init__(self):
        pass

    def new_block(self):
        # 创建一个区块并将它添加到区块链上
        pass


    def new_transaction(self):
        # 添加一个新交易到交易链上
        pass

    @staticmethod
    def hash(self):
        # hash加密一个区块
        pass

    @property
    def last_block(self):
        # 返回链上的一个最后区块
        pass