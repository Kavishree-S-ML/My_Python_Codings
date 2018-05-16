import socket
import subprocess
import time
import os
import sys
hostname = <host_ip>
current_port = 5509
password = <host_pswd>
username = <host_username>
filename = "test_socket_client.py"

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

def get_ip_addr(hostname):

        host_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host_socket.connect((hostname, 22))
        current_ip = host_socket.getsockname()[0]
        host_socket.close()

        return current_ip

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

current_ip = get_ip_addr(hostname)
print "*** Current IP : --> ",current_ip
listen_socket, port = init_listen_socket(current_ip, current_port)
print "Port : ",port
listen_socket.listen(5)
print "Listen to the scoket"
try:
    subprocess.call(['sshpass', '-p', password, 'scp', '-o', ' UserKnownHostsFile=~/.ssh/known_hosts', '-o', 'StrictHostKeyChecking=no', './'+filename, username+'@'+hostname + ':~/.'])
    process = subprocess.Popen(['sshpass', '-p', password, 'ssh', username+'@'+hostname, 'python', filename, current_ip, str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
except Exception, excep:
    print excep
conn, addr = listen_socket.accept()
print "ADDress : ",addr
input_data = get_socket_data(conn)
conn.send("end")
current_command = input_data[:input_data.find("|")]
print current_command
listen_socket.close()
