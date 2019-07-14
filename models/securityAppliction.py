from db import mysql


class SecurityApplictionModel():
    def __init__(self,securityId,securityRankId,part,applicationId,image,securityRankIdFeature):
        self.id=0
        self.securityId=securityId
        self.securityRankId=securityRankId
        self.part=part
        self.applicationId=applicationId
        self.image=image
        self.securityRankIdFeature =securityRankIdFeature



    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if( SecurityApplictionModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        input=(self.securityId,self.securityRankId,self.part,self.applicationId,self.image,self.securityRankIdFeature)
        query= """INSERT INTO securityAppliction (securityId,securityRankId,part,applicationId,image,securityRankIdFeature) VALUES (%s,%s,%s, %s, %s, %s)"""
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM securityAppliction ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()



    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE securityAppliction (id Integer(6) PRIMARY KEY AUTO_INCREMENT,securityId Integer(6),securityRankId Integer(6),part Integer(6),applicationId Integer(6),image VARCHAR(1024),securityRankIdFeature Integer(6))"
        cur.execute(query)
        cur.close()

    @classmethod
    def drop_db(self):
        cur = mysql.get_db().cursor()
        stmt = "SHOW TABLES LIKE 'securityAppliction'"
        cur.execute(stmt)
        result = cur.fetchone()
        if result:
            sql = "DROP TABLE securityAppliction"
            cur.execute(sql)
            cur.close()



    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from securityAppliction where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            SecurityAppliction=SecurityApplictionModel(row[1],row[2],row[3],row[4],row[5],row[6])
            SecurityAppliction.id=row[0]
            cur.close()
            return SecurityAppliction
        cur.close()
        return False




    @classmethod
    def delete_by_applicationID(cls, _applicationID):
        cur = mysql.get_db().cursor()
        query = """Delete from securityAppliction where applicationId = %s"""
        cur.execute(query,_applicationID)
        if(cur.rowcount > 0):
            cur.close()
            mysql.get_db().commit()
            return True
        cur.close()
        return False

    @classmethod
    def find_all_SecurityAppliction(cls):
        cur = mysql.get_db().cursor()
        query = """select * from securityAppliction"""
        cur.execute(query)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            SecurityApplictionArry=[]
            for row in rows:
                SecurityAppliction=SecurityApplictionModel(row[1],row[2],row[3],row[4],row[5],row[6])
                SecurityAppliction.id=row[0]
                SecurityApplictionArry.append(SecurityAppliction)
            return SecurityApplictionArry
        cur.close()
        return []



    @classmethod
    def find_by_applicationID(cls, _applicationID):
        cur = mysql.get_db().cursor()
        query = """select * from securityAppliction where applicationId= %s"""
        cur.execute(query,_applicationID)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            SecurityApplictionArry=[]
            for row in rows:
                SecurityAppliction=SecurityApplictionModel(row[1],row[2],row[3],row[4],row[5],row[6])
                SecurityAppliction.id=row[0]
                SecurityApplictionArry.append(SecurityAppliction)
            return SecurityApplictionArry
        cur.close()
        return []
