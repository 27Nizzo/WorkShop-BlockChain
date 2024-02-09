import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 5

        self.new_block(previous_hash="The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.", proof=100)

    # Método property
    def last_block(self):
        return self.chain[-1]

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        return self.last_block()['index'] + 1

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            proof_string = str(new_proof**2 - previous_proof**2 - previous_proof**2).encode()
            raw_hash = hashlib.sha256(proof_string)
            hex_hash = raw_hash.hexdigest()

            if hex_hash[:self.difficulty] == '0' * self.difficulty:
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def is_chain_valid(self, chain): 
        previous_block = chain[0]
        block_index = 1 

        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            proof_string = str(proof**2 - previous_proof**2).encode()
            raw_hash = hashlib.sha256(proof_string)
            hex_hash = raw_hash.hexdigest()
            if hex_hash[:self.difficulty] != '0' * self.difficulty:
                return False 
            previous_block = block
            block_index += 1
        return True
    
    def mine_block(self):
        previous_block = self.last_block
        previous_proof = previous_block['proof']
        proof = blockchain.proof_of_work(previous_proof)
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.new_block(proof, previous_hash)

        response = {
            'message': 'A block is MINED',
            'index': block['index'],
            'timestamp': block['timestamp'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']
        }

        return response 




# Testando
blockchain = Blockchain()
t1 = blockchain.new_transaction("Satoshi", "Mike", '5 BTC')
t2 = blockchain.new_transaction("Mike", "Satoshi", '1 BTC')
t3 = blockchain.new_transaction("Satoshi", "Hal Finney", '5 BTC')
blockchain.new_block(12345)

t4 = blockchain.new_transaction("Mike", "Alice", '1 BTC')
t5 = blockchain.new_transaction("Alice", "Bob", '0.5 BTC')
t6 = blockchain.new_transaction("Bob", "Mike", '0.5 BTC')
blockchain.new_block(6789)

print("Blockchain:")
print(json.dumps(blockchain.chain, indent=4, sort_keys=True))