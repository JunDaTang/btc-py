"""
learn from:https://medium.com/@vanflymen/learn-blockchains-by-building-one-117428612f46
"""
import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []

        # 创建一个创世块
        self.new_block(previous_hash = 1, proof = 100)

    def new_block(self, proof, previous_hash = None):
        """
        在区块链上创建一个新区块
        :param proof: <int> 工作证明，它由工作量算法给出的
        :param previous_hash: (Optional) <str> 上一个区块的hash值
        :return: <dict> 新区块
        """

        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : time(),
            'transactions' : self.current_transactions,
            'proof' : proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # 重置当前交易信息链
        self.current_transactions = []

        self.chain.append(block)
        return block


    def new_transaction(self, sender, recipient, amount):
        """
        创建一个新交易信息，并植入到下一个要挖出的区块里，并返回该索引
        :param sender: <str> 发送者地址
        :param recipient: <str> 接收者地址
        :param amount: <int> 数额
        :return: <int> 区块索引，它将拥有这交易信息
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient':recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        # 返回链上的一个最后区块
        return self.chain[-1]


    @staticmethod
    def hash(block):
        """
        # 对一个区块进行 SHA-256 hash加密
        :param block: <dict> 区块
        :return: <str>
        """
        # 我们必须确保字典是有序的，否则会得到一个不一致的hash值
        block_string = json.dumps(block, sort_keys=True).encode()
        return  hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        简单的工作证明算法
        - 找到一个数字 p' 使得 hash(pp') 后的值，拥有前4位数为0000，其中 p 是前一个 p'
        - p 是上一个工作证明， p'是新的工作证明
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof


    @staticmethod
    def valid_proof(last_proof, proof):
        """
        验证工作证明：判断hash(last_proof, proof)后的值是否包含前4位为0000？
        :param last_proof: <int> 前一个工作证明
        :param proof: <int> 当前工作证明
        :return: <bool> true代表判断正确，否则为Flase
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return  guess_hash[:4] == "0000"



# 实例化我们的节点
app = Flask(__name__)

# 给这节点生成一个全局唯一地址
node_identifier = str(uuid4()).replace('-', '')

# 实例化区块链
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    # 我们运行工作证明算法去获取下一个工作证明...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # 找到工作证明，我们需获得一个奖励
    #  发送者为“0”表示这节点已经挖到一个新币了
    blockchain.new_transaction(
        sender='0',
        recipient=node_identifier,
        amount = 1,
    )

    # 通过将其添加到区块链上来制作一个新区块
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "新区块制作",
        'index' : block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash' : block['previous_hash'],
    }
    return jsonify(response), 200



@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # 检查一下几个必要字段是否在Post数据中
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return '缺失值', 400

    # 创建一个新交易
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'交易信息将被添加到区块中，该区块索引为： {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain':blockchain.chain,
        'length':len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)