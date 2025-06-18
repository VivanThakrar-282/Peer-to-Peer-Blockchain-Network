Peer-to-Peer Blockchain Network
This project implements a simple Peer-to-Peer (P2P) Blockchain Network using Flask and Python. It allows nodes to mine blocks, add transactions, validate the blockchain, and sync with other nodes in the network.

Features
Mining Blocks: Proof-of-Work (PoW) mechanism
Transaction Handling: Users can send transactions between nodes
Blockchain Validation: Ensures data integrity
Node Discovery: Connect multiple nodes in the network
Chain Synchronization: Replace the local chain with the longest valid chain in the network
Requirements
Ensure you have Python 3 installed. Then install the dependencies using:

pip install flask requests
Running the Blockchain Node
Run the following command to start a node:

python blockchain.py
The Flask server will start at http://0.0.0.0:5000.

API Endpoints
1. Mine a Block
Endpoint: /mine_block
Method: GET
Description: Mines a new block and adds it to the blockchain.
{
    "message": "New Block Mined!",
    "block": { "index": 2, "timestamp": 1739509356.47, "transactions": [], "proof": 12345, "previous_hash": "xyz" }
}
2. Check Blockchain Validity
Endpoint: /is_valid
Method: GET
Description: Checks if the blockchain is valid.
{
    "valid": true
}
3. Add a Transaction
Endpoint: /add_transaction
Method: POST
Description: Adds a new transaction to the network.
Payload:
{
    "sender": "Alice",
    "receiver": "Bob",
    "amount": 10
}
Response:
{
    "message": "Transaction added to Block 2"
}
4. Connect a New Node
Endpoint: /connect_node
Method: POST
Description: Adds a new node to the network.
Payload:
{
    "nodes": ["http://127.0.0.1:5001"]
}
Response:
{
    "message": "Nodes connected successfully",
    "total_nodes": ["127.0.0.1:5001"]
}
5. Replace the Chain with the Longest One
Endpoint: /replace_chain
Method: GET
Description: Updates the chain if a longer valid chain is found in the network.
{
    "message": "Chain Replaced"
}
Running Multiple Nodes
To simulate a network, start multiple nodes on different ports:

python blockchain.py --port 5001
python blockchain.py --port 5002
Then, connect the nodes using the /connect_node endpoint
