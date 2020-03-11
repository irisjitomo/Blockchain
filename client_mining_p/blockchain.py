import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = [] # we have a chain which is a list
        self.current_transactions = [] # we have a list of current_transactions

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100) # this will create the genesis block

    def new_block(self, proof, previous_hash=None): # making a NEW BLOCK with the `proof` and `prev_hash` as parameters
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = { # were making a new block in the form of a dictionary to store it in the `self.chain` list
            'index': len(self.chain) + 1, # for every new block, the index must be longer than the len(self.chain) by 1
            'timestamp': time(),
            'transactions' : self.current_transactions,
            'proof': proof, # the proof is the proof param
            'previous_hash' : previous_hash or self.hash(self.chain[-1]) # self.hash(self.chain[-1]) will hash the LAST item in the `self.chain` list
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the block to the chain
        self.chain.append(block) # appends to the self.chain
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        string_block = json.dumps(block, sort_keys=True) # block is the block dictionary we created # sort_keys lets everything be in order in the block dictionary
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        raw_hash = hashlib.sha256(string_block.encode()) # making a `raw_hash` var which sha256 hashes the `string_block` var and we need to use .encode()
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes
        hex_hash = raw_hash.hexdigest() # .hexdigest() makes it into a hexadecimal format string

        # TODO: Create the block_string

        # TODO: Hash this string using sha256

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1] # returns the LAST block [-1]

    # def proof_of_work(self, block):
    #     """
    #     Simple Proof of Work Algorithm
    #     Stringify the block and look for a proof.
    #     Loop through possibilities, checking each one against `valid_proof`
    #     in an effort to find a number that is a valid proof
    #     :return: A valid proof for the provided block
    #     """
    #     block_string = json.dumps(block, sort_keys=True) # we need json.dumps to convert json to string # sort_keys is needed to make sure the object/dictionary is in order
    #     proof = 0 # proof
    #     while self.valid_proof(block_string, proof) is False: # checks to see if valid_proof is True
    #         proof += 1 # if not it increments proof by 1
    #     return proof

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string + proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # TODO
        guess = f"{block_string}{proof}".encode() # `guess` var which encode()'s
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:3] == '000' # sees if theres 3 LEADING zeroes in the hash. It returns TRUE in the proof_of_work


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()
    if 'proof' not in data and 'id' not in data:
        response = {
            'message': "unsuccessful"
        }
        return jsonify(response), 400
    proof = data['proof']
    miner_id = data['id']
    block_string = json.dumps(blockchain.last_block, sort_keys=True)

    if blockchain.valid_proof(block_string, proof):

        previous_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.new_block(proof, previous_hash)
        response = {
            'message' : 'New Block Forged',
            'index' : block['index'],
            'transactions' : block['transactions'],
            'proof' : block['proof'],
            'previous_hash': block['previous_hash']
        }
        return jsonify(response), 200
    else:
        response = {
            'message': "unsuccessful"
        }
        return jsonify(response), 400


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/last_block', methods=['GET'])
def last_block():
    response = {
        'last_block' : blockchain.last_block,
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

