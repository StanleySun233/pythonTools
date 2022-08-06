import tool


class Model:
    def __init__(self, table, sqlClient):
        self.table = table
        self.sqlClient: tool.SqliteHelper.SqliteHelper = sqlClient
        self.columns = self.sqlClient.getColumns(self.table)

    def insert(self, args):
        args['id'] = tool.Tools.getTimeStamp()
        self.sqlClient.insertInfo(self.table, args)
        return args['id']

    def deleteById(self, ids):
        self.sqlClient.delInfo(self.table, {'id': ids})
        return ids

    def updateById(self, ids, attrs):
        self.sqlClient.update(self.table, {'id': ids}, attrs)
        return ids

    def select(self, attrs=None, val=None, mult=True, isLike=False):
        res = []
        if val:
            col = val
        else:
            col = self.columns
        data = self.sqlClient.searchInfo(self.table, attrs, val, mult, isLike)
        if len(data) != 0:
            for i in data:
                model = {}
                for j in range(len(col)):
                    model[col[j]] = i[j]
                res.append(model)
        return res

    def selectById(self, ids):
        data = self.sqlClient.searchInfo(self.table, attrs={'id': ids}, mult=False)
        model = {}
        if len(data) != 0:
            model = {}
            for i in range(len(self.columns)):
                model[self.columns[i]] = data[i]
        else:
            for i in range(len(self.columns)):
                model[self.columns[i]] = None
        return model
