from db import mysql


class generalReportModel():
    def __init__(self,questionID,answer,experimentId,userID):
        self.id=0
        self.questionID=questionID
        self.answer=answer
        self.experimentId=experimentId
        self.userID=userID



    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if( generalReportModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        query= """INSERT INTO generalReport (questionID,answer,experimentId,userID) VALUES (%s,%s,%s,%s)"""
        input=(self.questionID,self.answer,self.experimentId,self.userID)
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM generalReport ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()

    def update_db(self):
        cur = mysql.get_db().cursor()
        query = """Update generalReport set questionID = %s,answer = %s,experimentId = %s,userID = %s where id = %s"""
        input=(self.questionID,self.answer,self.experimentId,self.userID,self.id)
        cur.execute(query,input)
        mysql.get_db().commit()
        cur.close()


    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from generalReport where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            report=generalReportModel(row[1],row[2],row[3],row[4])
            report.id=row[0]
            return report
        cur.close()
        return False


    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE generalReport (id Integer(6) PRIMARY KEY AUTO_INCREMENT,questionID Integer(6),answer VARCHAR(1024),experimentId Integer(6),userID Integer(6))"
        cur.execute(query)
        cur.close()

    @classmethod
    def drop_db(self):
        cur = mysql.get_db().cursor()
        stmt = "SHOW TABLES LIKE 'generalReport'"
        cur.execute(stmt)
        result = cur.fetchone()
        if result:
            sql = "DROP TABLE generalReport"
            cur.execute(sql)
            cur.close()



    @classmethod
    def delete_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """Delete from generalReport where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            cur.close()
            mysql.get_db().commit()
            return True
        cur.close()
        return False

    @classmethod
    def find_by_experimentId(cls, _experimentId):
        cur = mysql.get_db().cursor()
        query = """select * from generalReport where experimentId = %s"""
        cur.execute(query,_experimentId)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            generalArry=[]
            for row in rows:
                report=generalReportModel(row[1],row[2],row[3],row[4])
                report.id=row[0]
                generalArry.append(report)
            return generalArry
        cur.close()
        return []
