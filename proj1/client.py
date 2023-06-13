import threading
import time
import random

import socket

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    # Receive data from the server
    data_from_server=cs.recv(100)
    print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

    #
    # BEGIN STUDENT CONTRIBUTION
    # Read file
    # https://www.pythontutorial.net/python-basics/python-read-text-file/
    lines = []
    with open('in-proj.txt', 'r') as f:
        lines = f.readlines()

    # send line by line
    length = len(lines)
    num = str(length)
    cs.send(num.encode('utf-8'))
    time.sleep(1)
    # https://www.w3schools.com/python/python_for_loops.asp
    for line in lines:
        cs.send(line.encode('utf-8'))
        time.sleep(1)
    # END STUDENT CONTRIBUTION
    #

    # close the client socket
    cs.close()
    exit()

if __name__ == "__main__":

    t2 = threading.Thread(name='client', target=client)
    t2.start()

    time.sleep(5)
    print("Done.")