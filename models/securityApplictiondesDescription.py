from db import mysql


class SecurityApplictionDescriptionModel():
    def __init__(self,securityApplictionId,privacyId,privacyRankId):
        self.id=0
        self.securityApplictionId=securityApplictionId
        self.privacyId=privacyId
        self.privacyRankId=privacyRankId



    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if( SecurityApplictionDescriptionModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        input=(self.securityApplictionId,self.privacyId,self.privacyRankId)
        query= """INSERT INTO securityApplictionDescription (securityApplictionId,privacyId,privacyRankId) VALUES (%s, %s, %s)"""
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM securityApplictionDescription ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()



    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE securityApplictionDescription (id Integer(6) PRIMARY KEY AUTO_INCREMENT,securityApplictionId Integer(6),privacyId Integer(6),privacyRankId Integer(6))"
        cur.execute(query)
        cur.close()

    @classmethod
    def drop_db(self):
        cur = mysql.get_db().cursor()
        stmt = "SHOW TABLES LIKE 'securityApplictionDescription'"
        cur.execute(stmt)
        result = cur.fetchone()
        if result:
            sql = "DROP TABLE securityApplictionDescription"
            cur.execute(sql)
            cur.close()



    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from securityApplictionDescription where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            SecurityAppliction=SecurityApplictionDescriptionModel(row[1],row[2],row[3])
            SecurityAppliction.id=row[0]
            cur.close()
            return SecurityAppliction
        cur.close()
        return False


    @classmethod
    def delete_by_securityApplictionID(cls, _securityApplictionID):
        cur = mysql.get_db().cursor()
        query = """Delete from securityApplictionDescription where securityApplictionId = %s"""
        cur.execute(query,_securityApplictionID)
        if(cur.rowcount > 0):
            cur.close()
            mysql.get_db().commit()
            return True
        cur.close()
        return False

    @classmethod
    def find_all(cls):
        cur = mysql.get_db().cursor()
        query = """select * from securityApplictionDescription"""
        cur.execute(query)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            SecurityApplictionArry=[]
            for row in rows:
                SecurityAppliction=SecurityApplictionDescriptionModel(row[1],row[2],row[3])
                SecurityAppliction.id=row[0]
                SecurityApplictionArry.append(SecurityAppliction)
            return SecurityApplictionArry
        cur.close()
        return []
