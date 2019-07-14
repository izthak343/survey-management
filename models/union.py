import copy
from models.user import UserModel
from models.userDetails import UserDetailsModel
from models.userDetailsTemplate import UserDetailsTemplateModel
from models.application import ApplicationModel


from models.privacy import PrivacyModel
from models.privacyAppliction import PrivacyApplictionModel
from models.rankPrivacy import RankPrivacyModel

from models.securty import SecurtyModel
from models.securityAppliction import SecurityApplictionModel
from models.rankSecurty import RankSecurtyModel
from models.securityApplictiondesDescription import SecurityApplictionDescriptionModel

from models.experiment import ExperimentModel
from models.experimentApp import ExperimentAppModel
from models.experimentDetaile import ExperimentDetaileModel

from models.report import ReportModel
from models.question import QuestionModel
from models.generalReport import generalReportModel







from db import mysql


class unionModel():

    @classmethod
    def getUsersTable(self):
        users=UserModel.find_all_user()
        userDetailsTemplate=UserDetailsTemplateModel.find_all_UserDetailsTempate()
        userDetails=UserDetailsModel.find_all_UserDetails()
        table=[]
        column={}
        column['id']='-'
        column['name']='-'
        column['email']='-'
        if userDetailsTemplate!=False:
            for userDetaileTemplate in userDetailsTemplate:
                column[str(userDetaileTemplate.attr)]='-'
        for user in users:
            columnCopy=column.copy()
            columnCopy['id']=str(user.id)
            columnCopy['name']=str(user.name)
            columnCopy['email']=str(user.email)
            if userDetails!=False:
                for userDetaile in userDetails:
                    if(userDetaile.userId == user.id):
                        columnCopy[str(userDetaile.attrParent)]=str(userDetaile.value)
            table.append(columnCopy)
        return table

    @classmethod
    def getPrivacyDict(self,privacies):
        Dict={}
        for privacy in privacies:
            Dict[privacy.id]=privacy.name
        return Dict


    @classmethod
    def getPrivacyRankDict(self,RankPrivacies):
        Dict={}
        for RankPrivacy in RankPrivacies:
            Dict[RankPrivacy.id]=RankPrivacy.name
        return Dict


    @classmethod
    def getApplictionsDict(self,applictions):
        Dict={}
        for appliction in applictions:
            Dict[appliction.id]=appliction.falseName
        return Dict

    @classmethod
    def getUsersDict(self,Users):
        Dict={}
        for User in Users:
            Dict[User.id]=str(User.name)+'=>'+str(User.email)
        return Dict


    @classmethod
    def getSecurtyDict(self,Securties):
        Dict={}
        for Securty in Securties:
            Dict[Securty.id]=Securty.name
        return Dict

    @classmethod
    def getSecurtyRankDict(self,RankSecurties):
        Dict={}
        for RankSecurty in RankSecurties:
            Dict[RankSecurty.id]=RankSecurty.name
        return Dict

    @classmethod
    def getQustionDict(self,Qustions):
        Dict={}
        for Qustion in Qustions:
            Dict[Qustion.id]=Qustion.question
        return Dict

    @classmethod
    def getApplictionTable(self):
        applicationsCategory1=ApplicationModel.find_by_categoryId(1)
        applicationsCategory2=ApplicationModel.find_by_categoryId(2)
        applicationsCategory3=ApplicationModel.find_by_categoryId(3)
        applicationsCategory4=ApplicationModel.find_by_categoryId(4)


        privacies=PrivacyModel.find_all_PrivacyFact()
        RankPrivacy=RankPrivacyModel.find_all_RankPrivacy()
        PrivaciesAppliction=PrivacyApplictionModel.find_all_PrivacyFact()

        Securties=SecurtyModel.find_all_SecurtyFeature()
        RankSecurty=RankSecurtyModel.find_all_RankSecurty()
        SecuritiesAppliction=SecurityApplictionModel.find_all_SecurityAppliction()
        SecurityApplictionDescriptions=SecurityApplictionDescriptionModel.find_all()

        table=[]
        privacyDict=unionModel.getPrivacyDict(privacies)
        privacyRankDict=unionModel.getPrivacyRankDict(RankPrivacy)

        SecurtyDict=unionModel.getSecurtyDict(Securties)
        SecurtyRankDict=unionModel.getSecurtyRankDict(RankSecurty)

        for applicationCategory1 in applicationsCategory1:
            column={}
            column['id']=str(applicationCategory1.id)
            column['realName']=str(applicationCategory1.realName)
            column['falseName']=str(applicationCategory1.falseName)
            column['category']='high privacy and high security'
            column['Traditional_summary_old']={}
            column['Traditional_summary_new']={}
            column['Contextual']={}
            column['Traditional_summary_old']['Privacy']={}
            column['Traditional_summary_new']['Privacy']={}
            for PrivacyAppliction in PrivaciesAppliction:
                if(PrivacyAppliction.applicationId==applicationCategory1.id and PrivacyAppliction.part == 1):
                    column['Traditional_summary_old']['Privacy'][str(privacyDict[PrivacyAppliction.privacyId])]=privacyRankDict[PrivacyAppliction.privacyRankId]
                if(PrivacyAppliction.applicationId==applicationCategory1.id and PrivacyAppliction.part == 2):
                    column['Traditional_summary_new']['Privacy'][str(privacyDict[PrivacyAppliction.privacyId])]=privacyRankDict[PrivacyAppliction.privacyRankId]
            column['Traditional_summary_old']['Security']={}
            column['Traditional_summary_new']['Security']={}
            for SecurityAppliction in SecuritiesAppliction:
                if(SecurityAppliction.applicationId==applicationCategory1.id and SecurityAppliction.part == 1):
                    column['Traditional_summary_old']['Security'][str(SecurtyDict[SecurityAppliction.securityId])]=SecurtyRankDict[SecurityAppliction.securityRankId]
                if(SecurityAppliction.applicationId==applicationCategory1.id and SecurityAppliction.part == 2):
                    column['Traditional_summary_new']['Security'][str(SecurtyDict[SecurityAppliction.securityId])]=SecurtyRankDict[SecurityAppliction.securityRankId]
                    if(SecurityAppliction.securityRankIdFeature!=-1):
                        column['Contextual'][str(SecurtyDict[SecurityAppliction.securityId])]={}
                    for SecurityApplictionDescription in SecurityApplictionDescriptions:
                        if(SecurityApplictionDescription.securityApplictionId==SecurityAppliction.id):
                            column['Contextual'][str(SecurtyDict[SecurityAppliction.securityId])][privacyDict[SecurityApplictionDescription.privacyId]]=privacyRankDict[SecurityApplictionDescription.privacyRankId]
            table.append(column)


        for applicationCategory2 in applicationsCategory2:
            column={}
            column['id']=str(applicationCategory2.id)
            column['realName']=str(applicationCategory2.realName)
            column['falseName']=str(applicationCategory2.falseName)
            column['category']='low privacy and high security'
            column['Traditional_summary_old']={}
            column['Traditional_summary_new']={}
            column['Contextual']={}
            column['Traditional_summary_old']['Privacy']={}
            column['Traditional_summary_new']['Privacy']={}
            for PrivacyAppliction in PrivaciesAppliction:
                if(PrivacyAppliction.applicationId==applicationCategory2.id and PrivacyAppliction.part == 1):
                    column['Traditional_summary_old']['Privacy'][str(privacyDict[PrivacyAppliction.privacyId])]=privacyRankDict[PrivacyAppliction.privacyRankId]
                if(PrivacyAppliction.applicationId==applicationCategory2.id and PrivacyAppliction.part == 2):
                    column['Traditional_summary_new']['Privacy'][str(privacyDict[PrivacyAppliction.privacyId])]=privacyRankDict[PrivacyAppliction.privacyRankId]
            column['Traditional_summary_old']['Security']={}
            column['Traditional_summary_new']['Security']={}
            for SecurityAppliction in SecuritiesAppliction:
                if(SecurityAppliction.applicationId==applicationCategory2.id and SecurityAppliction.part == 1):
                    column['Traditional_summary_old']['Security'][str(SecurtyDict[SecurityAppliction.securityId])]=SecurtyRankDict[SecurityAppliction.securityRankId]
                if(SecurityAppliction.applicationId==applicationCategory2.id and SecurityAppliction.part == 2):
                    column['Traditional_summary_new']['Security'][str(SecurtyDict[SecurityAppliction.securityId])]=SecurtyRankDict[SecurityAppliction.securityRankId]
                    if(SecurityAppliction.securityRankIdFeature!=-1):
                        column['Contextual'][str(SecurtyDict[SecurityAppliction.securityId])]={}
                    for SecurityApplictionDescription in SecurityApplictionDescriptions:
                        if(SecurityApplictionDescription.securityApplictionId==SecurityAppliction.id):
                            column['Contextual'][str(SecurtyDict[SecurityAppliction.securityId])][privacyDict[SecurityApplictionDescription.privacyId]]=privacyRankDict[SecurityApplictionDescription.privacyRankId]
            table.append(column)


        for applicationCategory3 in applicationsCategory3:
            column={}
            column['id']=str(applicationCategory3.id)
            column['realName']=str(applicationCategory3.realName)
            column['falseName']=str(applicationCategory3.falseName)
            column['category']='high privacy and low security'
            column['Traditional_summary_old']={}
            column['Traditional_summary_new']={}
            column['Contextual']={}
            column['Traditional_summary_old']['Privacy']={}
            column['Traditional_summary_new']['Privacy']={}
            for PrivacyAppliction in PrivaciesAppliction:
                if(PrivacyAppliction.applicationId==applicationCategory3.id and PrivacyAppliction.part == 1):
                    column['Traditional_summary_old']['Privacy'][str(privacyDict[PrivacyAppliction.privacyId])]=privacyRankDict[PrivacyAppliction.privacyRankId]
                if(PrivacyAppliction.applicationId==applicationCategory3.id and PrivacyAppliction.part == 2):
                    column['Traditional_summary_new']['Privacy'][str(privacyDict[PrivacyAppliction.privacyId])]=privacyRankDict[PrivacyAppliction.privacyRankId]
            column['Traditional_summary_old']['Security']={}
            column['Traditional_summary_new']['Security']={}
            for SecurityAppliction in SecuritiesAppliction:
                if(SecurityAppliction.applicationId==applicationCategory3.id and SecurityAppliction.part == 1):
                    column['Traditional_summary_old']['Security'][str(SecurtyDict[SecurityAppliction.securityId])]=SecurtyRankDict[SecurityAppliction.securityRankId]
                if(SecurityAppliction.applicationId==applicationCategory3.id and SecurityAppliction.part == 2):
                    column['Traditional_summary_new']['Security'][str(SecurtyDict[SecurityAppliction.securityId])]=SecurtyRankDict[SecurityAppliction.securityRankId]
                    if(SecurityAppliction.securityRankIdFeature!=-1):
                        column['Contextual'][str(SecurtyDict[SecurityAppliction.securityId])]={}
                    for SecurityApplictionDescription in SecurityApplictionDescriptions:
                        if(SecurityApplictionDescription.securityApplictionId==SecurityAppliction.id):
                            column['Contextual'][str(SecurtyDict[SecurityAppliction.securityId])][privacyDict[SecurityApplictionDescription.privacyId]]=privacyRankDict[SecurityApplictionDescription.privacyRankId]
            table.append(column)


        for applicationCategory4 in applicationsCategory4:
            column={}
            column['id']=str(applicationCategory4.id)
            column['realName']=str(applicationCategory4.realName)
            column['falseName']=str(applicationCategory4.falseName)
            column['category']='low privacy and low security'
            column['Traditional_summary_old']={}
            column['Traditional_summary_new']={}
            column['Contextual']={}
            column['Traditional_summary_old']['Privacy']={}
            column['Traditional_summary_new']['Privacy']={}
            for PrivacyAppliction in PrivaciesAppliction:
                if(PrivacyAppliction.applicationId==applicationCategory4.id and PrivacyAppliction.part == 1):
                    column['Traditional_summary_old']['Privacy'][str(privacyDict[PrivacyAppliction.privacyId])]=privacyRankDict[PrivacyAppliction.privacyRankId]
                if(PrivacyAppliction.applicationId==applicationCategory4.id and PrivacyAppliction.part == 2):
                    column['Traditional_summary_new']['Privacy'][str(privacyDict[PrivacyAppliction.privacyId])]=privacyRankDict[PrivacyAppliction.privacyRankId]
            column['Traditional_summary_old']['Security']={}
            column['Traditional_summary_new']['Security']={}
            for SecurityAppliction in SecuritiesAppliction:
                if(SecurityAppliction.applicationId==applicationCategory4.id and SecurityAppliction.part == 1):
                    column['Traditional_summary_old']['Security'][str(SecurtyDict[SecurityAppliction.securityId])]=SecurtyRankDict[SecurityAppliction.securityRankId]
                if(SecurityAppliction.applicationId==applicationCategory4.id and SecurityAppliction.part == 2):
                    column['Traditional_summary_new']['Security'][str(SecurtyDict[SecurityAppliction.securityId])]=SecurtyRankDict[SecurityAppliction.securityRankId]
                    if(SecurityAppliction.securityRankIdFeature!=-1):
                        column['Contextual'][str(SecurtyDict[SecurityAppliction.securityId])]={}
                    for SecurityApplictionDescription in SecurityApplictionDescriptions:
                        if(SecurityApplictionDescription.securityApplictionId==SecurityAppliction.id):
                            column['Contextual'][str(SecurtyDict[SecurityAppliction.securityId])][privacyDict[SecurityApplictionDescription.privacyId]]=privacyRankDict[SecurityApplictionDescription.privacyRankId]
            table.append(column)

        return table


    @classmethod
    def getExperimentTable(self):
        Experiments=ExperimentModel.find_all_Experiment()
        ExperimentApps=ExperimentAppModel.find_all_ExperimentApp()
        Application=ApplicationModel.find_all()
        ExperimentDetailes=ExperimentDetaileModel.find_all_ExperimentDetailes()
        users=UserModel.find_all_user()
        table=[]
        dictApp=unionModel.getApplictionsDict(Application)
        dictUser=unionModel.getUsersDict(users)
        for Experiment in Experiments:
            column={}
            column['id']=str(Experiment.id)
            if(str(Experiment.type) == '1'):
                column['type']='Type 1 experiment'
            else:
                if(str(Experiment.type) == '2'):
                    column['type']='Type 2 experiment'
                else:
                    column['type']='Type 3 experiment'
            column['Number of participants']=str(Experiment.numberParti)
            if(Experiment.run==1):
                column['done']='no'
            else:
                column['done']='yes'
            column['app in experiment']=[]
            for ExperimentApp in ExperimentApps:
                if(ExperimentApp.ExperimentId==Experiment.id):
                    column['app in experiment'].append(dictApp[ExperimentApp.applicationId])
            column['ExperimentDetaile']={}
            for ExperimentDetaile in ExperimentDetailes:
                if ExperimentDetaile.ExperimentId==Experiment.id:
                    column['ExperimentDetaile'][ExperimentDetaile.groupExp]={}
                    column['ExperimentDetaile'][ExperimentDetaile.groupExp]['user']='-'
                    column['ExperimentDetaile'][ExperimentDetaile.groupExp]['order']=[]
            for ExperimentDetaile in ExperimentDetailes:
                if ExperimentDetaile.ExperimentId==Experiment.id:
                    if ExperimentDetaile.userID != 0:
                        column['ExperimentDetaile'][ExperimentDetaile.groupExp]['user']=dictUser[ExperimentDetaile.userID]
                    if ExperimentDetaile.questionDisplay==1:
                        column['ExperimentDetaile'][ExperimentDetaile.groupExp]['questionDisplay']='new traditional summary => Security features'
                    else:
                        if ExperimentDetaile.questionDisplay==2:
                            column['ExperimentDetaile'][ExperimentDetaile.groupExp]['questionDisplay']='Security features => new traditional summary'
                        else:
                            if ExperimentDetaile.questionDisplay==3:
                                column['ExperimentDetaile'][ExperimentDetaile.groupExp]['questionDisplay']='Security features'
                            else:
                                if ExperimentDetaile.questionDisplay==4:
                                    column['ExperimentDetaile'][ExperimentDetaile.groupExp]['questionDisplay']='old traditional summary'
                                else:
                                    column['ExperimentDetaile'][ExperimentDetaile.groupExp]['questionDisplay']='new traditional summary'
                    column['ExperimentDetaile'][ExperimentDetaile.groupExp]['order'].append(dictApp[ExperimentDetaile.applicationId])
            table.append(column)
        return table


    @classmethod
    def getAnswerTable(self,experimentId):
        Experiment=ExperimentModel.find_by_id(experimentId)
        ExperimentDetailes=ExperimentDetaileModel.find_all_ExperimentDetailes_by_ExperimentID(experimentId)
        users=UserModel.find_all_user()
        table=[]
        Application=ApplicationModel.find_all()
        Questions=QuestionModel.find_all_Question()

        dictApp=unionModel.getApplictionsDict(Application)
        dictUser=unionModel.getUsersDict(users)
        dictQustion=unionModel.getQustionDict(Questions)


        Securties=SecurtyModel.find_all_SecurtyFeature()
        SecurtyDict=unionModel.getSecurtyDict(Securties)

        generalReports=generalReportModel.find_by_experimentId(experimentId)
        column={}
        column['user']='-'
        column['Traditional_summary_old']='-'
        column['Traditional_summary_new']='-'


        for Securty in Securties:
            column[SecurtyDict[Securty.id]]='-'
        # run on all grop exp
        j=0
        for i in range(0,Experiment.numberParti):
            groupExpDict={}
            for ExperimentDetaile in ExperimentDetailes:
                if ExperimentDetaile.groupExp!=i:
                    continue;
                j+=1
                dictExp={}
                strType=""
                if ExperimentDetaile.questionDisplay==1:
                    strType='new traditional summary => Security features'
                else:
                    if ExperimentDetaile.questionDisplay==2:
                        strType='Security features => new traditional summary'
                    else:
                        if ExperimentDetaile.questionDisplay==3:
                            strType='Security features'
                        else:
                            if ExperimentDetaile.questionDisplay==4:
                                strType='old traditional summary'
                            else:
                                strType='new traditional summary'
                key=dictApp[ExperimentDetaile.applicationId ]+': '+strType
                dictExp[key]={}
                Reports=ReportModel.find_all_report_by_experimentDetailes(ExperimentDetaile.id)
                for Question in Questions:
                    if(Question.section==1):
                        columnCopy=column.copy()
                        if(ExperimentDetaile.userID != 0):
                            columnCopy['user']=dictUser[ExperimentDetaile.userID]
                        for Report in Reports:
                            if (Report.questionID==Question.id):
                                if Report.part==1 :
                                    columnCopy['Traditional_summary_old']=Report.answer
                                else:
                                    if Report.part==2 and int(Report.securityId)==0 :
                                        columnCopy['Traditional_summary_new']=Report.answer
                                    else:
                                        columnCopy[SecurtyDict[int(Report.securityId)]]=Report.answer
                        dictExp[key][dictQustion[Question.id]]=columnCopy
                groupExpDict[j]=dictExp
            table.append(groupExpDict)


        # generalReport
        columnGeneral={}
        for Question in Questions:
            if(Question.section==2):
                columnGeneral[dictQustion[Question.id]]='-'

        generalDict={}
        generalDict['general report']={}
        lastUser=-1
        for generalReport in generalReports:
            if( lastUser == -1 or (lastUser != -1 and lastUser != generalReport.userID)):
                generalDict['general report'][dictUser[generalReport.userID]]=copy.deepcopy(columnGeneral)
            lastUser=generalReport.userID
            generalDict['general report'][dictUser[generalReport.userID]][dictQustion[generalReport.questionID]]=generalReport.answer
        table.append(generalDict)

        return table
