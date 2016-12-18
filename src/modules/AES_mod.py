import sys
import base64
import os
import hashlib
import random

from Crypto.Cipher import AES
from Crypto import Random

BS = 16 #Block size for AES

#String to bytes because we are using python 3
def str_to_bytes(data):
    u_type = type(b''.decode('utf8'))
    if isinstance(data, u_type):
        return data.encode('utf8')
    return data


#Pad message if necessary for encryption
def pad(s):
    return s + (BS - len(s) % BS)*chr(BS - len(s) % BS)

#Unpad message if necessary for decryption
def unpad(s):
    return s[:-ord(s[len(s)-1:])]

#Ecryption Function: AES-256 CBC implementation
def encrypt(message):
    #Creating hash of message for authentication using sha-256 (Generates 64-characters)
    hash_msg = hashlib.sha256(message.encode())

    #Symmetric Encryption AES-256
    #key_str = 'This is the key'
    key_str = str(random.seed())
    key = hashlib.sha256(str_to_bytes(key_str)).digest()
    message = message + hash_msg.hexdigest()
    message = pad(message)
    IV=Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, IV)

    #Returns 64 character hex representation of the hash and the ecrypted message
    return hash_msg.hexdigest(), base64.b64encode(IV + cipher.encrypt(message)).decode('utf-8')

#Decryption Function: AES-256 CBC implementation
def decrypt(message):
    #Symmetric Decryption
    #key_str = 'This is the key'
    key_str=str(random.seed())
    key = hashlib.sha256(str_to_bytes(key_str)).digest()
    message = base64.b64decode(message)
    IV = message[:AES.block_size]

    cipher = AES.new(key, AES.MODE_CBC, IV)
    decrypted_message = unpad(cipher.decrypt(message[AES.block_size:])).decode('utf-8')
    hex_hash = decrypted_message[-64:]
    message = decrypted_message[:-64]
    return message, hex_hash

#Authentication Function: This fucntion checks the integrity of the message
def authenticate(message, hex_hash):
    hash_msg = hashlib.sha256(message.encode())
    if(hash_msg.hexdigest() == hex_hash):
        return True
    else:
        return False

