file1 = open("default_charset.txt","r")
key=file1.read()
file1.close()
key.replace('\n',"").replace('\t'," ").replace('\r',"")

print(key)
input()
