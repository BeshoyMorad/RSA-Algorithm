import socket
import sys
from Library import generateKey, RSA_Encrypt, RSA_Decrypt


# ================================================================================================
# Global Variables
# ================================================================================================
type = sys.argv[1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recvBytes = 50000
# ================================================================================================

# ================================================================================================
# My Key
# ================================================================================================
my_e, my_d, my_n = generateKey()
# ================================================================================================


# ================================================================================================
# Functions
# ================================================================================================
def sendMessage(socket, e, n):
	message = input('Enter message: ')

	# Encrypt message
	cipher = RSA_Encrypt(message, e, n)

	data = ""
	for item in cipher:
		data += str(item) + "Δ"
	data = data[:-1]
	
	socket.send(data.encode('utf-8'))

	return False if message.strip() == "quit" else True

def receiveMessage(socket):
	data = socket.recv(recvBytes).decode("utf-8")

	# Decrypt message
	encrypted = data.split('Δ')

	for i in range(len(encrypted)):
		encrypted[i] = int(encrypted[i])
	
	return RSA_Decrypt(encrypted, my_d, my_n)

def sendUsername(socket):
	username = input('Enter username: ').encode('utf-8')
	socket.send(username)

def receiveUsername(socket):
	return socket.recv(recvBytes).decode("utf-8")

def sendPublicKey(socket):
	key = str(my_e) + 'Δ' + str(my_n)
	socket.send(key.encode('utf-8'))

def receivePublicKey(socket):
	key = socket.recv(recvBytes).decode("utf-8")
	key = key.split('Δ')
	e = int(key[0])
	n = int(key[1])
	return e, n
# ================================================================================================


if type == "server":
	# ================================================
	# Connections
	# ================================================
	s.bind(('localhost', 9999))
	s.listen()
	conn, addr = s.accept()

	sendUsername(conn)

	otherUsername = receiveUsername(conn)

	sendPublicKey(conn)

	e, n = receivePublicKey(conn)
	# ================================================

	# ================================================
	# Main Loop
	# ================================================
	while True:
		# Receive message
		data = receiveMessage(conn)
		if data.strip() == "quit":
			break
		print(f'{otherUsername}: {data}')

		# Send message
		if (not sendMessage(conn, e, n)):
			break
	# ================================================

else:
	# ================================================
	# Connections
	# ================================================
	s.connect(('localhost', 9999))

	otherUsername = receiveUsername(s)

	sendUsername(s)

	e, n = receivePublicKey(s)

	sendPublicKey(s)
	# ================================================

	# ================================================
	# Main Loop
	# ================================================
	while True:
		# Send message
		if (not sendMessage(s, e, n)):
			break

		# Receive message
		data = receiveMessage(s)
		if data.strip() == "quit":
			break
		print(f'{otherUsername}: {data}')
	# ================================================


# Close connection
s.close()