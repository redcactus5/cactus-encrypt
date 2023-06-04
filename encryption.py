from random import randint

CHARACTERS=("q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"," ",";","1","2","3","4","5","6","7","8","9","0","-","=","!","#","$","%","^","&","*","(",")","_","+","Q","W","E","R","T","Y","U","I","O","P","A","S","D","F","G","H","J","K","L",":","Z","X","C","B","V","N","M","<",">","?",".",",")
#len is 83
key=None

ROTORNUM=10

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
    
    def getValue(self,number):
        searchNumber=number
        while(searchNumber+self.pos>len(self.wiring)-1):
            searchNumber-=len(self.wiring)
        return self.wiring[searchNumber]
    



def getNumberRange(start,end):
    temp=[]
    for i in range(start,end):
        temp.append(i)
    return temp


def generateKey():
    key=""
    for rotor in range(ROTORNUM):
        keyPeice=""
        numberRange=getNumberRange(0,len(CHARACTERS))
        for i in range(len(numberRange)):
            keyPeice+=str(numberRange.pop(randint(0,len(numberRange)-1)))
            if(len(numberRange)>=1):
                keyPeice+=", "
        key+=keyPeice+" | "
    for i in range(ROTORNUM):
        key+=(str(randint(0,len(CHARACTERS)))+" | ")
    
        
    
    #generate the initial scrambler key
    numberRange=getNumberRange(0,len(CHARACTERS))
    initScrambler=""
    for i in range(len(numberRange)):
        initScrambler+=str(numberRange.pop(randint(0,len(numberRange)-1)))
        if(len(numberRange)>=1):
            initScrambler+=", "
    key+=initScrambler
    print(key)
    return key
    


    
def loadKey(key):
    #first seperation of the text into lists
    splitKeyStringList=key.rsplit(" | ")
    keyInProgress=[]
    
    #seperates the keys into lists of strings of numbers
    for i in range(ROTORNUM):
        temp=splitKeyStringList.pop(0)
        keyInProgress.append(temp.rsplit(", "))
    #convert the strings of numbers into numbers
    for subKey in keyInProgress:
        for i in range(len(subKey)):
            subKey[i]=int(subKey[i])
    #convert start positions into integers
    for i in range(ROTORNUM):
        keyInProgress.append(int(splitKeyStringList.pop(0))) 


    
    
    return keyInProgress
    
(loadKey(generateKey()))


def encrypt(inputText):
    #convert the input text into a list of numbers
    chickenScratch=convertToNum(inputText)
    Rotors=[]
    #generate and initialize the Rotors
    for i in range(ROTORNUM):
        Rotors.append(Rotor(key[i],key[i+ROTORNUM]))
    




    

