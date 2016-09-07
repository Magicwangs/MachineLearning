# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 16:12:47 2016

@author: MagicWang
"""
__author__='MagicWang'

import SqlDB
import argparse

class Standard:
    #__init__构造函数
    def __init__(self,arg,mSqlDB):
        self.arg=arg
        print 'Standard Init !'
        print 'Arg=%s'% self.arg
        
        #判断是否为需要的类
        #利用isinstance函数，来判断一个对象是否是一个已知的类型
        #不能用type，无法判断是否
        if isinstance(mSqlDB,SqlDB.SqlDB):
            print 'This is SqlDB !'

    #__del__析构函数
    def __del__(self):
        print 'Standard End !'
        
    #__str__ 用于print，可读性高   输出print standard可见
    def __str__(self):
        return 'Standard String'
        
    #__repr__ 用于调试者看,更准确  直接输出standard   
    #一般可将__repr__ = __str__
    #When you compute a value in the REPL, 
    #Python calls __repr__ to convert it into a string. 
    #When you use print, however, Python calls __str__.
    def __repr__(self):
        return 'Standard Representation'
    
    def test(self):
        rep=self.__repr__()
        print '__repr__=%s'%rep
        
if __name__=="__main__":
    # 在cmd中输入python standard.py --engine Bing
    parser=argparse.ArgumentParser()
    parser.add_argument(        
        '-e','--engine',  #变量名称由--后面的字符决定
        default='Google',
        help="this is google"
        )
    args=parser.parse_args()
    print args.engine
    
    mSqlDB=SqlDB.SqlDB()
    standard=Standard(1,mSqlDB)
    standard.test()
    
    