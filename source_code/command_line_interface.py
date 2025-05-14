

'''
cactus encrypt is a simple cli text encryption program written in python that implements the cactus cipher algorithm
Copyright 2023-2025 Redcactus5

This file is part of Cactus Encrypt.

Cactus Encrypt is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Cactus Encrypt is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Cactus Encrypt. If not, see <https://www.gnu.org/licenses/>. 

this program is free, open source software released under the GNU General Public License version 3.0 or later version (GPL-3.0-or-later)
'''


#imports
import time
import backend
from os import system, name


#controls wether debug text is shown
GLOBALDEBUGFLAG=False


#TODO: remember to fix the version string for final release


#"V2.0 beta: debug build 3"
PRGVERSION="V2.0"
#"V2.0"



#the help screen text
help=None

#just here so that we only show the license warning once on startup
LICENSESHOWN=False


    



#handy newline function. not necessary just nice to have
def ln(*number:int):
    if(len(number)<1):
        print("")
    elif(len(number)>1):
        raise ValueError("that boi ain't right: too many arguments, only one argument supported")
    elif(type(number[0])!=int):
        raise ValueError("that boi ain't right: input must be an integer")
    elif(number[0]<=0):
        raise ValueError("that boi ain't right: input must be greater than zero")
    elif(number[0]==1):
        print("")
    
    elif(number[0]>1):
        print("\n"*(number[0]-1))

#self explanitory, it clears the terminal
def clear():

    try:

        if name == 'nt':

            system('cls')

        else:

            system('clear')

    except:
        ln(50)
    


#ui header function to save time
def uiHeader(currentMode:str):
    clear()
    global PRGVERSION
    global help
    global LICENSESHOWN
    global GLOBALDEBUGFLAG
    print("cactus encrypt "+PRGVERSION+" by Redcactus5")
    print("Copyright 2023-2025 Redcactus5")
    ln()
    if(GLOBALDEBUGFLAG):
        print("*debug mode*")
        ln()
        print("WARNING: this is a debug build.")
        print("DO NOT SHARE IT WITH UNAUTHORIZED PARTIES.")
        print("this build is for testing purposes ONLY.")
        ln()
    if(not LICENSESHOWN):
        
        print("cactus encrypt is free open source software released under")
        print("GPL-3.0-or-later. see help.txt or view the help screen for details.")
        ln()
        LICENSESHOWN=True
    


    #inneficent, but in the grand sceme of things, I dont care
    if(backend.isCharSetLoaded()):
        print("character set loaded")
    if(backend.isKeyLoaded()):
        print("encryption key loaded")

    if(not(backend.isKeyLoaded()) or not(backend.isCharSetLoaded()) or (help==None)):
        
        if(not backend.isKeyLoaded()):
            print("notice: no encryption key loaded")
        if(not backend.isCharSetLoaded()):
            print("notice: no character set loaded")
        if(help==None):
            print("warning, help file could not be loaded! encryption and decryption \ncan still be done in this state, but the help function will be disabled")
        ln()
        print("system not ready")
    else:
        ln()
        print("system ready")
    ln()
    print("current operation: " +currentMode)
    
    ln(3)
 


def multipleChoiceScreen(message:str, optionsMessage:tuple, options:tuple, accuracy:int, currentMode:str, accuracyMode:int):
    #this function has multiple accuracy modes, so accuracy mode is used to select the one you want
    #0 is exact mode, it ignores the accuracy argument and compares input to option exactly
    #1 is trim mode, it trims the user input to the length of the accuracy variable, then compares that to the options list
    #2 is adaptive mode, it dynamically adjusts the accuracy value to the length of the input if it is lower than accuracy, and trims both the input and the option strings to the same length, then compares those. this can result in incorrect selections being made, so use with caution
    if(accuracyMode<0 or accuracyMode>2):
        #put error throwing code here
        raise ValueError("argument error: invalid accuracy mode argument. argument: {"+str(accuracyMode)+"} given, \nonly inclusive integer values between 0 and 2 supported")
        

    while True:
        uiHeader(currentMode)
        print(message)

        ln()
        for m in optionsMessage:
            print(m)
        ln()

        selection=input("please enter selection:")

        if(len(selection)>=1):

            if(accuracyMode==0):#exact mode
                for i in range(len(options)):
                    if(selection==str(options[i])):
                        return i
                    

            elif(accuracyMode==1):#trim mode
                if(accuracy>len(selection)):
                    accuracy=len(selection)

                for i in range(len(options)):
                    if(selection[:accuracy]==str(options[i])):
                        return i
                    

            elif(accuracyMode==2):#adaptive mode
                if(accuracy>len(selection)):
                    accuracy=len(selection)

                for i in range(len(options)):
                    if(selection[:accuracy]==str(options[i])[:accuracy]):
                        return i




        uiHeader(currentMode)
        print("syntax error: bad input. please enter one of the provided options")
        ln(2)
        input("press enter to continue")




            

def booleanQuestionScreen(message:str,currentMode:str):
    choice=multipleChoiceScreen(message,("(y)es","(n)o"),("yes","no"),1,currentMode,2)
    if(choice==0):
        return True
    return False



def enterFileNameScreen(message:str, currentMode:str):
    while True:
        uiHeader(currentMode)

        print(message)
        ln()

        fileName=input("file name:")

        if(multipleChoiceScreen("is \""+fileName+"\" correct?",("(c)onfirm","(r)e-enter"),("confirm","re-enter","reenter"),1,currentMode,2)==0):
            return fileName




def errorScreen(errorMessage:str, currentMode:str):
    uiHeader(currentMode)
    print(errorMessage)

    ln()
    print("now returning to the main menu")
    ln(2)
    input("press enter to continue")





def finishedScreen(finishedMessage:str, completionTime:float, currentMode:str):
    uiHeader(currentMode)

    print(finishedMessage)
    print("finished in "+str(completionTime)+" second(s)")
    ln()
    print("now returning to the main menu")
    ln(2)
    input("press enter to continue")





def terminalExportScreen(finishedMessage:str, completionTime:float, exportMessage:str, exportedText:str, currentMode:str):
    uiHeader(currentMode)

    print(finishedMessage)
    print("finished in "+str(completionTime)+" second(s)")
    ln(2)
    print(exportMessage)
    print(exportedText)
    ln()
    print("now returning to the main menu")
    ln(2)
    input("press enter to continue")






def sanitizeInput(text:str):
    return text.replace("\n","").replace("\r","").replace("\t","").replace("\f","")
    
    


#i tried to make this faster and less messy by creating the easy cli toolkit, but it still ended up that way anyway. 
#in other words, abandon all hope, ye who edit here



def loadCharSet():
    menuName="load character set from terminal"

    if(booleanQuestionScreen("are you sure you want to load a new character set? \nany currently loaded character set will be over written, and any currently loaded key will be cleared.", menuName)):
        uiHeader(menuName)
        
        print("warning: the new character set cannot contain duplicate characters or the unicode replacement character {�}.")
        ln()
        print("please enter the new character set.")
        ln()
        newSet=input("character set:")
        uiHeader(menuName)
        print("now loading...")

        start=time.time()
        success=backend.loadCharSet(newSet)
        total=time.time()-start

        if(success[0]):
            finishedScreen("character set successfully loaded!",total,menuName)
        else:
            errorScreen("load failed!\n\n"+success[1], menuName)


def loadCharSetFromTXT():
    menuName="load character set from file"

    if(booleanQuestionScreen("are you sure you want to load a new character set? \nany currently loaded character set will be over written and any currently loaded key will be cleared.",menuName)):
        uiHeader(menuName)
        sourceFile=enterFileNameScreen("warning: the new character set cannot contain duplicate characters or the unicode replacement character {�}.\n\nplease enter the name of the file to load the character set from (include the file extension).",menuName)
        uiHeader(menuName)
        print("now loading...")

        start=time.time()
        success=backend.loadCharSetFromTXT(sourceFile)
        total=time.time()-start

        if(success[0]):
            finishedScreen("character set successfully loaded!",total,menuName)
        else:
            errorScreen("load failed!\n\n"+success[1], menuName)


def scrambleCharSet():
    menuName="scramble character set"
    if(backend.isCharSetLoaded()):
        if(booleanQuestionScreen("are you sure you want to scramble the currently loaded character set?\n this will replace the currently loaded character set, \nand break compatibility with anything encrypted with it. additionally, \nany currently loaded  key will be cleared.",menuName)):
            
            uiHeader(menuName)
            print("now scrambling...")

            start=time.time()
            success=backend.scrambleCharSet()
            total=time.time()-start
            if(success[0]):
                finishedScreen("character set scramble successful!",total,menuName)
            else:
                errorScreen("character set scramble failed!\n\n"+success[1],menuName)


    else:
        errorScreen("uh, oh!\nthere is no character set in memory to scramble!\nplease load a character set then try again!",menuName)


def exportCharSetToTXT():
    menuName="export character set to file"
    if(backend.isCharSetLoaded()):
        if(booleanQuestionScreen("are you sure you want to export the current character set to a file?",menuName)):
            sourceFile=enterFileNameScreen("please enter the name of the file to export the character set to (include the file extension).\nWarning! if the file does not exist, it will be created. if the file does exist, its contents will be overwritten.",menuName)
            
            uiHeader(menuName)
            print("exporting...")

            start=time.time()
            success=backend.exportCharSetToTXT(sourceFile)
            total=time.time()-start

            if(success[0]):
                finishedScreen("character set export successful!",total, menuName)
            else:
                errorScreen("character set export failed!\n\n"+success[1],menuName)
 

    else:
        errorScreen("uh, oh!\nthere is no character set in memory to export!\nplease load a character set then try again!",menuName)

       
def exportCharSet():
    menuName="export character set to terminal"
    if(backend.isCharSetLoaded()):
        if(booleanQuestionScreen("are you sure you want to export the current character set to the terminal?",menuName)):
            uiHeader(menuName)
            print("exporting...")

            start=time.time()
            charSetString=backend.exportCharSet()
            total=time.time()-start

            if(charSetString[0]):
                terminalExportScreen("character set export successful!",total,"please remember that curly braces are used to denote the start and end \nof the character set, but can also appear in it.","character set:{"+charSetString[1]+"}", menuName)
            else:
                errorScreen("character set export failed!\n\n"+charSetString[1],menuName)
 

    else:
        errorScreen("uh, oh!\nthere is no character set in memory to export!\nplease load a character set then try again!",menuName)

#remember to make this not work until a character set is loaded
def loadKeyFromTerminal():
    menuName="load encryption key from terminal entry"
    if(backend.isCharSetLoaded()):
        if(booleanQuestionScreen("are you sure you want to load a new encryption key? any currently loaded key will be overwritten.",menuName)):
            uiHeader(menuName)
            print("please enter the new encryption key.")
            ln()
            newKeyString=input("key:")

            uiHeader(menuName)
            print("now loading...")

            start=time.time()
            success=backend.loadKey(newKeyString)
            total=time.time()-start

            if(success[0]):
                finishedScreen("encryption key load successful!",total,menuName)
            else:
                errorScreen("encryption key load failed!\n\n"+success[1],menuName)  
    else:
        errorScreen("uh, oh!\nyou need a character set in memory in order to load a key!\nplease load the character set associated with your key then try again!",menuName)


def exportKeyToTerminal():
    menuName="export key to terminal"
    if(backend.isKeyLoaded()):
        if(booleanQuestionScreen("are you sure you want to export the current encryption key to the terminal?",menuName)):
            uiHeader(menuName)
            print("exporting...")

            start=time.time()
            keyString=backend.exportKey()
            total=time.time()-start

            if(keyString[0]):
                terminalExportScreen("encryption key export successful!",total,"please remember that curly braces are used to denote the start \nand end of the key, and are not part of it.","encryption key:{"+keyString[1]+"}", menuName)
            else:
                errorScreen("encryption key export failed!\n\n"+keyString[1],menuName)

    
    else:
        errorScreen("uh, oh!\nthere is encryption key in memory to export!\nplease load or generate a key then try again!",menuName)
        

def generateKey():
    menuName="generate key"

    if(backend.isCharSetLoaded()):
        if(booleanQuestionScreen("are you sure you want to generate a new encryption key?\n any currently loaded key will be overwritten.",menuName)):


            complexity=0

            while True:
                uiHeader(menuName)
                print("please enter a complexity value for the new key (complexity value must be a positive integer).")
                print("warning! though using a higher number improves security, it also increases key generation, \nencryption, and decryption times!")
                ln()
                userInput=input("complexity value:")


                inputError=False

                try:
                    userInput=userInput
                except:
                    inputError=True
                
                if(not userInput.isnumeric()):
                    inputError=True

                try:
                    userInput=int(userInput)
                except:
                    inputError=True

                if(inputError==False and userInput<1):
                    inputError=True

                


                if(inputError):
                    uiHeader(menuName)
                    print("input error: (error code: I-18-1) given complexity value is invalid. please check that the complexity \nvalue is a positive integer, then try again.")
                    ln(2)
                    input("press enter to continue")
                
                else:
                    complexity=userInput
                    break
            
            uiHeader(menuName)
            print("now generating...")

            start=time.time()
            success=backend.generateKey(complexity)
            total=time.time()-start

            if(success[0]):
                finishedScreen("encryption key generation successful!",total,menuName)
            else:
                errorScreen("encryption key generation failed!\n\n"+success[1],menuName)
    else:
        errorScreen("uh, oh!\nthere is no character set in memory, a requirement to generate a key!\nplease load a character set then try again!",menuName)

#remember to make this not work until a character set is loaded
def loadKeyFromTXT():
    menuName="load encryption key from file"
    if(backend.isCharSetLoaded()):
        if(booleanQuestionScreen("are you sure you want to load a new encryption key? any currently loaded key will be overwritten.",menuName)):
            
            fileName=enterFileNameScreen("please enter the name of the file to load the encryption key from (include the file extension).",menuName)

            uiHeader(menuName)
            print("now loading...")

            start=time.time()
            success=backend.loadKeyFromTXT(fileName)
            total=time.time()-start

            if(success[0]):
                finishedScreen("encryption key load successful!",total,menuName)
            else:
                errorScreen("encryption key load failed!\n\n"+success[1],menuName)
    else:
        errorScreen("uh, oh!\nyou need a character set in memory in order to load a key!\nplease load the character set associated with your key then try again!",menuName)



def exportKeyToTXT():
    menuName="export encryption key to file"

    if(backend.isKeyLoaded()):
        if(booleanQuestionScreen("are you sure you want to export the current encryption key to a file?",menuName)):

            fileName=enterFileNameScreen("please enter the name of the file to export the encryption key to (include the file extension).\nWarning! if the does not exist, it will be created. if the file does exist, its contents will be overwritten.",menuName)
            
            uiHeader(menuName)
            print("exporting...")

            start=time.time()
            success=backend.exportKeyToTXT(fileName)
            total=time.time()-start

            if(success[0]):
                finishedScreen("encryption key successfully exported!", total, menuName)
            else:
                errorScreen("encryption key export failed!\n\n"+success[1],menuName)
    
    else:
        errorScreen("uh, oh!\nthere is encryption key in memory to export!\nplease load or generate a key then try again!",menuName)

#actual encryption stuff

def encryptTerminalInput():
    menuName="encrypt terminal entry"
    if(backend.isCharSetLoaded() and backend.isKeyLoaded()):
        
        if(booleanQuestionScreen("are you sure you want to encrypt data?",menuName)):
            uiHeader(menuName)
            print("please enter the text to encrypt.")
            ln()
            toBeEncrypted=input("text:")

            uiHeader(menuName)
            print("encrypting...")

            start=time.time()
            encryptedText=backend.encryptText(toBeEncrypted)
            total=time.time()-start

            if(encryptedText[0]):
                terminalExportScreen("encryption successful!",total,"please remember that curly braces are used to denote the start \nand end of the encrypted text, but can also appear in it.","encrypted text:{"+encryptedText[1]+"}", menuName)
            
            else:
                errorScreen("encryption failed!\n\n"+encryptedText[1], menuName)

    else:
        if((not backend.isCharSetLoaded()) and (not backend.isKeyLoaded())):
            errorScreen("uh, oh! \nthere is no encryption key or character set in memory, and you need both to encrypt! \nplease load both of them then try again!",menuName)
        elif(not backend.isCharSetLoaded()):
            errorScreen("uh, oh! \nthere is no character set in memory, and you need that to encrypt! \nplease load one then try again!",menuName)
        else:
            errorScreen("uh, oh! \nthere is no encryption key in memory, and you need that to encrypt! \nplease load or generate one then try again!",menuName)


def decryptTerminalInput():
    menuName="decrypt terminal entry"

    if(backend.isCharSetLoaded() and backend.isKeyLoaded()):
        if(booleanQuestionScreen("are you sure you want to decrypt data?",menuName)):
            uiHeader(menuName)
            print("please enter the text to decrypt.")
            ln()
            toBeDecrypted=input("text:")

            uiHeader(menuName)
            print("decrypting...")

            start=time.time()
            decryptedText=backend.decryptText(toBeDecrypted)
            total=time.time()-start

            if(decryptedText[0]):
                terminalExportScreen("decryption successful!",total,"please remember that curly braces are used to denote the start \nand end of the decrypted text, but can also appear in it.","decrypted text:{"+decryptedText[1]+"}", menuName)
            
            else:
                errorScreen("encryption failed!\n\n"+decryptedText[1], menuName)

    else:
        if((not backend.isCharSetLoaded()) and (not backend.isKeyLoaded())):
            errorScreen("uh, oh! \nthere is no encryption key or character set in memory, and you need both to decrypt! \nplease load both of them then try again!",menuName)
        elif(not backend.isCharSetLoaded()):
            errorScreen("uh, oh! \nthere is no character set in memory, and you need that to decrypt! \nplease load one then try again!",menuName)
        else:
            errorScreen("uh, oh! \nthere is no encryption key in memory, and you need that to decrypt! \nplease load or generate one then try again!",menuName)


def encryptTXT():
    menuName="encrypt a text file"

    if(backend.isCharSetLoaded() and backend.isKeyLoaded()):

        
        if(booleanQuestionScreen("are you sure you want to encrypt a file?",menuName)):
            
            source=enterFileNameScreen("please enter the name of the file to encrypt (include the file extension).",menuName)


            output=enterFileNameScreen("please enter the name of the destination file (include the file extension).\nWarning! if the file does not exist, it will be created. if the file does exist, its contents will be overwritten.",menuName)
            
            
            uiHeader(menuName)
            print("encrypting...")

            start=time.time()
            success=backend.encryptTextFile(source,output)
            total=time.time()-start

            if(success[0]):
                finishedScreen("file encryption successful!", total, menuName)
            else:
                errorScreen("file encryption failed!\n\n"+success[1], menuName)
        
        

    else:
        if((not backend.isCharSetLoaded()) and (not backend.isKeyLoaded())):
            errorScreen("uh, oh! \nthere is no encryption key or character set in memory, and you need both to encrypt! \nplease load both of them then try again!",menuName)
        elif(not backend.isCharSetLoaded()):
            errorScreen("uh, oh! \nthere is no character set in memory, and you need that to encrypt! \nplease load one then try again!",menuName)
        else:
            errorScreen("uh, oh! \nthere is no encryption key in memory, and you need that to encrypt! \nplease load or generate one then try again!",menuName)


def decryptTXT():
    menuName="decrypt a text file"

    if(backend.isCharSetLoaded() and backend.isKeyLoaded()):

        if(booleanQuestionScreen("are you sure you want to decrypt a file?",menuName)):
            
            source=enterFileNameScreen("please enter the name of the file to decrypt (include the file extension).",menuName)


            output=enterFileNameScreen("please enter the name of the destination file (include the file extension)\nWarning! if the file does not exist, it will be created. if the file does exist, its contents will be overwritten.",menuName)
            
            
            uiHeader(menuName)
            print("decrypting...")

            start=time.time()
            success=backend.decryptTextFile(source,output)
            total=time.time()-start

            if(success[0]):
                finishedScreen("file decryption successful!", total, menuName)
            else:
                errorScreen("file decryption failed!\n\n"+success[1], menuName)



    else:
        if((not backend.isCharSetLoaded()) and (not backend.isKeyLoaded())):
            errorScreen("uh, oh! \nthere is no encryption key or character set in memory, and you need both to decrypt! \nplease load both of them then try again!",menuName)
        elif(not backend.isCharSetLoaded()):
            errorScreen("uh, oh! \nthere is no character set in memory, and you need that to decrypt! \nplease load one then try again!",menuName)
        else:
            errorScreen("uh, oh! \nthere is no encryption key in memory, and you need that to decrypt! \nplease load or generate one then try again!",menuName)



def sanitizeText():
    menuName="sanitize text"

    if(backend.isCharSetLoaded()):
        if(booleanQuestionScreen("are you sure you want to sanitize text?",menuName)):

            attemptReplacement=booleanQuestionScreen("would you like to attempt replacing invalid characters with valid replacements?\n\nwarning: this is not guaranteed to work perfectly, and the replacement you enter must already be \nin the loaded character set. additionally, using this feature may break formatting.",menuName)

            replacementChar=""
            if(attemptReplacement):
                while(True):
                    uiHeader(menuName)
                    print("please enter the character to replace invalid characters with:")
                    prospectiveReplacementChar=input("")
                    if(prospectiveReplacementChar==None):
                        attemptReplacement=False
                        break
                    elif(len(prospectiveReplacementChar)<=0):
                        attemptReplacement=False
                        break
                    elif(len(prospectiveReplacementChar)>1):
                        uiHeader(menuName)
                        print("input error: more than one character entered. please try again with a single character.")
                        ln(3)
                        input("press enter to continue")
                    elif(not(prospectiveReplacementChar in backend.getCharSet())):
                        uiHeader(menuName)
                        print("input error: entered character is not in the currently loaded character set. \nplease try again with a valid character.")
                        ln(3)
                        input("press enter to continue")
                    else:
                        replacementChar=prospectiveReplacementChar
                        break


            uiHeader(menuName)

            if(attemptReplacement):
                print("warning: this feature works by removing all instances of character not present in the currently\nloaded key from the text, and replacing them with valid spacing characters. using this feature can\nmake text unreadable and often breaks formatting.")
            else:
                print("warning: this feature works by removing all instances of character not present in the currently\nloaded key from the text. using this feature can make text unreadable and often breaks formatting.")

            ln(2)

            print("please enter the text to sanitize.")
            ln()
            toBeSanitized=input("text:")
            
            uiHeader(menuName)
            print("cleaning text...")

            start=time.time()
            cleanText=backend.sanitizeText(toBeSanitized,attemptReplacement,replacementChar)
            total=time.time()-start
     

            if(cleanText[0]):
                if(attemptReplacement):
                    terminalExportScreen("sanitization successful!\n"+str(cleanText[2])+" character(s) replaced.",total,"please remember that curly braces are used to denote the start \nand end of the text, but can also appear in it.","sanitized text:{"+cleanText[1]+"}", menuName)
                else:
                    terminalExportScreen("sanitization successful!\n"+str(cleanText[2])+" character(s) removed.",total,"please remember that curly braces are used to denote the start \nand end of the text, but can also appear in it.","sanitized text:{"+cleanText[1]+"}", menuName)
            else:
                errorScreen("sanitization failed!\n\n"+cleanText[1], menuName)

    else:
        errorScreen("uh, oh! \nthere is no character set in memory, and you need that to sanitize text! \nplease load or generate one then try again!",menuName)








def sanitizeTXT():
    menuName="sanitize a text file"

    if(backend.isCharSetLoaded()):

        if(booleanQuestionScreen("are you sure you want to sanitize a text file?",menuName)):

            attemptReplacement=booleanQuestionScreen("would you like to attempt replacing invalid characters with valid replacements?\n\nwarning: this is not guaranteed to work perfectly, and the replacement you enter must already be \nin the loaded character set. additionally, using this feature may break text formatting.",menuName)


            replacementChar=""
            if(attemptReplacement):
                while(True):
                    uiHeader(menuName)
                    print("please enter the character to replace invalid characters with:")
                    prospectiveReplacementChar=input("")
                    if(prospectiveReplacementChar==None):
                        attemptReplacement=False
                        break
                    elif(len(prospectiveReplacementChar)<=0):
                        attemptReplacement=False
                        break
                    elif(len(prospectiveReplacementChar)>1):
                        uiHeader(menuName)
                        print("input error: more than one character entered. please try again with a single character.")
                        ln(3)
                        input("press enter to continue")
                    elif(not(prospectiveReplacementChar in backend.getCharSet())):
                        uiHeader(menuName)
                        print("input error: entered character is not in the currently loaded character set. \nplease try again with a valid character.")
                        ln(3)
                        input("press enter to continue")
                    else:
                        replacementChar=prospectiveReplacementChar
                        break

            
            source=enterFileNameScreen("please enter the name of the file to sanitize (include the file extension).",menuName)


            output=enterFileNameScreen("please enter the name of the destination file (include the file extension)\nWarning! if the file does not exist, it will be created. if the file does exist, its contents will be overwritten.",menuName)
            
            
            uiHeader(menuName)
            print("cleaning...")

            start=time.time()
            success=backend.sanitizeTextFile(source,output,attemptReplacement,replacementChar)
            total=time.time()-start

            if(success[0]):
                if(attemptReplacement):
                    finishedScreen("file sanitization successful!\n"+str(success[2])+" character(s) replaced.", total, menuName)
                else:
                    finishedScreen("file sanitization successful!\n"+str(success[2])+" character(s) removed.", total, menuName)
            else:
                errorScreen("file sanitization failed!\n\n"+success[1], menuName)



    else:
        errorScreen("uh, oh! \nthere is no character set in memory, and you need that to sanitize text! \nplease load or generate one then try again!",menuName)














#ui stuff

def helpScreen():
    menuName="help"
    if(help==None):
        uiHeader(menuName)
        errorScreen("uh, oh!\nthe help file couldn't be loaded!\nplease check it for errors, and if it has been moved, please put it back. \nafter that, please restart the program then try again.",menuName)
    else:
        uiHeader(menuName)
        print(help)
        ln(3)
        input("press enter to return to the main menu")

    #just print readme.txt


def exit():
    menuName="quit?"
    return booleanQuestionScreen("are you sure you want to quit?",menuName)





#TODO:
def CLI_V2():
    menuName="main menu"
    run=True
    global GLOBALDEBUGFLAG
    selectionAccuracy=2

    options=("(1) encrypt text","(2) encrypt a text file","(3) decrypt text","(4) decrypt a text file", "(5) load an encryption key from the terminal","(6) load an encryption key from a file","(7) generate an encryption key","(8) export currently loaded encryption key to the terminal","(9) export the currently loaded encryption key to a file", "(10) load a character set from the terminal","(11) load a character set from a file", "(12) scramble the currently loaded character set", "(13) export the currently loaded character set to the terminal", "(14) export the currently loaded character set to a file", "(15) sanitize text", "(16) sanitize text file","(17) help", "(18) quit")
    optionCodes=("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","qu","q","ex","e")
    
        


    while run:
        selection=multipleChoiceScreen("welcome to cactus encrypt. please select an option:",options,optionCodes,selectionAccuracy,menuName,1)

        if(selection==0):
            encryptTerminalInput()
        
        elif(selection==1):
            encryptTXT()

        elif(selection==2):
            decryptTerminalInput()
        
        elif(selection==3):
            decryptTXT()

        elif(selection==4):
            loadKeyFromTerminal()

        elif(selection==5):
            loadKeyFromTXT()

        elif(selection==6):
            generateKey()

        elif(selection==7):
            exportKeyToTerminal()

        elif(selection==8):
            exportKeyToTXT()

        elif(selection==9):
            loadCharSet()

        elif(selection==10):
            loadCharSetFromTXT()

        elif(selection==11):
            scrambleCharSet()

        elif(selection==12):
            exportCharSet()

        elif(selection==13):
            exportCharSetToTXT()

        elif(selection==14):
            sanitizeText()

        elif(selection==15):
            sanitizeTXT()

        elif(selection==16):
            helpScreen()
        
        elif(selection>=17 and selection<=21):
            if(exit()):
                run=False
                break


    clear()
    print("thank you for using cactus encrypt!")
    



def start(debugMode):



    #these files are a completely optional feature, so we dont throw and error if they fail to load
    backend.loadCharSetFromTXT("default_charset.txt")
    backend.loadKeyFromTXT("default_key.txt")
    
    #we handle informing the user of helpfile errors elsewhere
    try:
        helpFile = backend.getTextFromFile("help.txt")
        if(helpFile[0]):
            global help
            help=helpFile[1]
            
    except:
        pass
    


    #users will almost never see this, it only triggers in debug builds
    if(debugMode):
        global GLOBALDEBUGFLAG
        global PRGVERSION
        GLOBALDEBUGFLAG=True
    
        print("done!")
        PRGVERSION+=": DEBUG"
        clear()
        print("WARNING: this is a debug build. it is for closed testing purposes \nonly and is not to be shared with unauthorized parties.")
        ln()
        print("if you do not agree to this, close the program.")
        ln(3)
        input("press enter to agree and continue")
        clear()
    else:
        print("done!")
    CLI_V2()
    
    


            
