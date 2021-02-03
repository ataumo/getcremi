#!/usr/bin/env python3

import sys
from Crypto.Cipher import AES







def main():
    #if the size of your password is not a multiple of 16, you have to add
    # this char '_'
    passwd = 'your_passwd_____'.encode()
    key = 'exemple_of_key__'.encode()
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(passwd)

    print(ciphertext)

    plaintext = cipher.decrypt(ciphertext)

    print(plaintext.decode())



if __name__ == "__main__":
    main()
