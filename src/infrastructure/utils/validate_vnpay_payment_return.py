import hashlib
import hmac
import urllib.parse

def __hmacsha512(key: str, data: str) -> str:
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()

def validate_vnpay_payment_return(data: dict, secret_key) -> bool:
    vnp_SecureHash = data['vnp_SecureHash']

    if 'vnp_SecureHash' in data.keys():
        data.pop('vnp_SecureHash')

    if 'vnp_SecureHashType' in data.keys():
        data.pop('vnp_SecureHashType')

    inputData = sorted(data.items())
    hasData = ''
    seq = 0
    for key, val in inputData:
        if str(key).startswith('vnp_'):
            if seq == 1:
                hasData = hasData + "&" + str(key) + '=' + urllib.parse.quote_plus(str(val))
            else:
                seq = 1
                hasData = str(key) + '=' + urllib.parse.quote_plus(str(val))
    hashValue = __hmacsha512(secret_key, hasData)
    return vnp_SecureHash == hashValue
