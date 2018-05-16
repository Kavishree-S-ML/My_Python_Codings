import subprocess
import platform

def get_os():
    """
    return os name
    :return:
    """
    return platform.dist()[0].lower()

def run_cmd(cmd, shell=True):
    """
    run a command don't check output
    :param cmd:
    :param shell:
    :return:
    """
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
        (out, err) = p.communicate()
        return out
    except subprocess.CalledProcessError as error:
        print >> sys.stderr, "Error: {0}".format(error)
        print "error ignored"
        return

log_file = ""
log_path = ""
os = get_os()
print "OS :", os
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
if os == "ubuntu" or os == "debian":
    cmd = "pg_lsclusters | awk '{ print $7 }'"
elif os == "centos":
    cmd = "ps auxw |  grep postgres | grep -- -D | awk '{ print $13 }'"
result = run_cmd(cmd)
if result:
    for line in result.splitlines():
        log_path = line

if os == "ubuntu" or os == "debian":
    log_file = log_path
elif os == "centos":
    for day in days:
        log_file = ','.join([log_path + "pg_log/Postgres-"+day+".log", log_file])
print "Log path : ",log_file
