import socket
from modules.comm_init import *
from modules.AES_mod import *
import pickle

def main():
    MYIP = "127.0.0.1"#"192.168.0.3"
    MYPORT = 8080
    BoothIP = "127.0.0.1"#"192.168.0.2"
    BoothPort = 8888
    #KeyIP = "127.0.0.1"
    #KeyPort = 5454
    MAXBUFF = 64000
    #Keysock = sender_init(KeyIP, KeyPort)
    Mysock = receiver_init(MYIP, MYPORT)

    tally={}

    ballot = ['1. Billy', '2. Annette', '3. Jim']

    Mysock.listen(1)
    conn, addr = Mysock.accept()

    while True:
        data = pickle.loads(conn.recv(MAXBUFF))
        if data == 3:
            BoothSock = sender_init(BoothIP, BoothPort)
            BoothSock.send(pickle.dumps(ballot))
            #key = Keysock.recv(MAXBUFF)
            #print(key)
            #vote = pickle.loads(BoothSock.recv(MAXBUFF))

            e_vote = BoothSock.recv(MAXBUFF)
            print('Received encrypted message: "%s"' % e_vote)

            #Decrypt encrypted vote
            vote, hex_hash = decrypt(e_vote)

            #Authenticate the message
            if(authenticate(vote, hex_hash)):
                print('Authenticated decrypted message: "%s"\n' % vote)
                #Store results in dictonary
                if vote in tally:
                    tally[vote] += 1
                else:
                    tally[vote] = 1
            else:
                print('message has been compromised\n')
            BoothSock.close()

            print(tally)

if __name__ == "__main__":
    main()
