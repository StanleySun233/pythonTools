import minio

import tool


class MinioHelper:
    def __init__(self, ip, port, account, password, bucket):
        self.ip = ip
        self.port = port
        self.account = account
        self.password = password
        self.url = '{}:{}'.format(self.ip, self.port)
        self.bucket = bucket
        self.connection: minio.Minio = None

    def setConnection(self):
        try:
            conn = minio.Minio(self.url, self.account, self.password, secure=False)
            self.connection = conn
            tool.Tools.logFormat(tool.Tools.INFO, 'MINIO文件管理系统连接成功')
        except:
            tool.Tools.logFormat(tool.Tools.WARN, 'MINIO文件管理系统连接失败')
            exit(0)

        try:
            if not self.connection.bucket_exists(self.bucket):
                self.connection.make_bucket(self.bucket)
            else:
                tool.Tools.logFormat(tool.Tools.INFO, 'MINIO文件管理系统初始化成功')
        except:
            tool.Tools.logFormat(tool.Tools.WARN, 'MINIO文件管理系统创建桶失败')
            exit(0)

    def uploadFileByUrl(self, name):
        return self.connection.presigned_put_object(self.bucket, name)

    def downloadFileByUrl(self, name):
        return self.connection.presigned_get_object(self.bucket, name)