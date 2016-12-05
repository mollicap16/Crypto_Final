from modules.comm_init import *
from modules.VoterBlockChain import *
import copy

def main():
    MYIP = "127.0.0.1"#"192.168.0.1"
    MYPORT = 5005
    BallotIP = "127.0.0.1"#"192.168.0.3"
    BallotPort = 8080
    MAXBUFF = 64000
    
    BlockChain = VoterBlockChain(True)
    
    MySock = receiver_init(MYIP, MYPORT)
    MySock.listen(1)
    conn, addr = MySock.accept()
    BallotSock = sender_init(BallotIP, BallotPort)
    
    while True:
        data = pickle.loads(conn.recv(MAXBUFF))
        if data[0] == 1: # one represents the voter booth needs an updated block chain
            conn.send(pickle.dumps(BlockChain.VoterChain))
        elif data[0] == 2: #two means the voter booth needs a ballot
            # change voter status to "voted"
            temp = BlockChain.VoterChain[-1].copy()
            BlockChain.VoterChain.append(temp)
            BlockChain.VoterChain[-1][data[1]] = 1
            print BlockChain.VoterChain
            BallotRequest = 3
            BallotSock.send(pickle.dumps(BallotRequest))
if __name__ == "__main__":
    main()
