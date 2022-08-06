import json
import MVC


class Service:
    def __init__(self, model: MVC.Model):
        self.model: MVC.Model = model

        self.msg = {'-1': '其他错误', '0': '失败', '1': '成功'}
        self.result = {'data': None, 'msg': self.msg['1'], 'code': 1}

    def insert(self, args, dump=True):
        result = self.result.copy()
        try:
            result['data'] = self.model.insert(args)
        except:
            result['msg'] = self.msg['0']
            result['code'] = 0
        if dump:
            return json.dumps(result, ensure_ascii=False)
        else:
            return result['data']

    def deleteById(self, ids, dump=True):
        result = self.result.copy()
        try:
            result['data'] = self.model.deleteById(ids)
        except:
            result['msg'] = self.msg['0']
            result['code'] = 0
        if dump:
            return json.dumps(result, ensure_ascii=False)
        else:
            return result['data']

    def updateById(self, ids, attrs, dump=True):
        result = self.result.copy()
        try:
            result['data'] = self.model.updateById(ids, attrs)
        except:
            result['msg'] = self.msg['0']
            result['code'] = 0
        if dump:
            return json.dumps(result, ensure_ascii=False)
        else:
            return result['data']

    def list(self, attrs=None, val=None, dump=True, isLike=False):
        result = self.result.copy()
        try:
            result['data'] = self.model.select(attrs, val, True, isLike)
        except:
            result['msg'] = self.msg['0']
            result['code'] = 0
        if dump:
            return json.dumps(result, ensure_ascii=False)
        else:
            return result['data']

    def getById(self, ids, dump=True):
        result = self.result.copy()
        try:
            result['data'] = self.model.selectById(ids)
        except:
            result['msg'] = self.msg['0']
            result['code'] = 0
        if dump:
            return json.dumps(result, ensure_ascii=False)
        else:
            return result['data']

    def isExist(self, attrs):
        result = self.model.select(attrs=attrs, mult=True)
        return result[0]['id'] if result else False
