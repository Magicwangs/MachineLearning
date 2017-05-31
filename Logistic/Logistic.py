#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 19:13:41 2017

@author: magicwang
"""
import random
import numpy as np
import matplotlib.pyplot as plt

def loadData():
    dataMat = []; labelMat = [];
    with open('./testSet.txt', 'r') as fr:
        for line in fr.readlines():
            arr = line.strip().split("\t")
            dataMat.append([1.0, float(arr[0]), float(arr[1])])
            labelMat.append(int(arr[2]))
    return dataMat, labelMat

def sigmoid(inX):
    return 1.0/(1 + np.exp(-inX))

def grandAscent(dataMatIn, classLabels):
    dataMat = np.array(dataMatIn)
    m, n = np.shape(dataMat)
    labelMat = np.array(classLabels).transpose().reshape((m, 1))
    alpha = 0.001
    maxCycles = 500
    weight = np.ones((n, 1))
    for k in range(maxCycles):
        h = sigmoid(np.dot(dataMat, weight))
        error = (labelMat - h)
        weight += alpha * np.dot(dataMat.transpose(),error)
    h = sigmoid(np.dot(dataMat, weight))
    error = (labelMat - np.round(h))
    return weight, error

def plotBestFit(weight):
    dataMat, labelMat = loadData()
    dataArr = np.array(dataMat)
    n = dataArr.shape[0]
    xcord1 = []; ycord1 = [];
    xcord2 = []; ycord2 = [];
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i, 1]); ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1]); ycord2.append(dataArr[i, 2])
            
    plt.scatter(xcord1, ycord1, c='red', marker='s')
    plt.scatter(xcord2, ycord2, c='blue', marker='o')
    x = np.arange(-3., 3., 0.1)
    x2 = -(weight[0] + weight[1] * x)/weight[2]
    plt.plot(x, x2)
    plt.xlabel("X1"); plt.ylabel("X2")
    plt.show()

def stocGradAscent(dataMatrix, classLabels, numIter=150):
    dataMat = np.array(dataMatrix)
    m, n = np.shape(dataMat)
    alpha = 0.01
    weights = np.ones(n)
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4/(1.0+j+i)+0.0001
            randIndex = int(random.uniform(0,len(dataIndex)))
            index = dataIndex[randIndex]
            h = sigmoid(sum(dataMat[index] * weights)) 
            error = classLabels[index] - h
            weights += alpha * error * dataMat[index]
            del (dataIndex[randIndex])
    return weights

if __name__ == "__main__":
    data, label = loadData()
#    weight, error = grandAscent(data, label)
    weight = stocGradAscent(data, label)
    plotBestFit(weight)