import json
from web3 import Web3, HTTPProvider
from flask import Flask, render_template, request, jsonify
import web3
from web3.types import Nonce
from datetime import datetime

#Define some constant here
blockchainAddress = 'http://127.0.0.1:7545'

w3 = Web3(HTTPProvider(blockchainAddress))
# Set the default account
w3.eth.defaultAccount = w3.eth.accounts[0];
# Path to the compiled contract JSON file
compiledContractPath = 'build/contracts/ProductFactory.json'
# Deployed contract address
deployedContractAddress = '0x440AB2e6731593A50e8E1C9358DEbBfEefC5758b'

productContract = w3.eth.contract('0x2279e2eF76678c2017533eb2EB8eD99A189e71aE')

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
    print(productName)

    # nonce is the number of transaction of an account
    nonce = w3.eth.getTransactionCount(w3.eth.default_account)
    print(nonce)
    transaction = contract.functions.createProduct(
        productName).buildTransaction({
        'from': w3.eth.defaultAccount,
        'maxFeePerGas': w3.toWei('2', 'gwei'),
        'maxPriorityFeePerGas': w3.toWei('1', 'gwei'),
        'nonce': nonce,
    })
    private_key = "e84682cbd5d24a515afea38b420003aa6718ef7895a51165365d797d4232c291"
    w3.eth.send_transaction(transaction)

    # signed_txn = w3.eth.account.signTransaction(transaction, private_key=private_key)
    # w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    res = 'Success!'
    result = {
        "output": res
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

@app.route('/addActionToProduct', methods=['GET','POST'])
def addActionToProduct():
    print(request.form['productId'])
    productId = int(request.form['productId'])
    action = request.form['action']

    # nonce is the number of transaction of an account
    nonce = w3.eth.getTransactionCount(w3.eth.default_account)
    print(nonce)    
    transaction = contract.functions.addActionToProduct(
        action, productId).buildTransaction({
        'from': w3.eth.defaultAccount,
        'maxFeePerGas': w3.toWei('2', 'gwei'),
        'maxPriorityFeePerGas': w3.toWei('1', 'gwei'),
        'nonce': nonce,
    })
    w3.eth.send_transaction(transaction)
    res = 'Success!'
    result = {
        "output": res
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)


@app.route('/searchProduct', methods=['GET','POST'])
def searchProduct():
    productId = int(request.form['productId'])

    output = contract.functions.getActionFromProduct(productId).call()
    [times, actions] = output

    # Output
    res = 'Success!<br>'

    for i in range(len(times)):
        time = datetime.utcfromtimestamp(times[i]).strftime('%Y-%m-%d %H:%M:%S')
        res += time + ": " + actions[i] + "<br>"
    result = {
        "output": res
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

if __name__ == 'main':
    app.run(debug=True) 