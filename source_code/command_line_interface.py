#imports
import time
import backend
from os import system, name




#TODO: remember to fix the version string for final release

PRGVERSION="V2.0 alpha 1: active development"
#"V2.0 beta: debug build 1"
#"V2.0 RC1"
#"V2.0"

HELP=None



'''
TO DO:
1.write readme/help file
3. add features in update manifest:
 a. add ability to load and store keys in a txt file
 b. add ability to encrypt and decrpyt text files
 c. add ability to load character sets from text files
 d. add ability to export character sets to text files
 e. have you you enter the name of the file to use in the above additional options
 f. overhaul ui function
 g. completely rewrite information text
 h. add a note saying that text feilds are encapsolated by curly braces
 i. add ability to scramble the current character set
 j. add ability to import and export character sets through the terminal
 k. it is recomended to try and make one set of functions for all the txt file stuff and then link those together with existing work
 l. make it attempt to load a default character set and key at startup
'''


    



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
    
    elif(number[0]>=1):
        print("\n"*(number[0]-1))


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
    global HELP
    print("cactus encrypt "+PRGVERSION+" by redcacus5")
    print(currentMode)
    ln()


    #inneficent, but in the grand sceme of things, I dont care
    if(backend.isCharSetLoaded()):
        print("character set loaded")
    if(backend.isKeyLoaded()):
        print("encryption key loaded")
    if(backend.isKeyLoaded() or backend.isCharSetLoaded()):
        ln()

    if(not(backend.isKeyLoaded()) or not(backend.isCharSetLoaded()) or (HELP==None)):
        print("system not ready. detected problems:")
        if(not backend.isKeyLoaded()):
            print("warning, no key in memory! please generate or load a key")
        if(not backend.isCharSetLoaded()):
            print("warning, no character set in memory! please load a character set")
        if(HELP==None):
            print("warning, readme file could not be loaded! encryption and decrpytion \ncan still be done in this state, but the help function will be disabled")
    else:
        print("no errors detected. system ready")

    ln(3)
 


def multipleChoiceScreen(message:str, optionsMessage:tuple, options:tuple, accuracy:int, currentMode:str):
    while True:
        uiHeader(currentMode)
        print(message)
        ln()
        for m in optionsMessage:
            print(m)
        ln()
        selection=input("please enter selection:")
        if(len(selection)>=1):
            if(accuracy>len(selection)):
                accuracy=len(selection)
            for i in range(len(options)):
                if(selection[:accuracy]==options[i]):
                    return i
        uiHeader(currentMode)
        print("syntax error: bad input. please enter one of the provided options")
        ln(2)
        input("press enter to continue")




            

def booleanQuestionScreen(message:str,currentMode:str):
    choice=multipleChoiceScreen(message,("(y)es","(n)o"),("y","n"),1,currentMode)
    if(choice==0):
        return True
    return False



def enterFileNameScreen(message:str, currentMode:str):
    while True:
        uiHeader(currentMode)

        print(message)
        ln()

        fileName=input("file name:")

        if(multipleChoiceScreen("is \""+fileName+"\" correct?",("(c)onfirm","(r)eenter"),("c","r"),1,currentMode)==0):
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
    
    



'''
options to implement (as functions this time):
load char set from text file
load char set from terminal
scramble char set
export char set to text file
export char set to terminal
encrypt text file
decrypt text file
load key from text file
export key to text file
encrypt text input
decrypt text input
load a key via text input
export key to terminal
generate new key
print readme.txt
exit

help is being farmed out to the readme file

you still need to rewrite everything from scratch or at least near scratch.
'''

#remember to check for presence of the things you need



def loadCharSet():
    menuName="load character set from terminal"

    if(booleanQuestionScreen("are you sure you want to load a new character set? \nany currently loaded character set will be over written", menuName)):
        uiHeader(menuName)
        print("please enter the new character set")
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

    if(booleanQuestionScreen("are you sure you want to load a new character set? \nany currently loaded character set will be over written",menuName)):
        uiHeader(menuName)
        sourceFile=enterFileNameScreen("please enter the name of the file to load the character set from (include the file extension)",menuName)
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
        if(booleanQuestionScreen("are you sure you want to scramble the currently loaded character set?\n this will overwrite the currently loaded character set, \nand break compatibility with anything encrypted with it",menuName)):
            
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
            sourceFile=enterFileNameScreen("please enter the name of the file to export the character set to (include the file extension)\nWarning! if the does not exist, it will be created. if the file does exist, its contents will be overwritten",menuName)
            
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
                terminalExportScreen("character set export successful!",total,"please remember that curly braces are used to denote the start and end \nof the character set, but can also appear in it","character set:{"+charSetString[1]+"}", menuName)
            else:
                errorScreen("character set export failed!\n\n"+charSetString[1],menuName)
 

    else:
        errorScreen("uh, oh!\nthere is no character set in memory to export!\nplease load a character set then try again!",menuName)



def loadKeyFromTerminal():
    menuName="load encryption key from terminal entry"
    if(booleanQuestionScreen("are you sure you want to load a new encryption key? any currently loaded key will be overwritten",menuName)):
        uiHeader(menuName)
        print("please enter the new encryption key")
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
                terminalExportScreen("encryption key export successful!",total,"please remember that curly braces are used to denote the start \nand end of the key, and are not part of it","encryption key:{"+keyString[1]+"}", menuName)
            else:
                errorScreen("encryption key export failed!\n\n"+keyString[1],menuName)

    
    else:
        errorScreen("uh, oh!\nthere is encryption key in memory to export!\nplease load or generate a key then try again!",menuName)
        

def generateKey():
    menuName="generate key"

    if(backend.isCharSetLoaded()):
        if(booleanQuestionScreen("are you sure you want to generate a new encryption key?\n any currently loaded key will be overwritten",menuName)):


            complexity=0

            while True:
                uiHeader(menuName)
                print("please enter a complexity value for the new key (complexity value must be a positive integer):")
                ln()
                userInput=input("complexity value:")


                inputError=False

                try:
                    userInput=int(userInput)
                except:
                    inputError=True
                

                if(inputError==False and userInput<1):
                    inputError=True


                if(inputError):
                    uiHeader(menuName)
                    print("input error: given complexity value is invalid. please check that the complexity \nvalue is a positive integer, then try again")
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




def loadKeyFromTXT():
    menuName="load encryption key from file"
    if(booleanQuestionScreen("are you sure you want to load a new encryption key? any currently loaded key will be overwritten",menuName)):
        
        fileName=enterFileNameScreen("please enter the name of the file to load the encryption key from (include the file extension)",menuName)

        uiHeader(menuName)
        print("now loading...")

        start=time.time()
        success=backend.loadKeyFromTXT(fileName)
        total=time.time()-start

        if(success[0]):
            finishedScreen("encryption key load successful!",total,menuName)
        else:
            errorScreen("encryption key load failed!\n\n"+success[1],menuName)


def exportKeyToTXT():
    menuName="export encryption key to file"

    if(backend.isKeyLoaded()):
        if(booleanQuestionScreen("are you sure you want to export the current encryption key to a file",menuName)):

            fileName=enterFileNameScreen("please enter the name of the file to export the encryption key to (include the file extension)\nWarning! if the does not exist, it will be created. if the file does exist, its contents will be overwritten",menuName)
            
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
        


#acual encryption stuff

def encryptTerminalInput():
    menuName="encrypt terminal entry"
    if(backend.isCharSetLoaded() and backend.isKeyLoaded()):
        
        if(booleanQuestionScreen("are you sure you want to encrypt data?",menuName)):
            uiHeader(menuName)
            print("please enter the text to decrypt")
            ln()
            toBeEncrypted=input("text:")

            uiHeader(menuName)
            print("encrypting...")

            start=time.time()
            encryptedText=backend.encryptText(toBeEncrypted)
            total=time.time()-start

            if(encryptedText[0]):
                terminalExportScreen("encryption successful!",total,"please remember that curly braces are used to denote the start \nand end of the encrypted text, but can also appear in it","encrypted text:{"+encryptedText[1]+"}", menuName)
            
            else:
                errorScreen("encryption failed!\n\n"+encryptedText[1], menuName)

    else:
        if((not backend.isCharSetLoaded()) and (not backend.isKeyLoaded())):
            errorScreen("uh, oh! \nthere is no encryption key or character set in memory, and you need both to encrypt! \nplease load both of them then try again!",menuName)
        elif(not backend.isCharSetLoaded()):
            errorScreen("uh, oh! \nthere is no character set in memory, and you need that to encrypt! \nplease load one then try again!",menuName)
        else:
            errorScreen("uh, oh! \nthere is no encryption key in memory, and you need that to encrypt! \nplease load or generate one then try again!")

        





def decryptTerminalInput():
    menuName="decrypt terminal entry"

    if(backend.isCharSetLoaded() and backend.isKeyLoaded()):
        if(booleanQuestionScreen("are you sure you want to decrypt data?",menuName)):
            uiHeader(menuName)
            print("please enter the text to decrypt")
            ln()
            toBeDecrypted=input("text:")

            uiHeader(menuName)
            print("decrypting...")

            start=time.time()
            decryptedText=backend.encryptText(toBeDecrypted)
            total=time.time()-start

            if(decryptedText[0]):
                terminalExportScreen("decryption successful!",total,"please remember that curly braces are used to denote the start \nand end of the decrypted text, but can also appear in it","decrypted text:{"+decryptedText[1]+"}", menuName)
            
            else:
                errorScreen("encryption failed!\n\n"+decryptedText[1], menuName)

    else:
        if((not backend.isCharSetLoaded()) and (not backend.isKeyLoaded())):
            errorScreen("uh, oh! \nthere is no encryption key or character set in memory, and you need both to decrypt! \nplease load both of them then try again!",menuName)
        elif(not backend.isCharSetLoaded()):
            errorScreen("uh, oh! \nthere is no character set in memory, and you need that to decrypt! \nplease load one then try again!",menuName)
        else:
            errorScreen("uh, oh! \nthere is no encryption key in memory, and you need that to decrypt! \nplease load or generate one then try again!")






def ecryptTXT():
    menuName="encrypt a text file"

    if(backend.isCharSetLoaded() and backend.isKeyLoaded()):
        
        
        
        
        
        pass#placeholder

    else:
        if((not backend.isCharSetLoaded()) and (not backend.isKeyLoaded())):
            errorScreen("uh, oh! \nthere is no encryption key or character set in memory, and you need both to encrypt! \nplease load both of them then try again!",menuName)
        elif(not backend.isCharSetLoaded()):
            errorScreen("uh, oh! \nthere is no character set in memory, and you need that to encrypt! \nplease load one then try again!",menuName)
        else:
            errorScreen("uh, oh! \nthere is no encryption key in memory, and you need that to encrypt! \nplease load or generate one then try again!")






def decryptTXT():
    menuName="decrypt a text file"

    if(backend.isCharSetLoaded() and backend.isKeyLoaded()):







        
        pass#placeholder

    else:
        if((not backend.isCharSetLoaded()) and (not backend.isKeyLoaded())):
            errorScreen("uh, oh! \nthere is no encryption key or character set in memory, and you need both to decrypt! \nplease load both of them then try again!",menuName)
        elif(not backend.isCharSetLoaded()):
            errorScreen("uh, oh! \nthere is no character set in memory, and you need that to decrypt! \nplease load one then try again!",menuName)
        else:
            errorScreen("uh, oh! \nthere is no encryption key in memory, and you need that to decrypt! \nplease load or generate one then try again!")


def helpScreen():
    menuName="help"
    if(HELP==None):
        uiHeader(menuName)
        errorScreen("uh, oh!\nthe help file couldn't be loaded!\nplease check it for errors, and if it has been moved, please put it back. \nafter that, please restart the program then try again",menuName)
    else:
        uiHeader(menuName)
        print(HELP)
        ln(3)
        input("press enter to return to the main menu")

    #just print readme.txt


def exit():
    menuName="quit?"
    return booleanQuestionScreen("are you sure you want to quit?",menuName)


#TODO:
def CLI_V2():
    #todo: rewrite readme.md and write help.txt
    pass



def start():

    backend.loadCharSetFromTXT("default_charset.txt")
    backend.loadKeyFromTXT("default_key.txt")

    try:
        helpFile = open("help.txt","r")
        global HELP
        HELP=helpFile.read()
        helpFile.close()
    except:
        pass

    CLI_V2()
    
    




    
#who ya gunna call?

#this is being depricated and will be removed on the production version if i remember 
#CLI user interface
def userInterface():
    running=True
    while running:
        ln(40)
        uiHeader()
        print("please select an option:")
        print("1: encrypt text")
        print("2: decrypt text")
        print("3: load a key")
        print("4: generate a key")
        print("5: export current key")
        print("6: information")
        print("7: exit")
        selection=input("please enter selection:")
        if(selection=="7"):
            ln(40)
            print("thank you for using cactus encrypt -red")
            running=False
            break
        elif(selection=="1"):
            if(backend.loadedKey==None):
                ln(40)
                uiHeader()
                print("error: encryption key not found! please load or generate a key to continue.")
                input("press enter to continue")
            else:
                ln(40)
                uiHeader()
                print("please enter text to be encrypted:")
                text=input()
                print("encrypting...")
                start=time.time()
                encryptedText=backend.encrypt(text)
                elapsed=time.time()-start
                ln(40)
                if(encryptedText[0]):
                    uiHeader()
                    print("encryption successful")
                    print("finished in "+str(elapsed)+" second(s)")
                    print("here is your encrypted text:{"+encryptedText[1]+"}")
                    ln()
                    input("press enter to continue")
                else:
                    uiHeader()
                    print("error: unsupported character {"+encryptedText[1]+"} in text! check text for the unsuported character. a complete list of supported characters can be found in the information menu.")
                    input("press enter to continue")
                    print("encrypting...")

        elif(selection=="2"):
            if(backend.loadedKey==None):
                ln(40)
                uiHeader()
                print("error: encryption key not found! please load the corisponding key to the text to continue.")
                input("press enter to continue")
            else:
                ln(40)
                uiHeader()
                print("please enter text to be decrypted:")
                text=input()
                print("decrypting...")
                start=time.time()
                decryptedText=backend.decrypt(text)
                elapsed=time.time()-start
                ln(40)
                if(decryptedText[0]):
                    uiHeader()
                    print("decryption successful")
                    print("finished in "+str(elapsed)+" second(s)")
                    print("here is your decrypted text:{"+decryptedText[1]+"}")
                    ln()
                    input("press enter to continue")
                else:
                    uiHeader()
                    print("error: unsupported character {"+encryptedText[1]+"} in text! check text for the unsuported character. a complete list of supported characters can be found in the information menu.")
                    input("press enter to continue")
        elif(selection=="3"):
            ln(40)
            uiHeader()
            print("are you sure you want to load a key?")
            print("this will replace any currently loaded key.")
            decision=input("(y/n)")
            if(decision=="y"):
                ln(40)
                uiHeader()
                print("please enter key:")
                try:
                    text=input()
                    start=time.time()
                    backend.setKey(backend.loadKey(text))
                    elapsed=time.time()-start
                    print("loading key...")
                    ln(40)
                    uiHeader()
                    print("key successfully loaded")
                    print("finished in "+str(elapsed)+" second(s)")
                    input("press enter to continue")
                except:
                    print("loading key...")
                    ln(40)
                    uiHeader()
                    print("error: key failed to load. please check key and try again")
                    input("press enter to continue")
        elif(selection=="4"):
            ln(40)
            uiHeader()
            print("are you sure you want to generate a new key?")
            print("this will replace any currently loaded key.")
            decision=input("(y/n)")
            if(decision=="y"):
            
            
                ln(40)
                uiHeader()
                print("please input key complexity value:")
                complexity=input()
                print("generating key...")
                
                try:
                    complexity=int(complexity)
                    start=time.time()
                    backend.setKey(backend.generateKey(complexity))
                    elapsed=time.time()-start
                    ln(40)
                    uiHeader()
                    print("key successfully generated")
                    print("finished in "+str(elapsed)+" second(s)")
                    input("press enter to continue")
                    
                    
                    
                except:
                    ln(40)
                    print("error: key generation error. please make sure key complexity value is a positive integer and try again")
                    input("press enter to continue")


        elif(selection=="5"):
            ln(40)
            uiHeader()
            if(backend.loadedKey==None):
                
                print("error: encryption key not found! please load or generate a key to continue.")
                input("press enter to continue")
            else:
                start=time.time()
                compiledKey=backend.exportKey(backend.loadedKey)
                elapsed=time.time()-start
                print("key:{"+compiledKey+"}")
                ln()
                print("finished in "+str(elapsed)+" second(s)")
                input("press enter to continue")
                
                


        elif(selection=="6"):
            ln(40)
            uiHeader()
            print("Cactus encrypt is a felxible encryption algorithm and associted program I wrote in my free time because I was bored. Though I tried to make it easy to use, it still has some complexity, so I will try to clear that up here. Cactus encrypt is very strict with its key formatting. keys must be entered exactly the same as they are exported (all the stuff between the curly braces and no extra). Also, it uses a nonstandard character set and errors out if it detects an unsupported character. To prevent confusion I have listed out all of the supported characters here: {qwertyuiopasdfghjklzxcvbnm ;1234567890-=!#$%^&*{}()_+QWERTYUIOPASDFGHJKL:ZXCBVNM<>?.,[]'\"\\~|@}. Please note that though curly braces are supported characters they are also used to denote the start and end of output text feilds, so be careful when copying. additionally spaces are also supported characters, so keep that in mind. have fun with cactus encrypt! -redcactus5")
            input("press enter to continue")
            
        else:
            ln(40)
            uiHeader()
            print("error: input error, selection not found")
            input("press enter to continue")




#incredibly important function call
#userInterface()
            
