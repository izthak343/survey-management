from db import mysql


class PrivacyApplictionModel():
    def __init__(self,privacyId,privacyRankId,part,applicationId):
        self.id=0
        self.privacyId=privacyId
        self.privacyRankId=privacyRankId
        self.part=part
        self.applicationId=applicationId




    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if( PrivacyApplictionModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        input=(self.privacyId,self.privacyRankId,self.part,self.applicationId)
        query= """INSERT INTO privacyAppliction (privacyId,privacyRankId,part,applicationId) VALUES (%s,%s,%s, %s)"""
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM privacyAppliction ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()



    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE privacyAppliction (id Integer(6) PRIMARY KEY AUTO_INCREMENT,privacyId Integer(6),privacyRankId Integer(6),part Integer(6),applicationId Integer(6))"
        cur.execute(query)
        cur.close()

    @classmethod
    def drop_db(self):
        cur = mysql.get_db().cursor()
        stmt = "SHOW TABLES LIKE 'privacyAppliction'"
        cur.execute(stmt)
        result = cur.fetchone()
        if result:
            sql = "DROP TABLE privacyAppliction"
            cur.execute(sql)
            cur.close()



    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from privacyAppliction where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            PrivacyAppliction=PrivacyApplictionModel(row[1],row[2],row[3],row[4])
            PrivacyAppliction.id=row[0]
            cur.close()
            return PrivacyAppliction
        cur.close()
        return False

    @classmethod
    def find_all_PrivacyFact(cls):
        cur = mysql.get_db().cursor()
        query = """select * from privacyAppliction"""
        cur.execute(query)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            PrivacyApplictionArry=[]
            for row in rows:
                PrivacyAppliction=PrivacyApplictionModel(row[1],row[2],row[3],row[4])
                PrivacyAppliction.id=row[0]
                PrivacyApplictionArry.append(PrivacyAppliction)
            return PrivacyApplictionArry
        cur.close()
        return []


    @classmethod
    def delete_by_applicationID(cls, _applicationID):
        cur = mysql.get_db().cursor()
        query = """Delete from privacyAppliction where applicationId = %s"""
        cur.execute(query,_applicationID)
        if(cur.rowcount > 0):
            cur.close()
            mysql.get_db().commit()
            return True
        cur.close()
        return False
