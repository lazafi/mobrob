# tello SDK boiler plate

import threading 
import socket
import sys
import time
import select

HOST = ''
PORT = 8889

locaddr = (HOST,PORT) 
tello_address = ('192.168.10.1', 8889)

def main():
    print('\r\n\r\nTello Control.\r\n')
    print('type quit to quit.\r\n')
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(0)
    sock.bind(locaddr)

    while True: 
        try:
            print ('$', end='', flush=True)
            msg = input("")
            if not msg:
                break
            if 'quit' in msg:
                print ('closing')
                sock.close()  
                break
            # Send data
            msg = msg.encode(encoding="utf-8") 
            sent = sock.sendto(msg, tello_address)
            print("sent: ", sent)

            # endless loop monitorig socket with select
            counter = 0
            while(True):
                ready = select.select([sock], [], [], 1.0)
                if ready[0]:
                    data, server = sock.recvfrom(1024)
                    print(data.decode(encoding="utf-8"))
                    break
                else:
                    print ('.', end='', flush=True)
                if counter > 10:
                    print ('\n timeout')                    
                    break
                counter += 1
        except KeyboardInterrupt:
            print ('\n . . .\n')
            sock.close()  
            break


def command(cmd, timeout=10):
    result = False




if __name__ == '__main__':
    main()
