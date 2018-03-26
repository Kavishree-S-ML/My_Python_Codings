import requests
import json
import sys
import time
import copy
import os
import socket
import binascii
import zlib
from os import path
from fabric.api import *
env.warn_only = False
output['everything'] = False
import logging
import logging.handlers

hostname = "10.11.0.81"
username = "root"
password = "maplelabs"
remote_path = "~/."
local_path = "./test_blockStreamer.py"
current_port = 54000
current_ip = "10.11.0.161"
vm_name = "SEETestGrpHxBenchVm1"
datastore = "Manirama_Datastore"
filename = "SEETestGrpHxBenchVm1/SEETestGrpHxBenchVm1_1.vmdk"
sampling_amount = 1

file_size = None
compressed_bytes = 0
dedupe_amount = 0
compression_amount = 0
current_data = 0
timeout = 300
current_command = ""

LOGGER_NAME = 'SEE_Executor.py,VM-'+vm_name
LOG_FILENAME = "SEE.log"
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)
ch = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1024*1024*1024, backupCount=10)
FORMAT ="[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
formatter = logging.Formatter(FORMAT,"%Y/%m/%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

def init_listen_socket(current_ip, current_port):
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            listen_socket.bind((current_ip, current_port))
            break
        except socket.error, excep:
            print excep.message
            current_port += 1
    return listen_socket, current_port
def get_socket_data(conn):
    socket_data = []
    data = '';
    while 1:
        try:
            data = conn.recv(8192)
            if not data.endswith('|end'):
                socket_data.append(data)
            else:
                socket_data.append(data)
                return ''.join(socket_data)[:-4]
        except Exception, excep:
            print 'get_socket_data: ' + excep.message
        return ''.join(socket_data)
@parallel(pool_size=2)
def host_execute(current_ip, port):
    logger.info("Started Blockstreamer Execution")
    with settings(host_string=hostname, user=username, password=password):
        logger.info("Started the Execution of BlockStreamer file in the host : "+hostname+" for the VM "+vm_name)
        cmd = "nohup python test_blockStreamer.py '"+datastore+"' '"+vm_name+"' '"+filename+"' "+str(current_ip)+" "+str(port)+ " "+str(sampling_amount) +" &> /test_kavi_SEE_output &"
        logger.info("Sent Command : "+cmd)
        result = run(cmd, shell=False, pty=False)
def compress_data(data):
    encoder = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, 25, 9, zlib.Z_HUFFMAN_ONLY)
    compressed_data = encoder.compress(data)
    return len(compressed_data)

logger.info("BlockStreamer pushing to Host: %s", hostname)
with settings(host_string=hostname, user=username, password=password):
    if put(local_path, 'test_blockStreamer.py'): logger.info("BlockStreamer pushed to Host: %s",hostname)
    else: logger.error("Failed in pushing BlockStreamer to Host : %s",hostname)

listen_socket, port = init_listen_socket(current_ip, current_port)
print "Port : ",port
listen_socket.listen(5)

try:
    execute(host_execute, current_ip, port, host=hostname)
except Exception, excep:
    logger.error(excep)
logger.info("Agent Process started for the vm %s in the host %s" %(vm_name, hostname))

try:
    listen_socket.settimeout(timeout)
    while not current_command == "finalize":
        conn, addr = listen_socket.accept()
        input_data = get_socket_data(conn)
        conn.send("end")
        current_command = input_data[:input_data.find("|")]
        logger.info("Current Command : %s " %current_command)

        if current_command == 'file_size':
            data = input_data[input_data.find("|") + 1:]
            logger.info("File Size : %s" % str(data))
        elif current_command == 'compression':
            data = input_data[input_data.find("|") + 1:]
            comp_data = binascii.unhexlify(data)
            compressed_bytes = compress_data(comp_data)
            logger.info(compressed_bytes)
        elif current_command == 'dedupe_ratio':
            data = input_data[input_data.find("|")+1:]
            dedupe_amount = float(data)
            logger.info("Dedupe Amount : %s" % str(dedupe_amount))
        elif current_command == 'error':
            data = input_data[input_data.find("|")+1:]
            logger.error(str(data))
            break
        elif current_command == 'finalize':
            compression_amount = (float(current_data) - float(compressed_bytes)) / float(current_data)
            logger.info("Compression Amount : %s" % str(compression_amount))
            break
except socket.timeout, excep:
    logger.error(str(excep))
except Exception, excep:
    logger.error(str(excep))
finally:
    logger.info("Agent Process Finished for the vm %s in the host %s" %(vm_name, hostname))
    listen_socket.close()