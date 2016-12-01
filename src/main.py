from modules.comm_init import *
# main script here

def main():
    sender_init("192.168.0.1", 5005)
    receiver_init("192.168.0.2", 8888)


if __name__ == "__main__":
    main()
    
