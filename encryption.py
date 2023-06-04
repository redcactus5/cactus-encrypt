from random import randint

CHARACTERS=("q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"," ",";","1","2","3","4","5","6","7","8","9","0","-","=","!","#","$","%","^","&","*","(",")","_","+","Q","W","E","R","T","Y","U","I","O","P","A","S","D","F","G","H","J","K","L",":","Z","X","C","B","V","N","M","<",">","?",".",",")
#len is 83
loadedKey=None

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
    #loop to creat the rotor wirings
    for rotor in range(ROTORNUM):
        keyPeice=""
        numberRange=getNumberRange(0,len(CHARACTERS))
        #create a string of scrambled numbers to act as the rotor wiring
        for i in range(len(numberRange)):
            keyPeice+=str(numberRange.pop(randint(0,len(numberRange)-1)))
            #add a comma as a seperator unless you are on the last number
            if(len(numberRange)>=1):
                keyPeice+=", "
        #add a seperator between the keys and add the rotor wiring to the key
        key+=keyPeice+" | "
    #create and add the rotor start positions to the key with seperators
    for i in range(ROTORNUM):
        key+=(str(randint(0,len(CHARACTERS)))+" | ")
    
        
    
    #generate the initial scrambler wiring (near identical to  rotor wiring generation)
    numberRange=getNumberRange(0,len(CHARACTERS))
    initScrambler=""
    for i in range(len(numberRange)):
        initScrambler+=str(numberRange.pop(randint(0,len(numberRange)-1)))
        #add a comma as a seperator unless you are on the last number
        if(len(numberRange)>=1):
            initScrambler+=", "
    #add initial scrambler to the key
    key+=initScrambler
    print(key)
    return key
    


    
def loadKey(key):
    #first seperation of the text into lists
    splitKeyStringList=key.rsplit(" | ")
    key=[]
    
    #for all the rotor wirings
    for i in range(ROTORNUM):
        #pop the rotor wiring from splitkeystringlist
        temp=splitKeyStringList.pop(0)
        #split the wiring into a list of strings
        temp=temp.rsplit(", ")
        #convert the number strings in the wiring list into integers
        for i in range(len(temp)):
            temp[i]=int(temp[i])
        #add the decoded wiring to key
        key.append(temp)
    
    #for all rotor start postions
    for i in range(ROTORNUM):
        #covert the start position string into an integer and move it to key
        key.append(int(splitKeyStringList.pop(0))) 



    #decode the initial scrambler in the same way as the rotors
    initialScrambler=splitKeyStringList.pop(0)
    initialScrambler=initialScrambler.rsplit(", ")
    for i in range(len(initialScrambler)):
        initialScrambler[i]=int(initialScrambler[i])
    #add the decoded scrambler key to key
    key.append(temp)
    
    global loadedKey
    loadedKey=key
    return key
    
test=generateKey()    
loadKey(test)


def exportKey():
    #get the currently loaded key
    global loadedKey
    #check to see if a key is loaded
    if(loadedKey!=None):
        
        #if a key is loaded
        key=""
        #for all the rotor keys
        for rotor in range(ROTORNUM):
            keyPeice=""
            #compile the key into a string
            for i in range(len(loadedKey[rotor])):
                keyPeice+=str(loadedKey[rotor][i])
                if(i<len(loadedKey[rotor])-1):
                    keyPeice+=", "
            #add string to key string
            key+=keyPeice+" | "
        #convert start positions into strings and add them to key
        for i in range(ROTORNUM):
            key+=(str(loadedKey[i+ROTORNUM])+" | ")
        
        
        print(key)

        return key
    return False
        
    


exportKey()

print(test==exportKey())

#to decrypt just trace the path back in reverse
    

