# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 20:38:54 2016

@author: MagicWang
"""

#  注释 ctrl+1

from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt
from cv2 import *
from os import listdir


# 创建数据集模块
def createDataSet():  
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return group,labels

#分类模块
#inX:input dataSet:sample one by one
#return:result labels
def classify_kNN(inX,dataSet,labels,k):
    #获取数组的长度
    dataSetSize=dataSet.shape[0]  
    #构建一个和dataSet同样维的数组,重复dataSetSize的行数
    diffMat=tile(inX,(dataSetSize,1))-dataSet
    #每一项的平方
    sqDiffMat=diffMat**2
    #变成1*datasize的数组
    sqDistances=sqDiffMat.sum(axis=1)
    distances=sqDistances**0.5
    #返回排序的索引数组
    sortedDistIndicies=distances.argsort()
    #字典数据类型
    classCount={}
    for i in range(k):
        #得到前k个点对应的标签
        voteIlabel=labels[sortedDistIndicies[i]]
        #字典数据，对应键值加1，默认值为0
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
    #根据个数从大到小的排列
    #可以参考印像笔记
    #classCount.iteritems()返回可遍历的（键,值）
    #key为函数，指定取待排序元素的哪一项进行排序  通过第二域————键值来排序operator.itemgetter(1)
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

#导入数据模块
#filename can be a C:\....
def file2matrix(filename):
    fr=open(filename)
    #read all lines to list
    arrayOLines=fr.readlines()
    numberOfLines=len(arrayOLines)
    #numpy zeros 矩阵
    returnMat=zeros((numberOfLines,3))     
    classLabelVector=[]
    index=0
    for line in arrayOLines:        
        #去掉字符串头尾的空格和/n/t等
        line=line.strip()
        #分割数据 以/t为标识符
        listFromLine=line.split('\t')
        returnMat[index,:]=listFromLine[0:3]
        #把最后一列的数据提出来(Label)
        classLabelVector.append(listFromLine[-1])
        index+=1
    return returnMat,classLabelVector
    
#归一化数据模块 Norm:规范
#newvalues=(oldvalues-minvalue)/(maxvalue-minvalue)
def autoNorm(dataSet):
    #提取所有列的数据中的最小值最大值
    minVals=dataSet.min(0)
    maxVals=dataSet.max(0)
    ranges=maxVals-minVals
    normDataSet=zeros(shape(dataSet))
    #m=1000 shape[0]*shape[1]
    m=dataSet.shape[0]
    #tile(A,reps):Construct an array by repeating A the number of times given by reps.
    normDataSet=dataSet-tile(minVals,(m,1))
    normDataSet=normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals

#测试分类器的准确率
def datingClassTest():    
    #10%的数据作为测试数据
    hoRatio=0.1
    datingDataMat,datingLabels=file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    m=datingDataMat.shape[0]    
    numTestVecs=int(m*hoRatio)
    errorCount=0.0
    for i in range(numTestVecs):
        classifierResult=classify_kNN(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with: %s,the real answer is: %s" % (classifierResult,datingLabels[i])
        if(classifierResult!=datingLabels[i]):
            errorCount+=1.0
    print "the total error rate is: %f" % (errorCount/float(numTestVecs))
    
def classifyPerson():
    #input返回的是数值类型，如int,float
    #raw_inpout返回的是字符串类型，string类型    
    percentTats=float(raw_input("\npercent of time spent playing video games ?"))
    ffMiles=float(raw_input("frequent flier miles ?"))
    iceCream=float(raw_input("liters of ice cream ?"))
    
    datingDataMat,datingLabels=file2matrix('datingTestSet.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    inArr=array([ffMiles,percentTats,iceCream])
    classifierResult=classify_kNN((inArr-minVals)/ranges,normMat,datingLabels,3)
    print "You will probably like this person: ",classifierResult

#图片转为txt存储，并将结果转化为1行矩阵输出
def pic2txt(infile):
    #flag=1 color pic flag=0 gray pic
    img = imread(infile,0)
    res=resize(img,(32,32),interpolation = INTER_CUBIC)
    pic=array(res)
    #替换数据
    pic=where(pic<=128,1,0)
    #分析文件名称
    infileName=infile.split('.')[0]
    outfile=infileName+'.txt'
    #保存为txt 只保存整数部分，无分隔符
    savetxt(outfile,pic,fmt='%s',delimiter='')
    #展示图片
#    imshow('image',res)
#    waitKey(0)
#    destroyAllWindows()
    
    #转化为一行  
    #pic.shape=1,-1
    pic_trans=pic.reshape((1,-1))
    return pic_trans

#导入txt数据
def txt2vector(filename):
    returnVect=zeros((1,1024))
    fr=open(filename)
    for i in range(32):
        lineStr=fr.readline()
        for j in range(32):
            returnVect[0,32*i+j]=int(lineStr[j])
    fr.close()
    return returnVect

def handwritingClassTest():
    hwLabels=[]
    #获取当前目录下的所有文件名称
    trainingFileList=listdir('trainingDigits')
    m=len(trainingFileList)
    trainingMat=zeros((m,1024))
    for i in range(m):
        fileNameStr=trainingFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:]=txt2vector('trainingDigits/%s'%fileNameStr)
#    testFileList=listdir('testDigits')
#    errorCount=0.0
#    mTest=len(testFileList)
#    for j in range(mTest):
#        testfileNameStr=testFileList[j]
#        fileStr=testfileNameStr.split('.')[0]
#        testclassNumStr=int(fileStr.split('_')[0])
#        vectorUnderTest=txt2vector('testDigits/%s'%testfileNameStr)
#        classifierResult=classify_kNN(vectorUnderTest,trainingMat,hwLabels,3)
#        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, testclassNumStr)
#        if(classifierResult !=testclassNumStr):
#            errorCount+=1.0
#    print "/nthe total number of errors is: %d" % errorCount
#    print "\nthe total error rate is: %f" % (errorCount/float(mTest))
    return trainingMat,hwLabels

if __name__=="__main__":
    trainingMat,hwLabels=handwritingClassTest()
    testfileNameStr='5.jpg'
    vectorUnderTest=pic2txt(testfileNameStr)
    classifierResult=classify_kNN(vectorUnderTest,trainingMat,hwLabels,3)
    print "\nthe classifier came back with: %d, the real answer is: %s" % (classifierResult,testfileNameStr)


#datingClassTest()

    
#group,labels=createDataSet()
#print "\nThe result is ",classify_kNN([1,1],group,labels,3)

#mat,labelVector=file2matrix('datingTestSet.txt')
#normMat,ranges,minVals=autoNorm(mat)
#
##list替换
#rep=['b' if x=='smallDoses' else x for x in labelVector]
#rep=['r' if x=='didntLike' else x for x in rep]
#color=['g' if x=='largeDoses' else x for x in rep]
#
#fig=plt.figure()
#plt.xlabel('Game Time Percent', fontsize=15)
#plt.ylabel('Ice Cream Liter', fontsize=15)
#plt.title('Scatter Diagram', fontsize=20)
#
##These are subplot grid parameters encoded as a single integer. 
##For example, "111" means "1x1 grid, first subplot" and "234" means "2x3 grid, 4th subplot".
##Alternative form for add_subplot(111) is add_subplot(1, 1, 1).
#ax=fig.add_subplot(111)
##x,y,s=area c=color
#x=normMat[:,1]
#y=normMat[:,2]
#ax.scatter(x,y,c=array(color))
#
##legend
#for (i,cla) in enumerate(set(labelVector)):
#    xc = [p for (j,p) in enumerate(x) if labelVector[j]==cla]
#    yc = [p for (j,p) in enumerate(y) if labelVector[j]==cla]
#    cols = [c for (j,c) in enumerate(color) if labelVector[j]==cla]
#    ax.scatter(xc,yc,c=cols,label=cla)
#ax.legend(loc=1)
#
#plt.show()






