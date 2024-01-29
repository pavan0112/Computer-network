import socket
import sys
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
file1 = "response1.html"
time1=time.time()
if len(sys.argv)==3:
	target_host = sys.argv[1]
	target_port = int(sys.argv[2])
	# Connect to the server
	client.connect((target_host, target_port))

	# Send an HTTP GET request
	request = f"GET http://gaia.cs.umass.edu HTTP/1.0\r\nHost: {target_host}:{target_port}\r\n\r\n"
	#request = f"GET /response.html HTTP/1.0\r\nHost: {target_host}:{target_port}\r\n\r\n"
	print("--------------------")
	client.send(request.encode())
elif len(sys.argv)==5:
	target_host = sys.argv[1]
	target_port = int(sys.argv[2])
	proxy_host=sys.argv[3]
	proxy_port=int(sys.argv[4])

	# Connect to the server
	client.connect((proxy_host, proxy_port))

	# Send an HTTP GET request
	request = f"GET http://gaia.cs.umass.edu HTTP/1.0\r\nHost: {target_host}:{target_port}\r\n\r\n"
	#request = f"GET /response.html HTTP/1.0\r\nHost: {target_host}:{target_port}\r\n\r\n"
	client.send(request.encode())
else:
	print("--------------------")
	print("supply enough data")
	exit(0)

# Receive and save the response
response = client.recv(4096)


# Close the connection
client.close()

# Extract the HTTP response headers and body
header, data = response.split(b"\r\n\r\n", 1)

# Print the HTTP response headers
print(header.decode())

# Save the response body to a file
with open(file1, "wb") as f:
    f.write(data)

print(f"HTTP response saved to {file1}")

from bs4 import BeautifulSoup


soup = BeautifulSoup(data, 'html.parser')

images = soup.find_all('img')

for img in images:
	img_url = img.get('src')
	print(img_url)
	print("--------------------")
	client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if len(sys.argv)==3:
		client1.connect((target_host, target_port))
	else:
		client1.connect((proxy_host, proxy_port))
	# Send an HTTP GET request
	request = f"GET /{img_url} HTTP/1.0\r\nHost: {target_host}:{target_port}\r\n\r\n"
	client1.send(request.encode())

	# Receive and save the response
	response = client1.recv(1048576)


	print(response)
	# Extract the HTTP response headers and body
	header, data = response.split(b"\r\n\r\n", 1)

	# Print the HTTP response headers
	print(header.decode())

	# Save the response body to a file
	with open(img_url, "wb") as f:
	    f.write(data)

	print(f"image saved to {img_url}")
	# Close the connection
	client1.close()
time2=time.time()
print(f"time elapsed : {time2-time1}")
# Close the connection
client.close()

