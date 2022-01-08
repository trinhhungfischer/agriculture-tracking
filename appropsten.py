import json
from web3 import Web3, HTTPProvider
from flask import Flask, render_template, request, jsonify
import web3
from web3.types import Nonce
from datetime import datetime

#Define some constant here
blockchainAddress = 'https://ropsten.infura.io/v3/509e8eb6c35e4806a69f61774b6829fb'

w3 = Web3(HTTPProvider(blockchainAddress))
# Set the default account
private_key = "837336b1d96e03e8d9be41e322fcbc2e9465edcba1117d53f92a357f22d48e39"
acc = w3.eth.account.privateKeyToAccount(private_key)
# Path to the compiled contract JSON file
compiledContractPath = 'build/contracts/ProductFactory.json'
# Deployed contract address
deployedContractAddress = '0x2279e2eF76678c2017533eb2EB8eD99A189e71aE'

productContract = w3.eth.contract('0xf92ACC91f65c3FDcFEbaa1aC5C1dd846282092B7')

with open(compiledContractPath) as file:
    contract_json = json.load(file) # load contract info as JSON
    contract_abi = contract_json['abi'] # fetch contract's abi - necessary to call its functions

# Fetch deployed contract reference
contract = w3.eth.contract(address=deployedContractAddress, abi=contract_abi)


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addProduct', methods=['GET','POST'])
def addProduct():
    productName = request.form['productName']
    
    # nonce is the number of transaction of an account
    nonce = w3.eth.getTransactionCount(acc.address)
    
    transaction = contract.functions.createProduct(
        productName).buildTransaction({
        'from': acc.address,
        'maxFeePerGas': w3.toWei('2', 'gwei'),
        'maxPriorityFeePerGas': w3.toWei('1', 'gwei'),
        'nonce': nonce,
    })
    # w3.eth.send_transaction(transaction)
    signed_txn = w3.eth.account.signTransaction(transaction, private_key=private_key)
    w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    res = 'Success!'
    result = {
        "output": res
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

@app.route('/addActionToProduct', methods=['GET','POST'])
def addActionToProduct():
    productId = int(request.form['productId'])
    action = request.form['action']

    # nonce is the number of transaction of an account
    nonce = w3.eth.getTransactionCount(acc.address)
    
    transaction = contract.functions.addActionToProduct(
        action, productId).buildTransaction({
        'from': acc.address,
        'maxFeePerGas': w3.toWei('2', 'gwei'),
        'maxPriorityFeePerGas': w3.toWei('1', 'gwei'),
        'nonce': nonce,
    })
    # w3.eth.send_transaction(transaction)
    signed_txn = w3.eth.account.signTransaction(transaction, private_key=private_key)
    w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    res = 'Success!'
    result = {
        "output": res
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)


@app.route('/searchProduct', methods=['GET','POST'])
def searchProduct():
    productId = int(request.form['productId'])

    # nonce is the number of transaction of an account
    nonce = w3.eth.getTransactionCount(acc.address)

    transaction = contract.functions.getActionFromProduct(
        productId).buildTransaction({
        'from': acc.address,
        'maxFeePerGas': w3.toWei('2', 'gwei'),
        'maxPriorityFeePerGas': w3.toWei('1', 'gwei'),
        'nonce': nonce,
    })
    signed_txn = w3.eth.account.signTransaction(transaction, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    if (tx_hash):
        print('OK')
    output = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120) 

    if (output):
        print(output)
    

    # Output
    res = 'Success!<br>'

    # for i in range(len(times)):
    #     time = datetime.utcfromtimestamp(times[i]).strftime('%Y-%m-%d %H:%M:%S')
    #     res += time + ": " + actions[i] + "<br>"
    result = {
        "output": res
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

if __name__ == 'main':
    app.run(debug=True) 