from db import mysql


class ExperimentModel():
    def __init__(self,type,numberParti,checkboxLen,run):
        self.id=0
        self.type=type
        self.numberParti=numberParti
        self.leftParti=numberParti
        self.checkboxLen=checkboxLen
        self.run=run

    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if(ExperimentModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        input=(self.type,self.numberParti,self.leftParti,self.checkboxLen,self.run)
        query= """INSERT INTO experiment (type,numberParti,leftParti,checkboxLen,run) VALUES (%s,%s,%s, %s, %s)"""
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM experiment ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()

    def update_db(self):
        cur = mysql.get_db().cursor()
        query = """Update experiment set type = %s,numberParti = %s,leftParti = %s,checkboxLen = %s,run = %s where id = %s"""
        input=(self.type,self.numberParti,self.leftParti,self.checkboxLen,self.run,self.id)
        cur.execute(query,input)
        mysql.get_db().commit()
        cur.close()

    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE experiment (id Integer(6) PRIMARY KEY AUTO_INCREMENT,type Integer(6),numberParti Integer(6),leftParti Integer(6),checkboxLen Integer(6) ,run Integer(6))"
        cur.execute(query)
        cur.close()

    @classmethod
    def drop_db(self):
        cur = mysql.get_db().cursor()
        stmt = "SHOW TABLES LIKE 'experiment'"
        cur.execute(stmt)
        result = cur.fetchone()
        if result:
            sql = "DROP TABLE experiment"
            cur.execute(sql)
            cur.close()

    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from experiment where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            Experiment=ExperimentModel(row[1],row[2],row[4],row[5])
            Experiment.leftParti=row[3]
            Experiment.id=row[0]
            cur.close()
            return Experiment
        cur.close()
        return False

    @classmethod
    def find_all_Experiment(cls):
        cur = mysql.get_db().cursor()
        query = """select * from experiment"""
        cur.execute(query)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            ExperimentArry=[]
            for row in rows:
                Experiment=ExperimentModel(row[1],row[2],row[4],row[5])
                Experiment.leftParti=row[3]
                Experiment.id=row[0]
                ExperimentArry.append(Experiment)
            return ExperimentArry
        cur.close()
        return []

    @classmethod
    def find_all_Experiment_run(cls):
        cur = mysql.get_db().cursor()
        query = """select * from experiment where run = %s"""
        cur.execute(query,1)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            ExperimentArry=[]
            for row in rows:
                Experiment=ExperimentModel(row[1],row[2],row[4],row[5])
                Experiment.leftParti=row[3]
                Experiment.id=row[0]
                ExperimentArry.append(Experiment)
            return ExperimentArry
        cur.close()
        return []

    @classmethod
    def find_Experiment_run_type(cls,_type):
        cur = mysql.get_db().cursor()
        query = """select * from experiment where run = %s AND type = %s"""
        cur.execute(query,1,_type)
        if(cur.rowcount > 0):
            rows = cur.fetchone()
            cur.close()
            Experiment=ExperimentModel(row[1],row[2],row[4],row[5])
            Experiment.leftParti=row[3]
            Experiment.id=row[0]
            return Experiment
        cur.close()
        return False
