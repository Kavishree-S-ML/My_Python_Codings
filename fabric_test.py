import subprocess
import socket
import sys
import time
#from fabric.api import *
hostname = <host_ip>
username = <host_username>
pwd = <host_pswd>
remote_path = "~/."
local_path = "./test_socket_client.py"
filename = "test_socket_client.py"
current_port = 12000
current_ip = <current_server_ip>
process_method = "Fabric"

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
listen_socket, port = init_listen_socket(current_ip, current_port)
print "Port : ",current_port
listen_socket.listen(5)
if process_method == "fabric":
    with settings(host_string=hostname, user=username, password=pwd):
        if put(local_path, remote_path, use_sudo=False): print "file transfered"

    with settings(user=username, password=pwd, host_string=hostname):
        #cmd = "python "+ local_path + " " + current_ip + " "+ str(port) + " &> /dev/null < /dev/null &"
	cmd = "python "+ local_path + " " + str(server_data) + " &> /dev/null < /dev/null &"
        print "command to run : ",cmd
        result = run(cmd, shell=False, pty=False)
        print result.return_code
    if result.return_code != 0:
        print "************ : ",result.stdout.splitlines()[-1].split("Exception: ")[-1]
else:
    try:
        subprocess.call(['sshpass', '-p', pwd, 'scp', '-o', ' UserKnownHostsFile=~/.ssh/known_hosts', '-o', 'StrictHostKeyChecking=no', './' + filename, username+'@'+hostname + ':~/.'])
        process = subprocess.Popen(['sshpass', '-p', pwd, 'ssh', username+'@'+hostname, 'python', filename, str(server_data)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    except Exception, excep:
        print excep
#conn, addr = listen_socket.accept()
#input_data = get_socket_data(conn)
#conn.send("end")
#current_command = input_data[:input_data.find("|")]
#print current_command
#listen_socket.close()
