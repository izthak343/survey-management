from db import mysql


class ApplicationModel():
    def __init__(self,realName,falseName,categoryId,picture1,picture2):
        self.id=0
        self.realName=realName
        self.falseName=falseName
        self.categoryId=categoryId
        self.picture1=picture1
        self.picture2=picture2


    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if( ApplicationModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        query= """INSERT INTO application (realName,falseName,categoryId,picture1,picture2) VALUES (%s, %s,%s,%s,%s)"""
        input=(self.realName,self.falseName,self.categoryId,self.picture1,self.picture2)
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM application ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()

    def update_db(self):
        cur = mysql.get_db().cursor()
        query = """Update application set realName = %s,falseName = %s,categoryId = %s,picture1 = %s,picture2 = %s where id = %s"""
        input=(self.realName,self.falseName,self.categoryId,self.picture1,self.picture2,self.id)
        cur.execute(query,input)
        mysql.get_db().commit()
        cur.close()


    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from application where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            application=ApplicationModel(row[1],row[2],row[3],row[4],row[5])
            application.id=row[0]
            return application
        cur.close()
        return False


    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE application (id Integer(6) PRIMARY KEY AUTO_INCREMENT,realName VARCHAR(1024),falseName VARCHAR(1024),categoryId Integer(6),picture1 VARCHAR(1024),picture2 VARCHAR(1024))"
        cur.execute(query)
        cur.close()

    @classmethod
    def drop_db(self):
        cur = mysql.get_db().cursor()
        stmt = "SHOW TABLES LIKE 'application'"
        cur.execute(stmt)
        result = cur.fetchone()
        if result:
            sql = "DROP TABLE application"
            cur.execute(sql)
            cur.close()

    @classmethod
    def find_by_categoryId(cls, _categoryId):
        cur = mysql.get_db().cursor()
        query = """select * from application where categoryId = %s"""
        cur.execute(query,_categoryId)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            applicationArry=[]
            for row in rows:
                application=ApplicationModel(row[1],row[2],row[3],row[4],row[5])
                application.id=row[0]
                applicationArry.append(application)
            return applicationArry
        cur.close()
        return None

    @classmethod
    def find_all(cls):
        cur = mysql.get_db().cursor()
        query = """select * from application"""
        cur.execute(query)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            applicationArry=[]
            for row in rows:
                application=ApplicationModel(row[1],row[2],row[3],row[4],row[5])
                application.id=row[0]
                applicationArry.append(application)
            return applicationArry
        cur.close()
        return None


    @classmethod
    def delete_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """Delete from application where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            cur.close()
            mysql.get_db().commit()
            return True
        cur.close()
        return False
