from db import mysql


class RankPrivacyModel():
    def __init__(self,name):
        self.id=0
        self.name=name


    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if(RankPrivacyModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        input=(self.name)
        query= """INSERT INTO  rankPrivacy (name) VALUES (%s)"""
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM rankPrivacy ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()



    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE rankPrivacy (id Integer(6) PRIMARY KEY AUTO_INCREMENT,name VARCHAR(1024))"
        cur.execute(query)
        cur.close()

    @classmethod
    def drop_db(self):
        cur = mysql.get_db().cursor()
        stmt = "SHOW TABLES LIKE 'rankPrivacy'"
        cur.execute(stmt)
        result = cur.fetchone()
        if result:
            sql = "DROP TABLE rankPrivacy"
            cur.execute(sql)
            cur.close()

    @classmethod
    def delete_all_rows(self):
        cur = mysql.get_db().cursor()
        sql = "TRUNCATE TABLE rankPrivacy"
        cur.execute(sql)
        cur.close()

    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from rankPrivacy where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            rankPrivacy=RankPrivacyModel(row[1])
            rankPrivacy.id=row[0]
            cur.close()
            return rankPrivacy
        cur.close()
        return False

    @classmethod
    def find_all_RankPrivacy(cls):
        cur = mysql.get_db().cursor()
        query = """select * from rankPrivacy"""
        cur.execute(query)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            RankPrivacyArry=[]
            for row in rows:
                rankPrivacy=RankPrivacyModel(row[1])
                rankPrivacy.id=row[0]
                RankPrivacyArry.append(rankPrivacy)
            return RankPrivacyArry
        cur.close()
        return []
