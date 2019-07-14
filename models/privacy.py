from db import mysql


class PrivacyModel():
    def __init__(self,name):
        self.id=0
        self.name=name


    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if( PrivacyModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        input=(self.name)
        query= """INSERT INTO privacy (name) VALUES ( %s)"""
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM privacy ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()



    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE privacy (id Integer(6) PRIMARY KEY AUTO_INCREMENT,name VARCHAR(1024))"
        cur.execute(query)
        cur.close()

    @classmethod
    def drop_db(self):
        cur = mysql.get_db().cursor()
        stmt = "SHOW TABLES LIKE 'privacy'"
        cur.execute(stmt)
        result = cur.fetchone()
        if result:
            sql = "DROP TABLE privacy"
            cur.execute(sql)
            cur.close()

    @classmethod
    def delete_all_rows(self):
        cur = mysql.get_db().cursor()
        sql = "TRUNCATE TABLE privacy"
        cur.execute(sql)
        cur.close()



    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from privacy where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            privacyFact=PrivacyModel(row[1])
            PrivacyModel.id=row[0]
            cur.close()
            return privacyFact
        cur.close()
        return False

    @classmethod
    def find_all_PrivacyFact(cls):
        cur = mysql.get_db().cursor()
        query = """select * from privacy"""
        cur.execute(query)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            PrivacyFactArry=[]
            for row in rows:
                privacyFact=PrivacyModel(row[1])
                privacyFact.id=row[0]
                PrivacyFactArry.append(privacyFact)
            return PrivacyFactArry
        cur.close()
        return []
