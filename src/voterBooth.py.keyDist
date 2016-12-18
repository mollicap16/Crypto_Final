import socket
import pickle
from modules.comm_init import *
from modules.VoterBlockChain import *
# main script here

def main():

    VoterAdvisoryIP = "127.0.0.1"#"192.168.0.1"
    VoterAdvisoryPort = 5005
    MYIP = "127.0.0.1"#"192.168.0.2"
    MYPORT = 8888
    KeyIP = "127.0.0.1"
    KeyPort = 5454
    MAXBUFF = 64000
    
    # initialize a socket to the Voter Advisory BlockChain
    #
    AdvSock = sender_init(VoterAdvisoryIP, VoterAdvisoryPort)
    KeySock = sender_init(KeyIP, KeyPort)
    Mysock = receiver_init(MYIP, MYPORT)

    #Instantiate the class object
    BlockChain = VoterBlockChain(False)
    BlockChain.RequestUp2DateChain(AdvSock)
    print BlockChain.VoterChain
    while True:
        user = raw_input("Enter Your Voter Credentials: ")
        IsRegistered = BlockChain.UIRequestBallot(user, AdvSock)
        if IsRegistered:
            Mysock.listen(1) # listen for incoming ballot from Ballot Server
            conn, addr = Mysock.accept()
            ballot = pickle.loads(conn.recv(MAXBUFF))
            KeySock.send("1")
            key = KeySock.recv(MAXBUFF)
            print key
            for choice in ballot:
                print choice
            vote = int(raw_input("Type the Number of Your Candidate: "))
            conn.send(pickle.dumps(vote))
            conn.close()

if __name__ == "__main__":
    main()
    
