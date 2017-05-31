#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 31 15:35:29 2017

@author: magicwang
"""
import numpy as np
from Logistic import *

def classifyVector(inX, weights):
    prob = sigmoid(sum(inX * weights))
    return round(prob)

def colicTest():
    trainSet = []; trainLabel = []
    with open("./horseColicTraining.txt", "r") as fr:
        for line in fr.readlines():
            currentline = line.strip().split("\t")
            lineArr = map(lambda x: float(x), currentline)
            trainSet.append(lineArr[:21])
            trainLabel.append(lineArr[-1])
    trainWeight  = stocGradAscent(trainSet, trainLabel, 500)
    ## test
    errorCount = 0; numTestVec = 0
    with open("./horseColicTest.txt", "r") as fr:
        for line in fr.readlines():
            currentline = line.strip().split("\t")
            lineArr = map(lambda x: float(x), currentline)
            data = np.array(lineArr[:21]); label = int(lineArr[-1])
            if int(classifyVector(data, trainWeight) != label):
                errorCount += 1
            numTestVec += 1
    errorRate = float(errorCount)/numTestVec
    print "the error rate is: %f" % errorRate
    return errorRate

def multiTest():
    numTest = 10;errorSum = 0.
    for k in range(numTest):
        errorSum += colicTest()
    print "after %d iter, average error rate is: %f" % (numTest, errorSum/numTest)

if __name__ == "__main__":
#    colicTest()
    multiTest()