from db import mysql


class CategoryModel():
    def __init__(self,name):
        self.id=0
        self.name=name

    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if( CategoryModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        query= """INSERT INTO category (name) VALUES (%s)"""
        input=(self.name)
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM category ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()


    def update_db(self):
        cur = mysql.get_db().cursor()
        query = """Update category set name = %s where id = %s"""
        input=(self.name,self.id)
        cur.execute(query,input)
        mysql.get_db().commit()
        cur.close()

    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from category where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            category=CategoryModel(row[1])
            category.id=row[0]
            return category
        cur.close()
        return False

    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE category (id Integer(6) PRIMARY KEY AUTO_INCREMENT,name VARCHAR(1024))"
        cur.execute(query)
        cur.close()
