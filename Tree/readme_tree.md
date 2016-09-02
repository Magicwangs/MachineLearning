Q&A:

**Q1**:
`*args` and`**kwargs`?

**A**:

`*args` = list of arguments -as positional arguments

`**kwargs` = dictionary - whose keys become separate keyword arguments and the values become values of these arguments.

see[This For More](http://stackoverflow.com/questions/3394835/args-and-kwargs)


**Q2**:
列表如何完整赋值？

**A**:

treeLabels=Labels只是指向同一内存空间

完整赋值应为：treeLabels=Labels[:]


**Q3**:
如何存储决策树？

**A**:

利用pickle模块，可以保存dict，list，array等多种类型数据
详见[Python官方文档](http://python.usyiyi.cn/python_278/library/pickle.html)


**Q4**:
`f.read()`,`f.readline()`,`f.readlines()`？

**A**:

`read()`每次读取整个文件，它通常用于将文件内容放到一个字符串变量中。然而 .read() 生成文件内容最直接的字符串表示，但对于连续的面向行的处理，它却是不必要的，并且如果文件大于可用内存，则不可能实现这种处理。

`readlines()`自动将文件内容分析成一个行的列表，该列表可以由 Python 的 **for... in ...**结构进行处理

`readline()`每次只读取一行,通常比 .readlines()慢得多。仅当没有足够内存可以一次读取整个文件时，才应该使用.readline()。