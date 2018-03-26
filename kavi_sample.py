import subprocess
import sys
hostname = "10.11.0.81"
username = "root"
pwd = "maplelabs"
local_path = "./test_socket_client.py"
filename = "test_socket_client.py"

server_data = []
server_info = {}
server_info['current_ip'] = "10.11.0.161"
server_info['port'] = 12678
server_data.append(server_info)
print server_data

try:
    print local_path
    import os
    cwd = os.getcwd()
    print cwd
    local_path = cwd + "/" + filename
    print local_path
    #subprocess.call(['sshpass', '-p', pwd, 'scp', '-o', ' UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no', local_path, username+'@'+hostname + ':~/.'])
    print "\n 778465745"
    process = subprocess.Popen(['sshpass', '-p', pwd, 'ssh', username+'@'+hostname, 'python', './' + filename, str(server_data)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
except Exception as excep:
    print "\n **********"
    print str(excep)
