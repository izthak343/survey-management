from db import mysql


class RankSecurtyModel():
    def __init__(self,name):
        self.id=0
        self.name=name


    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if( RankSecurtyModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        input=(self.name)
        query= """INSERT INTO rankSecurty (name) VALUES ( %s)"""
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM rankSecurty ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()



    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE rankSecurty (id Integer(6) PRIMARY KEY AUTO_INCREMENT,name VARCHAR(1024))"
        cur.execute(query)
        cur.close()

    @classmethod
    def delete_all_rows(self):
        cur = mysql.get_db().cursor()
        sql = "TRUNCATE TABLE rankSecurty"
        cur.execute(sql)
        cur.close()

    @classmethod
    def drop_db(self):
        cur = mysql.get_db().cursor()
        stmt = "SHOW TABLES LIKE 'rankSecurty'"
        cur.execute(stmt)
        result = cur.fetchone()
        if result:
            sql = "DROP TABLE rankSecurty"
            cur.execute(sql)
            cur.close()





    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from rankSecurty where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            rankSecurty=RankPrivacyModel(row[1])
            rankSecurty.id=row[0]
            cur.close()
            return rankSecurty
        cur.close()
        return False

    @classmethod
    def find_all_RankSecurty(cls):
        cur = mysql.get_db().cursor()
        query = """select * from rankSecurty"""
        cur.execute(query)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            RankSecurtyArry=[]
            for row in rows:
                rankSecurty=RankSecurtyModel(row[1])
                rankSecurty.id=row[0]
                RankSecurtyArry.append(rankSecurty)
            return RankSecurtyArry
        cur.close()
        return []
