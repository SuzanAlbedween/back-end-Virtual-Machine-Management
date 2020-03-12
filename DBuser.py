import pyodbc
import pandas as pd
import uuid


def CreatNewUser( UserName, PassWord):
    conn = pyodbc.connect(Driver='{SQL Server}', Server='DESKTOP-5BHLCG8', Database='users', Trusted_Connection='yes')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM [user]')
    UniqueiD = uuid.uuid4()
    print(UniqueiD)
    SQLTASK = ("INSERT INTO [user](ID,name,password) VALUES (?,?,?)")
    with cursor.execute(SQLTASK,UniqueiD,UserName,PassWord):
        print('Successfully Inserted!')
    conn.commit()
    conn.close()

def CheckLogIn(UserName, PassWord):
    conn = pyodbc.connect(Driver='{SQL Server}', Server='DESKTOP-5BHLCG8', Database='users', Trusted_Connection='yes')
    print('Searching for this user ....')
    SQLTASK = "select * from [user] WHERE name = ? AND password = ?"
    res=conn.execute(SQLTASK, UserName,PassWord)
    userres=list(res)
    if(len(userres)>0):
        print('Successfully !')
        return True
    else:
        return False


