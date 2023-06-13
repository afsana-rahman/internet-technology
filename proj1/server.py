import threading
import time
import random

import socket

def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50007)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))

    # send a intro message to the client.  
    msg = "Connected to server"
    csockid.send(msg.encode('utf-8'))

    # Receive data from the client
    lines = csockid.recv(100)
    lines.decode('utf-8')
    num = int(lines)

    # 
    # BEGIN STUDENT CONTRIBUTION:
    # receive and reverse line by line, put into file
    # https://www.pythontutorial.net/python-basics/python-write-text-file/
    with open('out-proj.txt', 'w') as f:
        # https://www.w3schools.com/python/python_for_loops.asp
        for x in range(num):
            line = csockid.recv(210)
            # https://www.w3schools.com/python/python_howto_reverse_string.asp
            line = line.strip()
            reverse = line[::-1]
            reverse += "\n"
            f.write(reverse)
            # print("[S]: Data received from client (backwards): {}".format(reverse))
    # END STUDENT CONTRIBUTION
    #

    # Close the server socket
    ss.close()
    exit()

if __name__ == "__main__":
    t1 = threading.Thread(name='server', target=server)
    t1.start()

    time.sleep(random.random() * 5)
    print("Done.")