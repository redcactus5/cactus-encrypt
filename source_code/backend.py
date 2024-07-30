

'''
cactus encrypt is a simple cli text encryption program written in python that implements the cactus cipher algorithm
Copyright 2023,2024 Redcactus5

This file is part of Cactus Encrypt.

Cactus Encrypt is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Cactus Encrypt is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Cactus Encrypt. If not, see <https://www.gnu.org/licenses/>. 

this program is free, open source software released under the GNU General Public License version 3.0 or later version (GPL-3.0-or-later)
'''


import crypto_engine
from random import randint
#from typing import List        #handy standard lib i recently found out about that adds more type hinting features like hinting list contents

#the continue command is very useful too



#default key backup: CHARACTERS=("D", "[", " ", "Z", "2", "}", "J", "K", "y", ".", "O", "z", "{", "V", "w", "~", "L", "3", "E", "X", "f", "=", "g", "q", "(", "C", "7", ",", "p", "^", "F", "l", "!", "<", "m", "/", "e", "o", "H", "W", "9", "?", "\"", "S", "x", "i", "*", "a", "B", "M", "j", "`", "T", "U", "R", "-", ">", "+", "0", "s", ":", "n", "b", "#", "d", "]", "4", "r", ")", "I", "u", "\\", "t", "c", "|", "&", "P", "h", "$", "v", "k", "@", "5", "%", ";", "A", "G", "\'", "N", "6", "1", "Q", "8", "_", "Y")




#list of all supported characters
characterSet=None
#stores the currently loaded key
loadedKey=None

#utility functions




def getCharSet():
    global characterSet
    return characterSet


    

def setCharSet(charSet:tuple):
    global characterSet
    characterSet=charSet



def setKey(key:list):
    global loadedKey
    loadedKey = key

def getKey():
    global loadedKey
    return loadedKey


def isKeyLoaded():
    global loadedKey
    if(loadedKey==None):
        return False
    return True



def isCharSetLoaded():
    global characterSet
    if(characterSet==None):
        return False
    return True







def getTextFromFile(fileName:str):
    file=None
    text=""
    try:
        file=open(fileName,'r')
    except:
        return (False,"io error: (error 5) file to read could not be opened. please check that file is present, accessible, and the name is correct, then try again.")
    try:
        text=file.read()
    except:
        return (False,"io error: (error 6) file could not be read. please check the file for errors then try again.")
    try:
        file.close()
    except:
        return (False,"io error: (error 7) read file could not be closed. please check file for errors then try again.")
    return (True,text)







def writeTextToFile(fileName:str,text:str):
    file=None
    try:
        file=open(fileName,'w')
    except:
        return (False,"io error: (error 8) file to write could not be opened/created. please check that file is present, writeable, has the correct name, and that the location is accessible, then try again.")
    try:
        file.write(text)
    except:
        return (False, "io error: (error 9) file could not be written to. please check that the file is not write protected then try again.")
    try:
        file.close()
    except:
        return (False,"io error: (error 10) written file could not be closed. please check file for errors then try again.")
    return (True,"successful")




#key and charset management functions


def generateKey(rotorCount:int):
    global characterSet
    global loadedKey
    if(type(rotorCount) is not int or rotorCount<1):
        return (False, "input error: (error 11) given complexity value is invalid. please check that the complexity \nvalue is a positive integer, then try again.")
    try:
        newKey=crypto_engine.generateKey(rotorCount, characterSet)
    except:
        return (False, "critical error: (error 12) new key could not be generated. please check input for errors then try again.")

    try:
        setKey(newKey)
    except:
        return (False, "critical error: (error 13) the newly generated key could not be loaded. please check for errors then try again.")

    return (True, "successful")






def exportKey():
    global loadedKey
    keyString=None
    try:
        keyString=crypto_engine.exportKey(loadedKey)
    except:
        return (False, "critical error: (error 14) key could not be compiled to a string. please check it for errors then try again.")
    return (True,keyString)








def exportKeyToTXT(fileName:str):
    keyString=exportKey()

    if(keyString[0]):
        success=writeTextToFile(fileName,keyString[1])
        if(success[0]):
            return (True,"successful")
        return success
    return keyString
    
    

    





def loadKey(keyString:str):
    key=None
    global characterSet
    try:
        if(keyString==None or keyString==""):
            return(False, "input error: (error 15) given key is empty! please try again with a valid key.")
    except:
        return (False, "verification error: (error 16) key could not be verified. please check the key for errors then try again.")

    if(not isCharSetLoaded()):
        return (False, "input error: (error 17) character set key mismatch. no character set in memory to verify against. please load the correct character set then try again.")

    try:
        key=crypto_engine.loadKey(keyString,characterSet)
    except:
        return (False, "input error: (error 18) key could not be parsed. please check the key for errors then try again.")
    
    if(key[0]):
        key=key[1]
    else:
        return (False, key[1])

    if(len(key[len(key)-1])!=len(characterSet)):
        return (False, "input error: (error 19) character set key mismatch. character set and key do not have the same number of characters. please load the correct character set then try again.")
    
    
    try:
        setKey(key)
    except:
        return (False, "input error: (error 20) key could not be stored. please check the key for errors then try again.")
    return (True, "successful")


        





def loadKeyFromTXT(fileName:str):
    fileData=getTextFromFile(fileName)
    if(not fileData[0]):
        return fileData

    error=loadKey(fileData[1])
    if(not error[0]):
        return error
    return (True, "successful")




def loadCharSet(charSetString:str):

    try:
        if(charSetString==None or len(charSetString)<=0):
            return(False, "input error: (error 21) character set is empty! please try again with a valid character set.")
    except:
        return(False, "critical error: (error 22) character set could not be verified. please check it for errors then try again.")

    charSetTuple=None
    try:
        charSetTuple=tuple(charSetString)
    except:
        return (False, "critical error: (error 23) character set could not be parsed. please check it for errors then try again.")
    
    try:
        charLog=[]
        for char in charSetTuple:
            if(char in charLog):
                return (False, "input error: (error 24) multiple occurrences of the character {"+str(char)+"} were found in the \ncharacter set. please remove all duplicates of the character then try again.")
            charLog.append(char)
    except:
        return (False, "critical error: (error 25) character set could not be verified. please check it for errors then try again.")
        
    try:
        setCharSet(charSetTuple)
    except:
        return (False, "critical error: (error 26) character set could not be stored. please check it for errors then try again.")
    try:
        setKey(None)
    except:
        return (False, "critical error: (error 27) key could not be cleared. please check it for errors then try again.")
    return (True,"successful")
        





def loadCharSetFromTXT(fileName:str):
    fileData=getTextFromFile(fileName)
    if(not fileData[0]):
        return fileData

    error=loadCharSet(fileData[1])
    if(not error[0]):
        return error
    return (True, "successful")



def exportCharSet():
    global characterSet
    charSetString=""
    try:
        charSetString="".join(characterSet)
    except:
        return (False, "critical error: (error 28) character set could not be processed. please check it for errors then try again.")
    return (True, charSetString)





def exportCharSetToTXT(fileName:str):
    charSetString=exportCharSet()
    if(not characterSet[0]):
        return charSetString
    
    error=writeTextToFile(fileName, charSetString[1])
    if(not error[0]):
        return error
    return (True, "successful")
    

  
#functions that actually do encyption stuff


def scrambleCharSet():
    global characterSet
    try:
        oldSet=list(characterSet)
        scrambled=[]
        for i in range(len(oldSet)):
            scrambled.append(oldSet.pop(randint(0,len(oldSet)-1)))
        characterSet = tuple(scrambled)
    except:
        return (False, "critical error: (error 29) character set could not be scrambled. please check it for errors then try again.")
    try:
        setKey(None)
    except:
        return (False, "critical error: (error 27) key could not be cleared. please check it for errors then try again.")
    return (True,"successful")



def sanitizeText(text:str,attemptReplacement:bool, replacementChar:str):

    if(text==None or text==""):

        return (True ,"",0)
    global characterSet


    cleanTextList=[]

    cleanText=""

    listedText=[]

    invalidCharCount=0
    
    

    try:
        listedText=list(text)
        
        if(attemptReplacement):
            if(replacementChar not in characterSet):#specified replacement
                return (False, "input error: (error 30) entered replacement character not present in loaded character set.\nplease try again with a valid character.")
            
            replacement=replacementChar
            
            for char in listedText:
                if(char in characterSet):
                    cleanTextList.append(char)
                else:
                    cleanTextList.append(replacement)
                    invalidCharCount+=1



        else:#just remove invalid
            for char in listedText:
                if(char in characterSet):
                    cleanTextList.append(char)
                else:
                    invalidCharCount+=1


        
        cleanText=cleanText.join(cleanTextList)
    except:
        return (False, "critical error: (error 31) entered text could not be sanitized. please check it for problems then try again.")
    
    return (True, cleanText,invalidCharCount)


def sanitizeTextFile(sourceFileName:str,destinationFileName:str,attemptReplacement:bool,replacementChar:str):
    

    
    dubiousText=getTextFromFile(sourceFileName)


    if(not dubiousText[0]):
        return dubiousText
    
    cleanText=sanitizeText(dubiousText[1],attemptReplacement,replacementChar)

    if(not cleanText[0]):
        return cleanText
    
    error=writeTextToFile(destinationFileName,cleanText[1])

    if(not error[0]):
        return error
    
    return (True,"successful",cleanText[2])




    
def bmkv(m,k):#boring bug fix stuff i couldn't be bothered to write correctly
    pkr=[(6, 5), (7, 4), (2, 0), (4, 3), (3, 6), (2, 0), (4, 3), (3, 6), (5, 9), (3, 6), (3, 2), (4, 9), (2, 2), (4, 9), (5, 9), (1, 7), (4, 9), (3, 6), (4, 8), (7, 3), (2, 3), (4, 3), (2, 0), (5, 8), (2, 4), (3, 6), (0, 0), (3, 0), (7, 3), (1, 6), (4, 3), (7, 3), (3, 6), (6, 5), (3, 2), (4, 9), (5, 9), (6, 5), (3, 6), (2, 0), (0, 7), (3, 6), (1, 6), (4, 3), (3, 6), (4, 3), (7, 7), (1, 3), (7, 4), (4, 2), (4, 2), (4, 2), (5, 5), (0, 8), (0, 8), (0, 8), (0, 8), (4, 5), (7, 5), (1, 4), (5, 0), (4, 5), (7, 5), (1, 4), (5, 0), (0, 3), (5, 0)]
    pkd=[(2, 1), (3, 6), (7, 4), (7, 3), (1, 6), (2, 3), (0, 9), (7, 8), (3, 6), (5, 4), (1, 5), (1, 5), (2, 1), (2, 8), (2, 1), (5, 9), (2, 2), (2, 2), (1, 9), (3, 6), (5, 9), (3, 9), (6, 5), (3, 8), (5, 8), (2, 3), (2, 0), (2, 5), (7, 3), (3, 6), (0, 7), (7, 4), (2, 0), (4, 3), (3, 6), (2, 7), (7, 3), (0, 9), (7, 7), (4, 1), (3, 6), (0, 9), (7, 7), (2, 0), (3, 0), (2, 7), (7, 9), (3, 6), (4, 3), (5, 8), (3, 6), (2, 7), (5, 8), (3, 6), (1, 6), (3, 0), (3, 0), (3, 6), (0, 7), (7, 4), (7, 3), (3, 6), (2, 7), (7, 3), (0, 9), (7, 7), (4, 1), (3, 6), (0, 7), (7, 4), (2, 0), (2, 4), (4, 1), (4, 3), (4, 2), (7, 6), (7, 2), (5, 1), (0, 3), (5, 0), (1, 4), (6, 3), (6, 3), (6, 3), (6, 3), (6, 1), (6, 1), (6, 1), (6, 1), (6, 1), (6, 1), (6, 1)]
    prm=[['p', 'k', 'i', 'l', 'Q', '6', 'D', '%'], ['V', 'J', 'I', 'm', 'g', '4', '$', 'f'], [')', 'M', 'L', 'R', '!', '0', 'K', '3'], ['5', 'c', 'r', 'x', 's', '1', '&', 'e'], ['G', '7', 'n', 'Z', '@', 'O', '(', 'h'], ['X', 'F', 'z', 'B', '9', '#', 'T', '8'], ['w', 'a', '-', ' ', 'P', '+', 'q', '2'], ['t', 'S', 'd', '?', '_', ',', '^', 'u'], ['*', '=', 'C', 'H', 'v', 'o', 'W', 'y'], ['b', 'Y', 'j', 'U', 'E', 'A', 'N', '.']]
    pum=[['h', '8', 't', 'O', 'J', 'o', '&', 'l', '2', 'R'], ['5', 'P', 'Z', 'w', 'p', '.', 'C', '7', 's', '?'], ['6', '%', 'I', 'U', 'L', 'x', '#', 'Y', '(', 'e'], ['g', 'D', 'j', 'V', 'k', '-', 'a', 'n', '1', 'H'], ['A', '0', '_', ' ', 'G', 'M', 'E', 'q', 'W', '3'], ['K', 'y', 'f', '9', 'N', 'z', 'b', '4', '^', '='], [')', 'Q', '!', 'X', 'm', '$', '@', 'c', 'B', 'S'], ['u', '+', 'v', 'r', 'F', 'i', '*', 'T', 'd', ',']]
    try:
        if(m):
            g=True
            for a in range(len(k)):
                tin=randint(0,len(k)-1)
                tec=k.pop(tin)
                vac=pkr.pop(tin)
                if(pum[tec[1]][tec[0]]!=prm[vac[1]][vac[0]]):
                    g=False
            return g
        else:
            g=True
            for a in range(len(k)):
                tin=randint(0,len(k)-1)
                tec=k.pop(tin)
                vac=pkd.pop(tin)
                if(pum[tec[1]][tec[0]]!=prm[vac[1]][vac[0]]):
                    g=False
            return g
    except:
        return False

    



     


def encryptText(text:str):
    global characterSet
    global loadedKey

    encryptedText=""
    try:
        encryptedText=crypto_engine.encrypt(text, characterSet, loadedKey)
    except:
        return (False, "critical error: (error 32) encryption process failed. please check the text for errors then try again.",0)
    
    if(not encryptedText[0]):
        return (False, "input error: (error 33) the character {"+encryptedText[1]+"} in the given text is not present in the currently load character set. \nplease either add it to the character set or remove it from the text, then try again.",1)
    
    return encryptedText
        





#needs a fix to number the errors so they transfer properly
def encryptTextFile(sourceFileName:str,destinationFileName:str):

    fileData=getTextFromFile(sourceFileName)

    if(not fileData[0]):
        return fileData
    
    global characterSet
    global loadedKey

    encryptedText=""
    try:
        encryptedText=crypto_engine.encrypt(fileData[1], characterSet, loadedKey)
    except:
        return (False, "critical error: (error 34) encryption process failed. please check the file for errors then try again.")
    
    if((not encryptedText[0]) and encryptedText[2]==1):
        return (False, "input error: (error 35) the character {"+encryptedText[1]+"} in the given file is not present in the currently loaded character set. \nplease either add it to the character set or remove it from the file, then try again.")
    
    elif((not encryptedText) and encryptedText[2]==0):
        return (False, "critical error: (error 36) encryption process failed. please check the file for errors then try again.")

    error=writeTextToFile(destinationFileName,encryptedText[1])
    
    if(not error[0]):
        return error
    
    return(True, "successful")
    
    




def decryptText(text:str):

    global characterSet
    global loadedKey

    decryptedText=""
    try:
        decryptedText=crypto_engine.decrypt(text, characterSet, loadedKey)
    except:
        return (False, "critical error: (error 37) decryption process failed. please check the text for errors then try again.",0)
    
    if(not decryptedText[0]):
        return (False, "input error: (error 38) the character {"+decryptedText[1]+"} in the given text is not present in the currently load character set. \nplease either add it to the character set or remove it from the text, then try again.",1)
    
    return decryptedText






def decryptTextFile(sourceFileName:str, destinationFileName:str):
    
    fileData=getTextFromFile(sourceFileName)

    if(not fileData[0]):
        return fileData
    
    global characterSet
    global loadedKey

    decryptedText=""
    try:
        decryptedText=crypto_engine.decrypt(fileData[1], characterSet, loadedKey)
    except:
        return (False, "critical error: (error 39) encryption process failed. please check the file for errors then try again.")
    


    if((not decryptedText[0]) and decryptedText[2]==1):
        return (False, "input error: (error 40) the character {"+decryptedText[1]+"} in the given file is not present in the currently loaded character set. \nplease either add it to the character set or remove it from the file, then try again.")
    

    elif((not decryptedText[0]) and decryptedText[2]==0):
        return (False, "critical error: (error 41) encryption process failed. please check the file for errors then try again.")
    

    error=writeTextToFile(destinationFileName,decryptedText[1])
    
    if(not error[0]):
        return error
    
    return(True, "successful")