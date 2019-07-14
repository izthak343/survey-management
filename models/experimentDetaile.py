from db import mysql


class ExperimentDetaileModel():
    def __init__(self,ExperimentId,applicationId,questionDisplay,userID,done,groupExp):
        self.id=0
        self.ExperimentId=ExperimentId
        self.applicationId=applicationId
        self.questionDisplay=questionDisplay
        self.userID=userID
        self.done=done
        self.groupExp=groupExp

    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if(ExperimentDetaileModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        input=(self.ExperimentId,self.applicationId,self.questionDisplay,self.userID,self.done,self.groupExp)
        query= """INSERT INTO experimentDetaile (ExperimentId,applicationId,questionDisplay,userID,done,groupExp) VALUES (%s,%s,%s,%s, %s, %s)"""
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM experimentDetaile ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()

    def update_db(self):
        cur = mysql.get_db().cursor()
        query = """Update experimentDetaile set ExperimentId = %s,applicationId = %s,questionDisplay = %s,userID = %s,done = %s,groupExp = %s where id = %s"""
        input=(self.ExperimentId,self.applicationId,self.questionDisplay,self.userID,self.done,self.groupExp,self.id)
        cur.execute(query,input)
        mysql.get_db().commit()
        cur.close()

    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE experimentDetaile (id Integer(6) PRIMARY KEY AUTO_INCREMENT,ExperimentId Integer(6),applicationId Integer(6),questionDisplay Integer(6),userID Integer(6),done Integer(6),groupExp Integer(6))"
        cur.execute(query)
        cur.close()

    @classmethod
    def drop_db(self):
        cur = mysql.get_db().cursor()
        stmt = "SHOW TABLES LIKE 'experimentDetaile'"
        cur.execute(stmt)
        result = cur.fetchone()
        if result:
            sql = "DROP TABLE experimentDetaile"
            cur.execute(sql)
            cur.close()

    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from experimentDetaile where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            Experiment=ExperimentDetaileModel(row[1],row[2],row[3],row[4],row[5],row[6])
            Experiment.id=row[0]
            cur.close()
            return Experiment
        cur.close()
        return False

    @classmethod
    def find_all_ExperimentDetailes_by_userID(cls,_userID,_ExperimentID):
        cur = mysql.get_db().cursor()
        query = """select * from experimentDetaile where userId = %s AND ExperimentId = %s And done=%s"""
        cur.execute(query,(_userID,_ExperimentID,0))
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            ExperimentArry=[]
            for row in rows:
                Experiment=ExperimentDetaileModel(row[1],row[2],row[3],row[4],row[5],row[6])
                Experiment.id=row[0]
                ExperimentArry.append(Experiment)
            return ExperimentArry
        cur.close()
        return []

    @classmethod
    def get_ExperimentDetaile(cls,_ExperimentID):
        cur = mysql.get_db().cursor()
        query = """select * from experimentDetaile where ExperimentId = %s AND done = %s AND userID = %s"""
        cur.execute(query,(_ExperimentID,0,0))
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            ExperimentDetaileArry=[]
            i=0
            gropFirst=-1
            for row in rows:
                if(gropFirst==-1):
                    gropFirst=row[6]
                else:
                    if(row[6]!=gropFirst):
                        return ExperimentDetaileArry
                ExperimentDetaile=ExperimentDetaileModel(row[1],row[2],row[3],row[4],row[5],row[6])
                ExperimentDetaile.id=row[0]
                ExperimentDetaileArry.append(ExperimentDetaile)

        cur.close()
        return []

    @classmethod
    def find_all_ExperimentDetailes(cls):
        cur = mysql.get_db().cursor()
        query = """select * from experimentDetaile"""
        cur.execute(query)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            ExperimentArry=[]
            for row in rows:
                Experiment=ExperimentDetaileModel(row[1],row[2],row[3],row[4],row[5],row[6])
                Experiment.id=row[0]
                ExperimentArry.append(Experiment)
            return ExperimentArry
        cur.close()
        return []


    @classmethod
    def find_all_ExperimentDetailes_by_ExperimentID(cls,_ExperimentID):
        cur = mysql.get_db().cursor()
        query = """select * from experimentDetaile where ExperimentId = %s"""
        cur.execute(query,_ExperimentID)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            ExperimentArry=[]
            for row in rows:
                Experiment=ExperimentDetaileModel(row[1],row[2],row[3],row[4],row[5],row[6])
                Experiment.id=row[0]
                ExperimentArry.append(Experiment)
            return ExperimentArry
        cur.close()
        return []
