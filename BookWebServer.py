#import socket module
from socket import *
import sys # In order to terminate the program
import io
import argparse

	


server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#Prepare a sever socket
server_socket.bind(('',12000))
server_socket.listen(10)
while True:
    #Establish the connection
    print('Ready to serve...')
    connection_socket, addr = server_socket.accept()
    print("Accepted")        
    try:
        message = connection_socket.recv(1024).decode()
        print("Connected")                
        filename = message.split()[1]
        print(filename)
       # filetype = filename.split('.')[1]
       # process_type(filetype, connection_socket)
        #Redirect to root directory                 
        f = io.open(filename[1:], encoding="latin1")
        print(filename[1:])                        
        outputdata = f.readlines()                 
        #Send one HTTP header line into socket
        #print(outputdata[0])
        response = """\
HTTP/1.1 200 OK
"""
        connection_socket.sendall(response.encode())              
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):           
            connection_socket.sendall(outputdata[i].encode('utf-8'))
            connection_socket.sendall("\r\n".encode('utf-8'))
        
        #connection_socket.close()
    except IOError:
        #Send response message for file not found
        
        print("Exception")
        notfound = """\
            HTTP/1.1 404 Not Found\r\n\r\n
            """
        connection_socket.send(notfound.encode()) 


        #Close client socket
        connection_socket.close()
         
serverSocket.close()
print("Closed")
sys.exit()#Terminate the program after sending the corresponding data                                    
