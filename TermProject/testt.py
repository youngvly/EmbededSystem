#-*-coding:utf-8-*-
print 1/2.0
print 1/float(2)

print "그래서".decode('utf-8')
print('\xea\xb7\xb8\xeb\x9e\x98\xec\x84\x9c').decode('utf-8')

filtertxt = open("FilteredWord.txt","r")
filtertxt_str = filtertxt.read()
global filterList
filterList = filtertxt_str.split('/')
filterList = [f.decode("EUC-KR").encode("utf-8") for f in filterList]
print("F:" , filterList)

def isFiltered(word):
    print(word)
    if word in filterList :
        return True
    return False

print(isFiltered("그래서"))
