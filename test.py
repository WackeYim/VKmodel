
import re
#测试动态正则表达式
# star = '*'
# end = '#'
# # reg = r'\*((?:.|\n)*?)\#'   #提取* 和 #之间的字符串
# reg0 = '((?:.|\n)*?)'
# reg1 = '\\' + star + reg0 + '\\' + end
# print('reg1='+reg1)
# reg = re.compile(r''+reg1+'')   

# data = 'MAER417'
# regstr= re.findall(reg,data)

# print('reg = ' + str(regstr))

#测试eval
# st = '[0:2]'
# strs = 'ABC,DEFG'
# # a = eval('strs'+st)
# # print('a = '+a)

# def _find(s):
#     if s.startswith('['):
#         st = eval('strs'+s)
#     else:

#         reg0 = '(.+?)' + s
#         reg = re.compile(r''+reg0+'')
#         st = re.findall(reg,strs)[0]
#     return st

# # sta = '_find(\',\')'
# sta = '_find(\'[0:2]\')'
# b = eval(sta)
# # b = re.split(r'[?|,]',strs)
# print('b='+str(b))

#测试异常
# class Test1(object):
#     	def init(self, switch):
# 		    self.switch = switch #开关
# 		def calc(self, a,b):
#             try:
# 				return a/b
# 			except Exception as result:
# 				if self.switch:
# 					print(“捕获开启，已经捕获到了异常，信息如下:”)
# 					print(result)
# 				else:
# 					#重新抛出这个异常，此时就不会被这个异常处理给捕获到，从而触发默认的异常处理
# 					raise

# import re
# import os
# class ExistsError(Exception):
#     pass
# class KeyInvalidError(Exception):
#     pass
# def fun(path,mnk):
#     """
#     去path路径的文件中，找到前缀为prev的一行数据，获取数据并返回给调用者。
#         1000,成功
#         1001,文件不存在
#         1002,关键字为空
#         1003,未知错误
#         ...
#     :return:
#     """
#     response = {'code': 1000, 'data': None}
#     try:
#         with  open(path,encoding="utf-8") as f1:
#             line=f1.readline()
#             str = re.match("mnk", line)
#         if not os.path.exists(path):
#             raise Exception() #抛出的是ExistsError类的一个实例
#         if not str:
#             raise KeyInvalidError()
 
#     except ExistsError as e:                #下面的捕获异常是逐行往下匹配的，只要捕获到异常就不往下执行了
#         response['code']=1003               #捕获异常以后可以做一些自己定义的东西
#         print(response['code'])
#     except Exception as e:                  #**自己定义多个异常类名的目的就是将来区分不同的错误类型，再没有别的意思
#         response['code'] = 1004
#         print(response['code'])
# fun(r"E:\day26\s15day26\test", "p")

# 测试提取多个括号的内容
# strs = '(&A0732142233550011405829060520190600&B0000000000) (&A0732142233550011405829060520190600&B0000000000) (&A0732142233550011405829060520190600&B0000000000)'
# reg0 = r'\((.*?)\)'
# extrama = re.findall(reg0, strs)
# print(extrama)

# ss = 'AB,142587'
# sp = ss.split(',')
# print('sp = '+str(sp))

# sc = re.split(r'[?|,]',ss)
# print('sc = '+str(sc))

#测试时间字符串和时间戳转换
import time
# a = '2019-07-12 16:42:35'
# b = int(time.mktime(time.strptime(a,"%Y-%m-%d %H:%M:%S")))
# print(b)

# # 字符串中提取日期时间
# import dateutil.parser as dparser
# s = dparser.parse("monkey 2010-07-10 12:35:24 love banana")
# print(s)

#替换字符串中的日期时间为时间戳
# def replace(x):
#     def _replace(matched):
#         m = matched.group()
#         _m = str(int(time.mktime(time.strptime(m,"%Y-%m-%d %H:%M:%S"))))
#         change = re.sub(r'+m+', '0000', m)
#         return change

#     pattern = r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})"
#     r = re.sub(pattern, _replace, x)
#     return r

# def wk(matched):
#     m = matched.group()
#     _m = str(time.mktime(time.strptime(m,"%Y-%m-%d %H:%M:%S")))
#     return _m

# a = 'abcd|efgh,2019-07-12 16:42:35'
# pattern = r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})"
# r = re.sub(pattern, wk, a)

# print(r)
# _date_all = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})",a)
# for _date in _date_all :
#     b = int(time.mktime(time.strptime(_date,"%Y-%m-%d %H:%M:%S")))
#     print(b)

# def replace(x):
#     def _replace(matched):
#         m = matched.group()
#         change = re.sub("\d", '0', m)
#         return change

#     pattern = "#((\d*\.)+\d+)#"
#     r = re.sub(pattern, _replace, x)
#     return r

# x = "ab.c.d.#1.0.3.4# 2.2.2asdf"
# r = replace(x)

# print (x)
# print (r)
# rx = |
# _parameter[0] = 18952703264|18952702453
# 正则字符串中的符号
# a = '18952703264|18952702453'
# pattern = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]") # 匹配不是中文、大小写、数字的其他字符
# rx = re.findall(pattern,a)
# rc = r'['+rx[0]+']'
# r = re.split(rc,a)
# print(r)

#正则&和字母开头的字符串
a = 'abc12&A001245'
pattern = r'^&'

list1 = ['physics', 'chemistry', 1997, 2000]
print('list = ')
print(list1[1:])
					
