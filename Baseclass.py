#coding=utf-8
import configparser
import re
import os,time,sys
import json
import copy
import WkError
class WackeConfigParser(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)
 
    def optionxform(self, optionstr):
        return optionstr

class Baseclass():
    __instance__ = None
    __CHECK_REGEXP__ = None  #数据合法校验表达式
    __RXD__ = None  #接收的数据
    __error__ = []

    def __init__(self,*args,**kwargs):
        self.__config__ = {
            "BOF":"*",
            "EOF":"/",
            "UDID":"VK",
            "VER":"20",
            "HS":''
        }
         #读配置文件
        self.__read_config_file__("config.conf","head")
        _reg = '\\' + self.__config__['BOF'] + '((?:.|\n)*?)' + '\\' + self.__config__['EOF']
        self.__CHECK_REGEXP__ = re.compile(r''+_reg+'') 

    # 加载配置文件
    def __read_config_file__(self,fileName,section):
       
        root_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.abspath(root_dir+"/"+fileName)
        if os.path.exists(path):
            cnf = WackeConfigParser()
            cnf.read( path )
            options = cnf.options( section )
            for key in options:
                self.__config__[key] = cnf.get( section, key )
        else:
            print("缺少配置文件")
            self.__error__.append( "缺少配置文件")
            raise WkError.WkError(self.__error__)
            # exit()

    #检查数据合法性
    def __checkdata__(self,data):
        if self.__CHECK_REGEXP__ != None:
            _rxd = re.findall(self.__CHECK_REGEXP__,data)
            if _rxd:
                self.__RXD__ = _rxd[0]
            else:
                self.__error__.append("接收的数据不合法")
                raise WkError.WkError(self.__error__)
                # exit()
        else:
            self.__error__.append("合法性检查错误")
            raise WkError.WkError(self.__error__)
            # exit()

    #根据配置文件定义的分隔符返回头部数据
    def __Vkheader(self,s):
        try:
            if s.startswith('['):
                st = eval('self.__RXD__'+s)
            else:
                reg0 = '(.+?)' + s
                reg = re.compile(r''+reg0+'')
                st = re.findall(reg,self.__RXD__)[0]
            return st
        except:
            self.__error__.append("头部分隔符错误")
            raise WkError.WkError(self.__error__)

    #
    def _delete_substr(self,in_str,in_substr):
        if not in_substr:
            return None
        if not in_str:
            in_str = self.__RXD__
        start_loc = in_str.find(in_substr)
        len_substr = len(in_substr)
        res_str = in_str[:start_loc] + in_str[start_loc + len_substr:]
        if res_str[0:1] != ',' :  #.isalnum(): 貌似不能直接判断为字母和数字
            return res_str
        else:
            return res_str[1:]

    
    #获取数据头部和payload
    #parameter: HS = 协议头部分隔符，
    # 上传数据，以","分隔；
    # 下发数据，固定长度，以"[5:7]"截取；
    def __get_header_payload__(self,HS):
        if self.__RXD__ != None :
            _rxheader = self.__Vkheader(HS)
            _payload = self._delete_substr('',_rxheader)
            #处理header，获取属性
            
            _udid = _rxheader[0:2]
            _ver = _rxheader[2:4]
            _reply = _rxheader[4:5]
            _tid = _rxheader[5:]
            _header = {'UDID':_udid,'VER':_ver,'REPLY':_reply,'TID':_tid}
            return {'head': _header,"payload":_payload}
        else:
            self.__error__.append('接收的数据为空')
            raise WkError.WkError(self.__error__)
            