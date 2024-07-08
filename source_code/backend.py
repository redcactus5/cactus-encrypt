#cactus encrypt is a simple cli text encryption program written in python that implements the cactus cipher algorithm
#Copyright 2023,2024 Redcactus5
'''
This file is part of Cactus Encrypt.

Cactus Encrypt is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Cactus Encrypt is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Cactus Encrypt. If not, see <https://www.gnu.org/licenses/>. 
'''
#this program is free, open source software released under the GNU General Public License version 3.0 or later version (GPL-3.0-or-later)



import crypto_engine
from random import randint
#from typing import List        #handy standard lib i recently found out about that adds more type hinting features like hinting list contents

#the continue command is very useful too



#default key backup: CHARACTERS=("D", "[", " ", "Z", "2", "}", "J", "K", "y", ".", "O", "z", "{", "V", "w", "~", "L", "3", "E", "X", "f", "=", "g", "q", "(", "C", "7", ",", "p", "^", "F", "l", "!", "<", "m", "/", "e", "o", "H", "W", "9", "?", "\"", "S", "x", "i", "*", "a", "B", "M", "j", "`", "T", "U", "R", "-", ">", "+", "0", "s", ":", "n", "b", "#", "d", "]", "4", "r", ")", "I", "u", "\\", "t", "c", "|", "&", "P", "h", "$", "v", "k", "@", "5", "%", ";", "A", "G", "\'", "N", "6", "1", "Q", "8", "_", "Y")




#list of all suported characters
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
        return (False,"io error: file to read could not be opened. please check that file is present, accessible, and the name is correct, then try again.")
    try:
        text=file.read()
    except:
        return (False,"io error: file could not be read. please check the file for errors then try again.")
    try:
        file.close()
    except:
        return (False,"io error: read file could not be closed. please check file for errors then try again.")
    return (True,text)







def writeTextToFile(fileName:str,text:str):
    file=None
    try:
        file=open(fileName,'w')
    except:
        return (False,"io error: file to write could not be opened/created. please check that file is present, writeable, has the correct name, and that the location is accessible, then try again.")
    try:
        file.write(text)
    except:
        return (False, "io error: file could not be written to. please check that the file is not write protected then try again.")
    try:
        file.close()
    except:
        return (False,"io error: written file could not be closed. please check file for errors then try again.")
    return (True,"successful")




#key and charset management functions


def generateKey(rotorCount:int):
    global characterSet
    global loadedKey
    if(type(rotorCount) is not int or rotorCount<1):
        return (False, "input error: given complexity value is invalid. please check that the complexity \nvalue is a positive integer, then try again.")
    try:
        newKey=crypto_engine.generateKey(rotorCount, characterSet)
    except:
        return (False, "critical error: new key could not be generated. please check input for errors then try again.")

    try:
        setKey(newKey)
    except:
        return (False, "critical error: the newly generated key could not be loaded. please check for errors then try again.")

    return (True, "successful")






def exportKey():
    global loadedKey
    keyString=None
    try:
        keyString=crypto_engine.exportKey(loadedKey)
    except:
        return (False, "critical error: key could not be compiled to a string. please check it for errors then try again.")
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
        key=crypto_engine.loadKey(keyString)
    except:
        return (False, "input error: key could not be parsed. please check the key for errors then try again.")
    
    if(characterSet==None):
        return (False, "input error: character set key mismatch, character set and key do not have the same number of characters. please load the correct character set then try again.")

    if(len(key[len(key)-1])!=len(characterSet)):
        return (False, "input error: character set key mismatch, character set and key do not have the same number of characters. please load the correct character set then try again.")
    
    
    try:
        setKey(key)
    except:
        return (False, "critical error: key could not be loaded. please check the key for errors then try again.")
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
    charSetTuple=None
    try:
        charSetTuple=tuple(charSetString)
        charLog=[]
        for char in charSetTuple:
            if(char in charLog):
                return (False, "input error: multiple occurrences of the character {"+str(char)+"} were found in the \ncharacter set.  please remove all duplicates of the character then try again.")
            charLog.append(char)
    except:
        return (False, "critical error: character set could not be parsed. please check it for errors then try again.")
        
    try:
        setCharSet(charSetTuple)
    except:
        return (False, "critical error: character set could not be parsed. please check it for errors then try again.")
    try:
        setKey(None)
    except:
        return (False, "critical error: key could not be cleared. please check it for errors then try again.")
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
        return (False, "critical error: character set could not be processed. please check it for errors then try again.")
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
        return (False, "critical error: character set could not be scrambled. please check it for errors then try again.")
    return (True,"successful")



def sanitizeText(text:str,attemptReplacement:bool):

    if(text==None or text==""):

        return ""
    global characterSet


    cleanTextList=[]

    cleanText=""

    listedText=[]

    replacementCandidates=list(" _-|*+.$?Xx")
    
   #need to add option to attempt to add spacing characters

    try:
        listedText=list(text)
        print

        
        if(attemptReplacement):
            replacement=""
            for rep in replacementCandidates:
                if(rep in characterSet):
                    replacement=rep
                    break

            for char in listedText:
                if(char in characterSet):
                    cleanTextList.append(char)
                else:
                    cleanTextList.append(replacement)



        else:
            for char in listedText:
                if(char in characterSet):
                    cleanTextList.append(char)

            

        
        cleanText=cleanText.join(cleanTextList)
    except:
        return (False, "critical error: entered text could not be sanitized. please check it for problems then try again.")
    
    return (True, cleanText)


def sanitizeTextFile(sourceFileName:str,destinationFileName:str,attemptReplacement:bool):
    

    
    dubiousText=getTextFromFile(sourceFileName)


    if(not dubiousText[0]):
        return dubiousText
    
    cleanText=sanitizeText(dubiousText[1],attemptReplacement)

    if(not cleanText[0]):
        return cleanText
    
    error=writeTextToFile(destinationFileName,cleanText[1])

    if(not error[0]):
        return error
    
    return (True,"successful")




    




     


def encryptText(text:str):
    global characterSet
    global loadedKey

    encryptedText=""
    try:
        encryptedText=crypto_engine.encrypt(text, characterSet, loadedKey)
    except:
        return (False, "critical error: encryption process failed. please check the text for errors then try again.")
    
    if(not encryptedText[0]):
        return (False, "character error: the character {"+encryptedText[1]+"} in the given text is not present in the currently load character set. \nplease either add it to the character set or remove it from the text, then try again.")
    
    return encryptedText
        






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
        return (False, "critical error: encryption process failed. please check the file for errors then try again.")
    
    if(not encryptedText[0]):
        return (False, "character error: the character {"+encryptedText[1]+"} in the given file is not present in the currently loaded character set. \nplease either add it to the character set or remove it from the file, then try again.")
    
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
        return (False, "critical error: decryption process failed. please check the text for errors then try again.")
    
    if(not decryptedText[0]):
        return (False, "character error: the character {"+decryptedText[1]+"} in the given text is not present in the currently load character set. \nplease either add it to the character set or remove it from the text, then try again.")
    
    return decryptedText






def decryptTextFile(sourceFileName:str,destinationFileName:str):
    
    fileData=getTextFromFile(sourceFileName)

    if(not fileData[0]):
        return fileData
    
    global characterSet
    global loadedKey

    decryptedText=""
    try:
        decryptedText=crypto_engine.decrypt(fileData[1], characterSet, loadedKey)
    except:
        return (False, "critical error: encryption process failed. please check the file for errors then try again.")
    
    if(not decryptedText[0]):
        return (False, "character error: the character {"+decryptedText[1]+"} in the given file is not present in the currently loaded character set. \nplease either add it to the character set or remove it from the file, then try again.")
    
    error=writeTextToFile(destinationFileName,decryptedText[1])
    
    if(not error[0]):
        return error
    
    return(True, "successful")