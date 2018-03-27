import atexit
import sys
import traceback
import warnings
from datetime import timedelta, datetime


class VCenterServerMonitor:
    """Connect to vcenter."""

    def __init__(self, vc_details):
        self.vcsa_ip = vc_details[INFO][IP_ADDR]
        self.vcsa_user = vc_details[INFO][UNAME]

        password = vc_details[INFO][PASSWORD]
        self.vcsa_passwd = decode_string(password) if IS_ENCODED else password

        self.vcsa_port = vc_details[INFO][PORT]
        self.metricId_list = []

    def connect_vc(self, node_type=None):
        warnings.simplefilter('ignore')
        try:
            self.si = connect.SmartConnect(host=self.vcsa_ip,
                                           user=self.vcsa_user,
                                           pwd=self.vcsa_passwd,
                                           port=self.vcsa_port)
            atexit.register(connect.Disconnect, self.si)
            content = self.si.RetrieveContent()
            if node_type == VCENTER:
                # Validation whether the details are ESXi or Vcenter Details
                if content.about.apiType == 'HostAgent':
                    raise Exception(CONNECTION_ERROR)
        except vim.fault.InvalidLogin:
            log_msg = ERR_CONNECTING
            print "INVALID_CREDENTIAL"
            raise Exception("INVALID_CREDENTIAL")
        except ConnectionError:
            print "Connection Error"
            raise Exception(Connection Error)
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
                    raise Exception(exc1)
            else:
                raise Exception(exc)

def get_vm_info(vc_obj, vm_uuid):
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

        #Collect the vm details
        vm_info['name'] = vm.name
        vm_info['host'] = vm.summary.runtime.host.name
        vm_info['power_state'] = vm.summary.runtime.powerState
        vm_info['virtual_disk'] = []
        #get the disk size
        for device in vm.config.hardware.device:
            if type(device).__name__ == 'vim.vm.device.VirtualDisk':
                disk_summ = {}
                disk_summ['label'] = device.deviceInfo.label
                disk_summ['summary'] = device.deviceInfo.summary.split(" ")[0]
                disk_summ['file_name'] = device.backing.fileName.split("] ")[1]
                if device.backing.thinProvisioned:
                    disk_summ['provisioning_type'] = "Thin"
                else:
                    disk_summ['provisioning_type'] = "Thick"
                datastore = device.backing.fileName.split("[")[1]
                disk_summ['datastore'] = datastore.split("]")[0]
                if device.capacityInBytes:
                    size_gb = round((float(device.capacityInBytes)/1024/1024/1024), 2)
                    disk_summ['capacity_in_gb'] = size_gb
                elif device.capacityInKB:
                    size_gb = round((float(device.capacityInKB)/1024/1024), 2)
                    disk_summ['capacity_in_gb'] = size_gb
                vm_info['virtual_disk'].append(disk_summ)
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
        #Connect to vcenter and fetch VM's disk details
        vc_obj = VCenterServerMonitor(data)
        vc_obj.connect_vc(node_type=VCENTER)
    except Exception as e:
        print str(e)
        raise MonitorException(ESXISTATERROR)

    vm_disk_stats = get_vm_info(vc_obj, vm_uuid)

    vc_obj.disconnect_vc()

    if not vm_disk_stats:
        raise MonitorException(ESXISTATERROR)
    return vm_disk_stats