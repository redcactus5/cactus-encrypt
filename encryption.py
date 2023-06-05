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
    #key structure [rotor keys],[rotor starts],[initial and final static cyphers]
    pass
    


    
def loadKey(inputKey):
    pass

    



def exportKey(inputKey):
    
    pass
    
    

  
    


    
#something in either loading or exporting is breaking the initial scrambler key




#to decrypt just trace the path back in reverse
    

