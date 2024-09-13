# 21BCT0097 ISHANK BHATNAGAR

import json
from web3 import Web3, HTTPProvider
# import RPi.GPIO as GPIO # Uncomment this for real Raspberry Pi hardware
from RPiSim.GPIO import GPIO
from flask import Flask, render_template

# Pin mapping: Maps human-readable pin names to GPIO numbers
pin_mapping = {
    'fourteen': 14,
    'fifteen': 15,
    'eighteen': 18,
    'twentythree': 23,
    'twentyfour': 24,
    'twentyfive': 25,
    'eight': 8,
    'seven': 7,
    'twelve': 12,
    'sixteen': 16,
    'twenty': 20,
    'twentyone': 21,
    'two': 2,
    'three': 3,
    'four': 4,
    'seventeen': 17,
    'twentyseven': 27,
    'twentytwo': 22,
    'ten': 10,
    'nine': 9,
    'eleven': 11,
    'five': 5,
    'six': 6,
    'thirteen': 13,
    'nineteen': 19,
    'twentysix': 26
}

# Set up GPIO pins: Configure GPIO pins for output
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pinList = list(pin_mapping.values())
for pin in pinList:
    GPIO.setup(pin, GPIO.OUT)  # Initialize each pin as an output pin

# Load contract artifacts: Read ABI and bytecode from the contract artifacts file
artifacts_path = './artifacts/contracts/PinController.sol/PinController.json'
with open(artifacts_path) as artifacts_file:
    artifacts = json.load(artifacts_file)
abi = artifacts['abi']  # ABI (Application Binary Interface) for the contract
bytecode = artifacts['bytecode']  # Bytecode for deploying the contract

# Initialize web3.py instance: Connect to the local Ethereum network
w3 = Web3(HTTPProvider("http://localhost:8545/"))

# Deploy contract and get contract instance
contract = w3.eth.contract(abi=abi, bytecode=bytecode)  # Create a contract object
tx_hash = contract.constructor().transact()  # Deploy the contract
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)  # Wait for deployment to complete
print('Contract deployed at:', tx_receipt.contractAddress)  # Output the address of the deployed contract

# Create a contract instance to interact with
contract_instance = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Get initial pin status: Query the status of each pin from the contract
for i in pinList:
    pin_status = contract_instance.functions.pinStatus(i).call()
    print(f'Pin {i} status is {pin_status}')

# Initialize Flask application
app = Flask(__name__)

@app.route("/")
def index():
    """Render the main page."""
    return render_template('index.html')  # Render the HTML template for the main page

@app.route("/<pin_id>/<action>")
def set_pin_status(pin_id, action):
    """Update the status of a GPIO pin and interact with the smart contract.

    Args:
        pin_id (str): The ID of the GPIO pin to control (e.g., 'fourteen').
        action (str): The desired action ('on' or 'off').

    Returns:
        str: The rendered HTML template for the main page.
    """
    # Validate pin_id
    if pin_id not in pin_mapping:
        return render_template('index.html')  # If pin_id is invalid, render the main page

    pin_number = pin_mapping[pin_id]  # Get the GPIO number from pin_id
    pin_status = 1 if action == 'on' else 0  # Determine the desired pin status

    # Interact with the smart contract to update pin status
    tx_hash = contract_instance.functions.setPinStatus(pin_number, pin_status).transact({'from': w3.eth.accounts[0]})
    print('Transaction submitted:', tx_hash.hex())  # Output the transaction hash

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)  # Wait for the transaction to be confirmed
    print('Transaction confirmed in block:', tx_receipt.blockNumber)  # Output the block number

    # Update GPIO pin based on the new status
    GPIO.output(pin_number, GPIO.HIGH if pin_status else GPIO.LOW)
    print(f'Pin {pin_number} status changed to {pin_status}')

    return render_template('index.html')  # Render the main page after updating the pin status

if __name__ == '__main__':
    # Run the Flask application
    app.run(port=8000, host='localhost')
