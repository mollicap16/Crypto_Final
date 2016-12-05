import socket
def sender_init(IP, PORT):
    # initialize TCP socket for sender
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    return s

def receiver_init(IP, PORT):
    # initialize TCP socket for receiver
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    return s
