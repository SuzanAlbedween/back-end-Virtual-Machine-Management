import pandas
import pyodbc
import pandas as pd
import uuid


def CreatNewUser( UserName, PassWord):
    conn = pyodbc.connect(Driver='{SQL Server}', Server='DESKTOP-5BHLCG8', Database='vmm', Trusted_Connection='yes')
    cursor = conn.cursor()
    #cursor.execute('SELECT * FROM [user]')
    UniqueiD = uuid.uuid4()
    print(UniqueiD)
    SQLTASK = ("INSERT INTO [users](id,name,password) VALUES (?,?,?)")
    with cursor.execute(SQLTASK,UniqueiD,UserName,PassWord):
        print('Successfully Inserted!')
    conn.commit()
    conn.close()

def CheckLogIn(UserName, PassWord):
    conn = pyodbc.connect(Driver='{SQL Server}', Server='DESKTOP-5BHLCG8', Database='vmm', Trusted_Connection='yes')
    print('Searching for this user ....')
    SQLTASK = "select * from [users] WHERE name = ? AND password = ?"
    res=conn.execute(SQLTASK, UserName,PassWord)
    userres=list(res)
    if(len(userres)>0):
        print('Successfully !')
        return True
    else:
        return False

def GetUserID(username,password):
    conn = pyodbc.connect(Driver='{SQL Server}', Server='DESKTOP-5BHLCG8', Database='vmm', Trusted_Connection='yes')
    SQLTASK = "select id from [users] WHERE name = ? AND password = ?"
    res = conn.execute(SQLTASK, username, password)
    data= res.fetchone()
    print(data[0])
    return data[0]

def deleteuser(name ,password):
    conn = pyodbc.connect(Driver='{SQL Server}', Server='DESKTOP-5BHLCG8', Database='vmm',Trusted_Connection='yes')
    cursor = conn.cursor()
    SQLTASK = "DELETE FROM [users] WHERE name= ? AND id= ? "
    with cursor.execute(SQLTASK, name, password):
        print('Successfully Deleted!')
    conn.commit()



#2dc09598-64dc-40c7-b50f-2ce4ed73cdc0
#2DC09598-64DC-40C7-B50F-2CE4ED73CDC0

#CreatNewUser("root", "1234567")
#GetUserID("root", "1234567")
#deleteuser("root", "12db4b8b-abc2-4e49-867b-6ef12dc89e98")
