import json
from models.user import UserModel
from models.experiment import ExperimentModel
from models.experimentDetaile import ExperimentDetaileModel
from models.application import ApplicationModel
from models.securityAppliction import SecurityApplictionModel
from models.question import QuestionModel
from models.report import ReportModel
from models.saver import saverModel
from models.generalReport import generalReportModel

class helper():
    appDict={}
    appSecurtyDict={}


    @classmethod
    def getAppImage(self,appId):
        if appId in self.appDict.keys():
            return self.appDict[appId]
        root='/pictures/'
        imageDict={}
        imageArray=[]
        Application=ApplicationModel.find_by_id(appId)
        if(Application!=False):
            imageDict['picture1']=root+Application.picture1
            imageDict['picture2']=root+Application.picture2
            imageArray.append(Application.picture1)
            imageArray.append(Application.picture2)
        SecurityApplictions=SecurityApplictionModel.find_by_applicationID(appId)
        imageDict['securtyImges']=[]
        for SecurityAppliction in SecurityApplictions:
            # check if to this security have image
            if SecurityAppliction.securityRankIdFeature!=-1:
                imageDict['securtyImges'].append(root+SecurityAppliction.image)
                imageArray.append(SecurityAppliction.image)
        self.appDict[appId]=imageDict
        return imageDict



    @classmethod
    def getSecurtyIds(self,appId):
        if appId in self.appSecurtyDict.keys():
            return self.appSecurtyDict[appId]
        SecurtyIdArray=[]
        Application=ApplicationModel.find_by_id(appId)
        SecurityApplictions=SecurityApplictionModel.find_by_applicationID(appId)
        for SecurityAppliction in SecurityApplictions:
            # check if to this security have image
            if SecurityAppliction.securityRankIdFeature!=-1:
                SecurtyIdArray.append(SecurityAppliction.securityId)
        self.appSecurtyDict[appId]=SecurtyIdArray
        return self.appSecurtyDict[appId]


    @classmethod
    def getData(self,userID,expId):
        ExperimentDetaile=saverModel.getExperimentDetaile(userID,expId)
        if ExperimentDetaile==False:
            return False
        images=helper.getAppImage(ExperimentDetaile.applicationId)
        if len(images)==0:
            return False
        data={}
        data['questionDisplay']=ExperimentDetaile.questionDisplay
        data['images']=images
        return data



    @classmethod
    def setReport(self,userID,expId,request):
        ExperimentDetaile=saverModel.getExperimentDetaile(userID,expId)
        allQuestions=QuestionModel.find_all_Question()
        questions=[]
        for question in allQuestions:
            if question.section==1:
                questions.append(question)
        type1Ids=[]
        type2Ids=[]
        type3Ids=[]
        for question in questions:
            if(question.type==1):
                type1Ids.append(question.id)
            else:
                if(question.type==2):
                    type2Ids.append(question.id)
                else:
                    type3Ids.append(question.id)
        if(ExperimentDetaile.questionDisplay==1):
            # first part => Traditional approach
            tempStr='$answer[0][]'
            answers=request.form.getlist(tempStr)
            indexAnswer=0
            ExperimentDetaileID=ExperimentDetaile.id
            for j in range(0,len(type1Ids)):
                questionId=type1Ids[j]
                answer=answers[indexAnswer]
                part=2
                securtyID=0
                indexAnswer+=1
                report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                report.save_to_db()
            for j in range(0,len(type2Ids)):
                questionId=type2Ids[j]
                answer=answers[indexAnswer]
                part=2
                securtyID=0
                indexAnswer+=1
                report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                report.save_to_db()
            for j in range(0,len(type3Ids)):
                questionId=type3Ids[j]
                answer=answers[indexAnswer]
                part=2
                securtyID=0
                indexAnswer+=1
                report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                report.save_to_db()
            # secind part => Contextual approach - fitzer image
            rowsNum=len(helper.getAppImage(ExperimentDetaile.applicationId))-2
            SecurtyIds=helper.getSecurtyIds(ExperimentDetaile.applicationId)
            i=1
            for SecurtyId in SecurtyIds:
                tempStr='$answer['+str(i)+'][]'
                answers=request.form.getlist(tempStr)
                indexAnswer=0
                ExperimentDetaileID=ExperimentDetaile.id
                for j in range(0,len(type1Ids)):
                    questionId=type1Ids[j]
                    answer=answers[indexAnswer]
                    part=2
                    securtyID=SecurtyId
                    indexAnswer+=1
                    report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                    report.save_to_db()
                for j in range(0,len(type2Ids)):
                    questionId=type2Ids[j]
                    answer=answers[indexAnswer]
                    part=2
                    securtyID=SecurtyId
                    indexAnswer+=1
                    report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                    report.save_to_db()
                for j in range(0,len(type3Ids)):
                    questionId=type3Ids[j]
                    answer=answers[indexAnswer]
                    part=2
                    securtyID=SecurtyId
                    indexAnswer+=1
                    report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                    report.save_to_db()
                i+=1
        else:
            if(ExperimentDetaile.questionDisplay==2):
                # first part => Contextual approach
                SecurtyIds=helper.getSecurtyIds(ExperimentDetaile.applicationId)
                i=0
                for SecurtyId in SecurtyIds:
                    tempStr='$answer['+str(i)+'][]'
                    answers=request.form.getlist(tempStr)
                    indexAnswer=0
                    ExperimentDetaileID=ExperimentDetaile.id
                    for j in range(0,len(type1Ids)):
                        questionId=type1Ids[j]
                        answer=answers[indexAnswer]
                        part=2
                        securtyID=SecurtyId
                        indexAnswer+=1
                        report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                        report.save_to_db()
                    for j in range(0,len(type2Ids)):
                        questionId=type2Ids[j]
                        answer=answers[indexAnswer]
                        part=2
                        securtyID=SecurtyId
                        indexAnswer+=1
                        report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                        report.save_to_db()
                    for j in range(0,len(type3Ids)):
                        questionId=type3Ids[j]
                        answer=answers[indexAnswer]
                        part=2
                        securtyID=SecurtyId
                        indexAnswer+=1
                        report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                        report.save_to_db()
                    i+=1
                # secind part => Traditional approach
                tempStr='$answer['+str(i)+'][]'
                answers=request.form.getlist(tempStr)
                indexAnswer=0
                ExperimentDetaileID=ExperimentDetaile.id
                for j in range(0,len(type1Ids)):
                    questionId=type1Ids[j]
                    answer=answers[indexAnswer]
                    part=2
                    securtyID=0
                    indexAnswer+=1
                    report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                    report.save_to_db()
                for j in range(0,len(type2Ids)):
                    questionId=type2Ids[j]
                    answer=answers[indexAnswer]
                    part=2
                    securtyID=0
                    indexAnswer+=1
                    report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                    report.save_to_db()
                for j in range(0,len(type3Ids)):
                    questionId=type3Ids[j]
                    answer=answers[indexAnswer]
                    part=2
                    securtyID=0
                    indexAnswer+=1
                    report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                    report.save_to_db()
            else:
                if(ExperimentDetaile.questionDisplay==3):
                    # first part => Contextual approach
                    SecurtyIds=helper.getSecurtyIds(ExperimentDetaile.applicationId)
                    i=0
                    for SecurtyId in SecurtyIds:
                        tempStr='$answer['+str(i)+'][]'
                        answers=request.form.getlist(tempStr)
                        indexAnswer=0
                        ExperimentDetaileID=ExperimentDetaile.id
                        for j in range(0,len(type1Ids)):
                            questionId=type1Ids[j]
                            answer=answers[indexAnswer]
                            part=2
                            securtyID=SecurtyId
                            indexAnswer+=1
                            report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                            report.save_to_db()
                        for j in range(0,len(type2Ids)):
                            questionId=type2Ids[j]
                            answer=answers[indexAnswer]
                            part=2
                            securtyID=SecurtyId
                            indexAnswer+=1
                            report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                            report.save_to_db()
                        for j in range(0,len(type3Ids)):
                            questionId=type3Ids[j]
                            answer=answers[indexAnswer]
                            part=2
                            securtyID=SecurtyId
                            indexAnswer+=1
                            report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                            report.save_to_db()
                        i+=1





                else:
                    if(ExperimentDetaile.questionDisplay==4):
                            # first part => Traditional approach
                            tempStr='$answer[0][]'
                            answers=request.form.getlist(tempStr)
                            indexAnswer=0
                            ExperimentDetaileID=ExperimentDetaile.id
                            for j in range(0,len(type1Ids)):
                                questionId=type1Ids[j]
                                answer=answers[indexAnswer]
                                part=1
                                securtyID=0
                                indexAnswer+=1
                                report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                                report.save_to_db()
                            for j in range(0,len(type2Ids)):
                                questionId=type2Ids[j]
                                answer=answers[indexAnswer]
                                part=i
                                securtyID=0
                                indexAnswer+=1
                                report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                                report.save_to_db()
                            for j in range(0,len(type3Ids)):
                                questionId=type3Ids[j]
                                answer=answers[indexAnswer]
                                part=i
                                securtyID=0
                                indexAnswer+=1
                                report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                                report.save_to_db()
                    else:
                            # first part => Traditional approach
                            tempStr='$answer[0][]'
                            answers=request.form.getlist(tempStr)
                            indexAnswer=0
                            ExperimentDetaileID=ExperimentDetaile.id
                            part=2
                            for j in range(0,len(type1Ids)):
                                questionId=type1Ids[j]
                                answer=answers[indexAnswer]
                                securtyID=0
                                indexAnswer+=1
                                report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                                report.save_to_db()
                            for j in range(0,len(type2Ids)):
                                questionId=type2Ids[j]
                                answer=answers[indexAnswer]
                                securtyID=0
                                indexAnswer+=1
                                report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                                report.save_to_db()
                            for j in range(0,len(type3Ids)):
                                questionId=type3Ids[j]
                                answer=answers[indexAnswer]
                                securtyID=0
                                indexAnswer+=1
                                report=ReportModel(ExperimentDetaileID,questionId,answer,part,securtyID)
                                report.save_to_db()
        return saverModel.removeExperimentDetaile(userID,expId)



    @classmethod
    def setReportPart2(self,userID,request):
        # one part => Traditional  approach - total image questionID,answer,experimentId
        allQuestions=QuestionModel.find_all_Question()
        questions=[]
        for question in allQuestions:
            if question.section==2:
                questions.append(question)
        type1Ids=[]
        type2Ids=[]
        type3Ids=[]
        for question in questions:
            if(question.type==1):
                type1Ids.append(question.id)
            else:
                if(question.type==2):
                    type2Ids.append(question.id)
                else:
                    type3Ids.append(question.id)
        tempStr='$answer[0][]'
        answers=request.form.getlist(tempStr)
        if(len(answers)==0):
            return;
        indexAnswer=0
        ExperimentId=UserModel.find_by_id(userID).ExperimentId
        for j in range(0,len(type1Ids)):
            questionId=type1Ids[j]
            answer=answers[indexAnswer]
            indexAnswer+=1
            generalReport=generalReportModel(questionId,answer,ExperimentId,userID)
            generalReport.save_to_db()
        for j in range(0,len(type2Ids)):
            questionId=type2Ids[j]
            answer=answers[indexAnswer]
            indexAnswer+=1
            generalReport=generalReportModel(questionId,answer,ExperimentId,userID)
            generalReport.save_to_db()
        for j in range(0,len(type3Ids)):
            questionId=type3Ids[j]
            answer=answers[indexAnswer]
            indexAnswer+=1
            generalReport=generalReportModel(questionId,answer,ExperimentId,userID)
            generalReport.save_to_db()
