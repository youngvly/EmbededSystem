#-*-coding:utf-8-*-
import re
import string
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')
#import regex


#WITH AVERAGE

def wordExtract(filename) :    
    frequency = {}
    txtfile = open(filename,"r")
    txt_string = txtfile.read()

   
    match_pattern = re.findall(r'[가-힣]+',txt_string)
    for word in match_pattern : 
        count = frequency.get(word.decode('utf-8'),0)
        frequency[word.decode('utf-8')] = count + 1    
 
    sortedFrequency = sorted(frequency.items(), key = lambda kv:kv[1],reverse=True)
    top5 = []
    if len(sortedFrequency) < 5 :
        return sortedFrequency
    i = 0
    avgCnt = sum(x[1] for x in sortedFrequency)/len(sortedFrequency)
    
    for sortF in sortedFrequency:
        if sortF[1] >= avgCnt:
            top5.append(sortedFrequency[i])
        i += 1
        if len(top5) == 5 :
            break
##    print (top5)
    return top5

if __name__ == "__main__" :
    top5 = wordExtract("Resources/speech.txt")
    print()
    for top in top5 :
        print(top[0] , ":" , top[1])