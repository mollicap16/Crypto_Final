import socket
import pickle
from modules.comm_init import *
from modules.VoterBlockChain import *
from modules.AES_mod import *

# init_Comms(): this function sets up the socket with the Advisory and Opens a socket for the Ballot Server
# Also returns the sockets and the instance of the block chain back to the main program
#
def init_Comms():
    VoterAdvisoryIP = "127.0.0.1"#"192.168.0.1"
    VoterAdvisoryPort = 5005
    MYIP = "127.0.0.1"#"192.168.0.2"
    MYPORT = 8888
    MAXBUFF = 64000

    # initialize a socket to the Voter Advisory BlockChain
    #
    AdvSock = sender_init(VoterAdvisoryIP, VoterAdvisoryPort)

    Mysock = receiver_init(MYIP, MYPORT)

    #Instantiate the class object
    BlockChain = VoterBlockChain(False)
    BlockChain.RequestUp2DateChain(AdvSock)

    return(AdvSock, Mysock, BlockChain)

# credentialHandler(credentials, AdvSock, Mysock) this function takes the credentials from the GUI
# as well as the local socket and the socket to the voter advisory. Checks the status of the voter,
# and updates the advisory. Also waits for the ballot server to connect to it. If the ballot server connects
# the voter has not voted anywhere else.
def credentialHandler(user, Mysock, AdvSock, BlockChain):
    MAXBUFF = 64000
    IsRegistered = BlockChain.UIRequestBallot(user, AdvSock)
    if IsRegistered:
        Mysock.listen(1) # listen for incoming ballot from Ballot Server
        conn, addr = Mysock.accept()
        #Encrypt Ballot to send back over
        hex_hash, e_msg = encrypt('Valid')
        ballot = e_msg
        #ballot = pickle.loads(conn.recv(MAXBUFF))
    else:
        hex_hash, e_msg = encrypt('Invalid')
        ballot = e_msg
        #ballot=False
        conn=False

    return(ballot, conn)

# castVote(vote, conn) this functions takes the vote from the GUI and sends it to the ballot
# server through the socket, conn.
def castVote(vote, conn):
    #conn.send(pickle.dumps(vote, protocol=2))
    conn.send(vote.encode())
    conn.close()
