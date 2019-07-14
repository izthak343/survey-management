from models.user import UserModel
from models.experiment import ExperimentModel
from models.experimentDetaile import ExperimentDetaileModel


class saverModel():
    userDict={}
    @classmethod
    def getExperimentDetaile(self,userID,expID):
        if (userID,expID) in self.userDict.keys():
            experimentDetaile = self.userDict[(userID,expID)][0]
            return experimentDetaile
        else:
            ExperimentDetailes=ExperimentDetaileModel.find_all_ExperimentDetailes_by_userID(userID,expID);
            # case of no Experiment to to the user
            if len(ExperimentDetailes)==0:
                return False
            self.userDict[(userID,expID)]=ExperimentDetailes
            return saverModel.getExperimentDetaile(userID,expID)

    @classmethod
    def removeExperimentDetaile(self,userID,expID):
        if (userID,expID) in self.userDict.keys():
            if (userID,expID) in self.userDict.keys():
                ExperimentDetaile=self.userDict[(userID,expID)].pop(0);
                ExperimentDetaile.done=1
                ExperimentDetaile.update_db()
                if len(self.userDict[(userID,expID)])==0:
                    del self.userDict[(userID,expID)]
                    return True
                return False
        return False
