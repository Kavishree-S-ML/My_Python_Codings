vm = {}
vm["host"] = {}
vm["host"]["vms"] = []
for i in range(0, 2):
    vm_detail = {"vm": "vm{0}".format(str(i)), 'filename': []}
    for j in range(0, 2):
        vm_detail["filename"].append("disk_file" + str(i))
    vm["host"]["vms"].append(vm_detail)
print("vm : %s" % str(vm))

"""
   storing in separate string
"""
vm_name = [v['vm'] for v in vm['host']['vms']]
filename = [v['filename'] for v in vm['host']['vms']]
print("VMs : %s" % str(vm_name))
print("Files : {}".format(str(filename)))

for i in range(0, len(vm_name)):
    vm_detail1 = vm_name[i] 
    for j in range(0, len(filename[i])):
        vm_detail1 = vm_name[i] + ":" + filename[i][j]
        if i == 0 and j == 0:
            vm_detail = vm_detail1
        else:
            vm_detail = vm_detail + "," +vm_detail1
print "*********************"
print "VM details - {0}".format(vm_detail)
print "********************"
