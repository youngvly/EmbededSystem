#-*-coding:utf-8-*-
import re
import string
#import regex

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
        count = frequency.get(word,0)
        frequency[word] = count + 1
    
    frequency_list = frequency.keys()
    
    sortedFrequency = sorted(frequency.items(), key = lambda kv:kv[1],reverse=True)
    #for words in frequency_list :
     #       print (words,sortedFrequency[words])
    #print(sortedFrequency)
    top3 = []
    if len(sortedFrequency) < 3 :
        return sortedFrequency
    for i in range (0, 3 ,1):
        #print(i)
        top3.append(sortedFrequency[i])
    return top3

if __name__ == "__main__" :
    top3 = wordExtract("Resources/speech.txt")
    print()
    for top in top3 :
        print(top[0] , ":" , top[1])