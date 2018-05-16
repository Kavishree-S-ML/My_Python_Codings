import sys
import os
import signal
import subprocess
import socket   
hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname)
host_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host_socket.connect((hostname, 22))
current_ip = host_socket.getsockname()[0]
host_socket.close()   
print("Your Computer Name is:"+hostname)   
print("Your Computer IP Address is:"+IPAddr)
print("Your Computer IP Address is:"+current_ip)
"""
to_run = "kill -9 `ps -Tcjstv | grep 'python blockStreamer' | grep -v 'grep' | awk '{print $1}'`"
#to_run = "ps -P | grep 'python blockStreamer'"
process = subprocess.call(['sshpass', '-p', 'maplelabs', 'ssh', 'root@10.11.0.81', to_run])
print process
"""

process_to_run = "kill -9 `ps -ef | grep SSET_Executor | grep SSET_82 | grep -v 'grep' | awk '{print $2}'`"
process = subprocess.call(process_to_run, shell=True)
#for i in range(0, len(process)):
print "Process: ",process
#os.setpgrp()
#pgrp = os.getpgid(process)
#os.killpg(pgrp, signal.SIGKILL)
