import sqlite3
import config

class MyDb:
    
    def __init__(self):
        self.conn=sqlite3.connect('Hotel.db')

    def verify(self,user,pwd):
        c=self.conn.cursor()
        c.execute(f'SELECT * FROM USERS WHERE ID="{user}" AND PASS ="{pwd}"')
        return True if c.fetchone() is not None else False

    def get_type(self,ID):
        c=self.conn.cursor()
        c.execute(f'SELECT TYPE FROM USERS WHERE ID="{ID}"')
        return c.fetchone()[0]

    def get_name(self,id):
        c=self.conn.cursor()
        c.execute(f'SELECT NAME FROM USERS WHERE ID="{id}"')
        return c.fetchone()[0]
    
    def change_password(self,id,pwd):
        c=self.conn.cursor()
        c.execute(f'UPDATE USERS SET PASS="{pwd}" WHERE ID = "{id}"')
        self.conn.commit()
    
    def log_event(self,type,id,data,event):
        c=self.conn.cursor()
        c.execute(f'INSERT INTO LOGS VALUES("{type}","{id}","{data}","{event}")')
        self.conn.commit()
    
    def get_history(self,id):
        c=self.conn.cursor()
        c.execute(f'SELECT DATA FROM LOGS WHERE ID="{id}"')
        ordr = ''
        for i in c.fetchall():
            ordr+='****\n'+i[0]+'\n*****'
        return ordr
    
    def search(self,text,Type=None):
        c=self.conn.cursor()
        if Type is not None:
            if 'RNO' in text:
                c.execute(f'SELECT NAME , ID, TYPE FROM USERS WHERE TYPE="GUEST" AND ID = "{text}"')
            else:
                c.execute(f'SELECT NAME , ID, TYPE FROM USERS WHERE TYPE="GUEST" AND NAME = "{text}"')
        else:
            if 'RNO' in text or 'E0' in text:
                c.execute(f'SELECT NAME , ID, TYPE FROM USERS WHERE ID = "{text}"')
            else:
                c.execute(f'SELECT NAME , ID, TYPE FROM USERS WHERE NAME = "{text}"')
        ordr = ''
        for i in c.fetchall():
            ordr+='****\n'
            for j in i:
                ordr+=j+" "
            ordr+='\n*****'
        return ordr

    def available(self):
        c=self.conn.cursor()
        c.execute(f'SELECT ID FROM ROOMS WHERE EMPTY = "TRUE"')
        return c.fetchone()

    def checkin(self,room,name):
        c=self.conn.cursor()
        c.execute(f'UPDATE ROOMS SET NAME="{name}", EMPTY="FALSE" WHERE ID = "{room}"')
        c.execute(f'INSERT INTO USERS VALUES("GUEST","{name}","{room}","12345")')
        self.conn.commit()
    
    def checkout(self,room,name):
        c=self.conn.cursor()
        c.execute(f'UPDATE ROOMS SET NAME="", EMPTY="TRUE" WHERE ID = "{room}"')
        c.execute(f'DELETE FROM USERS WHERE NAME="{name}" AND ID ="{room}"')
        self.conn.commit()

    def hire(self,eid,name):
        c=self.conn.cursor()
        c.execute(f'INSERT INTO USERS VALUES("EMP","{name}","{eid}","12345")')
        self.conn.commit()

    def fire(self,eid,name):
        c=self.conn.cursor()
        c.execute(f'DELETE FROM USERS WHERE NAME="{name}" AND ID ="{eid}"')
        self.conn.commit()

    def info(self):
        c=self.conn.cursor()
        c.execute(f'SELECT COUNT(EMPTY) FROM ROOMS WHERE EMPTY="TRUE"')
        rc=c.fetchone()[0]
        c.execute(f'SELECT COUNT(ID) FROM USERS WHERE TYPE="EMP"')
        ec=c.fetchone()[0]
        return f'{self.get_name(config.current)}\n{config.current}\nAvailable rooms {rc}/5\nNo of Employees {ec}'
    
    def show_logs(self):
        c=self.conn.cursor()
        c.execute("SELECT EVENT FROM LOGS")
        logs=''
        for i in c.fetchall():
            logs+=f'{i[0]}\n'
        return logs