import json
import time
from hashlib import sha256


class Block:
    def __init__(self, timestamp, data, index, nonce, previous_hash=None):
        self.index = index
        self.timestamp = timestamp or time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.difficulty = 7
        self.hash = self.calculate_hash()

    def __repr__(self):
        return json.dumps(self.__dict__, indent=4)

    def calculate_hash(self):
        hash = sha256()
        hash_str = (str(self.index) + str(self.previous_hash) + str(self.timestamp) + self.data + str(self.nonce)).encode("utf-8")
        hash.update(hash_str)
        return hash.hexdigest()

    def mine(self):
        seq = fibonacci_sequence(self.difficulty)
        while seq not in str(int(self.hash, 16)):  #проверяем, содержит ли хеш посчитанный ряд
            self.nonce += 1
            self.hash = self.calculate_hash()
        return


# возвращает строку, состояющую из n чисел ряда фибоначчи, начиная с 1
# например, при n = 6: 112358; n = 8: 1123581321
def fibonacci_sequence(n: int):
    fib_str = "11"
    digit = 1
    previous_digit = 1
    for i in range(n - 2):
        fib_str += str(previous_digit + digit)
        previous_digit, digit = digit, previous_digit + digit

    return fib_str


class BlockChain:
    def __init__(self):
        self.chain = [get_genesis_block()]

    def get_last_block(self):
        return self.chain[len(self.chain) - 1]

    def add_block(self, block: Block):
        block.mine()
        if is_valid_new_block(block, self.get_last_block()):
            self.chain.append(block)


# вспомогательные функции
def is_valid_new_block(new_block, previous_block) -> bool:
    if previous_block.index + 1 != new_block.index:
        return False
    elif previous_block.hash != new_block.previous_hash:
        return False
    elif Block.calculate_hash(new_block) != new_block.hash:
        return False
    return True


def generate_new_block(chain: BlockChain, data: str, nonce=0) -> Block:
    previous_block = chain.get_last_block()
    index = previous_block.index + 1
    timestamp = time.time() / 1000
    return Block(timestamp=timestamp, data=data, index=index, nonce=nonce, previous_hash=previous_block.hash)


def get_genesis_block():
    return Block(timestamp=1682839690, data="first block", index=0, previous_hash="0", nonce=0)
