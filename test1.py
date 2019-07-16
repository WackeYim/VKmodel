#coding=utf-8
import Vk
import re
import wkprint
from json import dumps

Vkdata = Vk.Vk()
data0 = '*VK20113800138000,AA0&A0732142233550011405829060520190600&B0000000000#@用例3.2.1.1'  #A类有数据(预)，无参数，有附加数据
data1 = '*VK20113800138000,AB&A0732142233550011405829060520190600&B0000000000#@用例3.2.1.2'   #A类无数据，无参数，有附加数据
data2 = '*VK20013800138000,AK00,S:V2.2.6,H:MX004-A,0000,2800,LFVBA24B313010396#@用例3.2.1.7'  #A类有数据（预），有参数，无附加
data3 = '*VK20013800138000,AU13800138000#@用例3.2.1.9'                                        #A类有数据（自），无参数，无附加
# #B类
dataB0 = '*VK20113800138000,BB3(&A0732142233550011405829060520190600&B0000000000)(&A1732142233550011405829060520190600&B0000000000)(&A2732142233550011405829060520190600&B0000000000)#@用例3.2.2.2'
dataB1 = '*VK20113800138000,BG&24664,18952703264|189527032414|189527031232|-18952702453,2015-12-03 14:24:32#@用例3.2.2.3'
dataB2 = '*VK20113800138000,BQ&number:5,222.76.219.174:20000;222.76.219.175:20000;211.139.145.129:10000;121.10.106.128:20000;119.47.85.69:20009#@用例3.2.2.4'
dataB3 = '*VK201123456789012347,BM(0x00470050005363d0793a003a60a8768472318f66542f52a8ff01)(101800589)(LSGPC52U6AF102554)(0x00470050005363d0793a003a60a8768472318f66542f52a8ff01)#@用例3.2.2.5'
# D类
dataD1 = '*VK201123456789012347,DO&VVKEL_MT6260D_1V0,0000_2015/01/15,VKEL_T7_20140115,0100#@用例3.2.3.1'
# G类
dataG1 = '*VK20113800138000,GC24664,18952703264|18952702453,2015-12-03 14:24:32&T0001#@用例3.2.4.3'


data = [data0,data1,data2,data3,dataB0,dataB1,dataB2,dataB3,dataD1,dataG1]
# data = [datax0]
for x in data:
    stc = re.split(r'[@]',x)
    print('\n收到的数据：（'+ stc[1]+'）')
    print("\t",str(stc[0]))
    try:
        vkcall = Vkdata.decode(x)
        afterdata = dumps(vkcall,ensure_ascii=False,indent=4)
        print('\n转换后的数据：')
        print(afterdata)
    except Exception as err:
        error = err.msg
        print ('error : '+str(error))


# _prodata = '3(&A0732142233550011405829060520190600&B0000000000)(&A0732142233550011405829060520190600&B0000000000)(&A0732142233550011405829060520190600&B0000000000)'
# _prodata = '00&A0732142233550011405829060520190600&B0000000000'
# _prodata = '0'
# _prodata = '(0x00470050005363d0793a003a60a8768472318f66542f52a8ff01)(101800589)(LSGPC52U6AF102554)'
# _prodata = 'AK00,S:V2.2.6,H:MX004-A,0000,2800,LFVBA24B313010396'
# try:
#     rg0 = r'(.*?)\((.*)\)(.*?)'
#     # rg1 = r'.*(\(.*\)).*'
#     extrama = list(re.match(rg0,_prodata).groups())
#     _parameter = None
#     _extr = extrama
#     del _extr[0]
# except:
#     extrama = re.split(r'[?|&]',_prodata)
#     _parameter = None
#     _extr = extrama
#     del _extr[0]
# if len(extrama) < 2:
#     extrama = re.split(r'[?|,]',_prodata)
#     _parameter = extrama
#     del _parameter[0]
#     _extr = None   
# _basedata = extrama[0]

# print(len(extrama))
# print(type(extrama))
# _basedata = _parameter = None
# _par = ''
# for x in range(len(extrama)):
#     if x == 0:
#         _basedata = extrama[0]
#     else:
#         if extrama[x]:
#             _par += extrama[x]
# _parameter = _par

# print('_basedata = '+ str(_basedata))
# print('_parameter = ' + str(_parameter))
# print('extra = '+ str(_extr))