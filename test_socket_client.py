import socket
import sys
import logging
import logging.handlers
name = 'sample'
LOG_FILENAME = "test_socket_client.log"
logger = logging.getLogger(name)
logger.setLevel(logging.ERROR)
#ch = logging.FileHandler(LOG_FILENAME)
ch = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1024*1024*1024, backupCount=100)
FORMAT ="[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
formatter = logging.Formatter(FORMAT,"%Y/%m/%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug("HAi")
"""
print "arg 1 : ",sys.argv[1]
print "arg 2 : ",sys.argv[2]
"""
print "arg 1 : ",sys.argv[1]
current_ip = ""
port = 0
for i in sys.argv[1]:
    current_ip = i['current_ip']
    port = i['port']
    print current_ip
    print port
try:
    logger.debug(sys.argv[1])
    #logger.debug(sys.argv[2])
    logger.error("HAI")
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((current_ip, port))
    logger.debug(connection)
    msg = "Connection Successful"
    logger.debug(msg)
    sent = connection.send(msg)
    connection.send("|end")
    logger.debug("msg : "+msg)
    #connection.recv(4096)
    connection.close()
except socket.error as err:
    raise Exception(err)
except Exception as e:
    print e
