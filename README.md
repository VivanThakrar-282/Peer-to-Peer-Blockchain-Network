# Peer-to-Peer Blockchain Network

This project implements a basic peer-to-peer blockchain network using Python and Flask. It demonstrates core blockchain concepts such as creating blocks, mining, adding transactions, validating chains, and decentralized node synchronization.

## Features

* **Blockchain Core:** Implements fundamental blockchain functionalities including block creation, hashing, and proof-of-work.
* **Transaction Management:** Allows for adding new transactions (sender, receiver, amount) to the current block.
* **Proof of Work:** A simplified proof-of-work algorithm ensures the integrity and security of the blockchain.
* **Chain Validation:** Verifies the integrity of the entire blockchain by checking block hashes and proofs.
* **Peer-to-Peer Networking:** Enables multiple nodes to connect and synchronize their blockchain, ensuring all participants have the most up-to-date and longest valid chain.
* **RESTful API:** Exposes endpoints via Flask for interacting with the blockchain, such as mining new blocks, adding transactions, connecting nodes, and checking chain validity.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.x
* Flask (`pip install Flask`)
* Requests (`pip install requests`)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Peer-to-Peer-Blockchain-Network.git](https://github.com/YOUR_USERNAME/Peer-to-Peer-Blockchain-Network.git)
    cd Peer-to-Peer-Blockchain-Network
    ```

2.  **Install dependencies:**
    ```bash
    pip install Flask requests
    ```

### Running the Nodes

To simulate a peer-to-peer network, you will need to run multiple instances of the application on different ports.

1.  **Open multiple terminal windows/tabs.**

2.  **Run the first node (e.g., on port 5000):**
    ```bash
    python Peer to Peer Blockchain Network.py
    ```

3.  **Run subsequent nodes on different ports (e.g., 5001, 5002, etc.):**
    You'll need to modify the `app.run` line in `Peer to Peer Blockchain Network.py` for each instance, or ideally, set up a way to pass the port as an argument. For a quick test, you can manually change `port = 5000` to `port = 5001` in a *copy* of the file and run it.

    *Self-correction:* A more robust way would be to pass the port as an argument from the command line. For example, modify the `if __name__ == '__main__':` block to:

    ```python
    if __name__ == '__main__':
        import sys
        port = 5000 # Default port
        if len(sys.argv) > 1:
            try:
                port = int(sys.argv[1])
            except ValueError:
                print("Invalid port number provided. Using default port 5000.")
        app.run(host = '0.0.0.0',port = port)
    ```
    Then you can run:
    ```bash
    python Peer to Peer Blockchain Network.py 5000
    python Peer to Peer Blockchain Network.py 5001
    python Peer to Peer Blockchain Network.py 5002
    ```

## API Endpoints

Once the nodes are running, you can interact with them using the following API endpoints. You can use tools like Postman, Insomnia, `curl`, or your web browser for testing.

### 1. Mine a New Block

* **URL:** `/mine_block`
* **Method:** `GET`
* **Description:** Mines a new block, adding it to the blockchain. This will also clear any pending transactions for the current node into the newly mined block.
* **Example Request (Node on port 5000):**
    ```
    GET [http://127.0.0.1:5000/mine_block](http://127.0.0.1:5000/mine_block)
    ```
* **Example Response:**
    ```json
    {
        "message": "New Block Mined",
        "block": {
            "index": 2,
            "timestamp": 1678886400.0,
            "transaction": [
                {"sender": "wallet_address_A", "receiver": "wallet_address_B", "amount": 10}
            ],
            "proof": 35789,
            "previous_hash": "a1b2c3d4e5f6..."
        }
    }
    ```

### 2. Check Chain Validity

* **URL:** `/is_valid`
* **Method:** `GET`
* **Description:** Checks if the blockchain of the current node is valid.
* **Example Request:**
    ```
    GET [http://127.0.0.1:5000/is_valid](http://127.0.0.1:5000/is_valid)
    ```
* **Example Response:**
    ```json
    {
        "valid": true
    }
    ```

### 3. Add a New Transaction

* **URL:** `/add_transaction`
* **Method:** `POST`
* **Description:** Adds a new transaction to the list of pending transactions. These transactions will be included in the next mined block.
* **Request Body (JSON):**
    ```json
    {
        "sender": "vivan",
        "receiver": "Trisha",
        "amount": 50000000
    }
    ```
* **Example Request:**
    ```
    POST [http://127.0.0.1:5000/add_transaction](http://127.0.0.1:5000/add_transaction)
    Content-Type: application/json

    {
        "sender": "Vivan",
        "receiver": "Trisha",
        "amount": 50000000
    }
    ```
* **Example Response:**
    ```json
    {
        "message": "Transaction added to Block3"
    }
    ```

### 4. Connect New Nodes

* **URL:** `/connect_node`
* **Method:** `POST`
* **Description:** Allows a node to register other nodes in the network. Once registered, nodes can participate in chain synchronization.
* **Request Body (JSON):**
    ```json
    {
        "nodes": [
            "[http://127.0.0.1:5001](http://127.0.0.1:5001)",
            "[http://127.0.0.1:5002](http://127.0.0.1:5002)"
        ]
    }
    ```
* **Example Request:**
    ```
    POST [http://127.0.0.1:5000/connect_node](http://127.0.0.1:5000/connect_node)
    Content-Type: application/json

    {
        "nodes": [
            "[http://127.0.0.1:5001](http://127.0.0.1:5001)",
            "[http://127.0.0.1:5002](http://127.0.0.1:5002)"
        ]
    }
    ```
* **Example Response:**
    ```json
    {
        "message": "Nodes connected successfuly",
        "total_nodes": [
            "127.0.0.1:5001",
            "127.0.0.1:5002"
        ]
    }
    ```

### 5. Replace Chain (Consensus)

* **URL:** `/replace_chain`
* **Method:** `GET`
* **Description:** This endpoint implements the consensus mechanism. It queries all registered nodes for their chains and replaces the current node's chain with the longest valid chain found in the network.
* **Example Request:**
    ```
    GET [http://127.0.0.1:5000/replace_chain](http://127.0.0.1:5000/replace_chain)
    ```
* **Example Response (Chain replaced):**
    ```json
    {
        "message": "chain Replaced"
    }
    ```
* **Example Response (Current chain is longest):**
    ```json
    {
        "message": "Current chain is the longest"
    }
    ```

## Project Structure

* `Peer to Peer Blockchain Network.py`: The main Python script containing the `Blockchain` class and Flask application.

## How it Works (Brief Explanation)

1.  **Blockchain Class:** Manages the core blockchain logic, including:
    * `__init__`: Initializes the blockchain with a genesis block.
    * `create_block`: Adds a new block to the chain.
    * `add_transaction`: Stores pending transactions.
    * `proof_of_work`: Finds a `proof` (nonce) that satisfies the mining difficulty.
    * `is_valid_proof`: Checks if a given `proof` is valid.
    * `hash`: Generates a SHA256 hash of a block.
    * `is_chain_valid`: Verifies the integrity of the entire chain.
    * `add_node`: Registers new nodes in the network.
    * `replace_chain`: Implements the longest chain consensus algorithm.

2.  **Flask App:** Provides the web interface (API) for interacting with the blockchain.

3.  **Mining:** The `mine_block` endpoint performs the proof-of-work, creating a new block that includes any pending transactions.

4.  **Consensus:** The `replace_chain` endpoint ensures that all nodes eventually agree on the same (longest and valid) version of the blockchain. This is crucial for maintaining a decentralized and consistent ledger.
