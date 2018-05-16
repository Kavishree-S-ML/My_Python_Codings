"""
with open("/etc/rsyslog.conf", "a") as f:
	f.writelines("if $app-name contains 'collectd' then {\nstop\n}")
f.close()
"""
from fabric.api import (env, run, execute, settings, sudo, shell_env)
from fabric.contrib.files import append, exists
from fabric.state import output

output['everything'] = False
username = "root"
password = "deepinsight"
def sys_config():
	with settings(user=username, password=password):
	    try:
		cmd = "sed -i '1i if $app-name contains \'collectd\' then {\\nstop\\n}' /etc/rsyslog.conf"
		print cmd
		result = run(cmd, timeout=self.timeout)
		print result
		return True
	    except Exception:
        	return False
result = execute(sys_config, hosts="10.11.100.12")
print result
