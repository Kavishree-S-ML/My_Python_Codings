import datetime
import socket
import sys
import binascii
import subprocess
import os
import zlib
import time
import math
import traceback

import logging
import logging.handlers
LOGGER_NAME = 'test_blockStreamer.py,VM-'+sys.argv[2]
LOG_FILENAME = "test_kavi_2_vmdk.log"
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)
ch = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1024*1024*1024, backupCount=10)
FORMAT ="[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
formatter = logging.Formatter(FORMAT,"%Y/%m/%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

"""

Sys Args:

1 - Datastore
2 - VM
3 - Filename
4 - Profiler IP
5 - Profiler Port
6 - Sampling Amount - Default 1

"""

def usage():
    print ("Blockstreamer Usage : python blockStream.py (Datastore Name) (VM Name) (Filename) (Profiler IP) (Profiler Port) (Sampling Amount)")

if len(sys.argv) < 7:
    usage()
    sys.exit()

subprocess.call(["esxcli", "network", "firewall", "set", "-d", "true"])

blocknum = 0
total_time_reading = 0
crc = 0
total_dupe_blocks = 0
dedupe_keys = {}
total_zero_blocks = 0
iteration_percent = 100

vm_name = ['SEETestGrpHxBenchVm1', 'SEETestGrpHxBenchVm2']
filename = ['SEETestGrpHxBenchVm1/SEETestGrpHxBenchVm1-flat.vmdk', 'SEETestGrpHxBenchVm2/SEETestGrpHxBenchVm2-flat.vmdk']
for i in range(0,2):
    filepath = "/vmfs/volumes/" + sys.argv[1] + "/" + filename[i]
    headers = {'content-type': 'application/json'}
    timeout = 30

    logger.info("Started Execution of BlockStreamer")
    logger.info("Profiler IP : %s, Port : %s " %(sys.argv[4], str(sys.argv[5])))
    logger.info("Datastore : %s " %sys.argv[1])
    logger.info("VM : %s, FilePath : %s " %(vm_name[i], filename[0]))
    logger.info("Sampling Amount : %s" %str(sys.argv[6]))

    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((sys.argv[4], int(sys.argv[5])))
    except Exception as err:
        logger.error(str(err))
        raise Exception(err)
    try:
        file_size = os.path.getsize(filepath)
        logger.debug("File Size : %s GB" %str(round((float(file_size)/1024/1024/1024), 2)))
        msg = "file_size|" + str(file_size)
    except Exception as err:
        msg = "error|" + str(err)
        logger.error(str(err))

    sent = connection.send(msg)
    connection.send("|end")
    connection.recv(4096)
    connection.close()

    total_iteration = file_size/4194304.0
    total_iteration_count = int(math.ceil(total_iteration))
    logger.debug("Total Iteration Count : %s" % (str(total_iteration_count)))

    try:
        sampling_amount = int(sys.argv[6])
    except IndexError:
        usage()
        sampling_amount = 1
    except TypeError:
        logger.error("Sampling amount must be an integer.")
        sampling_amount = 1

    try:
        with open(filepath, "rb") as in_file:
            while True:
                blocknum += 1
                t1 = datetime.datetime.now()
                for i in range(0, sampling_amount):
                    piece = in_file.read(4194304)
                t2 = datetime.datetime.now()
                total_time_reading += (t2 - t1).microseconds
                if piece == "":
                    break

                """
                Check if zero-filled string, skip and continue.
                """
                if not all(byte for byte in piece):
                    total_zero_blocks += 1
                    continue

                time.sleep(1)

                compression_byte = binascii.hexlify(piece)
                logger.debug("Compression Byte Length : %s" % str(len(compression_byte)))
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.connect((sys.argv[4], int(sys.argv[5])))
                msg = "compression|" + compression_byte
                totalsent = 0
                while totalsent < len(msg):
                    logger.debug("totalsent : %s" %str(totalsent))
                    sent = connection.send(msg[totalsent:])
                    logger.debug("sent : %s" %str(sent))
                    totalsent = totalsent + sent
                logger.debug("Compression sent successfully")
                connection.send("|end")
                #data = connection.recv(4096)
                #logger.debug(data)
                connection.close()

                for index in range(0, 512):
                    logger.debug("Dedupe key calculation")
                    crc = zlib.crc32(piece[0 + index * 8192:8192 + index * 8192], crc)
                    if not crc & 0xffffffff in dedupe_keys:
                        dedupe_keys[crc & 0xffffffff] = 1
                    else:
                        total_dupe_blocks += 1
                    logger.debug("Dedupa keys ended calcaulation")
                logger.debug("Next round")
                if total_iteration_count < 5:
                    logger.debug("Percentage of Iteration Completed --> %s%%" %(str(round(iteration_percent, 2))))
                elif blocknum <= total_iteration_count and (blocknum % 5) == 0:
                    iteration_percent = (blocknum / float(total_iteration_count)) * 100
                    logger.debug("Percentage of Iteration Completed --> %s%%" %(str(round(iteration_percent, 2))))
                
    except Exception, err:
        logger.error(str(err))
        msg = "error|" + str(err)
        logger.error(str(err))
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((sys.argv[4], int(sys.argv[5])))
        sent = connection.send(msg)
        connection.send("|end")
        connection.recv(4096)
        connection.close()
        raise Exception(err)

    if total_iteration_count > 5 and (blocknum - 1) % 5 != 0:
        iteration_percent = ((blocknum - 1) / float(total_iteration_count)) * 100
        logger.debug("Percentage of Iteration Completed --> %s%%" %(str(round(iteration_percent, 2))))

logger.debug("Dedupe Length : %s" %(str(len(dedupe_keys))))
logger.debug("Total Dedupe blocks : %s" % str(total_dupe_blocks))
dedupe_ratio = total_dupe_blocks / (float(len(dedupe_keys)) + total_dupe_blocks)
logger.debug("Dedupe Ratio : %s" % str(format(dedupe_ratio, 'f')))
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((sys.argv[4], int(sys.argv[5])))
dedupe_ratio = format(dedupe_ratio, 'f')
msg = "dedupe_ratio|" + str(dedupe_ratio)
totalsent = 0
while totalsent < len(msg):
    sent = connection.send(msg[totalsent:])
    totalsent = totalsent + sent
connection.send("|end")
connection.recv(4096)
connection.close()

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((sys.argv[4], int(sys.argv[5])))
msg = "finalize|"
totalsent = 0
while totalsent < len(msg):
    sent = connection.send(msg[totalsent:])
    totalsent = totalsent + sent

connection.send("|end")
connection.recv(4096)

logger.info("BlockStreamer Process Finished Successfully !!!")
connection.close()

logger.debug("Time spent for processing the VM ( %s ) : %s" %(sys.argv[2], str(total_time_reading / 1000.0)))
subprocess.call(["esxcli", "network", "firewall", "set", "-d", "false"])
