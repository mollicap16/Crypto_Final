import socket
from modules.comm_init import *
import random
import string

def main():
    MYIP = "127.0.0.1"
    MYPORT = 5454

    mysock = receiver_init(MYIP, MYPORT)

    # accept connection from ballot and booth
    mysock.listen(2)
    conn1, addr1 = mysock.accept()
    print addr1
    conn2, addr2 = mysock.accept()
    print addr2
    while True:
        data = conn2.recv(64000)
        print data
        if data == "1":
            # key generation
            key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            print key
            conn1.send(key)
            conn2.send(key)

if __name__ == "__main__":
    main()
