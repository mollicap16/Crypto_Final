#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from modules.voterBoothFunctions import *
from modules.AES_mod import *
import sys

AdvSock, Mysock, BlockChain = init_Comms()

#-------------------------------------------#
#-----------Application Functions-----------#
#-------------------------------------------#
#quit function: This method is called when vote is pressed  
def sendVote():
    if(donVar.get()):
        hex_hash, e_vote = encrypt('donald trump')
        castVote(e_vote, conn)
        print("You Voted Donald Trump")
        print('Ecrypted message = "%s"\n' % e_vote)
    elif(hillVar.get()):
        hex_hash, e_vote = encrypt('hillary clinton')
        castVote(e_vote, conn)
        print("You Voted Crooked Hillary")
        print('Ecrypted message = "%s"\n' % e_vote)
    elif(steinVar.get()):
        hex_hash, e_vote = encrypt('jill stein')
        castVote(e_vote,conn)
        print("You Voted Jill Stein")
        print('Ecrypted message = "%s"\n' % e_vote)
    else:
        hex_hash, e_vote = encrypt(write_in.get().lower())
        castVote(e_vote,conn)
        print("You Voted", write_in.get().lower(),"\n")
        print('Ecrypted message = "%s"\n' % e_vote)

    #----------------------------------------#
    #----ADD CODE TO SEND ENCRYPTED VOTED----#
    #----------------------------------------#

    #After the vote is sent to the server set everything back to its intial state
    don_box.configure(state=DISABLED)
    hill_box.configure(state=DISABLED)
    stein_box.configure(state=DISABLED)
    write_box.configure(state=DISABLED)
    vote.configure(state=DISABLED)
    cred_button.configure(state=NORMAL)
    cred_entry.configure(state=NORMAL)
    cred_entry.delete(0,END)
    message_entry.configure(state=NORMAL)
    message_entry.delete(0,END)
    message_entry.configure(state='readonly')

    #Make sure all the checkboxes are back to unchecked
    donVar.set(0)
    hillVar.set(0)
    steinVar.set(0)
    writeVar.set(0)

    #Make sure the write in box is empty for the next voter
    write_in.configure(state=NORMAL)
    write_in.delete(0,END)
    write_in.configure(state=DISABLED)

#credCheck: This method is used to check the credentials and enable all of the voting boxes
def credCheck():
    global conn

    #Encrypt the credential
    hex_hash, e_cred = encrypt(cred_entry.get()) 
    print('Hash = "%s"' % hex_hash)
    print('Encrypted message = "%s"' % e_cred)
    
    #Sent over encrypted credentials and recieved back encrypted validation
    ballot, conn = credentialHandler(e_cred, Mysock, AdvSock, BlockChain)
    print('Received the encrypted validation "%s"' % ballot)
    #Decrypt the validation message
    d_msg, hex_hash = decrypt(ballot)
    print('Decrypted validation is "%s"\n' % d_msg)
    authentic = authenticate(d_msg, hex_hash)

    #If we have proper credentials to vote. Enable the voter to be able to vote.
    if(d_msg == "Valid" and authentic):
        message_entry.configure(state=NORMAL)
        message_entry.delete(0,END)
        message_entry.insert(0, "Valid Credentials")
        message_entry.configure(state='readonly')
        write_box.configure(state=NORMAL)
        don_box.configure(state=NORMAL)
        hill_box.configure(state=NORMAL)
        stein_box.configure(state=NORMAL)
        cred_button.configure(state=DISABLED)
        cred_entry.configure(state=DISABLED)
    else:
        message_entry.configure(state=NORMAL)
        message_entry.delete(0, END)
        message_entry.insert(0,"Invalid Credentials")
        message_entry.configure(state='readonly')

#donCheck: This method is called when the Donald Trump check box is checked or unchecked
def donCheck():
    if(donVar.get()):
        vote.configure(state=NORMAL)
        write_box.configure(state=DISABLED)
        hill_box.configure(state=DISABLED)
        stein_box.configure(state=DISABLED)
    else:
        vote.configure(state=DISABLED)
        write_box.configure(state=NORMAL)
        hill_box.configure(state=NORMAL)
        stein_box.configure(state=NORMAL)

#hillCheck: This method is called when the Hillary Clinton check box is checked or unchecked
def hillCheck():
    if(hillVar.get()):
        vote.configure(state=NORMAL)
        write_box.configure(state=DISABLED)
        don_box.configure(state=DISABLED)
        stein_box.configure(state=DISABLED)
    else:
        vote.configure(state=DISABLED)
        write_box.configure(state=NORMAL)
        don_box.configure(state=NORMAL)
        stein_box.configure(state=NORMAL)

#steinCheck: This method is called when the Jill Stein check box is checked or unchecked
def steinCheck():
    if(steinVar.get()):
        vote.configure(state=NORMAL)
        write_box.configure(state=DISABLED)
        don_box.configure(state=DISABLED)
        hill_box.configure(state=DISABLED)
    else:
        vote.configure(state=DISABLED)
        write_box.configure(state=NORMAL)
        don_box.configure(state=NORMAL)
        hill_box.configure(state=NORMAL)

#write: This method is called when the write-in check box is checked or unchecked
def write():
    if(writeVar.get()):
        vote.configure(state=NORMAL)
        write_in.configure(state=NORMAL)
        don_box.configure(state=DISABLED)
        hill_box.configure(state=DISABLED)
        stein_box.configure(state=DISABLED)
    else:
        vote.configure(state=DISABLED)
        write_in.configure(state=DISABLED)
        don_box.configure(state=NORMAL)
        hill_box.configure(state=NORMAL)
        stein_box.configure(state=NORMAL)

#------------------------------------------#
#----- GUI Structure Code Starts here -----#
#------------------------------------------#
root = Tk()
root.title("Voting Booth")

#Global variables
labelVar = StringVar()
credVar = StringVar()
donVar = IntVar()
hillVar = IntVar()
steinVar = IntVar()
writeVar = IntVar()

#Create main widget
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

#Additional widgets
ttk.Label(mainframe, textvariable=credVar, font=('bold')).grid(column=1,row=0)
cred_entry = ttk.Entry(mainframe, width=17)
cred_entry.grid(column=1, row=1, sticky = (W, N))
cred_button = ttk.Button(mainframe, text="Register", command = credCheck)
cred_button.grid(column=1, row=2, sticky = W)
message_entry = ttk.Entry(mainframe, width=20, state=DISABLED)
message_entry.grid(column=1, row=4, sticky = (W,N))

ttk.Label(mainframe, textvariable=labelVar, font=('bold')).grid(column=2, row=0)
don_box = ttk.Checkbutton(mainframe, text="Donald Trump", command = donCheck, variable=donVar, state = DISABLED)
don_box.grid(column=2, row=1, sticky=W)
hill_box = ttk.Checkbutton(mainframe, text="Crooked Hillary", command = hillCheck, variable=hillVar, state = DISABLED)
hill_box.grid(column=2, row=2, sticky=W)
stein_box = ttk.Checkbutton(mainframe, text="Jill Stein", command = steinCheck, variable=steinVar, state = DISABLED)
stein_box.grid(column=2, row=3, sticky=W)
write_in = ttk.Entry(mainframe, width = 20, state=DISABLED)

write_in.grid(column=3, row=4, sticky=W)
write_box = ttk.Checkbutton(mainframe, text="Write in:", command = write, variable=writeVar, state = DISABLED)
write_box.grid(column=2, row=4, sticky=W)

vote = ttk.Button(mainframe, text="VOTE", command = sendVote, state=DISABLED)
vote.grid(column=4, row=5, sticky=E)

#Setting variables
labelVar.set("Presidential Nominees")
credVar.set("Enter your Credentials:")


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop();
