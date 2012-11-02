import os
import re
import properties
import shutil
import stat
import subprocess
import filecmp

from drudgelife import Drudge
from profile import Profile 



#use for testing purposes only
#class Profile:
#    path = os.getcwd()
#class Drudge:
#    profileName = "wikiking"
#    applicationName = "wikiking"
#    applicationPath = "D:\\IMS_WIN"
#    applicationExecutionPath = "D:\\IMS_WIN\\bin\\imsencrypt.cmd"
#    inputVectorList = ["D:\\IMS_WIN\\input\\ctsinput.txt","D:\\IMS_WIN\\config\\MDLConfig.properties"]
#    outputVectorList = ["D:\\IMS_WIN\\bin\\error.log","D:\\IMS_WIN\\output\\ctsoutput.txt"]



class TestCaseExecutor:
    
    testCases=[]
    
    def __init__(self):
        TestCaseExecutor.testCasePath = os.path.join(os.path.join(Profile.path,Drudge.profileName+".dprofile"),"testcases")
        TestCaseExecutor.testCases = os.listdir(TestCaseExecutor.testCasePath)
        TestCaseExecutor.foldersadded =[]
        TestCaseExecutor.filesadded =[]
        TestCaseExecutor.testcaseStatus = {}
        
    def executeTestCases(self,mode):
      try:
            print "\nBeginnning test case execution on",Drudge.applicationName
            print "\nNumber of test cases is",len(TestCaseExecutor.testCases)
            for testCaseName in TestCaseExecutor.testCases:
                print "\n---Executing",testCaseName+"---"
                TestCaseExecutor.currentTestCase = os.path.join(TestCaseExecutor.testCasePath,testCaseName)
                
                self.loadFiles(TestCaseExecutor.currentTestCase+os.sep+"input",Drudge.applicationPath)        
                if(mode == "S"):
                    raw_input("[Loaded] Press Enter key to continue...")
                self.executeProgram()
                if(mode == "S"):
                    raw_input("[Executed] Press Enter key to continue...")
                testcasePassed = self.compareOutput(TestCaseExecutor.currentTestCase+os.sep+"output",Drudge.applicationPath)
                
                if(testcasePassed):
                    TestCaseExecutor.testcaseStatus[testCaseName]="Passed"
                else:
                    TestCaseExecutor.testcaseStatus[testCaseName]="Failed"
                if(mode == "S"): 
                 if(testcasePassed):
                     print "Test Case passed"
                 else:
                     print "Test Case failed"
                 raw_input("[Compared] Press Enter key to continue...")
                #print "unloading files"
                self.unloadFiles()
            print "\n---Result---\n",
            keyList = TestCaseExecutor.testcaseStatus.keys()
            keyList.sort()
            for key in keyList:
                print key,":",TestCaseExecutor.testcaseStatus[key]
      except Exception,err:
            print "There were errors during the test case execution"
            print err

    def loadFiles(self,inputPath,applicationPath,level=-1):
        #print "Input path",inputPath
        # Go through input folder
        testCaseDirectories = os.listdir(inputPath)
        #print testCaseDirectories
        for element in testCaseDirectories:
            if os.path.isdir(inputPath+os.sep+element):
                #print "applicationPath is ",applicationPath,os.sep,element,"and input path is",inputPath+os.sep+element
                appDirPath = applicationPath+os.sep+element
                #check if directory exist in the application directory
                if not (os.path.isdir(appDirPath)):
                    #print "creating "+appDirPath+" directory in application"
                    os.makedirs(appDirPath)
                    TestCaseExecutor.foldersadded.append(appDirPath)
                    #print "lame add",TestCaseExecutor.foldersadded
                #print "appDirPath is",appDirPath
                #print "calling loadfiles with",inputPath+os.sep+element,appDirPath+os.sep+element
                self.loadFiles(inputPath+os.sep+element,appDirPath)
            else:
                #print "source",inputPath+os.sep+element,"dest",applicationPath+os.sep+element
                shutil.copyfile(inputPath+os.sep+element,applicationPath+os.sep+element)
                TestCaseExecutor.filesadded.append(applicationPath+os.sep+element)
                pass
            
    def executeProgram(self):
        #print Drudge.applicationExecutionPath

        # Change the current working directory to the application directory
        currWorkDir = os.getcwd()
        os.chdir(Drudge.applicationPath)
        print "\n","."*25,Drudge.applicationName,"."*25,"\n"
        subprocess.call(Drudge.applicationExecutionPath)
        print "."*(52+len(Drudge.applicationName)),"\n"
        os.chdir(currWorkDir)

    def compareOutput(self,outputPath,applicationPath):
        try:
            testcaseSuccess = True
            #print "calling compareOutput with",outputPath,"\n ++",applicationPath
            outputDirectories = os.listdir(outputPath)
            for element in outputDirectories:
                appDirPath = applicationPath+os.sep+element
                if os.path.isdir(outputPath+os.sep+element): #is a directory
                    # Check if the directory exits. If not, the test has failed
                    if(not os.path.exists(appDirPath)):
                        print "Directory does not exist ... failing"
                        return False
                    returnedTrue = self.compareOutput(outputPath+os.sep+element,appDirPath)
                    if(not returnedTrue):
                        return False
                else: #is a file
                    #print "source",outputPath+os.sep+element,"\n++dest",applicationPath+os.sep+element
                    if(not os.path.exists(appDirPath)):
                        #print appDirPath,"does not exist ... returning false"
                        return False
                    if not filecmp.cmp(outputPath+os.sep+element,applicationPath+os.sep+element,False):
                        #print "returning False"
                        testcaseSuccess = False
                        break
           
            #print "The value of testcaseSuccess",testcaseSuccess
            return testcaseSuccess
        except Exception:
            print "There were errors during the testcase execution\n",Exception.message
            return False

    def unloadFiles(self):
        #print "TestCaseExecutor.foldersadded is",TestCaseExecutor.foldersadded,"and files added are",TestCaseExecutor.filesadded
        for fileToRemove in TestCaseExecutor.filesadded:
            os.remove(fileToRemove)
            #print "*",fileToRemove, "was deleted"
        TestCaseExecutor.filesadded=[]

        #Reverse the order of folders added 
        TestCaseExecutor.foldersadded.reverse()
        for dirToRemove in TestCaseExecutor.foldersadded:
            os.rmdir(dirToRemove)
            #print  "*",dirToRemove, "was deleted"
        TestCaseExecutor.foldersadded=[]

        #Clear Input and Output Vectors
        for inputVector in Drudge.inputVectorList:
            try:
                os.remove(inputVector)
            except Exception:
                pass
        for outputVector in Drudge.outputVectorList:
            try:
                os.remove(outputVector)
            except Exception:
                pass                                    

#  * Remove this section after testing 
#  *************************************

#test = TestCaseExecutor()
#test.executeTestCases("mode")

#  *************************************
#
