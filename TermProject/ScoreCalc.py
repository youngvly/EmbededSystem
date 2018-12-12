def faceScoreCalc(faceCnt) :
    totalTry = sum(faceCnt.values())
    if totalTry == 0:
        return 0
    #faceScore = 50
    faceScore = 0
    #anger
    angerScore = faceCnt["anger"]/totalTry * 50
    surpriseScore = faceCnt["surprise"]/totalTry * 50
    joyScore = faceCnt["joy"]/totalTry * 50
    
    faceScore = faceScore + joyScore - angerScore - surpriseScore * 0.5
    #faceScore = faceScore - angerScore - surpriseScore * 0.5
    return faceScore
    
    
def wordScoreCalc (wordCnt) :
    wordScore = 25
    #1st : -5 , 2st -4, 3st -3 ...
    i = len(wordCnt)
    #if word cnt is upper than 3 times,
    for w in wordCnt :
        if w[1] >=5 :
            wordScore - w[1]*i
        i -= 1
    
def isFiltered(word):
    #print (filterList[0])
    if word in filterList :
        return True
    return False

#wordCnt : top5
def wordScoreCalc_Filter (wordCnt) :
    #print(wordCnt)
    filtertxt = open("FilteredWord.txt","r")
    filtertxt_str = filtertxt.read()
    global filterList
    filterList = filtertxt_str.split('/')
    filterList = [f.decode("EUC-KR").encode("utf-8") for f in filterList]
    #print("F:" , filterList)
    
    wordScore = 50
    #1st : -5 , 2st -4, 3st -3 ...
    i = len(wordCnt)
    #speech not detected
    if i == 0 :
        return 0
    #if word cnt is upper than 3 times,
    for w in wordCnt :
        if isFiltered(w[0]) :
            wordScore - (w[1]*i)
        i -= 1
    return wordScore
    
def calcScore(faceCnt,wordCnt) :
    facescore  = faceScoreCalc(faceCnt)
    wordscore = wordScoreCalc_Filter(wordCnt)
    #wordscore = wordScoreCalc(wordCnt)
    
    if facescore < 0 :
        facescore = 0
    if facescore > 50 :
        facescore = 50
    if wordscore < 0 :
        wordscore = 0
    if wordscore > 50 :
        wordscore = 50
    return facescore + wordscore