import ssl
import atexit
import math
from datetime import datetime
from datetime import timedelta
from pyVim import connect
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
from pyVim.connect import SmartConnect
from vmwc import VMWareClient

from DBuser import *
from ESXI import *
from VMDB import *


class Management:
    def __init__(self,UniqueiD, VMName, Ip, OperatingSystem, Status, Ram, Storage, LifeTime,iduser):
        self.UniqueiD = UniqueiD
        self.VMName = VMName
        self.Ip = Ip
        self.OperatingSystem = OperatingSystem
        self.Status = Status
        self.Ram = Ram
        self.Storage = Storage
        self.LifeTime = LifeTime
        self.IdUser=iduser


def Create(VMName,OS,ram,storage,lifetime,pwd,username,host,pathiso,Status):
    #**************************setting***************************
    s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    s.verify_mode = ssl.CERT_NONE
    si = SmartConnect(host=host, user=username, pwd=pwd, sslContext=s)
    content = si.RetrieveContent()
    datacenter = content.viewManager.CreateContainerView(content.rootFolder, [vim.Datacenter], recursive=True).view
    hostSysteminfo = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], recursive=True).view[0]
    datastoreinfo = content.viewManager.CreateContainerView(content.rootFolder, [vim.Datastore], recursive=True).view[0]
    #***********************************************************************
    res=CheckResourc(hostSysteminfo, ram, storage, datastoreinfo)
    if(res==True):
        print(res)
        vm=CreateVM(host, username, pwd, VMName, OS, ram*1024, storage, pathiso, Status)
        #get ip for vm TODO
        ip=None
        userid=GetUserID(username,pwd)
        vmdate=(datetime.now() + timedelta(days=lifetime)).date()
        virtualmachine=Management(vm.uuid,VMName,ip,OS,Status,ram,storage,vmdate,userid)
        InsertVM(virtualmachine.UniqueiD, virtualmachine.VMName,str( virtualmachine.Ip), virtualmachine.OperatingSystem,virtualmachine.Status,str(virtualmachine.Ram), str(virtualmachine.Storage),str( virtualmachine.LifeTime), str(virtualmachine.IdUser))
        return True
    else:
        print("It is impossible to produce such a virtual machine because there are insufficient resources !!!")
        return False



def DeleteVM(vmname,host,username,password):
    esxi_status=delete_vm_by_name(host, username, password, vmname)
    ID=GetUserID(username, password)
    db_status=Deletvm_DB(ID,vmname)
    if(esxi_status==True and db_status==True):
        print("Successfully Deleted from DB and ESXI ! ")
        return True
    else:
        if(esxi_status==False and db_status==True):
            print("Successfully Deleted from DB ! ")
        elif(esxi_status==True and db_status==False):
            print("Successfully Deleted from ESXI ! ")
        else:
            print("Deletion failed on both sides  ! ")
        return False

def ExtendVM(username, password,vmname,newdate):
    iduser=GetUserID(username,password)
    status=Extend_DB(iduser, vmname, newdate)
    if(status==True):
        print('Successfully Updated!')
        return True
    else:
        print("Update failed !")
        return False
def CheckVMS(vms_db,vms_esxi):
    vms_justin_esxi = []
    vms_justin_db = []
    both=[]

    if(len(vms_db)>len(vms_esxi)):
        for item in vms_esxi:
            flage=False
            for i in vms_db[1]:
                if(i==item):
                    both=vms_db[i]
                    flage=True

def ConverttoManagementObj(vmsdb):
    mangementobjs=[]
    for i in vmsdb:
        mangementobjs.append(Management(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))
    print(mangementobjs[0].VMName)
    return mangementobjs


def GetAllVm(host,username, password,typesearch):
    iduser=GetUserID(username,password)
    vms_exist=[]
    info_vms=[]
    vms_db = GetAllVmDB(iduser, typesearch)
    vms_ESXI = ViewAllVMByName(host, username, password)
    for i in vms_db:
        for j in vms_ESXI:
            if (i[1] == j):
                vms_exist.append(i[1])
                vms_ESXI.remove(j)
                vms_db.remove(i)
    info_vms.append(vms_exist)
    # vms_missing_from_db
    info_vms.append(vms_ESXI)
    # vms_missing_from_esxi
    info_vms.append(vms_db)
    print("print all info from managment ",info_vms)
    return info_vms









#res=ExtendVM("root","1234567","vm4","30-8-2020")
#print(res)
   # CreateVM(host, username, password, "vm5", "ubuntuGuest", 1024, 20, 'C:\\Users\\suzi2\\Desktop\\ubuntu.iso',  "PowerOn")
#tt=Create("vm88", "ubuntuGuest","PowerOn", 2, 30, 60, "1234567", "root","192.168.75.128", 'C:\\Users\\suzi2\\Desktop\\ubuntu.iso', "PowerOn")
#print(tt)
#res=DeleteVM("vm88","192.168.75.128","root","1234567")
#print("******",res)
#GetAllVm("192.168.75.128","root", "1234567",".")