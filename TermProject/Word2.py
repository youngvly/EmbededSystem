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

    #between a~z, wordlength(3~15)
    #match_pattern = re.findall(r'\b[a-z]{3,15}\b',txt_string)
    #match_pattern = re.findall(r'\b["xAC00"-"xD7A3"]{3,15}\b',txt_string)
    #match_pattern = regex.findall(ur'[\p{Hangul}|\p{Latin}]+',txt_string)
    match_pattern = re.findall(r'[가-힣]+',txt_string)
    for word in match_pattern :
        #if isFiltered(word) :
        #    count = frequency.get(word,0)
        #    frequency[word] = count + 1
        count = frequency.get(word,0)
        frequency[word] = count + 1
        
    
    #frequency_list = frequency.keys()
    
    sortedFrequency = sorted(frequency.items(), key = lambda kv:kv[1],reverse=True)
    print(sortedFrequency , type(sortedFrequency))
    #for words in frequency_list :
     #       print (words,sortedFrequency[words])
    #print(sortedFrequency)
    top5 = []
    if len(sortedFrequency) < 5 :
        return sortedFrequency
    i = 0
    avgCnt = sum(x[1] for x in sortedFrequency)/len(sortedFrequency)
##    print("average Cnt" , avgCnt)
##    print (sortedFrequency)
    for sortF in sortedFrequency:
        #print(i)
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