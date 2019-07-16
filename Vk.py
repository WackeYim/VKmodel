#coding=utf-8
import Baseclass 
import re,os,time,sys,json
import WkError

class Vk(Baseclass.Baseclass):
    def __init__(self):
        super().__init__()
        self.__config__ = {}
        self.__extraconfig__ = {}
        self.__read_defaults_file__("ta.json","extradata.json")
    #读配置文件
    def __read_defaults_file__(self,fileName1,fileName2):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.abspath(root_dir+"/"+fileName1)
        if os.path.exists(path):
            with open(path, "r",encoding='utf-8') as f:
                self.__config__  = json.load(f)
                f.close()
        else:
            raise WkError.WkError("缺少JSON文件")
              
        #加载附加指令配置文件
        epath = os.path.abspath(root_dir+"/"+fileName2)
        if os.path.exists(epath):
            with open(epath, "r",encoding='utf-8') as f2:
                self.__extraconfig__  = json.load(f2)
                f.close()
        else:
            raise WkError.WkError("缺少extra.json文件")  

    def __Wackeval(self,s,d):
        if not s:
            return None
        try:
            if s.startswith('['):
                st = eval('d'+s)
            else:
                reg0 = '(.+?)' + s
                reg = re.compile(r''+reg0+'')
                #没有匹配的情况
                st = re.findall(reg,d)
                if st:
                    st = st[0]
                else:
                    st = d
            return st
        except:
            
            raise WkError.WkError('分隔符错误')

    #替换字符串中的日期时间为时间戳
    def __datereplace(self,x):
        def _replace(matched):
            m = matched.group()
            _m = str(int(time.mktime(time.strptime(m,"%Y-%m-%d %H:%M:%S"))))
            return _m
        pattern = r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})"
        r = re.sub(pattern, _replace, x)
        return r
    #提取字符串中的符号
    def __getsep(self,x):
        pattern = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^.^-]") # 匹配不是中文、大小写、数字的其他字符
        r = re.findall(pattern,x)
        return r

    #解析数据payload
    def __parsing_data__(self,payload):
        _typecode = payload[0:1]
        _typekey  = payload[1:2]
        _datas = re.split(r'[&]',payload[2:])
        #数据(不含附加参数,即数据+参数)
        _dvdata = _datas[0]
        #附加参数
        _extradata = _datas[1:]
        _basedata = _basedataval = _explain = new_para = None
        try:
            _tmp = self.__config__.get(_typecode).get(_typekey)
            _explain = _tmp.get('explain')
        except:
            raise WkError.WkError('JSON文件未找到对应的功能类型或功能键')
        try:
            if _tmp :
                if _tmp.get('sep'):
                    _basedata = self.__Wackeval(_tmp.get('sep'),_dvdata)
                    _surdata = super()._delete_substr(_dvdata,_basedata) #提取basedata后剩余的字符串，参数
                    _parameterdata = self.__datereplace(_surdata) #参数中的日期时间转为时间戳
                
            else:
                raise WkError.WkError('JSON文件未找到对应的功能键')
            if _tmp.get('vals'):
                if isinstance(_tmp.get('vals'),dict):
                    _basedataval = _tmp.get('vals').get(_basedata)
                elif isinstance(_tmp.get('vals'),str):
                    _basedataval = _tmp.get('vals')

            #处理参数
            #TODO 待验证
            _parameterconfig = _tmp.get('parameter')
            if _parameterconfig:
                _par_sep = _parameterconfig.get('sep')  #参数分隔符
                #根据不同分隔符执行不同的提取方法
                if _par_sep == ',' :
                    _parameter = re.split(r'[,]',_parameterdata)
                elif _par_sep == '()' :
                    _parameter = re.findall(r'\((.*?)\)', _parameterdata)
                else:
                    raise WkError.WkError('未定义的参数分隔符')

                #继续解析参数内容
                if _parameterconfig.get('vals') and _parameter :
                    #遍历参数，分别提取分隔符.这里对JSON定义的参数分隔符分出来的list继续分隔
                    #2019-07-15 貌似没必要全分，只有3.2.1.7要处理一下
                    # for x in range(len(_parameter)):
                    #     x_sep = self.__getsep(_parameter[x])
                    #     for r in x_sep:
                    #         rx = r'['+r+']'
                    #         x_re_split = re.split(rx,_parameter[x])  
                    #         #x_re_split是list，只取第2项。3.2.1.7
                    #         if isinstance(x_re_split,list) :
                    #             _parameter[x] = x_re_split[1]
                    #         else:
                    #             _parameter[x] = x_re_split
                    for x in range(len(_parameter)) :
                        x_re_split = re.split(r'[:]',_parameter[x])  
                        if len(x_re_split) > 1 :
                            _parameter[x] = x_re_split[1]
                        else:
                            _parameter[x] = x_re_split[0]
                            
                    new_para = dict(zip(_parameterconfig['vals'],_parameter))
                    # print('new_para = '+str(new_para))
                elif (not _parameterconfig.get('vals')) and _parameter :
                    #没有配置项，直接将参数转成dict
                    _new_para = {}
                    for index,item in enumerate(_parameter):
                        _new_para[index] = item
                    new_para = _new_para
                

        except:
            raise 

        #返回结果，暂定
        _result = {'funckey':_typecode+_typekey,'explain':_explain,'data':_basedata,"title":_basedataval,"parameter":new_para}
        return {'payload':_result,'extradata':_extradata}
    #解析附加数据
    def __parsing_extra__(self,extradata):
        _extradata = {}
        if extradata == None:
            return None
        if isinstance(extradata,list) :
            for x in extradata:
                _extkey = x[0:1]   #关键字
                _extdata = x[1:]   #数据
                _extkey_json = self.__extraconfig__.get(_extkey)
                if _extkey_json :
                    _funckey = _extkey_json.get('explain')
                    # if _extkey_json.get('valtype') == 'str' :
                    #     _extvals = _extkey_json.get('vals')
                    #     for val in _extvals :
                    #         _s = eval('_extdata'+val['lens'])
                    #         _k = val['dic']
                    #         _ex = {_k:_s}
                    #         _extradata.update(_ex)
                    # elif _extkey_json.get('valtype') == 'dict' :
                    #     _sep = _extkey_json.get('sep')
                    #     _ext = self.__Wackeval(_sep,_extdata)
                    _sep = _extkey_json.get('sep')
                    if _sep and _sep != '' :
                        _ext = self.__Wackeval(_sep,_extdata)
                        _extval = _extkey_json.get('vals').get(_ext)
                        if not _extval or _extval == '':
                            _extval = super()._delete_substr(_extdata,_ext)
                    else:
                        _extval = _extkey_json.get('vals')
                        if isinstance(_extval,dict) :
                            for ex in _extval:
                                _extval[ex] = self.__Wackeval(_extval[ex],_extdata)

                        
                    _ex = {_funckey:_extval}
                    _extradata.update(_ex)
                        
            # print(_extradata)
            return _extradata



    #入口方法
    def decode(self,data):
        try:
            super().__checkdata__(data)
            headers = super().__get_header_payload__(',')
            ds = self.__parsing_data__(headers['payload'])
            payload = ds['payload']
            extradata = {'extradata':self.__parsing_extra__(ds['extradata'])}
            payload.update(extradata)
            #解析包数据
            decodedata = {'Header':headers['head'],
                          'Payload': payload
                        }
            return decodedata

        except:
            raise
            
        # header = self.__get_header__()
        # print('header = ')
        # print(header)

#testtesttest


