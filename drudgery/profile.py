import os
import re
import properties
from drudgelife import Drudge 

class Profile:
    def __init__(self):
        self.loadProfileList()

    def loadProfileList(self):
        Profile.listOfProfiles = []
        Profile.path = os.getcwd()
        listOfDirectories = os.listdir(Profile.path)
        for directory in listOfDirectories:
            if re.search(".dprofile",directory):
                 Profile.listOfProfiles.append(directory)
                 
    def showProfiles(self):
        self.loadProfileList()
        return Profile.listOfProfiles

    def createProfile(self):
       try:
        while(True):
            profileName = raw_input("Enter profile name : ")
            profileName = profileName.lower()
            if(str(profileName+'.dprofile') in Profile.listOfProfiles):
                print "A profile with the same name already exists"
                continue
            else:
                print 'Creating ',str(profileName+'.dprofile')
                os.makedirs(profileName+'.dprofile')
                os.makedirs(Profile.path+os.sep+profileName+'.dprofile'+os.sep+"testcases")
                profileFile = open(Profile.path+os.sep+profileName+".dprofile"+os.sep+"application.properties","w")
                print '----------',profileName,'----------'
                profileFile.write("APP_NAME = "+profileName+"\n")
                application_path = raw_input("Enter the application path : ")
                profileFile.write("APP_PATH = "+application_path+"\n")
                program = raw_input("Enter the application executable path (Include full path) : ")
                profileFile.write("APP_EXEC_PATH = "+application_path+"\n")
                numberOfInputVectors = int(raw_input("Enter the number of input vectors : "))
                count = 0
                while(numberOfInputVectors != 0 ):
                    numberOfInputVectors-=1
                    count+=1
                    profileFile.write("INPUT_VECTOR_"+str(count)+" = "+raw_input(str('Enter the path of input vector '+str(count)+' : '))+"\n")
                numberOfOutputVectors = int(raw_input("Enter the number of output vectors : "))
                count = 0
                while(numberOfOutputVectors != 0 ):
                    numberOfOutputVectors-=1
                    count+=1
                    profileFile.write("OUTPUT_VECTOR_"+str(count)+" = "+raw_input(str('Enter the path of output vector '+str(count)+' : '))+"\n")
                profileFile.close()
                choice = (raw_input("Do you wish to create test case skeleton? (y/n)")).lower()
                if(choice=='y'):
                    folderformat = raw_input("Enter the test case prefix : ")
                    number_of_testcases = int(raw_input("Enter the number of test cases : "))
                    print "Creating test case skeleton..."
                    digitLenTestCases = len(str(number_of_testcases))
                    count = 0
                    while(count < number_of_testcases):
                        count+=1
                        diff = digitLenTestCases - len(str(count))
                        strcount=""
                        while(diff != 0):
                            strcount+="0"
                            diff-=1
                        strcount+=str(count)
                        os.makedirs(Profile.path+os.sep+profileName+'.dprofile'+os.sep+"testcases"+os.sep+"testcase"+strcount)
                        os.makedirs(Profile.path+os.sep+profileName+'.dprofile'+os.sep+"testcases"+os.sep+"testcase"+strcount+os.sep+"input")
                        os.makedirs(Profile.path+os.sep+profileName+'.dprofile'+os.sep+"testcases"+os.sep+"testcase"+strcount+os.sep+"output")
                print "Profile successfully created"
                self.loadProfileList()
                break
       except Exception,err:
            print "Profile creation encountered errors"
            profileFile.close()
            os.remove(Profile.path+os.sep+profileName+".dprofile"+os.sep+"application.properties")
            os.rmdir(Profile.path+os.sep+profileName+'.dprofile'+os.sep+"testcases") 
            os.rmdir(profileName+".dprofile")
            print "Error : ",err

    def loadProfile(self,profileName):
        #Unload existing vectors
        Drudge.inputVectorList = []
        Drudge.outputVectorList = [] 
        if (profileName+".dprofile")not in Profile.listOfProfiles:
            print profileName,"does not exist"
            return 0
        else:
            try:
                file = open(Profile.path+os.sep+profileName+".dprofile"+os.sep+"application.properties")
                propertyFile = properties.Properties()
                propertyFile.load(file)
                Drudge.profileName = profileName
                Drudge.applicationName = propertyFile.get("APP_NAME")
                Drudge.applicationPath = propertyFile.get("APP_PATH")
                Drudge.applicationExecutionPath = propertyFile.get("APP_EXEC_PATH")
                count = 1
                while(propertyFile.get("INPUT_VECTOR_"+str(count))!= None):
                      Drudge.inputVectorList.append(propertyFile.get("INPUT_VECTOR_"+str(count)))
                      count+=1
                count = 1
                while(propertyFile.get("OUTPUT_VECTOR_"+str(count))!= None):
                      Drudge.outputVectorList.append(propertyFile.get("OUTPUT_VECTOR_"+str(count)))
                      count+=1
                print "Successfully loaded profile:",profileName
                file.close()
                return 1
            except Exception,err:
                print "Profile could not be loaded"
                print "Error : ",err
                file.close()
                return 0
            
    def editProfile(self):
          try:
                file = open(Profile.path+os.sep+Drudge.profileName+".dprofile"+os.sep+"application.properties","w")
                propertyFile = properties.Properties()
                print "Application Name : ",Drudge.applicationName
                choice = raw_input("Edit Application Name (y)? : ").lower()
                if(choice == 'y'):
                    propertyFile["APP_NAME"] = raw_input("Enter New Application Name : ")
                else:
                    if(Drudge.applicationName!=None):
                        propertyFile["APP_NAME"]=Drudge.applicationName
                    else:
                        propertyFile["APP_NAME"]=""
                print "Application Path : ",Drudge.applicationPath
                choice = raw_input("Edit Application Path (y)? : ").lower()
                if(choice == 'y'):
                    propertyFile["APP_PATH"]= raw_input("Enter New Application Path : ")
                else:
                    if( Drudge.applicationPath!=None):
                        propertyFile["APP_PATH"]=Drudge.applicationPath
                    else:
                        propertyFile["APP_PATH"]=""
                print "Application Executable Path : ",Drudge.applicationExecutionPath
                choice = raw_input("Edit Application Executable Path (y)?").lower()
                if(choice == 'y'):
                    propertyFile["APP_EXEC_PATH"]=raw_input("Enter New Application Executable Path : ")
                else:
                    if(Drudge.applicationExecutionPath!=None):
                        propertyFile["APP_EXEC_PATH"]=Drudge.applicationExecutionPath
                    else:
                        propertyFile["APP_EXEC_PATH"]=""
                editInputVectors = raw_input("Do you want to edit the input vectors (y)? : ").lower()
                if(editInputVectors == 'y'):
                    count = 1
                    for inputVector in Drudge.inputVectorList:
                      print "INPUT_VECTOR_",str(count)," = ",inputVector
                      propertyFile["INPUT_VECTOR_"+str(count)]=raw_input("Enter the new input vector "+str(count)+" path : ")
                      count+=1
                else:
                    count = 1
                    for inputVector in Drudge.inputVectorList:
                        propertyFile["INPUT_VECTOR_"+str(count)]=inputVector
                        count += 1
                editOutputVectors = raw_input("Do you want to edit the output vectors (y)? : ").lower()
                if(editOutputVectors == 'y'):
                    count = 1
                    for outputVector in Drudge.inputVectorList:
                      print "OUTPUT_VECTOR_",str(count)," = ",outputVector
                      propertyFile["OUTPUT_VECTOR_"+str(count)] = raw_input("Enter the new output vector "+str(count)+" path : ")
                      count+=1
                else:
                    count = 1
                    for outputVector in Drudge.outputVectorList:
                        propertyFile["OUTPUT_VECTOR_"+str(count)]=outputVector
                        count += 1
                propertyFile.store(file)
                file.close()
                print "Successfully edited profile:",Drudge.profileName
                return 1
          except Exception,err:
               print "Profile could not be edited"
               print "Error : ",err
               file.close()
               return 0     
