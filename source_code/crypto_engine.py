#cactus encrypt is a simple cli text encryption program written in python that implements the cactus cipher algorithm
#Copyright 2023,2024 Redcactus5
'''
This file is part of Cactus Encrypt.

Cactus Encrypt is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Cactus Encrypt is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Cactus Encrypt. If not, see <https://www.gnu.org/licenses/>. 
'''

#this program is free, open source software released under the GNU General Public License version 3.0 or later version (GPL-3.0-or-later)

from random import randint



#special thank you to the devs of Nuikita for making this project possible


#i completely forget how must of the logic and math here work, so abandon all hope ye who enter here
#cut me some slack, this started off as a simple small personal project i made in highschool. i never expected for it to get this big



#next error is error 39




'''
#converts of string of characters into a list of their corresponding number values as 
defined in the characters tuple (the index of the character is its number)
'''
def convertToNum(text:str, characterSet:tuple):

    textList=list(text)
    numList=[]

    for character in textList:
        numList.append(characterSet.index(character))

    return numList



'''
converts a list of number into their corresponding text characters in the characterSet tuple 
(what character is at that index). returns them all as a concatenated string
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
        #the wiring list used for encryption
        self.encodingWiring=wiring
        #the wiring list used for decryption. it stores the index where a number in encoding wiring is found at the index of the number itself.
        self.decodingWiring = [0] * len(wiring)

        #precompute the index values and populate decoding wiring with them
        for i in range(len(wiring)):
            self.decodingWiring[wiring[i]] = i


    #advance the rotor forwards by 1
    def advance(self):#self explanatory logic
        self.pos+=1
        if(self.pos>len(self.encodingWiring)-1):
            self.pos-=len(self.encodingWiring)
            return True
        return False
    
    #self explanitory name
    def encodeValue(self,number:int):
        searchNumber=number+self.pos#calculate number to get
        while(searchNumber>len(self.encodingWiring)-1):#logic to prevent index errors and enforce rollover
            searchNumber-=len(self.encodingWiring)
        return self.encodingWiring[searchNumber]#return final number
    
     #self explanitory name
    def decodeValue(self, number: int):#basically the same type of logic as encode value
        numIndex = self.decodingWiring[number] - self.pos #get the index of number and adjust it for the rotor position
        while numIndex < 0:#adjust back up if we roll over
            numIndex += len(self.decodingWiring)
        return numIndex#return final number
    







#randomly generates a new key with a user provided complexity value (how many rotors to use)
def generateKey(rotorCount:int, characterSet:tuple):
    #key structure [rotor keys],[rotor starts],[initial and final static cyphers]
    key=[rotorCount]#start off key
    #generate the requested number of rotors
    for rotor in range(rotorCount):
        #generate the wiring for one rotor

        #create a list of all the indexes of the characters in the character set
        catalog=list(range(0, len(characterSet)))
        #create a variable to store the wiring for one rotor. the decode wiring is generated in the rotor constructor
        rotorWiring=[]
        #generate the random wiring by popping a random character index from catalog and appending it to rotor wiring
        for character in range(len(catalog)):
            rotorWiring.append(catalog.pop(randint(0,len(catalog)-1)))
        #add the completed wiring for this rotor to the key
        key.append(rotorWiring)
    #generate the start positions of the rotors
    for i in range(rotorCount):#generates one position for each of the rotors
        #come up with a random starting position(0-length) for the rotor and append it to the key
        key.append(randint(0,len(characterSet)-1))#used to be a huge fencepost bug here, but now 
    
    #generate the wiring for the initial and final static cyphers
    for cypher in range(2):#the exact same as generating the rotor wiring, as it literally is just two rotors that never advance (possibly due to their incompetence)
        
        catalog=list(range(0, len(characterSet)))
        rotorWiring=[]
        for character in range(len(catalog)):
            rotorWiring.append(catalog.pop(randint(0,len(catalog)-1)))
        key.append(rotorWiring)
    return key



#compiles the string argument into a key
def exportKey(key:list):
    #converts a key list into a string that can be loaded by the load key function
    #pipes are used to separate key sections
    keyString=str(key[0])+" | "
    #compile the rotor wirings into importable strings
    for rotor in range(key[0]):#key 0 is the number of rotors in the key
        #compile the wiring of a rotor
        for character in range(len(key[rotor+1])):#rotors are all same length so this works
            #add the character to the key string
            keyString+=str(key[rotor+1][character])
            #add a comma too unless it is the final character
            if(character<len(key[rotor+1])-1):
                keyString+=","
        #add terminator pipe
        keyString+=" | "
    #compile the rotor start positions
    for rotor in range((key[0])):#rotor count is stored in key 0
        keyString+=str(key[rotor+1+key[0]])+" | "#add the position plus a terminating pipe
    #compile the starting and ending static cyphers 
    for cypher in range(2):#same as the normal rotors
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


#loads the encryption key from the string argument and returns the key
def loadKey(keyString:str,characterSet:tuple):

    #the key goes through a series of checks as it is loaded to make sure it is readable

    characterSetLen=len(characterSet)
 
    #integrity check 0 (has part separation characters)
    if(not (" | " in keyString)):
        return (False, "input error: (error 39) integrity check 0 failed; could not find separator 1. given key data is \ninvalid and possibly corrupted. please check the key for errors then try again.")
    

    #separate the keystring into a list at the terminator strings
    keyList=keyString.split(" | ")


    #integrity check 1 (has at least the minimum number of parts)
    if(len(keyList)<5):
        return (False, "input error: (error 40) integrity check 1 failed; key data is incomplete. given key data is \ninvalid and possibly corrupted. please check the key for errors then try again.")


    #integrity check 2 (has a numeric part count)
    if(not keyList[0].isnumeric()):
        return (False, "input error: (error 41) integrity check 2 failed; key data has invalid complexity value. given key \ndata is invalid and possibly corrupted. please check the key for errors then try again.")


    #convert the rotor count into a int and put it in its place in the decoded list
    key=[int(keyList[0])]
 
    #integrity check 3 (the part count is greater than zero)
    if(key[0]<1):
        return (False, "input error: (error 42) integrity check 3 failed; key data has invalid complexity value. given key \ndata is invalid and possibly corrupted. please check the key for errors then try again.")
   
    
    #integrity check 4 (the length of the key is 3 plus the part count times 2 or 3+(C*2) )
    if(len(keyList)!=(key[0]*2)+3):
        #(1 part count + C wiring lists + C start positions+ 1 initial cypher + 1 final cypher))
        return (False, "input error: (error 43) integrity check 4 failed; key data is improperly partitioned. given key data \nis invalid and possibly corrupted. please check the key for errors then try again.")


    #decode the rotors
    for rotor in range(key[0]):#key 0 is the number of rotors
        #decode the wiring of a rotor


        #integrity check 5 (wiring is a properly formatted list)
        if(not ("," in keyList[rotor+1])):
            return (False, "input error: (error 44) integrity check 5 failed; could not find separator 2. given key data is \ninvalid and possibly corrupted. please check the key for errors then try again.")


        #split the string into list at the commas and put it in key
        key.append(keyList[rotor+1].split(","))


        #integrity check 6 (wiring has the same number of characters as the current character set)
        if(not(len(key[rotor+1])==characterSetLen)):
            return (False, "input error: (error 45) integrity check 6 failed; key data incompatible with loaded character \nset and may be corrupted. given key data is invalid and possibly corrupted. please \ncheck the key for errors then try again.")


        #integerize rotor wiring in key
        for character in range(len(key[rotor+1])):

            #integrity check 7 (all indexes are numeric)
            if(not (key[rotor+1][character].isnumeric())):
                return (False, "input error: (error 46) integrity check 7 failed; invalid values found in key data. given key data\nis invalid and possibly corrupted. please check the key for \nerrors then try again.")
            

            key[rotor+1][character]=int(key[rotor+1][character])

            #integrity check 8 (all indexes are within bounds)
            if(not(key[rotor+1][character]>=0 and key[rotor+1][character]<characterSetLen)):
                return (False, "input error: (error 47) integrity check 8 failed; out of range values found in key data. \ngiven key data is invalid and possibly corrupted. please check the key for \nerrors then try again.")



    #append the rotor starting positions to the key
    for rotor in range(key[0]):

        #integrity check 9 (starting positions are numeric)
        if(not (keyList[rotor+1+key[0]].isnumeric())):
            return (False, "input error: (error 48) integrity check 9 failed; invalid values found in key data. given key \ndata is invalid and possibly corrupted. please check the key for \nerrors then try again.")
        
        key.append(int(keyList[rotor+1+key[0]]))

        #integrity check 10 (starting positions are within bounds)
        if(not ((key[rotor+1+key[0]]>=0) and (key[rotor+1+key[0]]<characterSetLen))):
            return (False, "input error: (error 49) integrity check 10 failed; out of range values found in key data. given \nkey data is invalid and possibly corrupted. please check the key \nfor errors then try again.")
        


    
    #for both the input and output static cypher
    for cypher in range(2):#same as rotor compilation
        #compile the wiring of a cypher
   
        #integrity check 11 (cypher is a properly formatted list)
        if(not ("," in keyList[cypher+1+(key[0]*2)])):
            return (False, "input error: (error 50) integrity check 11 failed; could not find separator 3. given key data \nis invalid and possibly corrupted. please check the key for \nerrors then try again.")
        
        #take the string of the cypher wiring and split it into a list of strings, then add it to the end of the key
        key.append(keyList[cypher+1+(key[0]*2)].split(","))

        #integrity check 12 (cypher has the same number of characters as the current character set)
        if(not(len(key[cypher+1+(key[0]*2)])==characterSetLen)):
            return (False, "input error: (error 51) integrity check 12 failed; key data is incompatible with currently loaded \ncharacter set and may be corrupted. given key data is invalid and possibly corrupted. \nplease check the key for errors then try again.")

        #convert these strings into integers
        for character in range(len(key[cypher+1+(key[0]*2)])):

            #integrity check 13 (all indexes are numeric)
            if(not (key[cypher+1+(key[0]*2)][character].isnumeric())):
                return (False, "input error: (error 52) integrity check 13 failed; invalid values found in key data. given key \ndata is invalid and possibly corrupted. please check the key for \nerrors then try again.")

            key[cypher+1+(key[0]*2)][character]=int(key[cypher+1+(key[0]*2)][character])

            #integrity check 14 (all indexes are within bounds)
            if(not(key[cypher+1+(key[0]*2)][character]>=0 and key[cypher+1+(key[0]*2)][character]<characterSetLen)):
                return (False, "input error: (error 53) integrity check 14 failed; out of range values found in key data. \ngiven key data is invalid and possibly corrupted. please check the key for errors then \ntry again.")
    
   
    #integrity check 15 (check to make sure what should be a rotor is in the right spot and a list)
    verificationRotorCount=0
    for check in range(key[0]):
        if(type(key[check+1])!=list):
            return (False, "input error: (error 54) integrity check 15 failed; key data is improperly formatted. given key \ndata is invalid and possibly corrupted. please check the key for errors then \ntry again.")
        verificationRotorCount+=1
    

    
    #integrity check 16 (check to make sure what should be a start position is in the right spot and a list)
    verificationStartPosCount=0
    for check in range(key[0]):
        if(type(key[key[0]+check+1])!=int):
            return (False, "input error: (error 55) integrity check 16 failed; key data is improperly formatted. given key \ndata is invalid and possibly corrupted. please check the key for errors then \ntry again.")
        verificationStartPosCount+=1


    #integrity check 17 (check to make sure what should be a cypher is in the right spot and a list)
    verificationCypherCount=0
    for check in range(2):
        if(type((key[0]*2)+check+1)!=list):
            return (False, "input error: (error 56) integrity check 17 failed; key data is improperly formatted. given key \ndata is invalid and possibly corrupted. please check the key for errors then \ntry again.")
        verificationCypherCount+=1
    
    #integrity check 18 (check to make sure what we counted adds up to the whole key length)
    if(1+verificationRotorCount+verificationStartPosCount+verificationCypherCount!=len(key)):
        (False, "input error: (error 57) integrity check 18 failed; key data is improperly partitioned. given key data is \ninvalid and possibly corrupted. please check the key for errors then \ntry again.")


    return (True, key)
    





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
    #check for character compatibility's
    for character in list(text):
        if(not character in characterSet):
            return (False,str(character))
    #initialize variables and the two static cyphers
    rotors=[]
    cyphers=(Rotor(encryptionKey[len(encryptionKey)-2],0),Rotor(encryptionKey[len(encryptionKey)-1],0))
    toBeEncrypted=convertToNum(text,characterSet)
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
    return (True,convertToText(encryptedNumList,characterSet))
    


#I hate documenting but I want this code to be maintainable so its a necessary evil


#decrypts string argument. returns a tuple of either success and the decrypted string or failure and the problem character
def decrypt(text:str, characterSet:tuple, encryptionKey:list):
    #check for character compatibility
    for character in list(text):
        if(not character in characterSet):
            return (False,str(character))
    #initialize variables and the two static cyphers
    rotors=[]
    cyphers=(Rotor(encryptionKey[len(encryptionKey)-2],0),Rotor(encryptionKey[len(encryptionKey)-1],0))
    toBeDecrypted=convertToNum(text,characterSet)
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
    return (True,convertToText(decryptedNumList,characterSet))


