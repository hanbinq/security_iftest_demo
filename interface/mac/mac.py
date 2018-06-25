from time import time
import hashlib

# 当前时间
def get_timstamp():
    timestamp = str(time()).split('.')[0]
    return timestamp


# 前后端约定的key
def get_key():
    key = '9d884b9cf414fc974a824e736f850780'
    return key

def get_signature():
    timestamp = get_timstamp()
    key = get_key()
    # md5 signature
    md5 = hashlib.md5()
    sign_str = '&timestamp=' + timestamp + key
    sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
    md5.update(sign_bytes_utf8)
    signature = md5.hexdigest()
    return signature
