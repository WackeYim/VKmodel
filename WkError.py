#_*_coding=UTF-8_*_
#自定义异常类
class WkError(Exception):
    def __init__(self,msg):
        super(WkError,self).__init__()
        self.msg = msg
