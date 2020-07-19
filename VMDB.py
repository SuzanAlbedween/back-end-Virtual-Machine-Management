import pandas
import pyodbc
import pandas as pd
import uuid

def InsertVM(UniqueiD,VMName, Ip, OperatingSystem, Status, Ram, Storage, LifeTime,IdUser):
    conn = pyodbc.connect(Driver='{SQL Server}', Server='DESKTOP-5BHLCG8', Database='vmm', Trusted_Connection='yes')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM [vm]')
    SQLTASK = ("INSERT INTO [vm]( UniqueiD,VMName,Ip,OperatingSystem,Status,Ram,Storage,LifeTime,IdUser) VALUES (?,?,?,?,?,?,?,?,?)")
    with cursor.execute(SQLTASK, UniqueiD,VMName,Ip,OperatingSystem,Status,Ram,Storage,LifeTime,IdUser):
        print('Successfully Inserted data for VM!')
    conn.commit()
    conn.close()

def Deletvm_DB(iduser,vmname):
    conn = pyodbc.connect(Driver='{SQL Server}', Server='DESKTOP-5BHLCG8', Database='vmm', Trusted_Connection='yes')
    cursor = conn.cursor()
    status=False
    SQLTASK = "DELETE FROM [vm] WHERE VMName= ? AND IdUser= ? "
    with cursor.execute(SQLTASK,vmname,iduser):
        print('Successfully Deleted!')
        status=True
    conn.commit()
    return status
def Extend_DB(iduser,vmname,newdate):
    conn = pyodbc.connect(Driver='{SQL Server}', Server='DESKTOP-5BHLCG8', Database='vmm', Trusted_Connection='yes')
    cursor = conn.cursor()
    print('Updating Lifetime of  Virtual Machine  in DataBase...')
    status = False
    SQLTASK = "UPDATE [vm] SET LifeTime = ? WHERE  VMName= ? AND IdUser= ?  "
    with cursor.execute(SQLTASK,newdate, vmname, iduser):
        print('Successfully Updated!')
        status = True
    conn.commit()
    return status
def GetLifetime_Per_vm(iduser,vmname):
    conn = pyodbc.connect(Driver='{SQL Server}', Server='DESKTOP-5BHLCG8', Database='vmm', Trusted_Connection='yes')
    SQLTASK = "select LifeTime from [vm] WHERE  VMName= ? AND IdUser= ? "
    res = conn.execute(SQLTASK, vmname,iduser)
    lifetime = res.fetchone()
    print(lifetime[0])
    return lifetime[0]
def GetAllVmDB(iduser,searchtype="."):
    conn = pyodbc.connect(Driver='{SQL Server}', Server='DESKTOP-5BHLCG8', Database='vmm', Trusted_Connection='yes')
    print("Get All VM DATA from DataBase...  ")
    if(searchtype=="."):
        SQLTASK = "SELECT * FROM [vm] WHERE IdUser= ? "
        try:
            res = conn.execute(SQLTASK, iduser)
            vms = list(res)
            print(vms)
            return vms
        except pyodbc.DatabaseError as err:
            print("Error Occurred while fetching VM Details", err)
            return None
        conn.close()
    else:
        SQLTASK = "SELECT * FROM [vm] WHERE IdUser= ? AND VMName= ?"
        try:
            res = conn.execute(SQLTASK, iduser,searchtype)
            vms = list(res)
            print(vms)
            return vms
        except pyodbc.DatabaseError as err:
            print("Error Occurred while fetching VM Details", err)
            return None
        conn.close()








