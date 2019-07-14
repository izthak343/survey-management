from db import mysql


class ExperimentAppModel():
    def __init__(self,ExperimentId,applicationId):
        self.id=0
        self.ExperimentId=ExperimentId
        self.applicationId=applicationId

    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if(ExperimentAppModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        input=(self.ExperimentId,self.applicationId)
        query= """INSERT INTO experimentApp (ExperimentId,applicationId) VALUES ( %s,%s)"""
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM experimentApp ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()

    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE experimentApp (id Integer(6) PRIMARY KEY AUTO_INCREMENT,ExperimentId Integer(6),applicationId Integer(6))"
        cur.execute(query)
        cur.close()

    @classmethod
    def drop_db(self):
        cur = mysql.get_db().cursor()
        stmt = "SHOW TABLES LIKE 'experimentApp'"
        cur.execute(stmt)
        result = cur.fetchone()
        if result:
            sql = "DROP TABLE experimentApp"
            cur.execute(sql)
            cur.close()

    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from experimentApp where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            ExperimentApp=ExperimentAppModel(row[1],row[2])
            ExperimentApp.id=row[0]
            cur.close()
            return ExperimentApp
        cur.close()
        return False

    @classmethod
    def find_all_ExperimentApp(cls):
        cur = mysql.get_db().cursor()
        query = """select * from experimentApp"""
        cur.execute(query)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            ExperimentAppArry=[]
            for row in rows:
                ExperimentApp=ExperimentAppModel(row[1],row[2])
                ExperimentApp.id=row[0]
                ExperimentAppArry.append(ExperimentApp)
            return ExperimentAppArry
        cur.close()
        return []


    @classmethod
    def find_ExperimentApp_by_ExperimentID(cls,_ExperimentID):
        cur = mysql.get_db().cursor()
        query = """select * from experimentApp where ExperimentId = %s"""
        cur.execute(query,_ExperimentID)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            ExperimentAppArry=[]
            for row in rows:
                ExperimentApp=ExperimentAppModel(row[1],row[2])
                ExperimentApp.id=row[0]
                ExperimentAppArry.append(ExperimentApp)
            return ExperimentAppArry
        cur.close()
        return []
