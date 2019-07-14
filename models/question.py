from db import mysql


class QuestionModel():
    def __init__(self,question,section,type,answer1,answer2,answer3,answer4):
        self.id=0
        self.question=question
        self.section=section
        self.type=type
        self.answer1=answer1
        self.answer2=answer2
        self.answer3=answer3
        self.answer4=answer4

    def save_to_db(self):
        cur = mysql.get_db().cursor()
        if( QuestionModel.find_by_id(self.id) != False ):
            cur.close()
            return False
        query= """INSERT INTO question (question,section,type,answer1,answer2,answer3,answer4) VALUES (%s,%s, %s,%s, %s,%s, %s)"""
        input=(self.question,self.section,self.type,self.answer1,self.answer2,self.answer3,self.answer4)
        cur.execute(query,input)
        mysql.get_db().commit()
        query = """SELECT * FROM question ORDER BY id DESC LIMIT 1"""
        cur.execute(query)
        if(cur.rowcount > 0):
            self.id=cur.fetchone()[0]
        cur.close()

    def update_db(self):
        cur = mysql.get_db().cursor()
        query = """Update question set question = %s,section = %s,type = %s,answer1 = %s,answer2 = %s,answer3 = %s,answer4 = %s where id = %s"""
        input=(self.question,self.section,self.type,self.answer1,self.answer2,self.answer3,self.answer4,self.id)
        cur.execute(query,input)
        mysql.get_db().commit()
        cur.close()

    @classmethod
    def create_db(self):
        cur = mysql.get_db().cursor()
        query = "CREATE TABLE question (id Integer(6) PRIMARY KEY AUTO_INCREMENT,question VARCHAR(1024),section Integer(6),type Integer(6),answer1 VARCHAR(1024),answer2 VARCHAR(1024),answer3 VARCHAR(1024),answer4 VARCHAR(1024))"
        cur.execute(query)
        cur.close()

    @classmethod
    def find_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """select * from question where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            row = cur.fetchone()
            cur.close()
            question=QuestionModel(row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            question.id=row[0]
            return question
        cur.close()
        return False

    @classmethod
    def delete_by_id(cls, _id):
        cur = mysql.get_db().cursor()
        query = """Delete from question where id = %s"""
        cur.execute(query,_id)
        if(cur.rowcount > 0):
            mysql.get_db().commit()
            cur.close()
            return True
        cur.close()
        return False


    @classmethod
    def find_all_Question(cls):
        cur = mysql.get_db().cursor()
        query = """select * from question"""
        cur.execute(query)
        if(cur.rowcount > 0):
            rows = cur.fetchall()
            cur.close()
            QuestionArry=[]
            for row in rows:
                question=QuestionModel(row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                question.id=row[0]
                QuestionArry.append(question)
            return QuestionArry
        cur.close()
        return None
