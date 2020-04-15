import atexit
import math

from pyVim import connect
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
from vmwc import VMWareClient

#s=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
#s.verify_mode=ssl.CERT_NONE
#si= SmartConnect(host="192.168.75.128", user="root", pwd="1234567",sslContext=s)
#my_cluster=si.content
MBFACTOR = float(1 << 20) #MB
# delete_vm_by_name:
def CreateVM(host,username,password,name,OS,Ram , Storage,PathISO ,Status ):
    with VMWareClient(host, username, password) as client:
        vm = client.new_virtual_machine(name=name, cpus=2, ram_mb=Ram, disk_size_gb=Storage,operating_system_type=OS)
        disk=PathISO
        vm.configure_bios(boot_delay=5000, boot_order=['network', 'disk'])
        if(Status=="PowerOn"):
            vm.power_on()
        else:
            vm.power_off()
    print(vm.uuid)
    return vm
def delete_vm_by_name(host, username, password,vmname):
    status =False
    with VMWareClient(host, username, password) as client:
        for vm in client.get_virtual_machines():
            if (vm.name == vmname) :
                if(vm.is_powered_on()==True):
                    print('power OFF  "{}" ...'.format(vm.name))
                    vm.power_off()
                vm.delete()
                status = True
                print('Deleted  "{}" ...'.format(vm.name))
    if status != True :
        print("No virtual machines were found with this name!!!")
    return status
def ViewAllVMByName(host, username, password):
    status = 0
    all_vm=[]
    with VMWareClient(host, username, password) as client:
        for vm in client.get_virtual_machines():
            print("VM name:",vm.name)
            all_vm.append(vm.name)
            status = 1

    if status != 1 :
        print("No virtual machines were found with this name!!!")
    return all_vm
def GetManagedObject(content, vimtype):
        # Return an object by type
        return [item for item in content.viewManager.CreateContainerView(content.rootFolder, [vimtype], recursive=True).view]
def CheckResourc(host, rmemoryGB, rspaceGB, datastore):
        #host: HostSystem obj
        #datastore: Datastore obj
        #rmemoryGB, rspaceGB: The resource required for VM
        try:
            summary = host.summary
            stats = summary.quickStats
            hardware = host.hardware
            memoryCapacityInMB = hardware.memorySize / MBFACTOR
            memoryCapacityGB = memoryCapacityInMB / 1024
            memoryUsage = (stats.overallMemoryUsage) / 1024
            print((math.ceil(memoryCapacityGB) - memoryUsage))
            if ((math.ceil(memoryCapacityGB) - memoryUsage) < rmemoryGB):
                return False
        except Exception as error:
            print("Unable to access information for host: ", host.name)
            print(error)
            return

        try:
            summary = datastore.summary
            freeSpaceMB = summary.freeSpace / MBFACTOR
            if ((freeSpaceMB / 1024) < rspaceGB):
                return False
        except Exception as error:
            print("Unable to access summary for datastore: ", datastore.name)
            print(error)

        return True
def main():
    host = "192.168.75.128"
    username = "root"
    password = "1234567"
    #view_vm_by_name(host, username, password)
    #CreateVM(host, username, password, "vm5", "ubuntuGuest", 1024, 20, 'C:\\Users\\suzi2\\Desktop\\ubuntu.iso', "PowerOn")
   # delete_vm_by_name(host, username, password, "Vvm3")
    #si = SmartConnect(host, user=username,  pwd=password, port=int(443))


if __name__ == '__main__':
    main()