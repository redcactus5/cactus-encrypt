#cactus encrypt is a simple cli text encryption program written in python that implements the cactus cipher algorithm
#Copyright 2023,2024 Redcactus5
'''
This file is part of Cactus Encrypt.

Cactus Encrypt is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Cactus Encrypt is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Cactus Encrypt. If not, see <https://www.gnu.org/licenses/>. 
'''
#this program is free, open source software released under the GNU General Public License version 3.0 or later version (GPL-3.0-or-later)



#this file is basically just a launcher for the main program



print("starting up...")

#import needed files
import command_line_interface
#this file determines what type of build this is and what mode to run in as a result
import build_mode

#attempt get the build mode from the file
mode=None
ableToStart=True
try:
    mode=build_mode.getBuildMode()
except:
    ableToStart=False
    print("\n"*50)
    print("a fatal error occurred. the program has aborted the start operation for safety.")
    print("detected error: (error 1) start configuration file could either not be read or not be found.")
    input("press enter to finish")



#determine if this is a release build
if(mode[0]=="RELEASE" and ableToStart):
    if(command_line_interface.backend.bmkv(True,mode[1])):
        try:#if so start in release mode
            
            command_line_interface.start(False)
        except Exception as e:
            print("\n"*50)
            print("a fatal error occurred. error(2). the program has quit for safety.")
            print("detected error: "+str(e))
            input("press enter to finish")
    else:
        print("\n"*50)
        print("a fatal error occurred. the program has aborted the start operation to prevent damage to your system.")
        print("detected error: (error 3) could not start due to invalid start configuration constant part 2.")
        input("press enter to finish")
#determine if this is a debug build
elif(mode[0]=="TESTING BUILD" and ableToStart):
    if(command_line_interface.backend.bmkv(False,mode[1])):
        #if so start in debug mode
        
        command_line_interface.start(True)
    else:
        print("\n"*50)
        print("a fatal error occurred. the program has aborted the start operation to prevent damage to your system.")
        print("detected error: (error 3) could not start due to invalid start configuration constant part 2.")
        input("press enter to finish")
elif(ableToStart):#error out if no valid build type tag
    print("\n"*50)
    print("a fatal error occurred. the program has aborted the start operation to prevent damage to your system.")
    print("detected error: (error 4) could not start due to invalid start configuration constant part 1.")
    input("press enter to finish")







