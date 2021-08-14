from web3 import Web3
from django.core.cache import cache


def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/11e38c6e035e4de894510e1c930864df'))
    address = '0xb031F1C728fF4bb4214C7F478B698cf94b61c2ED'
    privateKey = '0x4736722728ea6812d7789c3b40076b2cb73783094ebffaf4e467190e26e87145'
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    signedTx = w3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice=gasPrice,
        gas=100000,
        to='0x0000000000000000000000000000000000000000',
        value=value,
        data=message.encode('utf-8')
    ), privateKey)

    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId


def get_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def differentIp(ip, user):
    if cache.get(f"{user}"):
        if cache.get(f"{user}") != ip:
            cache.set(f"{user}", ip, timeout=None)
            return True
    else:
        cache.set(f"{user}", ip, timeout=None)
        return False
