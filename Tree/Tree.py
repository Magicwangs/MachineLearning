# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 21:23:34 2016

@author: MagicWang
"""

from math import log
import operator

def creatDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return dataSet, labels

#计算香农信息熵
#dataSet是List格式，最后一列是标签数据  只与最后一列标签数据的比例
def calc_Shannon_Ent(dataSet):
    numEntries=len(dataSet)
    #labelCounts为字典格式
    labelCounts={}
    for featVec in dataSet:
        #逆序寻找
        currentLabel=featVec[-1]
        #如果字典中不存在就新建一个key，键值为 0
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel]+=1
    shannonEnt=0.0
    #逐个取出键
    for key in labelCounts:
        #prob(概率)=每个种类的个数/总共有几组数据
        prob=float(labelCounts[key])/numEntries
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

#按照给定的特征划分数据集
#axis:特征 从0开始  value该特征的某个值
#extend() 函数用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）（只能是添加到原序列中的值）
#append() 方法用于在列表末尾添加新的对象(只能添加一个,但可以是对象（list等）)
def splitDataSet(dataSet,axis,value):
    retDataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            #featVec[:axis] 返回axis前面的所有值
            reducedFeatVec=featVec[:axis]
            #featVec[axis+1:]返回axis+1后面的值    即去掉axis所在的数据
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

#选择最佳特征模块            
def chooseBestFeature_To_Split(dataSet):
    #必须-1，因为最后一列是标签数据，剩下的是判断特征的数量
    numFeature=len(dataSet[0])-1
    baseEntropy=calc_Shannon_Ent(dataSet)
    bestInfoGain=0.0
    bestFeature=-1
    for i in range(numFeature):
        #逐个提取各特征的所有值
        featList=[example[i] for example in dataSet]
        #set:集合，其中没有重复的值
        unique_Vals=set(featList)
        newEntropy=0.0
        for value in unique_Vals:
            subDataSet=splitDataSet(dataSet,i,value)
            prob=float(len(subDataSet))/len(dataSet)
            newEntropy+=prob*calc_Shannon_Ent(subDataSet)
        #信息增益=熵的减少  信息增益最高的就是最佳划分特征
        infoGain=baseEntropy-newEntropy
        if(infoGain>bestInfoGain):
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature

#多数表决模块
#classList 标签数据列表  可通过[example[-1] for example in dataSet]得到
def majorityCnt(classList):
    classCount={}
    for vote in classList:
#        if vote not in classCount.keys():
#            classCount[vote]=0
#        classCount[vote]+=1
        #更简洁的表示，意义同上三行
        classCount[vote]=classCount.get(vote,0)+1
        
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

#创建树模块
#dataSet:前几列是判断特征，最后一列为分类
#labels:每一列判断特征的名称
def createTree(dataSet,labels):
    classList=[example[-1] for example in dataSet]
    #count()统计某元素出现的次数
    #所有实例都是同一标签分类
    if classList.count(classList[0])==len(classList):
        return classList[0]
    #已经处理完所有特征
    if len(dataSet[0])==1:
        return majorityCnt(classList)
    bestFeature=chooseBestFeature_To_Split(dataSet)
    bestFeatureLabel=labels[bestFeature]
    #多层字典
    myTree={bestFeatureLabel:{}}
    #删除特征    
    del(labels[bestFeature])
    #提取目标特征所在列的所有值
    featValues=[example[bestFeature] for example in dataSet]
    uniqueVals=set(featValues)
    for value in uniqueVals:
        subLabels=labels[:]
        myTree[bestFeatureLabel][value]=createTree(splitDataSet(dataSet,bestFeature,value),subLabels)
    return myTree

if __name__=='__main__':
    dataSet,Labels=creatDataSet()
    print createTree(dataSet,Labels)

    
    