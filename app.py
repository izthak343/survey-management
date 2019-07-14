import os
import json
import pandas as pd
import smtplib
import time
import xlsxwriter
import copy
from io import BytesIO

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flaskext.mysql import MySQL
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging , send_file
from werkzeug.utils import secure_filename
from passlib.hash import sha256_crypt
from functools import wraps
import datetime
import random
from models.user import UserModel
from models.userDetails import UserDetailsModel
from models.userDetailsTemplate import UserDetailsTemplateModel
from models.category import CategoryModel
from models.application import ApplicationModel
from models.question import QuestionModel
from models.privacyAppliction import PrivacyApplictionModel
from models.securityAppliction import SecurityApplictionModel
from models.privacy import PrivacyModel
from models.rankPrivacy import RankPrivacyModel
from models.securty import SecurtyModel
from models.experiment import ExperimentModel
from models.experimentApp import ExperimentAppModel
from models.securty import SecurtyModel
from models.rankSecurty import RankSecurtyModel
from models.experimentDetaile import ExperimentDetaileModel
from models.report import ReportModel
from models.securityApplictiondesDescription import SecurityApplictionDescriptionModel
from models.generalReport import generalReportModel
from models.helper import helper
from models.saver import saverModel
from models.union import unionModel
from forms.forms import RegisterForm, ApplicationForm ,QuestionForm





app = Flask(__name__,static_url_path = "/pictures", static_folder = "pictures")
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['UPLOAD_FOLDER'] = './pictures'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Asd0147896325!'
app.config['MYSQL_DATABASE_DB'] = 'survey'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])




@app.before_first_request
def create_tables():
    builDatabase()


################################# public #################################
@app.route('/')
def home():
    if ('logged_in' in session):
        if 'admin' in session :
            return redirect(url_for('administratorMenu'))
        else:
            return redirect(url_for('participantMenu'))
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')




# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if ('logged_in' in session):
        if 'admin' in session :
            return redirect(url_for('administratorMenu'))
        else:
            return redirect(url_for('participantMenu'))
    form = RegisterForm(request.form)
    nameTypeArray=[]
    userDetailsTemplate=UserDetailsTemplateModel.find_all_UserDetailsTempate()
    if(userDetailsTemplate!=False):
        for userDetail in userDetailsTemplate:
            nameTypeArray.append([userDetail.name,userDetail.type])
    if request.method == 'POST' and form.validate():
        editData=request.form.getlist('editData')
        name = form.name.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        if UserModel.find_by_email(email):
            flash('משתמש עם מייל זה קיים במערך', 'warning')
            return render_template('register.html', form=form),400
        user = UserModel(name,email,password,2,1,0,0)
        user.save_to_db()
        i=0
        if(userDetailsTemplate!=False):
            for userDetail in userDetailsTemplate:
                i=i
                userDetails = UserDetailsModel(editData[i],userDetail.attr,user.id)
                userDetails.save_to_db()
                i+=1
        flash('נרשמת בהצלחה, מייל עם אישור הרשמה בדרך אליך!', 'success')
        registrationEmail(email)
        return redirect(url_for('login'))
    return render_template('register.html',form=form,nameTypeArray=nameTypeArray),400

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if ('logged_in' in session):
        if 'admin' in session :
            return redirect(url_for('administratorMenu'))
        else:
            return redirect(url_for('participantMenu'))
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']
        user=UserModel.find_by_email(email)
        if user:
            password = user.password
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                if(user.startSurvy == 0):
                    error = 'עדיין לא קיבלת אישור להשתתף בסקר '
                    return render_template('login.html', error=error)
                session['startSurvy']=True
                session['logged_in'] = True
                session['username'] = user.name
                session['id']=user.id
                if(user.type==1):
                    session['admin'] = True
                flash('התחברת!', 'success')
                if(user.type == 2):
                    session['expId']=user.ExperimentId
                    if(user.agreed==2):
                        session['agreed']=True
                        return redirect(url_for('participantMenu'))
                    else:
                        return redirect(url_for('agreedPage',id=user.id))
                else:
                    return redirect(url_for('administratorMenu'))
            else:
                error = 'סיסמה לא נכונה'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'משתמש לא קיים'
            return render_template('login.html', error=error)

    return render_template('login.html')

#buil demo Database
def builDatabase():
    # ExperimentDetaileModel.create_db()
    # UserModel.create_db()
    # ExperimentAppModel.create_db()
    # ExperimentModel.create_db()
    # PrivacyModel.create_db()
    # RankPrivacyModel.create_db()
    # SecurtyModel.create_db()
    # RankSecurtyModel.create_db()
    # UserDetailsModel.create_db()
    # UserDetailsTemplateModel.create_db()
    # SecurityApplictionModel.create_db()
    # PrivacyApplictionModel.create_db()
    # CategoryModel.create_db()
    # QuestionModel.create_db()
    # ApplicationModel.create_db()
    # ReportModel.create_db()
    # generalReportModel.create_db()
    # SecurityApplictionDescriptionModel.create_db()
    password = sha256_crypt.encrypt("aaa")
    # user = UserModel("admin","admin",password,1,False,1,0)
    # user.save_to_db()
    # user = UserModel("participant","participant",password,2,False,0,0)
    # user.save_to_db()
    # category = CategoryModel("high privacy and high privacy")
    # category.save_to_db()
    # category = CategoryModel("low privacy and high privacy")
    # category.save_to_db()
    # category = CategoryModel("high privacy and low privacy")
    # category.save_to_db()
    # category = CategoryModel("low privacy and low privacy")
    # category.save_to_db()




# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('לא מורשה להיכנס לדף זה , אנא התחבר', 'danger')
            return redirect(url_for('login'))
    return wrap


# Check if user logged in
def is_startSurvy(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'startSurvy' in session:
            return f(*args, **kwargs)
        else:
            flash('עדיין לא קיבלת אישור להשתתף בסקר', 'danger')
            return redirect(url_for('thankYou.html'))
    return wrap




# Check if user admin
def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin' in session :
            return f(*args, **kwargs)
        else:
            session.clear()
            flash('לא מורשה להיכנס לדף זה , אנא התחבר', 'danger')
            return redirect(url_for('login'))
    return wrap

# Check if user participant
def is_participant(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not ('admin' in session):
            return f(*args, **kwargs)
        else:
            session.clear()
            flash('לא מורשה להיכנס לדף זה , אנא התחבר', 'danger')
            return redirect(url_for('login'))
    return wrap

# Check if user aggred to the aggred page
def is_agreed(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('agreed' in session):
            return f(*args, **kwargs)
        else:
            flash('לא מורשה להיכנס לדף ללא אישור הסכם', 'danger')
            return redirect(url_for('agreedPage',id=session['id']))
    return wrap

# Check if user aggred to the aggred page
def is_notAgreed(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('agreed' in session):
            flash('לא מורשה להיכנס לדף ללא אישור הסכם', 'danger')
            return redirect(url_for('agreedPage',id=session['id']))
        else:
            return f(*args, **kwargs)
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('התנתקת!', 'success')
    return redirect(url_for('login'))





################################# admin #################################

# administratorMenu
@app.route('/administratorMenu')
@is_logged_in
@is_admin
def administratorMenu():
    return render_template('administratorMenu.html')


# applicationDashboard
@app.route('/applicationDashboard')
@is_logged_in
@is_admin
def applicationDashboard():
    applications=[]
    category=[]
    for i in range(1,5):
        temp=ApplicationModel.find_by_categoryId(i)
        if(temp!=None):
            applications.append(temp)
        else:
            applications.append([])
        category.append(CategoryModel.find_by_id(i))
    # return str(applications[1][0].categoryId)
    return render_template('applicationDashboard.html', applicationsByCatagorty=applications , category=category)

#allowed_file function used in add question & edit question
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Add Application
@app.route('/add_application/<string:categoryId>', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def add_application(categoryId):
    # Get form
    form = ApplicationForm(request.form)
    privacyFacts=PrivacyModel.find_all_PrivacyFact()
    rankPrivacies=RankPrivacyModel.find_all_RankPrivacy()
    securtyFeatures=SecurtyModel.find_all_SecurtyFeature()
    rankSecurties=RankSecurtyModel.find_all_RankSecurty()
    if request.method == 'POST' :
            # check if the post request has the file part
            if 'method1image' not in request.files or 'method2image' not in request.files:
                flash('לא נבחרה תמונה לאפליקציה', 'danger')
                return redirect(request.url)
            file = request.files['method1image']
            file1 = request.files['method2image']
            files=request.files.getlist('newFitzarsImage')
            FitzarsNames=request.form.getlist("fitzarName")
            # return str(FitzarsNames)
            FitzarRanks=request.form.getlist("fitzarRank")
            if file.filename == '' or file1.filename == '':
                flash('לא נבחרה תמונה לאפליקציה', 'danger')
                return redirect(request.url)
            if( not (allowed_file(file.filename)) or not (allowed_file(file1.filename))):
                flash('סוג הקובץ אינו מורשה!', 'danger')
                return redirect(request.url)
            realName = request.form['realName']
            falseName = request.form['falseName']
            categoryId = request.form['categoryId']
            k=0
            securityRankIdFeatures = request.form.getlist('securty_fizer')
            filename = falseName + "_Method1.jpg"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            picture1=filename
            filename =falseName + "_Method2.jpg"
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            picture2=filename
            application=ApplicationModel(realName,falseName,categoryId,picture1,picture2)
            application.save_to_db()
            privacies=PrivacyModel.find_all_PrivacyFact()
            privacyForChooseSecurty=[]
            for privacy in privacies:
                privacyForChooseSecurty.append(request.form.getlist('fizer_'+str(privacy.id)))
                privacyRank=""
                privacyRank=request.form.getlist('privacy'+str(privacy.id))
                if(not(privacyRank)):
                    return "Erore"+privacy.name
                PrivacyAppliction=PrivacyApplictionModel(privacy.id,int(privacyRank[0]),1,application.id)
                PrivacyAppliction.save_to_db()
                PrivacyAppliction=PrivacyApplictionModel(privacy.id,int(privacyRank[1]),2,application.id)
                PrivacyAppliction.save_to_db()
            securities=SecurtyModel.find_all_SecurtyFeature()
            chooseSecurties=[]
            for security in securities:
                securityRank=request.form.getlist('securty'+str(security.id))
                if(not(securityRank)):
                    return "Erore"+security.name
                securityAppliction=SecurityApplictionModel(security.id,int(securityRank[0]),1,application.id,"",-1)
                securityAppliction.save_to_db()
                i=0
                savedName=""
                securityRankIdFeature=-1
                for Fitzars in files:
                    if(allowed_file(Fitzars.filename)==False):
                        flash('סוג הקובץ אינו מורשה!', 'danger')
                        return redirect(request.url)
                    else:
                        # print(str(int(FitzarsNames[i]) == security.id))
                        # print(str(int(FitzarsNames[i])))
                        # print(str(int(security.id)))
                        if int(FitzarsNames[i]) == security.id:
                            securityRankIdFeature=int(securityRankIdFeatures[k])
                            k+=1
                            savedName=falseName + "_Method2_"+ security.name +".jpg"
                            Fitzars.save(os.path.join(app.config['UPLOAD_FOLDER'], savedName))
                            break;
                    i+=1

                securityAppliction=SecurityApplictionModel(security.id,int(securityRank[0]),2,application.id,savedName,securityRankIdFeature)
                if(savedName!=""):
                    chooseSecurties.append(securityAppliction)
                securityAppliction.save_to_db()
            j=0
            for chooseSecurty in chooseSecurties:
                i=0
                for privacy in privacies:
                    # print('i: '+str(i)+',j: '+str(j))
                    SecurityApplictionDescription=SecurityApplictionDescriptionModel(chooseSecurty.id,privacy.id,privacyForChooseSecurty[i][j])
                    SecurityApplictionDescription.save_to_db()
                    i+=1
                j+=1
            flash('האפליקציה נוספה', 'success')
            return redirect(url_for('applicationDashboard'))
    return render_template('add_application.html', form=form,privacyFacts=privacyFacts,rankPrivacies=rankPrivacies,securtyFeatures=securtyFeatures,rankSecurties=rankSecurties,categoryId=categoryId)


# Remove Application picture
def removeFiless(appName):
    filename=app.config['UPLOAD_FOLDER'] + "/" +appName+"_Method1"+".jpg"
    if os.path.exists(filename):
      os.remove(filename)
    else:
        print("The file does not exist" + filename)

    filename=app.config['UPLOAD_FOLDER'] + "/" +appName+"_Method2"+".jpg"
    if os.path.exists(filename):
      os.remove(filename)
    else:
        print("The file does not exist" + filename)
    FitzarsNames=SecurtyModel.find_all_SecurtyFeature()
    for name in FitzarsNames:
        filename=app.config['UPLOAD_FOLDER'] + "/" +appName+"_Method2_"+name.name+".jpg"
        if os.path.exists(filename):
          os.remove(filename)



# Edit Application
@app.route('/edit_application/<string:id>', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def edit_application(id):
    # Get form
    form = ApplicationForm(request.form)
    application=ApplicationModel.find_by_id(id)
    # Populate application form fields
    form.realName.data = application.realName
    form.falseName.data = application.falseName
    # form.categoryId.data = application.categoryId
    privacyFacts=PrivacyModel.find_all_PrivacyFact()
    rankPrivacies=RankPrivacyModel.find_all_RankPrivacy()
    securtyFeatures=SecurtyModel.find_all_SecurtyFeature()
    rankSecurties=RankSecurtyModel.find_all_RankSecurty()
    if request.method == 'POST' :
            # check if the post request has the file part
            if 'method1image' not in request.files or 'method2image' not in request.files:
                flash('לא נבחרה תמונה לאפליקציה', 'danger')
                return redirect(request.url)
            file = request.files['method1image']
            file1 = request.files['method2image']
            files=request.files.getlist('newFitzarsImage')
            FitzarsNames=request.form.getlist("fitzarName")
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '' or file1.filename == '':
                flash('לא נבחרה תמונה לאפליקציה', 'danger')
                return redirect(request.url)
            if( not (allowed_file(file.filename)) or not (allowed_file(file1.filename))):
                flash('סוג הקובץ אינו מורשה!', 'danger')
                return redirect(request.url)
            realName = request.form['realName']
            falseName = request.form['falseName']
            categoryId = request.form['categoryId']
            k=0
            securityRankIdFeatures = request.form.getlist('securty_fizer')
            PrivacyApplictionModel.delete_by_applicationID(id)
            privacies=PrivacyModel.find_all_PrivacyFact()
            removeFiless(application.falseName)
            for privacy in privacies:
                privacyRank=request.form.getlist('privacy'+str(privacy.name))
                if(not(privacyRank)):
                    return "Erore"+privacy.name
                PrivacyAppliction=PrivacyApplictionModel(privacy.id,int(privacyRank[0]),1,application.id)
                PrivacyAppliction.save_to_db()
                PrivacyAppliction=PrivacyApplictionModel(privacy.id,int(privacyRank[1]),2,application.id)
                PrivacyAppliction.save_to_db()
            SecurityApplictionModel.delete_by_applicationID(id)
            securities=SecurtyModel.find_all_SecurtyFeature()
            for security in securities:
                securityRank=request.form.getlist('securty'+str(security.name))
                if(not(securityRank)):
                    return "Erore"+security.name
                securityAppliction=SecurityApplictionModel(security.id,int(securityRank[0]),1,application.id,"")
                securityAppliction.save_to_db()
                i=0
                savedName=""
                for Fitzars in files:
                    if(allowed_file(Fitzars.filename)==False):
                        flash('סוג הקובץ אינו מורשה!', 'danger')
                        return redirect(request.url)
                    else:
                        if FitzarsNames[i] == security.name:
                            savedName=falseName + "_Method2_"+ FitzarsNames[i] +".jpg"
                            Fitzars.save(os.path.join(app.config['UPLOAD_FOLDER'], savedName))
                    i+=1
                securityAppliction=SecurityApplictionModel(security.id,int(securityRank[0]),2,application.id,savedName)
                securityAppliction.save_to_db()
            if file:
                filename = falseName + "_Method1.jpg"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                picture1=filename
                if file1:
                    filename =falseName + "_Method2.jpg"
                    file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    picture2=filename
                    application.realName=realName
                    application.falseName=falseName
                    application.categoryId=categoryId
                    application.picture1=picture1
                    application.picture2=picture2
                    application.update_db()
                    flash('האפליקציה עודכנה', 'success')
                    return redirect(url_for('applicationDashboard'))
    return render_template('edit_application.html', form=form,privacyFacts=privacyFacts,rankPrivacies=rankPrivacies,securtyFeatures=securtyFeatures,rankSecurties=rankSecurties,categoryId=application.categoryId)


# Delete Application
@app.route('/delete_appliction/<string:id>', methods=['POST'])
@is_logged_in
@is_admin
def delete_appliction(id):
    application=ApplicationModel.find_by_id(id)
    removeFiless(application.falseName)
    PrivacyApplictionModel.delete_by_applicationID(id)
    SecurityApplictions=SecurityApplictionModel.find_by_applicationID(id)
    for SecurityAppliction in SecurityApplictions:
        SecurityApplictionDescriptionModel.delete_by_securityApplictionID(SecurityAppliction.id)
    SecurityApplictionModel.delete_by_applicationID(id)
    ApplicationModel.delete_by_id(id)
    flash('אפליקציה נמחקה', 'success')
    return redirect(url_for('applicationDashboard'))


# editUserDetails
@app.route('/editUserDetails', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def editUserDetailes():
    if request.method == 'POST':
        UserDetailsTemplateModel.delete_all_rows()
        editNames=request.form.getlist("editname")
        editattrs=request.form.getlist("editattr")
        editType=request.form.getlist("edittype")
        i=0
        for i in range(0,len(editType)):
            if(UserDetailsTemplateModel.find_by_attr(editattrs[i].replace(" ", "_"))!=False):
                continue
            UserDetails =UserDetailsTemplateModel(editNames[i],editattrs[i].replace(" ", "_"),editType[i])
            UserDetails.save_to_db()
        return redirect(url_for('administratorMenu'))
    UserDetails=UserDetailsTemplateModel.find_all_UserDetailsTempate()
    if(UserDetails==False):
        UserDetails=[]
    return render_template('editUserDetails.html',UserDetails=UserDetails)





# UserDetails
@app.route('/UserDetails', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def UserDetails():
    users=UserModel.find_all_user()
    experiments=ExperimentModel.find_all_Experiment_run()
    return render_template('UserDetails.html',users=users,experiments=experiments)

# removePermission
@app.route('/removePermission',methods=['GET', 'POST'])
@is_logged_in
@is_admin
def removePermission():
    if request.method == 'POST':
        userId=request.form['userId']
        user=UserModel.find_by_id(int(userId))
        user.startSurvy=0
        user.update_db()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


# addPermission
@app.route('/addPermission',methods=['GET', 'POST'])
@is_logged_in
@is_admin
def addPermission():
    if request.method == 'POST':
        userId=request.form['userId']
        type=request.form['type']
        user=UserModel.find_by_id(int(userId))
        exp=ExperimentModel.find_by_id(int(type))
        if(user!=False and exp!=False):
            user.startSurvy=1
            user.ExperimentId=int(type)
            user.update_db()
            ExperimentDetaileArry=ExperimentDetaileModel.get_ExperimentDetaile(exp.id)
            for ExperimentDetaile in ExperimentDetaileArry:
                ExperimentDetaile.userID=user.id
                ExperimentDetaile.update_db()
            participationEmail(user.email)
        else:
            print("Erore!!")
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

# editUserDetails
@app.route('/editApplictionDetails', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def editApplictionDetails():
    if request.method == 'POST':
        FactNames=request.form.getlist("FactName")
        FactNums=request.form.getlist("FactNum")
        FizerNames=request.form.getlist("FizerName")
        FizerNums=request.form.getlist("FizerNum")
        PrivacyModel.delete_all_rows()
        RankPrivacyModel.delete_all_rows()
        SecurtyModel.delete_all_rows()
        RankSecurtyModel.delete_all_rows()
        i=0
        for i in range(0,len(FactNames)):
            privacyFact=PrivacyModel(FactNames[i])
            privacyFact.save_to_db()
            i+=1
        for FactNum in FactNums:
            rankPrivacy=RankPrivacyModel(FactNum)
            rankPrivacy.save_to_db()
        i=0
        for i in range(0,len(FizerNames)):
            if(FizerNames[i]==''):
                FizerNames[i]='0'
            securtyFeature=SecurtyModel(FizerNames[i])
            securtyFeature.save_to_db()
            i+=1
        for FizerNums in FizerNums:
            rankSecurty=RankSecurtyModel(FizerNums)
            rankSecurty.save_to_db()
        flash('הנתונים נשמרו בהצלחה' , 'success')
        return redirect(url_for('administratorMenu'))
    privacyFacts=PrivacyModel.find_all_PrivacyFact()
    rankPrivacies=RankPrivacyModel.find_all_RankPrivacy()
    securtyFeatures=SecurtyModel.find_all_SecurtyFeature()
    rankSecurties=RankSecurtyModel.find_all_RankSecurty()
    return render_template('editApplictionDetails.html',privacyFacts=privacyFacts,rankPrivacies=rankPrivacies,securtyFeatures=securtyFeatures,rankSecurties=rankSecurties)

# questionDashboard
@app.route('/questionDashboard', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def questionDashboard():
    if request.method == 'POST':
        newQustions=request.form.getlist("newQustion")
        section=request.form.getlist("newSection")
        newOption=request.form.getlist("newOption")
        newAnswer=request.form.getlist("newAnswer")
        i=0
        j=0
        for i in range(0,len(newQustions)):
            # return str(newQustions[i]+":"+section[i])
            if(newOption[i]=='3'):
                question=QuestionModel(newQustions[i],section[i],newOption[i],newAnswer[j],newAnswer[j+1],newAnswer[j+2],newAnswer[j+3])
                j+=4;
            else:
                question=QuestionModel(newQustions[i],section[i],newOption[i],"","","","")
            i+=1
            question.save_to_db()
        flash('השאלות נוספו בהצלחה' , 'success')

    questions=(QuestionModel.find_all_Question())
    if(questions==None):
        questions=[]
    return render_template('questionDashboard.html', questions=questions)


#edit_question
@app.route('/edit_question', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def edit_question():
    if request.method == 'POST':
        questionId=request.form['questionId']
        questionText=request.form['question']
        question=QuestionModel.find_by_id(questionId)
        question.question=questionText
        question.update_db()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


# Delete question
@app.route('/delete_question', methods=['POST'])
@is_logged_in
@is_admin
def delete_question():
    if request.method == 'POST':
        questionId=request.form['questionId']
        QuestionModel.delete_by_id(questionId)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/surveyManagement', methods=['POST','GET'])
@is_logged_in
@is_admin
def surveyManagement():
    applictions=[]
    for i in range(1,5):
        if(ApplicationModel.find_by_categoryId(i)==None):
            applictions.append([])
        else:
            applictions.append(ApplicationModel.find_by_categoryId(i))
    # if request.method == 'POST':
    #     questionId=request.form['questionId']
    #     QuestionModel.delete_by_id(questionId)
    #     return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    return render_template('surveyManagement.html', applictions1=applictions[0],applictions2=applictions[1],applictions3=applictions[2],applictions4=applictions[3])


def createExperiment(numberParti,appsIds,experiment,new):
    arrayApp=[]
    for i in range(0,4):
        arrayApp.append([])
    for appId in appsIds:
        app=ApplicationModel.find_by_id(appId)
        arrayApp[app.categoryId-1].append(appId)
    numOfAppInCat=len(arrayApp[0])
    if(experiment.type=='1'):
        Round=int(int(numberParti)/24)
        for i in range(0,Round):
            order=[]
            for j in range(0,12):
                one=1
                two=1
                three=1
                four=1
                while True:
                    one=random.randint(0,3)
                    two=random.randint(0,3)
                    three=random.randint(0,3)
                    four=random.randint(0,3)
                    if (one==two or one==three or one==four or two==three or two==four or three==four):
                        continue;
                    # print('one: '+str(one)+',two: '+str(two)+',three: '+str(three)+',four: '+str(four))
                    # print('one: '+str(arrayApp[one][0])+',two: '+str(arrayApp[two][0])+',three: '+str(arrayApp[three][0])+',four: '+str(arrayApp[four][0]))
                    stringOrder=""+str(one)+","+str(two)+","+str(three)+","+str(four)
                    if stringOrder not in order:
                        order.append(stringOrder)
                        break;
                for Index in range(0,numOfAppInCat):
                    ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[one][Index],1,0,0,i*24+j)
                    ExperimentDetaile.save_to_db()
                    ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[two][Index],1,0,0,i*24+j)
                    ExperimentDetaile.save_to_db()
                    ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[three][Index],1,0,0,i*24+j)
                    ExperimentDetaile.save_to_db()
                    ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[four][Index],1,0,0,i*24+j)
                    ExperimentDetaile.save_to_db()
            for j in range(0,12):
                one=1
                two=1
                three=1
                four=1
                while True:
                    one=random.randint(0,3)
                    two=random.randint(0,3)
                    three=random.randint(0,3)
                    four=random.randint(0,3)
                    if (one==two or one==three or one==four or two==three or two==four or three==four):
                        continue;
                    stringOrder=""+str(one)+","+str(two)+","+str(three)+","+str(four)
                    if stringOrder not in order:
                        order.append(stringOrder)
                        break;
                for Index in range(0,numOfAppInCat):
                    ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[one][Index],2,0,0,i*24+j+12)
                    ExperimentDetaile.save_to_db()
                    ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[two][Index],2,0,0,i*24+j+12)
                    ExperimentDetaile.save_to_db()
                    ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[three][Index],2,0,0,i*24+j+12)
                    ExperimentDetaile.save_to_db()
                    ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[four][Index],2,0,0,i*24+j+12)
                    ExperimentDetaile.save_to_db()
    else:
        if (experiment.type=='2'):
            Round=int(int(numberParti)/24)
            for i in range(0,Round):
                order=[]
                for j in range(0,24):
                    one=1
                    two=1
                    three=1
                    four=1
                    while True:
                        one=random.randint(0,3)
                        two=random.randint(0,3)
                        three=random.randint(0,3)
                        four=random.randint(0,3)
                        if (one==two or one==three or one==four or two==three or two==four or three==four):
                            continue;
                        stringOrder=""+str(one)+","+str(two)+","+str(three)+","+str(four)
                        if stringOrder not in order:
                            order.append(stringOrder)
                            break;
                    for Index in range(0,numOfAppInCat):
                        ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[one][Index],3,0,0,i*24+j)
                        ExperimentDetaile.save_to_db()
                        ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[two][Index],3,0,0,i*24+j)
                        ExperimentDetaile.save_to_db()
                        ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[three][Index],3,0,0,i*24+j)
                        ExperimentDetaile.save_to_db()
                        ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[four][Index],3,0,0,i*24+j)
                        ExperimentDetaile.save_to_db()
        else:
            Round=int(int(numberParti)/24)
            for i in range(0,Round):
                order=[]
                for j in range(0,24):
                    one=1
                    two=1
                    three=1
                    four=1
                    while True:
                        one=random.randint(0,3)
                        two=random.randint(0,3)
                        three=random.randint(0,3)
                        four=random.randint(0,3)
                        if (one==two or one==three or one==four or two==three or two==four or three==four):
                            continue;
                        stringOrder=""+str(one)+","+str(two)+","+str(three)+","+str(four)
                        if stringOrder not in order:
                            order.append(stringOrder)
                            break;
                    if not(new):
                        for Index in range(0,numOfAppInCat):
                            ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[one][Index],4,0,0,i*24+j)
                            ExperimentDetaile.save_to_db()
                            ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[two][Index],4,0,0,i*24+j)
                            ExperimentDetaile.save_to_db()
                            ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[three][Index],4,0,0,i*24+j)
                            ExperimentDetaile.save_to_db()
                            ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[four][Index],4,0,0,i*24+j)
                            ExperimentDetaile.save_to_db()
                    else:
                        for Index in range(0,numOfAppInCat):
                            ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[one][Index],5,0,0,i*24+j)
                            ExperimentDetaile.save_to_db()
                            ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[two][Index],5,0,0,i*24+j)
                            ExperimentDetaile.save_to_db()
                            ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[three][Index],5,0,0,i*24+j)
                            ExperimentDetaile.save_to_db()
                            ExperimentDetaile=ExperimentDetaileModel(experiment.id,arrayApp[four][Index],5,0,0,i*24+j)
                            ExperimentDetaile.save_to_db()


@app.route('/start_survy', methods=['POST','GET'])
@is_logged_in
@is_admin
def start_survy():
    if request.method == 'POST':
        type=request.form['type']
        numberParti=request.form['numberParti']
        checkboxLen=request.form['checkboxLen']
        new=False
        if(int(type)==3):
            if(request.form['new']=='true'):
                new=True
            else:
                new=False
        appsIds=[]
        for i in range(0,int(checkboxLen)):
            appsIds.append(request.form[str(i)])
        experiment=ExperimentModel(type,numberParti,checkboxLen,1)
        experiment.save_to_db()
        for appIds in appsIds:
            ExperimentApp=ExperimentAppModel(experiment.id,appIds)
            ExperimentApp.save_to_db()
        createExperiment(numberParti,appsIds,experiment,new)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/stop_survy', methods=['POST','GET'])
@is_logged_in
@is_admin
def stop_survy():
    if request.method == 'POST':
        type=request.form['type']
        Experiments=ExperimentModel.find_all_Experiment_run()
        for Experiment in Experiments:
            if(int(Experiment.type) == int(type)):
                Experiment.run=0
                Experiment.update_db()
                break
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/experimentRun', methods=['GET'])
@is_logged_in
@is_admin
def experimentRun():
    if request.method == 'GET':
        experimentsRun=ExperimentModel.find_all_Experiment_run()
        for experimentRun in experimentsRun:
            if(experimentRun.leftParti==0):
                experimentRun.run=0
                experimentRun.update_db()
        experimentsRuns=ExperimentModel.find_all_Experiment_run()
        sendBack=[]
        for experimentRun in experimentsRuns:
            sendBack.append(experimentRun.type)
            sendBack.append(experimentRun.numberParti)
            sendBack.append(experimentRun.leftParti)
        return json.dumps(sendBack)

@app.route('/experimentAppRun', methods=['GET'])
@is_logged_in
@is_admin
def experimentAppRun():
    if request.method == 'GET':
        experimentsRun=ExperimentModel.find_all_Experiment_run()
        sendBack=[]
        for experimentRun in experimentsRun:
            appsByExperimentID=ExperimentAppModel.find_ExperimentApp_by_ExperimentID(experimentRun.id)
            sendBack.append(experimentRun.type)
            if(experimentRun.type==3):
                experimentDetaile=ExperimentDetaileModel.get_ExperimentDetaile(experimentRun.id);
                if(len(experimentDetaile)>0):
                    if(experimentDetaile[0].questionDisplay==4):
                        sendBack.append('old: '+str(experimentDetaile[0].questionDisplay))
                    else:
                        sendBack.append('new: '+str(experimentDetaile[0].questionDisplay))
            for appByExperimentID in appsByExperimentID:
                sendBack.append(appByExperimentID.applicationId)
            sendBack.append(-1)
        return json.dumps(sendBack)

@app.route('/Reports', methods=['GET'])
@is_logged_in
@is_admin
def Reports():
    return render_template('Reports.html')



@app.route('/UserReport', methods=['GET'])
@is_logged_in
@is_admin
def UserReport():
    userDetailsTemplate=UserDetailsTemplateModel.find_all_UserDetailsTempate()
    columnNames=[]
    columnNames.append('id')
    columnNames.append('name')
    columnNames.append('email')
    if userDetailsTemplate!=False:
        for userDetaileTemplate in userDetailsTemplate:
            columnNames.append(str(userDetaileTemplate.attr))
    temp=unionModel.getUsersTable()
    Table=[]
    for row in temp:
        Table.append(row.values())
    # return str(unionModel.getUsersTable())
    return render_template('UserReport.html',columnNames=columnNames,Table=Table)

@app.route('/exportUsers', methods=['GET'])
@is_logged_in
@is_admin
def exportUsers():
    Table=unionModel.getUsersTable()
    userDetailsTemplate=UserDetailsTemplateModel.find_all_UserDetailsTempate()
    columnNames=[]
    newData={}
    columnNames.append('id')
    newData['id']=[]
    columnNames.append('name')
    newData['name']=[]
    columnNames.append('email')
    newData['email']=[]
    for userDetaileTemplate in userDetailsTemplate:
        columnNames.append(str(userDetaileTemplate.attr))
        newData[str(userDetaileTemplate.attr)]=[]
    for rows in Table:
        for columnName in columnNames:
            newData[str(columnName)].append(rows[columnName])
    # Create a Pandas dataframe from some data.
    df = pd.DataFrame(newData,columns=columnNames)
    output = BytesIO()
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(output,engine='xlsxwriter')
    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    output.seek(0)
    return send_file(output, attachment_filename=time.strftime('Users_%Y-%m-%d__%H-%M.xlsx'), as_attachment=True)


@app.route('/ApplicationReport', methods=['GET'])
@is_logged_in
@is_admin
def ApplicationReport():
    Table=unionModel.getApplictionTable()
    # return(str(Table))
    Traditional_summary_old_array={}
    Traditional_summary_new_array={}
    Contextual_array={}
    for row in Table:
        for key,val in row.items():
            if(key=='Traditional_summary_old'):
                Traditional_summary_old_array[row['id']]=val
            if(key=='Traditional_summary_new'):
                Traditional_summary_new_array[row['id']]=val
            if(key=='Contextual'):
                Contextual_array[row['id']]=val

    return render_template('ApplicationReport.html',Table=Table,Traditional_summary_old_array=Traditional_summary_old_array,Traditional_summary_new_array=Traditional_summary_new_array,Contextual_array=Contextual_array)


@app.route('/exportAppliction/<string:appID>', methods=['GET'])
@is_logged_in
@is_admin
def exportAppliction(appID):
    Table=unionModel.getApplictionTable()
    file_name=""
    for row in Table:
        if(row['id']==str(appID)):
            columnNames1=[]
            newData1={}
            columnNames1.append('id')
            newData1['id']=[]
            columnNames1.append('realName')
            newData1['realName']=[]
            columnNames1.append('falseName')
            newData1['falseName']=[]
            columnNames1.append('category')
            newData1['category']=[]
            newData1['id'].append(row['id'])
            newData1['realName'].append(row['realName'])
            newData1['falseName'].append(row['falseName'])
            newData1['category'].append(row['category'])
            file_name+=row['falseName']
            columnNames2=[]
            newData2={}
            newData2['privacy']=[]
            newData2['privacyRank']=[]
            newData2['securty']=[]
            newData2['securtyRank']=[]
            columnNames2.append('privacy')
            columnNames2.append('privacyRank')
            columnNames2.append('securty')
            columnNames2.append('securtyRank')
            for key,value in row['Traditional_summary_old'].items():
                if(key=='Privacy'):
                    for internalKey,internalValue in value.items():
                        newData2['privacy'].append(internalKey)
                        newData2['privacyRank'].append(internalValue)
                if(key=='Security'):
                    for internalKey,internalValue in value.items():
                        newData2['securty'].append(internalKey)
                        newData2['securtyRank'].append(internalValue)
            while(len(newData2['privacy']) != len(newData2['securty'])):
                newData2['securty'].append('')
                newData2['securtyRank'].append('')
            columnNames3=[]
            newData3={}
            newData3['privacy']=[]
            newData3['privacyRank']=[]
            newData3['securty']=[]
            newData3['securtyRank']=[]
            columnNames3.append('privacy')
            columnNames3.append('privacyRank')
            columnNames3.append('securty')
            columnNames3.append('securtyRank')
            for key,value in row['Traditional_summary_new'].items():
                if(key=='Privacy'):
                    for internalKey,internalValue in value.items():
                        newData3['privacy'].append(internalKey)
                        newData3['privacyRank'].append(internalValue)
                if(key=='Security'):
                    for internalKey,internalValue in value.items():
                        newData3['securty'].append(internalKey)
                        newData3['securtyRank'].append(internalValue)
            while(len(newData3['privacy']) != len(newData3['securty'])):
                newData3['securty'].append('')
                newData3['securtyRank'].append('')
            sheet_names=[]
            newData4={}
            columnNames4=[]
            columnNames4.append('privacy')
            columnNames4.append('privacyRank')
            for key,value in row['Contextual'].items():
                sheet_names.append(key)
                newData4[key]={}
                newData4[key]['privacy']=[]
                newData4[key]['privacyRank']=[]
                for internalKey,internalValue in value.items():
                    newData4[key]['privacy'].append(internalKey)
                    newData4[key]['privacyRank'].append(internalValue)
            break;
    df1 = pd.DataFrame(newData1,columns=columnNames1)
    df2 = pd.DataFrame(newData2,columns=columnNames2)
    df3 = pd.DataFrame(newData3,columns=columnNames3)
    df4 = {}
    for sheet_name in sheet_names:
        df4[sheet_name]=pd.DataFrame(newData4[sheet_name],columns=columnNames4)
    output = BytesIO()
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(output,engine='xlsxwriter')
    # Convert the dataframe to an XlsxWriter Excel object.
    df1.to_excel(writer, sheet_name='general_info')
    df2.to_excel(writer, sheet_name='Traditional_summary_old')
    df3.to_excel(writer, sheet_name='Traditional_summary_new')
    for sheet_name in sheet_names:
        df4[sheet_name].to_excel(writer, sheet_name=sheet_name)
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    output.seek(0)
    return send_file(output, attachment_filename=time.strftime(file_name+'_%Y-%m-%d__%H-%M.xlsx'), as_attachment=True)




@app.route('/ExperimentReport', methods=['GET'])
@is_logged_in
@is_admin
def ExperimentReport():
    Table=unionModel.getExperimentTable()
    # return str(Table)
    return render_template('ExperimentReport.html',Table=Table)


@app.route('/exportExperiment/<string:ExperimentID>', methods=['GET'])
@is_logged_in
@is_admin
def exportExperiment(ExperimentID):
    Table=unionModel.getExperimentTable()
    file_name=""
    for row in Table:
        if(row['id']==str(ExperimentID)):
            columnNames1=[]
            newData1={}
            columnNames1.append('id')
            newData1['id']=[]
            columnNames1.append('type')
            newData1['type']=[]
            columnNames1.append('Number of participants')
            newData1['Number of participants']=[]
            columnNames1.append('app in experiment')
            newData1['app in experiment']=[]
            columnNames1.append('done')
            newData1['done']=[]
            newData1['id'].append(row['id'])
            newData1['type'].append(row['type'])
            newData1['Number of participants'].append(row['Number of participants'])
            for value in row['app in experiment']:
                newData1['app in experiment'].append(value)
            newData1['done'].append(row['done'])
            file_name+='Experiment_'+str(row['id'])
            columnNames2=[]
            columnNames2.append('id')
            columnNames2.append('user')
            columnNames2.append('order')
            columnNames2.append('questionDisplay')
            newData2={}
            newData2['id']=[]
            newData2['user']=[]
            newData2['order']=[]
            newData2['questionDisplay']=[]
            for key,value in row['ExperimentDetaile'].items():
                newData2['id'].append(key)
                for internalkey,internalvalue in value.items():
                    if(internalkey == 'order'):
                        temp=''
                        i=0
                        for val in internalvalue:
                            if(i!=len(internalvalue)-1):
                                temp+=str(val)+' => '
                            else:
                                temp+=str(val)
                            i+=1
                        newData2['order'].append(temp)
                    else:
                        newData2[internalkey].append(internalvalue)
            break;

    for i in range(0,len(newData1['app in experiment'])-1):
        newData1['id'].append('')
        newData1['type'].append('')
        newData1['Number of participants'].append('')
        newData1['done'].append('')

    # print(str(newData2))


    df1 = pd.DataFrame(newData1,columns=columnNames1)
    df2 = pd.DataFrame(newData2,columns=columnNames2)
    output = BytesIO()
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(output,engine='xlsxwriter')
    # Convert the dataframe to an XlsxWriter Excel object.
    df1.to_excel(writer, sheet_name='general_info')
    df2.to_excel(writer, sheet_name='ExperimentDetaile')
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    output.seek(0)
    return send_file(output, attachment_filename=time.strftime(file_name+'_%Y-%m-%d__%H-%M.xlsx'), as_attachment=True)



@app.route('/answerReport/<string:ExperimentID>', methods=['GET'])
@is_logged_in
@is_admin
def answerReport(ExperimentID):
    Table=unionModel.getAnswerTable(int(ExperimentID))
    Securties=SecurtyModel.find_all_SecurtyFeature()
    SecurtyDict=unionModel.getSecurtyDict(Securties)
    Questions=QuestionModel.find_all_Question()
    QuestionsArrGenral=[]
    for Question in Questions:
        if(Question.section==2):
            QuestionsArrGenral.append(Question.question)


    # return str(Table)
    return render_template('answerReport.html',Table=Table,columns=SecurtyDict.values(),expId=int(ExperimentID),QuestionsArrGenral=QuestionsArrGenral)


@app.route('/exportAnswer/<string:ExperimentID>', methods=['GET'])
@is_logged_in
@is_admin
def exportAnswer(ExperimentID):
    genralFlag=False
    Table=unionModel.getAnswerTable(int(ExperimentID))
    Securties=SecurtyModel.find_all_SecurtyFeature()
    generalReports=generalReportModel.find_by_experimentId(ExperimentID)
    users=UserModel.find_all_user()
    dictUser=unionModel.getUsersDict(users)
    Questions=QuestionModel.find_all_Question()
    dictQustion=unionModel.getQustionDict(Questions)


    columnNames1=[]
    newDataTemp={}
    columnNames1.append('question')
    newDataTemp['question']=[]
    columnNames1.append('user')
    newDataTemp['user']=[]
    columnNames1.append('Traditional_summary_old')
    newDataTemp['Traditional_summary_old']=[]
    columnNames1.append('Traditional_summary_new')
    newDataTemp['Traditional_summary_new']=[]
    for Securty in Securties:
        columnNames1.append(Securty.name)
        newDataTemp[Securty.name]=[]
    columnNames1.append('question_display')
    newDataTemp['question_display']=[]


    # general
    columnNames2=[]
    newData2={}

    columnNames2.append('user')
    newData2['user']=[]
    for Question in Questions:
        if(Question.section==2):
            columnNames2.append(dictQustion[Question.id])
            newData2[dictQustion[Question.id]]=[]


    newData1={}
    df1={}
    i=1
    for row in Table:
        sheet_name="answer_experiment_"+str(i)
        newData1[sheet_name]=""
        newData1[sheet_name]=copy.deepcopy(newDataTemp)
        for key,value in row.items():
            if(key != 'general report'):
                for inkey,invalue in value.items():
                    for inInkey,inInvalue in invalue.items():
                        newData1[sheet_name]['question'].append(inInkey)
                        for inInInkey,inInInvalue in inInvalue.items():
                            newData1[sheet_name][inInInkey].append(inInInvalue)
                        newData1[sheet_name]['question_display'].append(inkey)
                if(list(row.keys()).index(key)+1 != len(row.keys())):
                    newData1[sheet_name]['question'].append('###')
                    newData1[sheet_name]['question'].append('###')
                    newData1[sheet_name]['user'].append('###')
                    newData1[sheet_name]['user'].append('###')
                    newData1[sheet_name]['Traditional_summary_old'].append('###')
                    newData1[sheet_name]['Traditional_summary_old'].append('###')
                    newData1[sheet_name]['Traditional_summary_new'].append('###')
                    newData1[sheet_name]['Traditional_summary_new'].append('###')
                    for Securty in Securties:
                        newData1[sheet_name][Securty.name].append('###')
                        newData1[sheet_name][Securty.name].append('###')
                    newData1[sheet_name]['question_display'].append('###')
                    newData1[sheet_name]['question_display'].append('###')
            else:
                genralFlag=True
                sheet_name="general report"
                for inkey,invalue in value.items():
                    newData2['user'].append(inkey)
                    for inInkey,inInvalue in invalue.items():
                        newData2[inInkey]=inInvalue
        if(not (genralFlag)):
            df1[sheet_name]=pd.DataFrame(newData1[sheet_name],columns=columnNames1)
        else:
            df1[sheet_name]=pd.DataFrame(newData2,columns=columnNames2)

        i+=1
    output = BytesIO()
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(output,engine='xlsxwriter')
    # Convert the dataframe to an XlsxWriter Excel object.
    for key,val in df1.items():
        val.to_excel(writer, sheet_name=key)
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    output.seek(0)
    return send_file(output, attachment_filename=time.strftime('answer_' + str(ExperimentID)+'_%Y-%m-%d__%H-%M.xlsx'), as_attachment=True)








def registrationEmail(you):
    me = "managesurveyprivacy@gmail.com"
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "אישור הרשמה"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    html = """\
    <html>
      <head></head>
      <body>
        <p style="text-align: center;"><span style="font-family: "Arial",sans-serif;">אישור הרשמה<br /><br /></span></p><p style="text-align: right;"><span style="font-size: 10.0pt; line-height: 107%; font-family: "Arial",sans-serif;">תודה שנרשמת להשתתפות בסקר! </span></p><p style="text-align: right;"><span style="font-size: 10.0pt; line-height: 107%; font-family: "Arial",sans-serif;">בזמן הקרוב תקבל מייל אישור כניסה למערכת , תודה</span><span style="font-size: 10.0pt; line-height: 107%; font-family: "Segoe UI Emoji",sans-serif;"></span></p>
      </body>
    </html>
    """
    text="אישור הרשמה\n תודה שרשמת להתתפות בסקר!\n בזמן הקרוב תקבל מייל אישור כניסה למערכת,תודה!"

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    # Send the message via local SMTP server.
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()
    s.starttls()
    s.login('managesurveyprivacy@gmail.com','Asd014789')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()
def participationEmail(you):
    me = "managesurveyprivacy@gmail.com"
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "הזמנה להשתתפות בסקר"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    html = """\
    <html>
      <head></head>
      <body>
      <p style="text-align: center;"><span style="font-family: "Arial",sans-serif;">רשאי להשתתף בסקרה<br /><br /></span></p><p style="text-align: right;"><span style="font-size: 10.0pt; line-height: 107%; font-family: "Arial",sans-serif;">!כעת תוכל להשתתף בסקר </span></p><p style="text-align: right;"><span style="font-size: 10.0pt; line-height: 107%; font-family: "Arial",sans-serif;">:כדי להשתתף הכנס עם פרטי ההתחברות שלך ללינק הבא http://68.183.218.37:5000/</span></p><p style="text-align: right;"><span style="font-size: 10.0pt; line-height: 107%; font-family: "Arial",sans-serif;">:אם שכחת את פרטי ההתחברות שלך ניתן לפנות ליצחק במייל itzhaco@ac.sce.ac.il </span></p>
      </body>
    </html>
    """

    text="רשאי להשתתף בסקר\nכעת תוכל להשתתף בסקר!\nכדי להשתתף הכנס עם פרטי ההתחברות שלך ללינק הבא: http://68.183.218.37:5000/ \n (אם שכחת את פרטי ההתחברות שלך ניתן לפנות ליצחק במייל: itzhaco@ac.sce.ac.il"

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    # Send the message via local SMTP server.
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()
    s.starttls()
    s.login('managesurveyprivacy@gmail.com','Asd014789')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()

################################# participant #################################

# agreedPage
@app.route('/agreedPage/<string:id>', methods=['GET', 'POST'])
@is_logged_in
@is_participant
@is_notAgreed
def agreedPage(id):
    if request.method == 'POST':
        if request.form.get("myCheck"):
            flash('ההסכם אושר', 'success')
            user=UserModel.find_by_id(id)
            user.agreed=2
            user.update_db()
            session['agreed']=True

            return redirect(url_for('participantMenu'))
        else:
            flash('אנא אשר כדי להמשיך', 'danger')
    return render_template('agreedPage.html')




# participantMenu
@app.route('/participantMenu')
@is_logged_in
@is_participant
@is_agreed
@is_startSurvy
def participantMenu():
    if(saverModel.getExperimentDetaile(session['id'],session['expId'])==False):
        return redirect(url_for('Survey_part2'))
    return render_template('participantMenu.html')

@app.route('/Survey', methods=['POST','GET'])
@is_logged_in
@is_participant
@is_agreed
@is_startSurvy
def Survey():
    data=helper.getData(session['id'],session['expId'])
    if(data==False):
        return redirect(url_for('Survey_part2'))
    allQuestions=QuestionModel.find_all_Question()
    type1=False
    type2=False
    type3=False
    questions=[]
    for question in allQuestions:
        if(question.type==1 and question.section==1):
            type1=True
            questions.append(question)
        else:
            if(question.type==2 and question.section==1 ):
                type2=True
                questions.append(question)
            else:
                if(question.type==3 and question.section==1 ):
                    type3=True
                    questions.append(question)

    # return str(data)
    return render_template('Survey.html',questions=questions,type1=type1,type2=type2,type3=type3,data=data,answers=[1,2,3,4,5,6,7])

@app.route('/Survey_part2')
@is_logged_in
@is_participant
@is_agreed
@is_startSurvy
def Survey_part2():
        allQuestions=QuestionModel.find_all_Question()
        type1=False
        type2=False
        type3=False
        questions=[]
        for question in allQuestions:
            if(question.type==1 and question.section==2):
                type1=True
                questions.append(question)
            else:
                if(question.type==2 and question.section==2 ):
                    type2=True
                    questions.append(question)
                else:
                    if(question.type==3 and question.section==2 ):
                        type3=True
                        questions.append(question)
        return render_template('Survey_part2.html',questions=questions,type1=type1,type2=type2,type3=type3,answers=[1,2,3,4,5,6,7])

@app.route('/saveReports', methods=['POST'])
@is_logged_in
@is_participant
@is_agreed
@is_startSurvy
def saveReports():
    if request.method == 'POST':
        helper.setReport(session['id'],session['expId'],request)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/saveReportsPart2', methods=['POST'])
@is_logged_in
@is_participant
@is_agreed
@is_startSurvy
def saveReportsPart2():
    if request.method == 'POST':
        helper.setReportPart2(session['id'],request)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/thankYou')
@is_logged_in
@is_participant
@is_agreed
@is_startSurvy
def thankYou():
    user=UserModel.find_by_id(session['id'])
    user.startSurvy=0
    user.update_db()
    experiment=ExperimentModel.find_by_id(user.ExperimentId)
    experiment.leftParti-=1
    experiment.update_db()
    session.clear()
    return render_template('thankYou.html')





##################################################################




if __name__ == '__main__':
    from db import mysql
    mysql.init_app(app)

    # from db import db
    # db.init_app(app)
    app.secret_key='aaa123'
    app.run( debug=True)
