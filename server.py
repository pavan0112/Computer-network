import socket
import threading

def fun(client_socket, client_address,server):
    # Receive and decode the client's request
    request = client_socket.recv(1024).decode()
    print(request)
    # Parse the request to get the requested file path
    request_lines = request.split("\n")
    print("--------------------")
    if len(request_lines) > 0:
        first_line = request_lines[0]
        file_path = first_line.split(" ")[1]
        print("--------------------")
        print("fileline..",first_line)
        print("--------------------")
        print("file..",file_path)
        print("--------------------")
        
        file_path=file_path[1:]
        print("--------------------")
        print(file_path)
        print("--------------------")
        # Check if the file exists
        try:
            with open(file_path, "rb") as file:
                content = file.read()
                response = f"HTTP/1.0 200 OK\r\nContent-Length: {len(content)}\r\n\r\n".encode() + content
        except:
            # If the file doesn't exist, return a 404 Not Found response
            not_found_response = "HTTP/1.0 404 Not Found\r\n\r\nFile Not Found"
            response = not_found_response.encode()

        # Send the response to the client
        client_socket.send(response)

        # Close the client socket
        client_socket.close()

server_host = "127.0.0.1"  
server_port = 7777

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server.bind((server_host, server_port))

# Listen for incoming connections
server.listen(5)

print(f"Server listening on {server_host}:{server_port}")
print("--------------------")
t=[]
k=0
while True:
    # Accept a connection from a client
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address}")
    print("--------------------")
    k=k+1
    t.append(threading.Thread(target=fun,args=(client_socket, client_address,server)))
    t[k-1].start()
    
for i in range(0,k):
    t[i].join()
server.close()

