from db import mysql


class UserModel():
    def __init__(self,name, email, password,type,agreed,startSurvy,ExperimentId):
        self.id=0
        self.name=name
        self.email = email
        self.password = password
        self.type = type
        self.agreed=agreed
        self.startSurvy=startSurvy
        self.ExperimentId=ExperimentId

    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if( UserModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        input=(self.name,self.email,self.password,self.type,self.agreed,self.startSurvy,self.ExperimentId)
        query= """INSERT INTO users (name,email,password,type,agreed,startSurvy,ExperimentId) VALUES (%s,%s, %s,%s,%s, %s, %s)"""
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM users ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()



    def update_db(self):
        cur = mysql.get_db().cursor()
        query = """Update users set name = %s,email = %s,password = %s,type = %s,agreed = %s,startSurvy = %s,ExperimentId = %s where id = %s"""
        input=(self.name,self.email,self.password,self.type,self.agreed,self.startSurvy,self.ExperimentId,self.id)
        cur.execute(query,input)
        mysql.get_db().commit()
        cur.close()


    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE users (id Integer(6) PRIMARY KEY AUTO_INCREMENT,name VARCHAR(1024),email VARCHAR(1024),password VARCHAR(1024),type Integer(6),agreed Integer(6),startSurvy Integer(6),ExperimentId Integer(6))"
        cur.execute(query)
        cur.close()

    @classmethod
    def drop_db(self):
        cur = mysql.get_db().cursor()
        stmt = "SHOW TABLES LIKE 'users'"
        cur.execute(stmt)
        result = cur.fetchone()
        if result:
            sql = "DROP TABLE users"
            cur.execute(sql)
            cur.close()

    @classmethod
    def find_by_email(cls, _email):
        cur = mysql.get_db().cursor()
        query = """select * from users where email = %s"""
        cur.execute(query,_email)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            user=UserModel(row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            user.id=row[0]
            return user
        cur.close()
        return False

    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from users where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            user=UserModel(row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            user.id=row[0]
            cur.close()
            return user
        cur.close()
        return False

    @classmethod
    def find_all_user(cls):
        cur = mysql.get_db().cursor()
        query = """select * from users"""
        cur.execute(query)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            UserArry=[]
            for row in rows:
                user=UserModel(row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                user.id=row[0]
                UserArry.append(user)
            return UserArry
        cur.close()
        return False
