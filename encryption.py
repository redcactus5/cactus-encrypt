
from random import randint


CHARACTERS=("q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"," ",";","1","2","3","4","5","6","7","8","9","0","-","=","!","#","$","%","^","&","*","(",")","_","+","Q","W","E","R","T","Y","U","I","O","P","A","S","D","F","G","H","J","K","L",":","Z","X","C","B","V","N","M","<",">","?",".",",","[","]","/","'")
CHARACTERCOUNT=len(CHARACTERS)

loadedKey=None

def convertToNum(text):

    textList=list(text)
    numList=[]
    for character in textList:
        numList.append(CHARACTERS.index(character))
    return numList

def convertToText(numlist):

    text=""
    for num in numlist:
        text+=CHARACTERS[num]
    return text



def getNumberRange(start,end):
    temp=[]
    for i in range(start,end):
        temp.append(i)
    return temp

def ln(*number):
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
    
    





class Rotor:
    def __init__(self, wiring, pos):
        self.pos=pos
        self.wiring=wiring
    
    def advance(self):
        self.pos+=1
        if(self.pos>len(self.wiring)-1):
            self.pos-=len(self.wiring)
            return True
        return False
    
    def encodeValue(self,number):
        searchNumber=number+self.pos
        while(searchNumber>len(self.wiring)-1):
            searchNumber-=len(self.wiring)
        return self.wiring[searchNumber]
    
    def decodeValue(self, number):
        numIndex=self.wiring.index(number)-self.pos
        while(numIndex<0):
            numIndex+=len(self.wiring)
        
        return numIndex
    






def generateKey(rotorCount):
    #key structure [rotor keys],[rotor starts],[initial and final static cyphers]
    key=[rotorCount]
    for rotor in range(rotorCount):
        #generate the wiring for one rotor
        catalog=getNumberRange(0,CHARACTERCOUNT)
        rotorWiring=[]
        for character in range(len(catalog)):
            rotorWiring.append(catalog.pop(randint(0,len(catalog)-1)))
        key.append(rotorWiring)
    #gnerate the start positions of the rotors
    for i in range(rotorCount):
        key.append(randint(0,CHARACTERCOUNT))
    
    #generate the wiring for the initial and final static cyphers
    for cypher in range(2):
        
        catalog=getNumberRange(0,CHARACTERCOUNT)
        rotorWiring=[]
        for character in range(len(catalog)):
            rotorWiring.append(catalog.pop(randint(0,len(catalog)-1)))
        key.append(rotorWiring)
    return key

    

def exportKey(key):
    
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
    
         


    


    
def loadKey(keyString):
    #seperate the keystring into a list at the terminator strings
    keyList=keyString.rsplit(" | ")
    #convert the rotor count into a string at put it in its place in the decoded list
    key=[int(keyList[0])]
    #decode the rotors
    for rotor in range(key[0]):
        #decode the wiring of a rotor
        #split the string into list at the commas
        key.append(keyList[rotor+1].rsplit(","))
        for character in range(len(key[rotor+1])):
            
            key[rotor+1][character]=int(key[rotor+1][character])
            
    
    
    for rotor in range(key[0]):
        key.append(int(keyList[rotor+1+key[0]]))
        
    for cypher in range(2):
        #compile the wiring of a cypher
        key.append(keyList[cypher+1+(key[0]*2)].rsplit(","))
        for character in range(len(key[cypher+1+(key[0]*2)])):
            key[cypher+1+(key[0]*2)][character]=int(key[cypher+1+(key[0]*2)][character])
    
   

    return key
    


def advanceRotors(rotorList):
    rollover=True
    for rotor in rotorList:
        if(rollover):
            rollover=rotor.advance()
        else:
            break
        
    


def encrypt(text):
    #check for character compatablility
    for character in text:
        if(not character in CHARACTERS):
            return (False, character)
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
    return convertToText(encryptedNumList)
    
def decrypt(text):
    #check for character compatability
    for character in text:
        if(not character in CHARACTERS):
            return (False, character)
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
    return convertToText(decryptedNumList)




    

  





    





#to decrypt just trace the path back in reverse
    

