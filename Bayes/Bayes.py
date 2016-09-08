# -*- coding: utf-8 -*-
"""
Created on Fri Sep 02 22:34:51 2016

@author: MagicWang
"""
from numpy import *
from cv2 import *

#创建实验样本
def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 侮辱型文字, 0 正常言论
    return postingList,classVec

#去重，整合成一个list
def createVocabList(dataSet):
    vocabSet=set([])
    for document in dataSet:
        vocabSet=vocabSet|set(document)
    #返回按小写字母顺序排列的字符
    return sorted(list(vocabSet),key=str.lower)

#判断单词是否在vocabList中
#vocabList:词汇表 inputSet:被判断的单词list
def setOfWord2Vec(vocabList,inputSet):
    #全零List
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
        else:
            print "the word: %s is not in my Vocabulary"%word
    return returnVec

#trainMat：词汇矩阵(0,1构成，是否为辱骂词)；trainCategory：每篇文档的类别标签
def trainNB(trainMat,trainCategory):
    numTrainDocs=len(trainMat)
    numWords=len(trainMat[0])
    #侮辱性文档/所有文档中的数量
    pAbusive=sum(trainCategory)/float(numTrainDocs)
    #初始化为1，是为了减少概率为0的词对结果的影响
    #初始情况每个词出现的概率都是0.5
    p0Num=ones(numWords)
    p1Num=ones(numWords)
    p0Denom=2.0
    p1Denom=2.0
    #和石子的例子一样
    for i in range(numTrainDocs):
        if trainCategory[i]==1:
            p1Num+=trainMat[i]
            p1Denom+=sum(trainMat[i])
        else:
            p0Num+=trainMat[i]
            p0Denom+=sum(trainMat[i])
    #侮辱性文档中的侮辱词向量/侮辱性文档中侮辱词的总个数
    p1Vect=log(p1Num/p1Denom)
    p0Vect=log(p0Num/p0Denom)
    return p0Vect,p1Vect,pAbusive
    
def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    #直接*，是点乘，dot是叉乘
    p1=sum(dot(vec2Classify,p1Vec))+log(pClass1)[0]
    p0=sum(dot(vec2Classify,p0Vec))+log(1.0-pClass1)[0]
    if p1>p0:
        return 1
    else:
        return 0

def testingNB():
    postingList,classVec=loadDataSet()
    myVocabList=createVocabList(postingList)
    trainMat=[]
    for postinDoc in postingList:
        trainMat.append(setOfWord2Vec(myVocabList,postinDoc))
    p0V,p1V,pAb=trainNB(array(trainMat),array(classVec))
    #开始输入测试数据
    testEntry=['stupid','garbage','dog']
    thisDoc=array(setOfWord2Vec(myVocabList,testEntry))
    print testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb)

if __name__=="__main__":
    testingNB()