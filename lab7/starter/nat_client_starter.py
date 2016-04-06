#http://www.binarytides.com/programming-udp-sockets-in-python/

import socket
import sys
import json
import traceback
import pprint

#socket
s=None
#Source http://stackoverflow.com/questions/10883399/unable-to-encode-decode-pprint-output
class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, bytes):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

my_pprint = MyPrettyPrinter()

def setup_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        timeout_length = 10
        s.settimeout(timeout_length)
        s.bind(("",5228))
        return s

    except socket.error:
        print ('Failed to create socket')
        tb = traceback.format_exc()
        print(tb)
        sys.exit()

def client(name):
    print(name)    
   
    host = 'localhost'
    host = "52.38.116.193" #your ec2 IP
    
    port = 5228
      
    set_names(name)

    global s
    s = setup_socket()    
 
    try :
        get_internal_ip()

        #msg = input('This is ' + name + '. Enter message : ')
        content = name+" (This is from "+ name+")"
        msg = create_message(content, "hello")        

        #Set the whole string
        print("Step 1: Send to server")

        s.sendto(msg, (host, port))

        sockname = s.getsockname()
        print(sockname)

        
        my_pprint.pprint( get_message() )    
      
    
    # Some problem sending data ??
    except socket.error as e:
        print ('Error Code : ' + str(e[0]) )
        #print ('Error Code : ' + str(e[0]) + ' Message ' + e[1])
        sys.exit()
    
    

    print('Complete')

def get_internal_ip():
    internal_ip = socket.gethostbyname(socket.gethostname())
    print(internal_ip)

def create_message(content, type):
    msg={}
    msg['type']=type
    msg['content']=content
    msg=json.dumps(msg)
    msg = msg.encode('utf-8')
    return msg

#Take message and transform it into a dictionary
def get_message():
    data, addr = s.recvfrom(1024)
   
    msg={}
    msg['ip']=addr[0]
    msg['port']=addr[1]
    data = data.decode('utf-8')
    msg = json.loads(data)
    return msg



#a=local(you) and b=remote(other player)
def set_names(name):    
    if name=="a":
        not_name = "b"
    else:
        not_name = "a"

if(len(sys.argv) >=1):
    client(sys.argv[1])