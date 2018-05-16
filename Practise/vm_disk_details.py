import atexit
import sys
import traceback
import warnings
from datetime import timedelta, datetime
import base64
from pyVmomi import vim
from pyVim import connect

IS_ENCODED = False


def decode_string(enc_string):
    try:
        return base64.b64decode(enc_string)
    except TypeError as e:
        print("Decoding string error :%s" % str(e))
        raise Exception(e)


class VCenterServerMonitor:
    """Connect to vcenter."""

    def __init__(self, vc_details):
        self.vcsa_ip = vc_details["info"]["ip_addr"]
        self.vcsa_user = vc_details["info"]["username"]

        password = vc_details["info"]["password"]
        self.vcsa_passwd = decode_string(password) if IS_ENCODED else password

        self.vcsa_port = vc_details["info"]["port"]

    def connect_vc(self, node_type=None):
        warnings.simplefilter('ignore')
        print "**** Try to conenct to the vCenter ***"
        try:
            self.si = connect.SmartConnect(host=self.vcsa_ip,
                                           user=self.vcsa_user,
                                           pwd=self.vcsa_passwd,
                                           port=self.vcsa_port)
            atexit.register(connect.Disconnect, self.si)
            content = self.si.RetrieveContent()
            if node_type == 'vcenter':
                # Validation whether the details are ESXi or Vcenter Details
                if content.about.apiType == 'HostAgent':
                    print "Connection Error"
                    raise Exception("CONNECTION_ERROR")
        except vim.fault.InvalidLogin:
            print "INVALID_CREDENTIAL"
            raise Exception("INVALID_CREDENTIAL")
        except ConnectionError:
            print "Connection Error"
            raise Exception("Connection Error")
        except Exception as exc:
            if (isinstance(exc, vim.fault.HostConnectFault) and
                    '[SSL: CERTIFICATE_VERIFY_FAILED]' in exc.msg):
                try:
                    import ssl
                    default_context = ssl._create_default_https_context
                    create_context = ssl._create_unverified_context
                    ssl._create_default_https_context = create_context
                    self.si = connect.SmartConnect(host=self.vcsa_ip,
                                                   user=self.vcsa_user,
                                                   pwd=self.vcsa_passwd,
                                                   port=self.vcsa_port)
                    ssl._create_default_https_context = default_context
                except vim.fault.InvalidLogin:
                    print "ERR_CONNECTING"
                    raise Exception("INVALID_CREDENTIAL")
                except ConnectionError:
                    print "ConnectionError"
                    raise Exception("ConnectionError")
                except Exception as exc1:
                    print str(exc1)
                    raise Exception(exc1)
            else:
                raise Exception(exc)

    def disconnect_vc(self):
        """Disconnect the connection"""
        connect.Disconnect(self.si)


def get_vm_info(vc_obj, vm_uuid):
    print "** Get the vm details **"
    """
    function to find the information of particular vm
    """
    try:
        vm_info = {}
        content = vc_obj.si.RetrieveContent()
        search_index = vc_obj.si.content.searchIndex

        vm = None
        if vm_uuid:
            vm = search_index.FindByUuid(None, vm_uuid, True, True)

        if not vm:
            print "VM not found"
            return {}

        # Collect the vm details
        vm_info['name'] = vm.name
        vm_info['host'] = vm.summary.runtime.host.name
        vm_info['power_state'] = vm.summary.runtime.powerState
        vm_info['virtual_disk'] = []
        # get the disk size
        for device in vm.config.hardware.device:
            if type(device).__name__ == 'vim.vm.device.VirtualDisk':
                disk_summ = {'label': device.deviceInfo.label, 'summary': device.deviceInfo.summary.split(" ")[0],
                             'file_name': device.backing.fileName.split("] ")[1]}
                if device.backing.thinProvisioned:
                    disk_summ['provisioning_type'] = "Thin"
                else:
                    disk_summ['provisioning_type'] = "Thick"
                datastore = device.backing.fileName.split("[")[1]
                disk_summ['datastore'] = datastore.split("]")[0]
                if device.capacityInBytes:
                    size_gb = round((float(device.capacityInBytes) / 1024 / 1024 / 1024), 2)
                    disk_summ['capacity_in_gb'] = size_gb
                elif device.capacityInKB:
                    size_gb = round((float(device.capacityInKB) / 1024 / 1024), 2)
                    disk_summ['capacity_in_gb'] = size_gb
                vm_info['virtual_disk'].append(disk_summ)
        print "--> VM Info : %s" % str(vm_info)
        return vm_info
    except Exception as e:
        ex_type, ex, tb = sys.exc_info()
        print (traceback.print_tb(tb))
        print str(e)
        return {}


def get_disk_stats(data):
    prog_startTime = datetime.now()

    try:
        vm_uuid = data['vm_uuid']
        # Connect to vcenter and fetch VM's disk details
        vc_obj = VCenterServerMonitor(data)
        vc_obj.connect_vc(node_type='vcenter')
    except Exception as e:
        print str(e)
        raise Exception(e)

    vm_disk_stats = get_vm_info(vc_obj, vm_uuid)

    vc_obj.disconnect_vc()

    if not vm_disk_stats:
        print "vm disk is not found"
        raise Exception("vm disk is not found")
    return vm_disk_stats


disk_data = {"info": {}}
disk_data["info"]["username"] = "root"
disk_data["info"]["password"] = "vmware"
disk_data["info"]["ip_addr"] = "10.11.1.162"
disk_data["info"]["port"] = "443"
disk_data['vm_uuid'] = "50012b83-31fc-3e9c-042d-96c9e047cc37"
disk_detail = get_disk_stats(disk_data)
print "--> Disk Detail : %s" % str(disk_detail)
