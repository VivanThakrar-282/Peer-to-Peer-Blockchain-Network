import hashlib
import json
import time
from flask import Flask, jsonify, request
from urllib.parse import urlparse
import requests

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transaction = []
        self.nodes = set()
        self.create_block(proof = 1 ,previous_hash = '0')

    def create_block(self, proof, previous_hash):
        block = {
            'index' : len(self.chain)+1,
            'timestamp' : time.time(),
            'transaction' : self.transaction,
            'proof' : proof,
            'previous_hash' : previous_hash
        }
        self.transaction =[]
        self.chain.append(block)
        return block
    
    def add_transaction(self, sender, receiver, amount):
        self.transaction.append({'sender': sender, 'receiver': receiver, 'amount': amount})
        return self.chain[-1]['index']+1
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        while not self.is_valid_proof(self, previous_proof, new_proof):
            new_proof +=1
        return new_proof
    
    def is_valid_proof(self, previous_proof, new_proof):
        guess = f"(previous_proof)(new_proof)".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] =="000"
    
    def hash(self, block):
        return hashlib.sha256(json.dumps(block, sort_keys= True).encode()).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        for i in range(1,len(chain)):
            block = chain[i]
            if block ["prvious_hash"] != self.hash(previous_block):
                return False
            if not self.is_valid_proof(previous_block["proof"], block["proof"]):
                return False
            previous_block = block
        return True

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        longest_chain = None
        max_length = len(self.chain)

        for node in self.nodes:
            response = requests.get(f"http://{node}/get_chain")
            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True
        return False

# Flask app setup
app = Flask(__name__)
Blockchain = Blockchain()

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = Blockchain.get_previous_block()
    proof = Blockchain.proof_of_work(previous_block["proof"])
    previous_hash = Blockchain.hash(previous_hash)
    block = Blockchain.create_block(proof, previous_hash)
    response = {"message": "New Block Mined", "block": block}
    return jsonify (response), 200

@app.route('/is_valid',methods = ['GET'])
def is_valid():
    response = {
        "valid": Blockchain.is_chain_valid(Blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    data = request.get_json()
    require_fields = ["sender","receiver","amount"]

    if not all(field in data for field in require_fields):
        return jsonify({"message":"Missing Transaction Data"},400)
        
    index = Blockchain.add_transaction(data["sender"], data["receiver"],data["amount"])

    return jsonify({"message":f"Transaction added to Block{index}"}), 201

@app.route('/connect_node',methods = ['POST'])
def connect_node():
    data = request.get_json()
    nodes = data.get("nodes")

    if not nodes:
        return jsonify({"message": "NO Nodes Provides"}), 400

    for node in nodes:
        Blockchain.add_node(node)

    return jsonify({
        "message": "Nodes connected successfuly",
        "total_nodes": list(Blockchain.nodes)
        }), 201

@app.route('/replace_chain',methods = ['GET'])
def replace_chain():
    replaced = Blockchain.replace_chain()
    response = {
        "message":"chain Replaced" if replaced else "Current chain is the longest"
    }
    return jsonify(response),200

# Run the Flask App
if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 5000)
    