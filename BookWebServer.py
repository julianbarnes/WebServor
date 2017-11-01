#import socket module
from socket import *
import sys # In order to terminate the program
import io
import argparse
import os
	
def main():
	#Request params from user
	args = get_params()
	#Initialize socket 
	server_socket = socket(AF_INET, SOCK_STREAM)
	server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	#Bind socket to port 
	server_socket.bind(('',args.port))
	#Set socket to listen for connection requests
	server_socket.listen(10)

	while True:
		#Establish the connection
		print('Ready to serve...')
		connection_socket, addr = server_socket.accept()
		#Send and receive http messages
		connect_client(connection_socket, args)
		#Close the TCP Connection socket
		connection_socket.close()
	#Close the server socket
	server_socket.close()
	print("Closed")
	#Terminate the program after sending the corresponding data
	sys.exit()
	
	
#Specify port and root folder from user
def get_params():
	#Initialize parser
	parser = argparse.ArgumentParser(description='Configure IP Address and Port number for server.')
	parser.add_argument('port', type=int, help='Port number')
	parser.add_argument('root', type=str, help='Root folder')
	
	#Set variable args to results of parser
	args = parser.parse_args()
	return args

#Send response message for file not found
def create_error(path):
		#Creates error message with path 
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

#Check to see if request is made from mobile device
def is_mobile(message):
	return message.upper().find("MOBILE") != -1

#Extract the requested file name and the requested file's type
def get_filename(message):
	#parse file name from http request
	filename = message.decode().split()[1]
	
	#look up extension in dictionary to get file type
	content_ext = filename.split(".")[-1]
	extensions = {"html":"text/html", "css":"text/css","js":"text/javascript","jpg":"image/jpeg","png":"image/png", } 
	filetype = extensions.get(content_ext)
	return (filename, filetype)
	
#Attempts to open requested file and send http response
def connect_client(connection, args):
	try:
		#Receive http request from client
		message = connection.recv(1024)
		#Gather file name and file type
		filename, filetype = get_filename(message)
		#Redirect to root directory
		if(filename == "/"):
			filename = "/index.html"
		#Check to see if request is made from mobile device
		if(is_mobile(message)):
			path = args.root + "/mobile" + filename
		else:
			path = args.root + filename
		#Calculate file size
		if(os.path.exists(path)):
			size = os.path.getsize(path)
		else:
			size = 0
		#Open file
		f = open(path, "rb")                        
		outputdata = f.read()               
		#Send one HTTP header line into socket
		response = """HTTP/1.1 200 OK\nContent-Type: {}\nContent-Length: {}\n\n""".format(filetype, size)
		connection.send(response)              
		#Send the content of the requested file to the client
		connection.send(outputdata)
		#Handle 404 error
	except IOError as e:
		connection.send(create_error(path))
		print(e)
	
if __name__ == "__main__":
	main()
