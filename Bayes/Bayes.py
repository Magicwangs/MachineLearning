# -*- coding: utf-8 -*-
"""
Created on Fri Sep 02 22:34:51 2016

@author: MagicWang
"""
import re
import random
import feedparser
from operator import itemgetter
import numpy as np
from math import log
from os import listdir

# 加载数据
def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 侮辱型言论, 0 正常言论
    return postingList,classVec

# 去除重复词，制作词典
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

# word2vec,只考虑词出现与否
def setOfWord2Vec(vocabList, inputSet):
    retVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            retVec[vocabList.index(word)] = 1
        else:
            print "the word: %s is not in my Vocabulary!" % word
    return retVec


def trainNBO(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    # python中不要用连等
    p0Num = np.ones(numWords); p1Num = np.ones(numWords)
    p0Denom = 2.; p1Denom = 2.
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = np.log(p1Num/p1Denom)
    p0Vect = np.log(p0Num/p0Denom)
    return p0Vect, p1Vect, pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    # 点乘，只计算每个出现的词
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.-pClass1)
#    print p1,p0
    if p1 > p0:
        return 1
    else:
        return 0
    
def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for Doc in listOPosts:
        trainMat.append(np.array(setOfWord2Vec(myVocabList, Doc)))
    p0Vect, p1Vect, pAb = trainNBO(np.array(trainMat), np.array(listClasses))
    
    testWord = ['love', 'my', 'dalmation']
    thisDoc = np.array(setOfWord2Vec(myVocabList, testWord))
    print "Class is %d" % classifyNB(thisDoc, p0Vect, p1Vect, pAb)

# 词袋模型
def bagOfWord2VecMN(vocabList, inputSet):
    retVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            retVec[vocabList.index(word)] += 1
#        else:
#            print "Word: %s is not in vocabulary." % word
    return retVec

# 文本解析，过滤无意义的短单词
def textParse(bigString):
    listOfTokens = re.split(r"\W+", bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def spamTest():
    docList = []; classList = []; fullText = []
    hamDir = "./email/ham/"
    spamDir = "./email/spam/"
    fileName = listdir(hamDir)
    for name in fileName:
        wordList = textParse(open(hamDir + name).read())
        docList.append(wordList)
#        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open(spamDir + name).read())
        docList.append(wordList)
#        fullText.extend(wordList)
        classList.append(0)    
    vocabList = createVocabList(docList)
    # 交叉验证
    trainSet = range(len(docList)); testSet = []
    for i in range(10):
        randomNum = random.randint(0, len(trainSet)-1)
        testSet.append(trainSet[randomNum])
        del(trainSet[randomNum])
    # 构造训练数据集
    trainMat = []; trainClass = []
    for index in trainSet:
        trainMat.append(bagOfWord2VecMN(vocabList, docList[index]))
        trainClass.append(classList[index])
    p0V, p1V, pAb = trainNBO(np.array(trainMat), np.array(trainClass))
    # 测试
    errorCount = 0
    for index in testSet:
        wordVec = bagOfWord2VecMN(vocabList, docList[index])
        if classifyNB(np.array(wordVec), p0V, p1V, pAb) != classList[index]:
            errorCount += 1
    print "The errorCount is %d" % errorCount

# 计算单词出现频率, 返回元祖类型    
def calcMostFreq(vocabList, fullText):
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.iteritems(), key=itemgetter(1), reverse=True)
    return sortedFreq[:30]

# 输入两个城市的RSS
def localWords(feed1, feed0):
    docList = []; classList = []; fullText = []
    minLen = min(len(feed1['entries']), len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    top30Word = calcMostFreq(vocabList, fullText)
    # top30word是元祖类型，去除top30
    for pairWord in top30Word:
        if pairWord[0] in vocabList:
            vocabList.remove(pairWord[0])
    # 交叉验证
    trainSet = range(2*minLen); testSet = []
    for index in range(20):
        randIndex = random.randint(0, len(trainSet)-1)
        testSet.append(trainSet[randIndex])
        del(trainSet[randIndex])
    # 训练  
    trainMat = []; trainClass = []
    for index in trainSet:
        trainMat.append(bagOfWord2VecMN(vocabList, docList[index]))
        trainClass.append(classList[index])
    p0V, p1V, pAb = trainNBO(np.array(trainMat), np.array(trainClass))
    # 测试
    errorCount = 0
    for index in testSet:
        wordVec = bagOfWord2VecMN(vocabList, docList[index])
        if classifyNB(np.array(wordVec), p0V, p1V, pAb) != classList[index]:
            errorCount += 1
    print "The errorCount is %f" % (errorCount/20.)
    return vocabList, p0V, p1V

def getTopWord(ny, sf):
    vocabList, p0V, p1V = localWords(ny, sf)
    topNY = []; topSF = []
    for i in range(len(p0V)):
        if p0V[i] > -5.0:
            topSF.append((vocabList[i], p0V[i]))
        if p1V[i] > -5.0:
            topNY.append((vocabList[i], p1V[i]))
    print "======SF======="
    sortedSF = sorted(topSF, key=itemgetter(1), reverse=True)
    print [pair[0] for pair in sortedSF[:10]]
    print "======NY======="
    sortedNY = sorted(topNY, key=itemgetter(1), reverse=True)
    print [pair[0] for pair in sortedNY[:10]]

if __name__=="__main__":    
    ny = feedparser.parse("https://newyork.craigslist.org/stp/index.rss")
    sf = feedparser.parse("https://sfbay.craigslist.org/stp/index.rss")
    getTopWord(ny, sf)