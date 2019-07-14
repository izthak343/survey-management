from db import mysql


class SecurtyModel():
    def __init__(self,name):
        self.id=0
        self.name=name


    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if(SecurtyModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        input=(self.name)
        query= """INSERT INTO securty (name) VALUES (%s)"""
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM securty ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()



    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE securty (id Integer(6) PRIMARY KEY AUTO_INCREMENT,name VARCHAR(1024))"
        cur.execute(query)
        cur.close()

    @classmethod
    def drop_db(self):
        cur = mysql.get_db().cursor()
        stmt = "SHOW TABLES LIKE 'securty'"
        cur.execute(stmt)
        result = cur.fetchone()
        if result:
            sql = "DROP TABLE securty"
            cur.execute(sql)
            cur.close()
    @classmethod
    def delete_all_rows(self):
        cur = mysql.get_db().cursor()
        sql = "TRUNCATE TABLE securty"
        cur.execute(sql)
        cur.close()

    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from securty where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            securtyFeature=SecurtyModel(row[1])
            SecurtyFeature.id=row[0]
            cur.close()
            return securtyFeature
        cur.close()
        return False

    @classmethod
    def find_all_SecurtyFeature(cls):
        cur = mysql.get_db().cursor()
        query = """select * from securty"""
        cur.execute(query)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            SecurtyFeatureArry=[]
            for row in rows:
                securtyFeature=SecurtyModel(row[1])
                securtyFeature.id=row[0]
                SecurtyFeatureArry.append(securtyFeature)
            return SecurtyFeatureArry
        cur.close()
        return []
