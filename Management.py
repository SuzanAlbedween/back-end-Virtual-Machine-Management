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
import json
from DBuser import *
from ESXI import *
from VMDB import *


class VM:
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
    print("this is http in angular is get \n",VMName,OS,ram,storage,lifetime,pwd,username,host,pathiso,Status)
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
        mangementobjs.append(VM(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]))
    print(mangementobjs[0].VMName)
    return mangementobjs


def GetAllVm(host,username, password,typesearch):
    res=[]
    data={}
    cutvm=[]
    iduser=GetUserID(username,password)
    common_vms=[] #Virtual machines that are at the DB and also in esxi
    vms_db = GetAllVmDB(iduser, typesearch)
    vms_ESXI = ViewAllVMByName(host, username, password)
    for i in vms_db:
        for j in vms_ESXI:
            if (i[1] == j):
                cutvm = [x for x in i]
                common_vms.append(VM(cutvm[0],cutvm[1],cutvm[2],cutvm[3],cutvm[4],cutvm[5],cutvm[6],cutvm[7],cutvm[8]));
    print("common vm's",common_vms)
    for c in common_vms:
        print("this is",c)
        res.append(c.__dict__)
    print(res)
    return res








