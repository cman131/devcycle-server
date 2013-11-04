__author__ = 'ejm2095'
import base64
from Crypto.Cipher import AES
from dataCollection.settings import KEY
from dataCollection.settings import SALT


cipher = AES.new(KEY)
salt = int(SALT)


def create_uuid(id):
#    get id & convert to int
    id = int(id)
#    create secret (salt+id)
    secret = id+salt
#    convert secret to string for encryption
    secret = str(secret)
#    send over message
    s = cipher.encrypt(pad_data(secret))
#    convert the encrypted id to base 64
    s = base64.encodestring(s)
    return s


def decrypt_uuid(msg):
#    convert the message from base 64 encoding
    msg = base64.decodestring(msg)
#    get message
    secret = cipher.decrypt(msg)
#    decrypt the message
    secret = int(unpad_data(secret))
#    get the id from the decrypted message
    id = secret - salt
#    send over id
    return id

def pad_data(data):
    # return data if no padding is required
    if len(data) % 16 == 0:
        return data
    # subtract one byte that should be the 0x80
    # if 0 bytes of padding are required, it means only
    # a single \x80 is required.
    
    padding_required = 15 - (len(data) % 16)
    data = '%s\x80' % data
    data = '%s%s' % (data, '\x00' * padding_required)
    return data

def unpad_data(data):
    if not data:
        return data
    data = data.rstrip('\x00')
    if data[-1] == '\x80':
        return data[:-1]
    else:
        return data
