import socket
from modules.comm_init import *
import pickle

def main():
    MYIP = "127.0.0.1"#"192.168.0.3"
    MYPORT = 8080
    BoothIP = "127.0.0.1"#"192.168.0.2"
    BoothPort = 8888
    MAXBUFF = 64000
    
    Mysock = receiver_init(MYIP, MYPORT)

    ballot = ['1. Billy', '2. Annette', '3. Jim']

    Mysock.listen(1)
    conn, addr = Mysock.accept()

    while True:
        data = pickle.loads(conn.recv(MAXBUFF))
        if data == 3:
            BoothSock = sender_init(BoothIP, BoothPort)
            BoothSock.send(pickle.dumps(ballot))
            #vote = pickle.loads(BoothSock.recv(MAXBUFF))
            vote = BoothSock.recv(MAXBUFF)
            BoothSock.close()
            print vote

if __name__ == "__main__":
    main()
