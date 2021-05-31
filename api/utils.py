from web3 import Web3
from django.core.cache import cache


def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/11e38c6e035e4de894510e1c930864df'))
    address = '0xb7Fb13f4087FA3a04543C6fA6E8F6a662713a474'
    privateKey = '0xceedafeafd8e930e53c5d35209e5cf87813671674ded1c84aff1f5c38b3915ad'
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
