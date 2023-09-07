import socket

ADDRESS = ('chals.sekai.team', 3062)

def sock():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(ADDRESS)

    flag = 'STRING TO LOOK FOR'
    data = recvUntil(s, flag)    

    print("Connection Closed")
    s.close()

def recvUntil(s, flag):
    data = b''
    while True:
        input = s.recv(1024)
        data += input
        print(repr(input))
        if (input.find(flag) != -1):
            break
    return data

sock()