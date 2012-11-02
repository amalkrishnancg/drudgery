import string
import sys
import profile

from testcaseexecutor import TestCaseExecutor
from drudgelife import Drudge
from profile import Profile 

class Menu:

    #Load Profiles
    def __init__(self):
        Menu.profileInstance = Profile()
        
    def showRootMenu(self):
        print "Choose your option"
        print "[s] Show existing profiles"
        print "[c] Create profile"
        print "[l <name>] Load application profile <name>"
        print "[q] Quit"
        while(True):
            self.choice = raw_input("\ndrudge>")
            self.processRootMenuInput(self.choice.strip())
            
    def showProfileMenu(self):
        print "Choose your option"
        print "[v] View profile details"
        print "[e] Edit profile details"
        print "[r] Execute"
        print "[s] Step Execute"
        print "[q] Return to main menu"
        while(True):
            self.choice = raw_input("\ndrudge|"+Drudge.profileName+"|>")
            if (self.processProfileMenuInput(self.choice.strip())==0):
                return
            
    def processRootMenuInput(self,choice):
        self.choice = choice.lower()
        if(self.choice == 's'):
            profiles = Menu.profileInstance.showProfiles()
            if profiles.count == 0:
                print "\nNo profiles present"
                return
            else:
                print "\nProfiles available are :"
                for profile in profiles:
                    print profile[:-9]
        elif (self.choice == 'c'):
           Menu.profileInstance.createProfile()   
        elif (self.choice[:1] == 'l'):
            if(self.choice[1:2]== ' ' and self.choice[3:].strip()!=''):
                print
                success = Menu.profileInstance.loadProfile(self.choice[1:].strip())
                if (success):
                    Menu.testcaseExecutorInstance = TestCaseExecutor() 
                    print
                    self.showProfileMenu()
            else:
                print "\nError: Profile name to be loaded was not specified"
        elif (self.choice == 'q'):
            sys.exit(0)
        elif (self.choice == 'h'):
            print 
            print "[s] Show existing profiles"
            print "[c] Create profile"
            print "[l <name>] Load application profile <name>"
            print "[q] Quit"
        else:
            print "Incorrect choice. Enter 'h' for help"
          
    def processProfileMenuInput(self,choice):
        self.choice = choice.lower()
        print 
        if(self.choice == 'v'):
            print "Profile Name : ",Drudge.profileName
            print "Application Name : ",Drudge.applicationName
            print "Application Path : ",Drudge.applicationPath
            print "Application Execution Path : ",Drudge.applicationExecutionPath
            print "Input Vectors :"
            for vector in Drudge.inputVectorList:
                print " -"+vector
            print "Output Vectors :"
            for vector in Drudge.outputVectorList:
                print " -"+vector
        elif(self.choice == 'e'):
            if(Menu.profileInstance.editProfile()!=0):
                Menu.profileInstance.loadProfile(Drudge.profileName)
        elif(self.choice == 'r'):
            Menu.testcaseExecutorInstance.executeTestCases("R")
        elif(self.choice == 's'):
            Menu.testcaseExecutorInstance.executeTestCases("S")
        elif(self.choice == 'q'):
            return 0
        elif(self.choice == 'h'):
            print "[v] View profile details"
            print "[e] Edit profile details"
            print "[r] Execute"
            print "[s] Step Execute"
            print "[q] Return to main menu"
        else:
            print "Incorrect choice. Enter 'h' for help"
