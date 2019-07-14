from wtforms import  Form, StringField, TextAreaField, PasswordField, validators ,SelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import DateField



class ApplicationForm(Form):
    realName = StringField('Real name', [validators.Length(min=1, max=50,message='שדה זה חייב להיות באורך של 1 עד 50 תוים')])
    falseName = StringField('False name', [validators.Length(min=1, max=50,message='שדה זה חייב להיות באורך של 1 עד 50 תוים')])
    # categoryId = SelectField('Category', choices=[(1, 'בטיחות גבוהה ופרטיות גבוהה'),(2, 'בטיחות גבוהה ופרטיות נמוכה'),(3, 'בטיחות נמוכה ופרטיות גבוהה'),(4, 'בטיחות נמוכה ופרוטיות נמוכה')])
    method1image = FileField('First part image' )
    method2image = FileField('Second part image' )




class QuestionForm(Form):
    question = StringField('שאלה', [validators.Length(min=1, max=256,message='שדה זה חייב להיות באורך 1 עד 256 תוים')])
    answer1 = StringField('תשובה 1', [validators.Length(min=1, max=256,message='שדה זה חייב להיות באורך 1 עד 256 תוים')])
    answer2 = StringField('תשובה 2', [validators.Length(min=1, max=256,message='שדה זה חייב להיות באורך 1 עד 256 תוים')])
    answer3 = StringField('תשובה 3', [validators.Length(min=1, max=256,message='שדה זה חייב להיות באורך 1 עד 256 תוים')])
    answer4 = StringField('תשובה 4', [validators.Length(min=1, max=256,message='שדה זה חייב להיות באורך 1 עד 256 תוים')])
    image = FileField('תמונה' )


class RegisterForm(Form):
    name = StringField('שם', [validators.Length(min=1, max=50,message='שדה זה חייב להיות באורך של 1 עד 50 תוים')])
    email = StringField('Email', [validators.Email('שדה זה חייב להיות אימייל')])
    password = PasswordField('סיסמה', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='סיסמה לא מתאימה')
    ])
    confirm = PasswordField('אישור סיסמה')
