import hmac
import hashlib
import urllib.parse

def __hmacsha512(key: str, data: str) -> str:
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def create_payment_url(vnpay_url_params: dict, vnpay_payment_url: str, vnpay_hash_secret_key: str) -> str:
    inputData = sorted(vnpay_url_params.items())
    queryString = ''
    seq = 0
    for key, val in inputData:
        if seq == 1:
            queryString = queryString + "&" + key + '=' + urllib.parse.quote_plus(str(val))
        else:
            seq = 1
            queryString = key + '=' + urllib.parse.quote_plus(str(val))

    hashValue = __hmacsha512(vnpay_hash_secret_key, queryString)
    return vnpay_payment_url + "?" + queryString + '&vnp_SecureHash=' + hashValue
