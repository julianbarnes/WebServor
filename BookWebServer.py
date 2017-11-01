#import socket module
from socket import *
import sys # In order to terminate the program
import io
import argparse
import os

def get_params():
	parser = argparse.ArgumentParser(description='Configure IP Address and Port number for server.')
	parser.add_argument('port', type=int, help='Port number')
	parser.add_argument('root', type=str, help='Root folder')
	args = parser.parse_args()
	return args

def create_error(file, path):
	#Send response message for file not found
		error_response = """
		<div align="center">
		<h2>{}</h2>
		<h1>404 NOT FOUND</h1>
		<hr>
		<h3>Computer Network Project 2</h3>
		<h3>2017843537</h3>
		</div>
		""".format(path)
		notfound = "HTTP/1.1 404 Not Found\n"
		notfound += "Content-Type: text/html\n"
		notfound += "Content-Length: " + str(sys.getsizeof(error_response))
		notfound += "\n\n" + error_response
		notfound += ""
		return notfound

def is_mobile(message):
	print(message)
	return message.upper().find("MOBILE") != -1

def is_aa3(message):
	return message.find("aa3.html") != -1

def get_host(message):
	lines = message.split()
	for line in lines:
		if("Host:" in line):
			host = line[6:]
	return host
	

def connect_client(connection, args):
	try:
		message = connection.recv(1024)
		#print("Connected")
		print(message)
		filename = message.decode().split()[1]
		content_ext = filename.split(".")[-1]
		extensions = {"html":"text/html", "css":"text/css","js":"text/javascript","jpg":"image/jpeg","png":"image/png"} 
		filetype = extensions.get(content_ext)
		
		if(is_aa3(message)):
			message.format(get_host(message))
		#Redirect to root directory
		if(filename == "/"):
			print("default")
			filename = "/index.html"
		
		if(is_mobile(message)):
			print("\nMOBILE\n")
			path = args.root + "/mobile" + filename
		else:
			path = args.root + filename
		
		#Calculate file size
		if(os.path.exists(path)):
			size = os.path.getsize(path)
		else:
			size = 0

		f = open(path, "rb")                        
		outputdata = f.read()               
		#Send one HTTP header line into socket
		response = """HTTP/1.1 200 OK\nContent-Type: {}\nContent-Length: {}\n\n""".format(filetype, size)
		print(response)
		connection.send(response)              
		#Send the content of the requested file to the client

		connection.send(outputdata)
        
	except IOError as e:
		connection.send(create_error(filename, path))
		print(e)
	
args = get_params()
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#Prepare a sever socket
server_socket.bind(('',args.port))
server_socket.listen(10)

while True:
	#Establish the connection
	print('Ready to serve...')
	connection_socket, addr = server_socket.accept()
	#print("Accepted")        
	connect_client(connection_socket, args)
	connection_socket.close()
	
server_socket.close()
print("Closed")
sys.exit()#Terminate the program after sending the corresponding data                                    
