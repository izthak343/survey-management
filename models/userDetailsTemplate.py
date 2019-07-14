from db import mysql


class UserDetailsTemplateModel():
    def __init__(self,attr,name,type):
        self.id=0
        self.attr=attr
        self.name=name
        self.type = type



    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if(UserDetailsTemplateModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        input=(self.name,self.attr,self.type)
        query= """INSERT INTO userDetailsTempate (attr,name,type) VALUES (%s,%s,%s)"""
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM userDetailsTempate ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()


    def update_db(self):
        cur = mysql.get_db().cursor()
        query = """Update userDetailsTempate set attr = %s,name = %s,type = %s where id = %s"""
        input=(self.attr ,self.name ,self.type,self.id)
        cur.execute(query,input)
        mysql.get_db().commit()
        cur.close()


    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE userDetailsTempate (id Integer(6) PRIMARY KEY AUTO_INCREMENT,attr VARCHAR(1024),name VARCHAR(1024),type Integer(6))"
        cur.execute(query)
        cur.close()


    @classmethod
    def drop_db(self):
        cur = mysql.get_db().cursor()
        sql = "DROP TABLE userDetailsTempate"
        cur.execute(sql)
        cur.close()

    @classmethod
    def delete_all_rows(self):
        cur = mysql.get_db().cursor()
        sql = "TRUNCATE TABLE userDetailsTempate"
        cur.execute(sql)
        cur.close()


    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from userDetailsTempate where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            UserDetails=UserDetailsTemplateModel(row[1],row[2],row[3],row[4])
            UserDetails.id=row[0]
            cur.close()
            return UserDetails
        cur.close()
        return False

    @classmethod
    def find_by_attr(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from userDetailsTempate where attr = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            UserDetails=UserDetailsTemplateModel(row[1],row[2],row[5],row[4])
            UserDetails.id=row[0]
            cur.close()
            return UserDetails
        cur.close()
        return False

    @classmethod
    def find_all_UserDetailsTempate(cls):
        cur = mysql.get_db().cursor()
        query = """select * from userDetailsTempate"""
        cur.execute(query)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            UserDetailsArry=[]
            for row in rows:
                UserDetails=UserDetailsTemplateModel(row[1],row[2],row[3])
                UserDetails.id=row[0]
                UserDetailsArry.append(UserDetails)
            return UserDetailsArry
        cur.close()
        return False
