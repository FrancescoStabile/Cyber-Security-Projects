import sys
import socket
from datetime import datetime

print('''
██████╗  ██████╗ ██████╗ ████████╗███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
██████╔╝██║   ██║██████╔╝   ██║   ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
██║     ╚██████╔╝██║  ██║   ██║   ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
                                                                                              
''')

# Defining a target
if len(sys.argv) == 2:  # If user input is 2 it assumes the argument as IP/Hostname
    # Translate hostname to IPv4
    target = socket.gethostbyname(sys.argv[1])
else:
    print("Invalid argument")
 
# Banner
print("-" * 100)
print("Scanning Target: " + target)
print("Scanning started at:" + str(datetime.now()))
print("-" * 100)
  
try:
    # Scan ports between 1 and 65,535, and create a new socket for each port
    for port in range(1,65535):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)     

        # Try to establish a TCP connection
        result = s.connect_ex((target,port))
        if result ==0:
            print("Port {} is open".format(port))
        s.close()
         
except KeyboardInterrupt:
        print("\n Program Closed")
        sys.exit()
except socket.gaierror:
        print("\n Hostname or Address cannot be resolved")
        sys.exit()
except socket.error:
        print("\ Error: Timeout / Protocol Error / Connection Failure")
        sys.exit()
