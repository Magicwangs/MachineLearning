# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 21:23:34 2016

@author: MagicWang
"""

from math import log
import operator
import matplotlib
import matplotlib.pyplot as plt

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



#centerPt：中心节点位置 parentPt：父节点位置 
#nodeTxt：中心节点的名称 nodeType：中心节点的类型 
def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    #创建注释Create an annotation: a piece of text referring to a data point.
    #parentPt:注释点的位置 xycoords:注释的类型
    #详见ax.annotate
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction',
                            xytext=centerPt,textcoords='axes fraction',
                            va="center",ha="center",bbox=nodeType,arrowprops=arrow_args)
#获取叶节点的个数
def getNumLeafs(myTree):
    numLeafs=0
    firstStr=myTree.keys()[0]
    secondDict=myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs+=getNumLeafs(secondDict[key])
        else:
            numLeafs+=1
    return numLeafs

#获取决策树的层数
def getTreeDepth(myTree):
    maxDepth=0
    firstStr=myTree.keys()[0]
    secondDict=myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth=1+getTreeDepth(secondDict[key])
        else:
            thisDepth=1
        if thisDepth>maxDepth:maxDepth=thisDepth
    return maxDepth

#写下连线中间的0，1等特征值，cntrPt子节点位置，parentPt父节点位置  ——元组类型
def plotMidText(cntrPt,parentPt,txtString):
    xMid=(parentPt[0]-cntrPt[0])/2+cntrPt[0]
    yMid=(parentPt[1]-cntrPt[1])/2+cntrPt[1]
    createPlot.ax1.text(xMid,yMid,txtString)

#
def plotTree(myTree,parentPt,nodeTxt):
    numLeafs=getNumLeafs(myTree)
    depth=getTreeDepth(myTree)
    firstStr=myTree.keys()[0]    
    cntrPt=(plotTree.xOff+(1.0+float(numLeafs))/2.0/plotTree.totalW,plotTree.yOff)
    plotMidText(cntrPt,parentPt,nodeTxt)
    plotNode(firstStr,cntrPt,parentPt,decisionNode)
    secondDict=myTree[firstStr]
    plotTree.yOff=plotTree.yOff-1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            plotTree(secondDict[key],cntrPt,str(key))
        else:
            plotTree.xOff=plotTree.xOff+1.0/plotTree.totalW
            plotNode(secondDict[key],(plotTree.xOff,plotTree.yOff),cntrPt,leafNode)
            plotMidText((plotTree.xOff,plotTree.yOff),cntrPt,str(key))
    plotTree.yOff=plotTree.yOff+1.0/plotTree.totalD

#dict()新建字典数据
decisionNode=dict(boxstyle="sawtooth",fc="0.8")
leafNode=dict(boxstyle="round4",fc="0.8")
arrow_args=dict(arrowstyle="<-")

#画出树
def createPlot(inTree):
    #新建图1,背景色为白色
    fig=plt.figure(1,facecolor='white')
    #Clear the current figure
    fig.clf()
    axprops=dict(xticks=[],yticks=[])
    #creatPlot.ax1是一个全局变量
    #frameon:背景框是否在，False背景透明
    #axprops:隐藏刻度
    #subplot:Return a subplot axes positioned by the given grid definition.
    createPlot.ax1=plt.subplot(111,**axprops)
    plotTree.totalW=float(getNumLeafs(inTree))
    plotTree.totalD=float(getTreeDepth(inTree))
    plotTree.xOff=-0.5/plotTree.totalW
    plotTree.yOff=1.0
    plotTree(inTree,(0.5,1.0),'')
#    #U''means string is a unicode string.
#    plotNode(U'决策节点',(0.5,0.1),(0.1,0.5),decisionNode)
#    plotNode(U'叶节点',(0.8,0.1),(0.3,0.8),leafNode)
    plt.show()
    
if __name__=='__main__':
    dataSet,Labels=creatDataSet()
    print '\nthe tree is'
    myTree=createTree(dataSet,Labels)
    print myTree
    
    createPlot(myTree)
    
    
    
    
    
    
    
    
    