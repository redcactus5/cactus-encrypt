

'''
cactus encrypt is a simple cli text encryption program written in python that implements the cactus cipher algorithm
Copyright 2023-2025 Redcactus5

This file is part of Cactus Encrypt.

Cactus Encrypt is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Cactus Encrypt is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Cactus Encrypt. If not, see <https://www.gnu.org/licenses/>. 

this program is free, open source software released under the GNU General Public License version 3.0 or later version (GPL-3.0-or-later)
'''


#this file is basically just a launcher for the main program, and it does a whole lot of unnecessesary verifaction




import os


print("starting up...")
preStartCheck1=True

#import needed files, and check if they exist at all
try:
    #this file determines what type of build this is and what mode to run in as a result
    import build_mode
except ImportError:
    (preStartCheck1)=False
    print("\n"*50)
    print("a fatal error occurred. the program has aborted the start operation to prevent further errors.")
    print("detected error: (error code: L-1-1) start configuration file could not be found.")
    input("press enter to finish")
if((preStartCheck1)):
    try:
        import command_line_interface
    except ImportError:
        (preStartCheck1)=False
        print("\n"*50)
        print("a fatal error occurred. the program has aborted the start operation to prevent further errors.")
        print("detected error: (error code: L-1-2) the main program files could not be found or had a dependancy error.")
        input("press enter to finish")


if(not os.path.exists("LICENSES/COPYING.txt")):
    (preStartCheck1)=False
    print("\n"*50)
    print("a fatal error occurred. the program has aborted the start operation to prevent further errors.")
    print("detected error: (error code: L-1-3) this program is open source and must be distributed with its licenses.\nPlease ensure the LICENSES directory is present and contains COPYING.txt and Nuitka-Apache-2.0-LICENSE.txt.")
    input("press enter to finish")

if(not os.path.exists("LICENSES/Nuitka-Apache-2.0-LICENSE.txt")):
    (preStartCheck1)=False
    print("\n"*50)
    print("a fatal error occurred. the program has aborted the start operation to prevent further errors.")
    print("detected error: (error code: L-1-3) this program is open source and must be distributed with its licenses.\nPlease ensure the LICENSES directory is present and contains COPYING.txt and Nuitka-Apache-2.0-LICENSE.txt.")
    input("press enter to finish")

#attempt get the build mode from the file
mode=None

preStartCheck2=False

if((preStartCheck1)):
    preStartCheck2=True


    try:
        mode=build_mode.getBuildMode()
    except:
        preStartCheck2=False
        mode=None
        print("\n"*50)
        print("a fatal error occurred. the program has aborted the start operation to prevent further errors.")
        print("detected error: (error code: L-2-1) start configuration file could either not be read or not be found.")
        input("press enter to finish")

ableToStart=False

if(preStartCheck2):
    #do some basic config formatting checks before we even do verifacation. this is not a deep verfiaction
    errorcode=1
    if(not(mode is None)):
        errorcode+=1
        if(isinstance(mode, tuple)):
            errorcode+=1   
            if(len(mode)>1):
                errorcode+=1
                ableToStart=True   
    else:
        print("\n"*50)
        print("a fatal error occurred. the program has aborted the start operation to prevent further errors.")
        print("detected error: (error code: L-3-"+str(errorcode)+") start configuration file is corrupted or improperly formatted.")
        input("press enter to finish")


        


if(ableToStart):

    #determine if this is a release build
    if(mode[0]=="RELEASE"):


        
    
        if(command_line_interface.backend.bmkv(True,mode[1])==1):
            try:#if so start in release mode
                
                command_line_interface.start(False)
            except Exception as e:
                print("\n"*50)
                print("a fatal error occurred (error code: L-4-1). the program has quit to prevent further errors.")
                print("detected error: "+str(e))
                input("press enter to finish")



        elif(command_line_interface.backend.bmkv(True,mode[1])==0):
            print("\n"*50)
            print("a fatal error occurred. the program has aborted the start operation to prevent further errors.")
            print("detected error: (error code: L-4-2) could not start due to invalid start configuration file part 2.")
            input("press enter to finish")
    
        elif(command_line_interface.backend.bmkv(True,mode[1])==-1):
            print("\n"*50)
            print("a fatal error occurred. the program has aborted the start operation to prevent further errors.")
            print("detected error: (error code: L-4-3) could not start due to configuration verifaction process failure.")
            input("press enter to finish")
    
    
    #determine if this is a debug build
    elif(mode[0]=="TESTING BUILD"):
        
        
        if(command_line_interface.backend.bmkv(False,mode[1])==1):
            #if so start in debug mode
            command_line_interface.start(True)


        elif(command_line_interface.backend.bmkv(False,mode[1])==0):
            print("\n"*50)
            print("a fatal error occurred. the program has aborted the start operation to prevent further errors.")
            print("detected error: (error code: L-5-1) could not start due to invalid start configuration file part 2.")
            input("press enter to finish")
        
        elif(command_line_interface.backend.bmkv(False,mode[1])==-1):
            print("\n"*50)
            print("a fatal error occurred. the program has aborted the start operation to prevent further errors.")
            print("detected error: (error code: L-6-2) could not start due to configuration verifaction process failure.")
            input("press enter to finish")



    elif(ableToStart):#error out if no valid build type tag
        print("\n"*50)
        print("a fatal error occurred. the program has aborted the start operation to prevent further errors.")
        print("detected error: (error code: L-7-1) could not start due to invalid start configuration file part 1.")
        input("press enter to finish")



