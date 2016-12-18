
#
# Python Voter Block Chain Handler
# Author: Robert Irwin

import socket
import pickle
from modules.AES_mod import *

class VoterBlockChain:

    def __init__(self, initialize ):
        self.VoterChain = list()
        self.MAXBUFF = 64000
        if initialize:
            self.CreateFirstVoterChain()


    def CreateFirstVoterChain(self):
        self.VoterChain = [dict()] # initialize the list of dictionaries
        entry = input("Enter Voter's Name: ")
        while True:
            if entry == "DONE":
                break
            self.VoterChain[0][entry] = 0 # a zero represents that the voter has not yet voted
            entry = input("Enter Voter's Name: ")
#        print(self.VoterChain)  # for debugging

    # Get Most Up to Date Chain from the Trusted Admin
    def RequestUp2DateChain(self, Advisory):
        requestChain = [1] # one means request an up2date ballot
        Advisory.send(pickle.dumps(requestChain,protocol=2))
        self.VoterChain = pickle.loads(Advisory.recv(self.MAXBUFF))

    # This function verifies with the blockchain that the voter is registered and has not yet voted.
    # It also sends a request to the blockchain on behalf of the voter.
    def UIRequestBallot(self, user, Advisory):
        # First Ensure that we have the most recent Chain
        self.RequestUp2DateChain(Advisory)
        d_user, hex_hash = decrypt(user)
        if(authenticate(d_user, hex_hash)): 
            IsRegistered = self.CheckRegistrationStatus(d_user)
            if not IsRegistered:
                print("Sorry, but you didn't register!! Try again next election!")
                return (IsRegistered)
            elif (self.VoterChain[-1][d_user] == 1):
                print("You voted Already!!! SOUND THE ALARM!!!")
                return False
            else:
                print("Access Granted. Please wait while we retreive your ballot...")
            requestBallot = [2, d_user]
            Advisory.send(pickle.dumps(requestBallot,protocol=2))
            return (IsRegistered)
        else:
            print("Data is not Authentic")
            return False

    def CheckRegistrationStatus(self, user):
        if user in self.VoterChain[-1]:
            return True
        else:
            return False

