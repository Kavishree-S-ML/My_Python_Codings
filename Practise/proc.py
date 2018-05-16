import psutil
service = "apache"
print psutil.process_iter(attrs=['pid', 'name', 'username'])
for proc in psutil.process_iter(attrs=['pid', 'name', 'username']):
        # Java processes
	print proc.info
        if service in ["elasticsearch"]:
            if proc.info.get("name") == "java" and proc.info.get("username") == service:
                processID = proc.info.get("pid")
                break
        # Non java processes
        elif service in str(proc.info.get("name")):
            processID = proc.info.get("pid")
            break

