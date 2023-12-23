from random import randint



#special thank you to the devs of Nuikita for making this project possible






'''
#converts of string of characters into a list of their corisponding number values as 
defined in the characters tuple (the index of the character is its number)
'''
def convertToNum(text:str, characterSet:tuple):

    textList=list(text)

    numList=[]
    for character in textList:
        numList.append(characterSet.index(character))
    return numList


'''
converts a list of number into their corisponding text characters in the characterSet tuple 
(what character is at that index). returns them all as a concatinated string
'''
def convertToText(numlist:list, characterSet:tuple):

    text=""
    
    for num in numlist:
        text+=characterSet[num]
    return text








# the rotor class. used for both the rotors and the initial and final cyphers. the path a value takes through the rotors encrypts it
class Rotor:
    def __init__(self, wiring:list, pos:int):
        self.pos=pos
        self.wiring=wiring
    #advance the rotor fowards by 1
    def advance(self):#self explanitory logic
        self.pos+=1
        if(self.pos>len(self.wiring)-1):
            self.pos-=len(self.wiring)
            return True
        return False
    
    #self explanitory name
    def encodeValue(self,number:int):
        searchNumber=number+self.pos#calculate number to get
        while(searchNumber>len(self.wiring)-1):#logic to prevent index errors and enforce rollover
            searchNumber-=len(self.wiring)
        return self.wiring[searchNumber]#return final number
    
        #self explanitory name
    def decodeValue(self, number:int):#logic of encode value in reverse
        numIndex=self.wiring.index(number)-self.pos
        while(numIndex<0):
            numIndex+=len(self.wiring)
        
        return numIndex
    





#randomly generates a new key with a user provided compelxity value (how many rotors to use)
def generateKey(rotorCount:int, characterSet:tuple):
    #key structure [rotor keys],[rotor starts],[initial and final static cyphers]
    key=[rotorCount]
    for rotor in range(rotorCount):
        #generate the wiring for one rotor
        catalog=list(range(0, len(characterSet)))
        rotorWiring=[]
        for character in range(len(catalog)):
            rotorWiring.append(catalog.pop(randint(0,len(catalog)-1)))
        key.append(rotorWiring)
    #gnerate the start positions of the rotors
    for i in range(rotorCount):
        key.append(randint(0,len(characterSet)))
    
    #generate the wiring for the initial and final static cyphers
    for cypher in range(2):
        
        catalog=list(range(0, len(characterSet)))
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
def encrypt(text:str, characterSet:tuple, encryptionKey:list):
    #check for character compatablility
    for character in text:
        if(not character in characterSet):
            return (False,character)
    #initialize variables and the two static cyphers
    rotors=[]
    cyphers=(Rotor(encryptionKey[len(encryptionKey)-2],0),Rotor(encryptionKey[len(encryptionKey)-1],0))
    toBeEncrypted=convertToNum(text)
    encryptedNumList=[]
    #generate number of rotor objects specified in the key from the wiring provided in the key
    for i in range(encryptionKey[0]):
        rotors.append(Rotor(encryptionKey[i+1],encryptionKey[encryptionKey[0]+i+1]))
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
def decrypt(text, characterSet:tuple, encryptionKey:list):
    #check for character compatability
    for character in text:
        if(not character in characterSet):
            return (False,character)
    #initialize variables and the two static cyphers
    rotors=[]
    cyphers=(Rotor(encryptionKey[len(encryptionKey)-2],0),Rotor(encryptionKey[len(encryptionKey)-1],0))
    toBeDecrypted=convertToNum(text)
    decryptedNumList=[]
    #generate number of rotor objects specified in the key from the wiring provided in the key
    for i in range(encryptionKey[0]):
        rotors.append(Rotor(encryptionKey[i+1],encryptionKey[encryptionKey[0]+i+1]))
    
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


