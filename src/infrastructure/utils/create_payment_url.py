import hmac
import hashlib
import urllib.parse

from ..config.variables import VNPAY_HASH_SECRET_KEY, VNPAY_PAYMENT_URL

def __hmacsha512(key: str, data: str) -> str:
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def create_payment_url(vnpay_url_params: dict) -> str:
    inputData = sorted(vnpay_url_params.items())
    queryString = ''
    seq = 0
    for key, val in inputData:
        if seq == 1:
            queryString = queryString + "&" + key + '=' + urllib.parse.quote_plus(str(val))
        else:
            seq = 1
            queryString = key + '=' + urllib.parse.quote_plus(str(val))

    hashValue = __hmacsha512(VNPAY_HASH_SECRET_KEY, queryString)
    return VNPAY_PAYMENT_URL + "?" + queryString + '&vnp_SecureHash=' + hashValue
