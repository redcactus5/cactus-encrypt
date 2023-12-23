import core
from random import randint



'''
guide for adding file support:
https://www.geeksforgeeks.org/reading-writing-text-files-python/

using File_object.read() should work for loading
File_object.write(str1) should work for writing

use try catch to detect file not found errors


remember to add warnings to the prompts

remember to close the file when done

# Opening and Closing a file "MyFile.txt"
# for object name file1.
file1 = open("MyFile.txt","a")
file1.close()

use "w" open mode for writing, and "r" open mode for reading


when loading remember to replace all "\n" with " "
there is a built in function that can do this


'''




#default key backup: CHARACTERS=("D", "[", " ", "Z", "2", "}", "J", "K", "y", ".", "O", "z", "{", "V", "w", "~", "L", "3", "E", "X", "f", "=", "g", "q", "(", "C", "7", ",", "p", "^", "F", "l", "!", "<", "m", "/", "e", "o", "H", "W", "9", "?", "\"", "S", "x", "i", "*", "a", "B", "M", "j", "`", "T", "U", "R", "-", ">", "+", "0", "s", ":", "n", "b", "#", "d", "]", "4", "r", ")", "I", "u", "\\", "t", "c", "|", "&", "P", "h", "$", "v", "k", "@", "5", "%", ";", "A", "G", "\'", "N", "6", "1", "Q", "8", "_", "Y")




#list of all suported characters
characterSet=None
#stores the currently loaded key
loadedKey=None



def scrambleCharSet():
    global characterSet
    oldSet=list(characterSet)
    scrambled=[]
    for i in range(len(oldSet)):
        scrambled.append(oldSet.pop(randint(0,len(oldSet)-1)))
    characterSet= tuple(scrambled)



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
        file=open(fileName,"r")
    except:
        return (True,"io error: file could not be opened. please check that file is present, accessible, and the name is correct")
    try:
        text=file.read()
    except:
        return (True,"io error: file could not be read. please check the file for errors")
    try:
        file.close()
    except:
        return (True,"io error: file could not be closed. please check file for errors")
    return (False,text)







def writeTextToFile(fileName:str,text:str):
    file=None
    try:
        file=open(fileName,"w")
    except:
        return (True,"io error: file could not be opened/created. please check that file is present, accessible, and the name is correct, or that the destination is writeable")
    try:
        file.write(text)
    except:
        return (True, "io error: file could not be written to. please check that the file is not write protected")
    try:
        file.close()
    except:
        return (True,"io error: file could not be closed. please check file for errors")
    return (False,"successful")







def generateKey(rotorCount:int):
    global characterSet
    core.generateKey(rotorCount, characterSet)






def exportKey():
    global loadedKey
    return core.exportKey(loadedKey)






def loadKey(keyStringVer:str):
    setKey(core.loadKey(keyStringVer))



def encryptText(text:str):

    global characterSet
    global loadedKey

    return core.encrypt(text, characterSet, loadedKey)






def encryptTextFile(fileName:str):
    pass





def decryptText(text:str):

    global characterSet
    global loadedKey

    return core.decrypt(text,characterSet, loadedKey)





    


    

#move text file handleing code here... maybe