#
#
#       
#       Drudgery : An Application Testing Framework
#
#       version: 0.1
#       author : Amal Krishnan | amalkrishnancg@gmail.com
#       date   : 11/2009
#
#

import menu

program_information = ["Drudgery",0.1]

print """
                    
                         
                                        (__)           
                                        (oo)      
                               /---------\/    
                              / |       ||       
                             *  ||------||
                      
                                 Drudgery
                                Version %2.1f

"""%program_information[1]

menu.Menu().showRootMenu()
