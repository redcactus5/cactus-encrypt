
from random import randint
import time



#list of all suported characters
CHARACTERS=("q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"," ",";","1","2","3","4","5","6","7","8","9","0","-","=","!","#","$","%","^","&","*","(",")","_","+","Q","W","E","R","T","Y","U","I","O","P","A","S","D","F","G","H","J","K","L",":","Z","X","C","B","V","N","M","<",">","?",".",",","[","]","/","\'","\"","\\","~")

#stores the currently loaded key
loadedKey=None




'''
#converts of string of characters into a list of their corisponding number values as 
defined in the characters tuple (the index of the character is its number)
'''
def convertToNum(text:str):

    textList=list(text)

    numList=[]
    for character in textList:
        numList.append(CHARACTERS.index(character))
    return numList


'''
converts a list of number into their corisponding text characters in the CHARACTERS tuple 
(what character is at that index). returns them all as a concatinated string
'''
def convertToText(numlist:list):

    text=""
    
    for num in numlist:
        text+=CHARACTERS[num]
    return text








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
    
    




# the rotor class. used for both the rotors and the initial and final cyphers. the path a value takes through the rotors encrypts it
class Rotor:
    def __init__(self, wiring:list, pos:int):
        self.pos=pos
        self.wiring=wiring
    #advance the rotor fowards by 1
    def advance(self):
        self.pos+=1
        if(self.pos>len(self.wiring)-1):
            self.pos-=len(self.wiring)
            return True
        return False
    
    def encodeValue(self,number:int):
        searchNumber=number+self.pos
        while(searchNumber>len(self.wiring)-1):
            searchNumber-=len(self.wiring)
        return self.wiring[searchNumber]
    
    def decodeValue(self, number:int):
        numIndex=self.wiring.index(number)-self.pos
        while(numIndex<0):
            numIndex+=len(self.wiring)
        
        return numIndex
    





#randomly generates a new key with a user provided compelxity value (how many rotors to use)
def generateKey(rotorCount:int):
    #key structure [rotor keys],[rotor starts],[initial and final static cyphers]
    key=[rotorCount]
    for rotor in range(rotorCount):
        #generate the wiring for one rotor
        catalog=list(range(0, len(CHARACTERS)))
        rotorWiring=[]
        for character in range(len(catalog)):
            rotorWiring.append(catalog.pop(randint(0,len(catalog)-1)))
        key.append(rotorWiring)
    #gnerate the start positions of the rotors
    for i in range(rotorCount):
        key.append(randint(0,len(CHARACTERS)))
    
    #generate the wiring for the initial and final static cyphers
    for cypher in range(2):
        
        catalog=list(range(0, len(CHARACTERS)))
        rotorWiring=[]
        for character in range(len(catalog)):
            rotorWiring.append(catalog.pop(randint(0,len(catalog)-1)))
        key.append(rotorWiring)
    return key

    
#compiles the string argument into a key
def exportKey(key:list):
    
    keyString=str(key[0])+" | "
    #compile the rotor wirings into importable strings
    for rotor in range(key[0]):
        #compile the wiring of a rotor
        for character in range(len(key[rotor+1])):
            keyString+=str(key[rotor+1][character])
            #add a comma unless it is the final character
            if(character<len(key[rotor+1])-1):
                keyString+=","
        #add terminator
        keyString+=" | "
    #compile the rotor start positions
    for rotor in range((key[0])):
        keyString+=str(key[rotor+1+key[0]])+" | "
    #compile the starting and ending static cyphers 
    for cypher in range(2):
        #compile the wiring of a cypher
        for character in range(len(key[cypher+1+(key[0]*2)])):
            keyString+=str(key[cypher+1+(key[0]*2)][character])
            #add a comma unless it is the final character
            if(character<len(key[cypher+1+(key[0]*2)])-1):
                keyString+=","
        #add terminator if not the last one
        if(cypher<1):
            keyString+=" | "
    
    return keyString
    
         


#red was here


#loads the encyption key from the string argument
def loadKey(keyString:str):
    #seperate the keystring into a list at the terminator strings
    keyList=keyString.split(" | ")
    #convert the rotor count into a string at put it in its place in the decoded list
    key=[int(keyList[0])]
    #decode the rotors
    for rotor in range(key[0]):
        #decode the wiring of a rotor
        #split the string into list at the commas
        key.append(keyList[rotor+1].split(","))
        #integerize keys
        for character in range(len(key[rotor+1])):
            
            key[rotor+1][character]=int(key[rotor+1][character])
            
    
    #append the rotor wirings to the key
    for rotor in range(key[0]):
        key.append(int(keyList[rotor+1+key[0]]))
        
    for cypher in range(2):
        #compile the wiring of a cypher
        key.append(keyList[cypher+1+(key[0]*2)].split(","))
        for character in range(len(key[cypher+1+(key[0]*2)])):
            key[cypher+1+(key[0]*2)][character]=int(key[cypher+1+(key[0]*2)][character])
    
   

    return key
    

#function that advances a list of rotors given as the argument using mechanical counter logic. critical to the program's functionality. 
def advanceRotors(rotorList:list):
    rollover=True
    for rotor in rotorList:
        if(rollover):
            rollover=rotor.advance()
        else:
            break
        
    

#encrypts string argument. returns a tuple of success and encrypted string or failure and the problem character
def encrypt(text:str):
    #check for character compatablility
    for character in text:
        if(not character in CHARACTERS):
            return (False,character)
    #initialize variables and the two static cyphers
    rotors=[]
    cyphers=(Rotor(loadedKey[len(loadedKey)-2],0),Rotor(loadedKey[len(loadedKey)-1],0))
    toBeEncrypted=convertToNum(text)
    encryptedNumList=[]
    #generate number of rotor objects specified in the key from the wiring provided in the key
    for i in range(loadedKey[0]):
        rotors.append(Rotor(loadedKey[i+1],loadedKey[loadedKey[0]+i+1]))
    #do the actual encryption
    for character in toBeEncrypted:
        #put text through initial cypher
        temp=cyphers[0].encodeValue(character)
        #put text through rotors
        for rotor in rotors:
            temp=rotor.encodeValue(temp)
        #put text through the final cypher
        temp=cyphers[1].encodeValue(temp)
        #add encrypted character to list of encrypted characters
        encryptedNumList.append(temp)
        #advance the rotors
        advanceRotors(rotors)
    return (True,convertToText(encryptedNumList))
    


#I hate documenting but I want this code to be maintainable so its a neccesary evil


#decrypts string argument. returns a tuple of either success and the decrypted string or failure and the problem character
def decrypt(text):
    #check for character compatability
    for character in text:
        if(not character in CHARACTERS):
            return (False,character)
    #initialize variables and the two static cyphers
    rotors=[]
    cyphers=(Rotor(loadedKey[len(loadedKey)-2],0),Rotor(loadedKey[len(loadedKey)-1],0))
    toBeDecrypted=convertToNum(text)
    decryptedNumList=[]
    #generate number of rotor objects specified in the key from the wiring provided in the key
    for i in range(loadedKey[0]):
        rotors.append(Rotor(loadedKey[i+1],loadedKey[loadedKey[0]+i+1]))
    
    #do the actual decryption
    for character in toBeDecrypted:
        #put text through final cypher
        temp=cyphers[1].decodeValue(character)
        #put text through the rotors
        for rotor in range(len(rotors)-1,-1,-1):
            temp=rotors[rotor].decodeValue(temp)
        #put text through initial cypher
        temp=cyphers[0].decodeValue(temp)
        #add decrypted character to decrypted characters list
        decryptedNumList.append(temp)
        #advance the rotors by one
        advanceRotors(rotors)
    #convert the decrypted list into a string of plain text and return it
    return (True,convertToText(decryptedNumList))




    


#ui header function to save time
def uiHeader():
    print("cactus encrypt v1.1 release canidate 1 by redcacus5")
    ln()
    if(loadedKey==None):
        print("no key found!")
    else:
        print("ready")
    ln(3)
 


    
#who ya gunna call?

#CLI user interface
def userInterface():
    global loadedKey
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
            if(loadedKey==None):
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
                encryptedText=encrypt(text)
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
            if(loadedKey==None):
                ln(40)
                uiHeader()
                print("error: encryption key not found! please load the corisponding key to continue.")
                input("press enter to continue")
            else:
                ln(40)
                uiHeader()
                print("please enter text to be decrypted:")
                text=input()
                print("decrypting...")
                start=time.time()
                decryptedText=decrypt(text)
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
                    start=time.time()
                    loadedKey=loadKey(input())
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
                    loadedKey=generateKey(complexity)
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
            if(loadedKey==None):
                
                print("error: encryption key not found! please load or generate a key to continue.")
                input("press enter to continue")
            else:
                print("key:{"+exportKey(loadedKey)+"}")
                input("press enter to continue")
                
                


        elif(selection=="6"):
            ln(40)
            uiHeader()
            print("Cactus encrypt is a felxible encryption algorithm and associted program I wrote in my free time because I was bored. Though I tried to make it easy to use, it still has some complexity, so I will try to clear that up here. Cactus encrypt is very strict with its key formatting. keys must be entered exactly the same as they are exported (all the stuff between the curly braces and no extra). Also, it uses a nonstandard character set and errors out if it detects an unsupported character. To prevent confusion I have listed out all of the supported characters here: {qwertyuiopasdfghjklzxcvbnm ;1234567890-=!#$%^&*()_+QWERTYUIOPASDFGHJKL:ZXCBVNM<>?.,[]'\"\\~}. Please note that curly braces are not supported characters and are only used to denote the start and end of text feilds. pipe characters are only used in keys and are also not supported characters. on the contrary, spaces are supported characters, so keep that in mind. have fun with cactus encrypt! -redcactus5")
            input("press enter to continue")
            
        else:
            ln(40)
            uiHeader()
            print("error: input error, selection not found")
            input("press enter to continue")




#incredibly important function call
userInterface()