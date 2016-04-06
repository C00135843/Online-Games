#ssh -i roger1.pem ubuntu@54.186.22.79 

import socket	
import json

port = 5228

#setup socket
def setup_socket():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(("", port))
	return s

s = setup_socket()
print ("waiting on port:", port)

#Take message and transform it into a dictionary
def get_message(data):
	msg={}
	data = data.decode('utf-8')
	msg = json.loads(data)
	return msg

def create_message(content, type):
    msg={}
    msg['type']=type
    msg['content']=content
    msg=json.dumps(msg)
    msg = msg.encode('utf-8')
    return msg

def get_internal_ip():
    internal_ip = socket.gethostbyname(socket.gethostname())
    print(internal_ip)



get_internal_ip()


while 1:
	data, addr = s.recvfrom(1024)
	#remote ip
	ip = addr[0]
	#remote port
	port = addr[1]
	
	#address = socket.getnameinfo(addr, socket.socket.AI_NUMERIC_HOST)
	print("from "+str(ip) +":"+ str(port))
	
	msg = get_message(data)
	print(msg)

	if msg['type'] == "hello":
		msg_reply=create_message("hello received!", "hello")
		
	
	s.sendto(msg_reply, (ip, port))

	
