#-*-coding:utf-8-*-
import re
import string
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')
#import regex


# WITH FILTER

def isFiltered(word):
    #print (filterList[0])
    if word in filterList :
        return True
    return False
    
    
def wordExtract(filename) :
    #in filtertxt = open("FilteredWord.txt","r",encoding = "ISO-8859-1")
    filtertxt = open("FilteredWord.txt","r")
    filtertxt_str = filtertxt.read()
    global filterList
    filterList = filtertxt_str.split('/')
    filterList = [f.decode("EUC-KR").encode("utf-8") for f in filterList]
    #print("F:" , filterList)
    
    filtered_frequency = {}
    normal_frequency = {}
    txtfile = open(filename,"r")
    txt_string = txtfile.read()

    #between a~z, wordlength(3~15)
    #match_pattern = re.findall(r'\b[a-z]{3,15}\b',txt_string)
    #match_pattern = re.findall(r'\b["xAC00"-"xD7A3"]{3,15}\b',txt_string)
    #match_pattern = regex.findall(ur'[\p{Hangul}|\p{Latin}]+',txt_string)
    match_pattern = re.findall(r'[가-힣]+',txt_string)
    for word in match_pattern :
        #if isFiltered(word) :
        #    count = filtered_frequency.get(word,0)
        #    filtered_frequency[word] = count + 1
        count = filtered_frequency.get(word,0)
        filtered_frequency[word] = count + 1
        
    
    frequency_list = filtered_frequency.keys()
    
    sortedFrequency = sorted(filtered_frequency.items(), key = lambda kv:kv[1],reverse=True)
    #for words in frequency_list :
     #       print (words,sortedFrequency[words])
    #print(sortedFrequency)
    #top5 = []
    #if len(sortedFrequency) < 5 :
    #   return sortedFrequency
    #i = 0
    #while(len(top5) == 5 or len(sortedFrequency) <=i):
    #    top5.append(sortedFrequency[i])
    #return top5
    return sortedFrequency

if __name__ == "__main__" :
    top5 = wordExtract("Resources/speech.txt")
    print()
    for top in top5 :
        print(top[0] , ":" , top[1])