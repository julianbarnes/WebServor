#import socket module
from socket import *
import sys # In order to terminate the program
import io
import argparse
import os

	
#Add arguments
parser = argparse.ArgumentParser(description='Configure IP Address and Port number for server.')
parser.add_argument('port', type=int, help='Port number')
parser.add_argument('root', type=str, help='Root folder')
args = parser.parse_args()


server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#Prepare a sever socket
server_socket.bind(('',args.port))
server_socket.listen(10)

while True:
    #Establish the connection
    print('Ready to serve...')
    connection_socket, addr = server_socket.accept()
    print("Accepted")        
    try:
        message = connection_socket.recv(1024)
        print("Connected")
        #print(message)
        filename = message.decode().split()[1]
        content_ext = filename.split(".")[-1]
        extensions = {"html":"text/html", "css":"text/css","js":"text/javascript","jpg":"image/jpeg","png":"image/png"} 
        #print(filename)
        filetype = extensions.get(content_ext)
        
        if(os.path.exists("."+args.root+"/"+filename)):
            size = os.path.getsize("."+args.root+"/"+filename)
        else:
            size = 0
        
        
        
        #Redirect to root directory
        #if("html" in filename[1:]):
        f = io.open("." + args.root + "/" + filename[1:], encoding="latin1")
        #else:
            #f = io.open(filename[1:], encoding="latin1")
            
        print("." + args.root + "/" + filename[1:])                        
        outputdata = f.readlines()                 
        #Send one HTTP header line into socket
        #print(outputdata[0])
        response = """\
HTTP/1.1 200 OK
Content-Type: {}
Content-Length: {}
            """.format(filetype, size)
        print(response)
        connection_socket.sendall(response.encode())              
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):           
            connection_socket.sendall(outputdata[i].encode('utf-8'))
            connection_socket.sendall("\r\n".encode('utf-8'))
        
        connection_socket.close()
    except IOError as e:
        #Send response message for file not found
        
        print(e)
        notfound = """\
        HTTP/1.1 404 Not Found\r\n\r\n
        
        Content-Type: text/html
        Content-Length: 400
        
        <h1>404 NOT FOUND</h1>
        
        """
        connection_socket.sendall(notfound.encode()) 


        #Close client socket
        connection_socket.close()
        
server_socket.close()
print("Closed")
sys.exit()#Terminate the program after sending the corresponding data                                    
