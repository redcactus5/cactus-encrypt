#imports
import time
import crypto_engine
from os import system, name


#TODO: remember to fix the version string for final release

PRGVERSION="V2.0 alpha 1: active development"
#"V2.0 beta: debug build 1"
#"V2.0 RC1"
#"V2.0"

'''
TO DO:
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


    



#handy newline function. not neccesary just nice to have
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
def uiHeader():
    global PRGVERSION
    print("cactus encrypt "+PRGVERSION+" by redcacus5")
    ln()
    print("checking system state...")
    ln()
    if(not(crypto_engine.isKeyLoaded) or not(crypto_engine.isCharSetLoaded)):
        print("system not ready. detected problems:")
        if(crypto_engine.isKeyLoaded):
            print("warning, no key in memory! please generate or load a key")
        if(crypto_engine.isCharSetLoaded):
            print("warning, no character set in memory! please load a character set")
    else:
        print("no errors detected. system ready")
    ln(3)
 


def multipleChoiceScreen(message:str, optionsMessage:tuple, options:tuple, accuracy:int):
    while True:
        clear()
        uiHeader()
        ln()
        print(message)
        ln()
        for m in optionsMessage:
            print(m)
        ln()
        selection=input()
        if(len(selection)>=1):
            if(accuracy>len(selection)):
                accuracy=len(selection)
            for i in range(len(options)):
                if(selection[slice(0,accuracy-1)]==options[i]):
                    return i
        clear()
        uiHeader()
        print("syntax error: bad input. please enter one of the provided options")
        ln(2)
        input("press enter to continue")




            

def booleanQuestionScreen(message:str):
    choice=multipleChoiceScreen(message,("(y)es","(n)o"),("y","n"),1)
    if(choice==1):
        return True
    return False


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

#remember to check for presence of thne things you need

def loadCharSet():
    pass

def loadCharSetFromTXT():
    pass

def scrambleCharSet():
    pass

def exportCharSetToTXT():
    pass

def exportCharSet():
    pass

def ecryptTXT():
    pass

def decryptTXT():
    pass

def loadKeyFromTXT():
    pass

def exportKeyToTXT():
    pass

def encryptTerminalInput():
    pass

def decryptTerminalInput():
    pass

def loadKeyFromTerminal():
    pass

def exportKeyToTerminal():
    pass

def generateKey():
    pass

def helpScreen():
    pass #just print readme.txt


#todo:
def CLI_V2():
    pass



def startup():
    try:
        characterSetFile = open("default_charset.txt","r")
        charSet=characterSetFile.read()
        charSet.replace("\n","").replace("\t"," ").replace("\r"," ").replace("\f"," ")
        charSet=list(charSet)
        crypto_engine.setCharSet(tuple(charSet))

    except:
        pass

    try:
        keyFile = open("default_key.txt","r")
        key=keyFile.read()
        key.replace("\n","").replace("\t"," ").replace("\r"," ").replace("\f"," ")
        crypto_engine.setKey(crypto_engine.loadKey(key))
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
            if(crypto_engine.loadedKey==None):
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
                encryptedText=crypto_engine.encrypt(text)
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
            if(crypto_engine.loadedKey==None):
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
                decryptedText=crypto_engine.decrypt(text)
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
                    crypto_engine.setKey(crypto_engine.loadKey(text))
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
                    crypto_engine.setKey(crypto_engine.generateKey(complexity))
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
            if(crypto_engine.loadedKey==None):
                
                print("error: encryption key not found! please load or generate a key to continue.")
                input("press enter to continue")
            else:
                start=time.time()
                compiledKey=crypto_engine.exportKey(crypto_engine.loadedKey)
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
            
