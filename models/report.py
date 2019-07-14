from db import mysql


class ReportModel():
    def __init__(self,experimentDetaileID,questionID,answer,part,securityId):
        self.id=0
        self.experimentDetaileID=experimentDetaileID
        self.questionID=questionID
        self.answer=answer
        self.part=part
        self.securityId=securityId


    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if( ReportModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        query= """INSERT INTO report (experimentDetaileID,questionID,answer,part,securityId) VALUES (%s,%s,%s,%s,%s)"""
        input=(self.experimentDetaileID,self.questionID,self.answer,self.part,self.securityId)
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM report ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()

    def update_db(self):
        cur = mysql.get_db().cursor()
        query = """Update report set experimentDetaileID = %s,questionID = %s,answer = %s,part = %s,securityId = %s where id = %s"""
        input=(self.experimentDetaileID,self.questionID,self.answer,self.part,self.securityId,self.id)
        cur.execute(query,input)
        mysql.get_db().commit()
        cur.close()

    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from report where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            report=ReportModel(row[1],row[2],row[3],row[4],row[5])
            report.id=row[0]
            return report
        cur.close()
        return False

    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE report (id Integer(6) PRIMARY KEY AUTO_INCREMENT,experimentDetaileID Integer(6),questionID Integer(6),answer VARCHAR(1024),part Integer(6),securityId VARCHAR(1024))"
        cur.execute(query)
        cur.close()

    @classmethod
    def drop_db(self):
        cur = mysql.get_db().cursor()
        stmt = "SHOW TABLES LIKE 'report'"
        cur.execute(stmt)
        result = cur.fetchone()
        if result:
            sql = "DROP TABLE report"
            cur.execute(sql)
            cur.close()

    @classmethod
    def delete_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """Delete from report where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            cur.close()
            mysql.get_db().commit()
            return True
        cur.close()
        return False


    @classmethod
    def find_all_report_by_experimentDetailes(cls,_experimentDetailesId):
        cur = mysql.get_db().cursor()
        query = """select * from report where experimentDetaileID = %s"""
        cur.execute(query,_experimentDetailesId)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            reportArry=[]
            for row in rows:
                report=ReportModel(row[1],row[2],row[3],row[4],row[5])
                report.id=row[0]
                reportArry.append(report)
            return reportArry
        cur.close()
        return []
