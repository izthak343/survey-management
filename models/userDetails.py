from db import mysql


class UserDetailsModel():
    def __init__(self,value,attrParent,userId):
        self.id=0
        self.attrParent=attrParent
        self.value=value
        self.userId = userId



    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if(UserDetailsModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        input=(self.value,self.attrParent,self.userId)
        query= """INSERT INTO userDetails (value,attrParent,userId) VALUES (%s,%s,%s)"""
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM userDetails ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()

    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE userDetails (id Integer(6) PRIMARY KEY AUTO_INCREMENT,value VARCHAR(1024),attrParent VARCHAR(1024),userId Integer(6))"
        cur.execute(query)
        cur.close()


    @classmethod
    def drop_db(self):
        cur = mysql.get_db().cursor()
        sql = "DROP TABLE userDetails"
        cur.execute(sql)
        cur.close()


    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from userDetails where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            UserDetails=UserDetailsModel(row[1],row[2],row[3],row[4])
            UserDetails.id=row[0]
            cur.close()
            return UserDetails
        cur.close()
        return False

    @classmethod
    def find_by_attrParent(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from userDetails where attrParent = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            UserDetails=UserDetailsModel(row[1],row[2],row[5],row[4])
            UserDetails.id=row[0]
            cur.close()
            return UserDetails
        cur.close()
        return False

    @classmethod
    def find_all_UserDetails(cls):
        cur = mysql.get_db().cursor()
        query = """select * from userDetails"""
        cur.execute(query)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            UserDetailsArry=[]
            for row in rows:
                UserDetails=UserDetailsModel(row[1],row[2],row[3])
                UserDetails.id=row[0]
                UserDetailsArry.append(UserDetails)
            return UserDetailsArry
        cur.close()
        return False
