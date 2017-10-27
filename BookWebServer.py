#import socket module
from socket import *
import sys # In order to terminate the program
import io

def process_type(extension):
    if extension == "html":
        pass
    if extension == "css":
        pass
    if extension == "js":
        pass
    if extension == "jpg":
        pass
    if extension == "png":
        pass

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#Prepare a sever socket
#Fill in start
server_socket.bind(('',12000))
server_socket.listen(10)
#Fill in end
while True:
    #Establish the connection
    print('Ready to serve...')
    connection_socket, addr = server_socket.accept()
    print("Accepted")  #Fill in start   #Fill in end          
    try:
        message = connection_socket.recv(1024).decode()
        print("Connected")  #Fill in start          #Fill in end               
        filename = message.split()[1]
        print(filename)
       # filetype = filename.split('.')[1]
       # process_type(filetype, connection_socket)
        #Redirect to root directory                 
        f = io.open(filename[1:], encoding="latin1")
        print(filename)                        
        outputdata = f.readlines()#Fill in start       #Fill in end                   
        #Send one HTTP header line into socket
        #print(outputdata[0])
        response = """\
HTTP/1.1 200 OK
"""
        connection_socket.sendall(response.encode())              
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):           
            connection_socket.sendall(outputdata[i].encode())
            connection_socket.sendall("\r\n".encode())
        
        #connection_socket.close()
    except IOError:
        #Send response message for file not found
        #Fill in start
        print("Exception")
        notfound = """\
            HTTP/1.1 404 Not Found\r\n\r\n
            """
        connection_socket.send(notfound.encode()) 

        #Fill in end
        #Close client socket
        #Fill in start
        connection_socket.close()
        #Fill in end            
serverSocket.close()
print("Closed")
sys.exit()#Terminate the program after sending the corresponding data                                    
