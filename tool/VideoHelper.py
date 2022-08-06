import time

import cv2
from PyQt5.QtGui import QImage, QPixmap

import tool


class CameraReader:
    def __init__(self, code, flip=True):
        self.code = code
        self.flip = flip
        begTime = time.time()
        self.cap = cv2.VideoCapture(self.code)
        if not self.cap.isOpened():
            tool.Tools.logFormat(tool.Tools.WARN, f'摄像头{self.code} 打开失败')
            exit(0)
        else:
            tool.Tools.logFormat(tool.Tools.INFO, f'耗时 {round(time.time() - begTime, 4)} 摄像头{self.code} 打开成功')

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.showInfo()

    def showInfo(self):
        tool.Tools.logFormat(tool.Tools.INFO,
                             f'摄像头{self.code}\t帧率：{round(self.fps, 2)}\t大小：({self.width}x{self.height})')

    def readCamera(self, picSize=None, show=True):
        ret, frame = self.cap.read()
        if not ret:
            tool.Tools.logFormat(tool.Tools.WARN, f'摄像头 {self.code} 访问失败')

        img_save = cv2.flip(frame, 1)

        if picSize:
            img_save = cv2.resize(img_save, picSize)

        cv2.waitKey(1)

        if show:
            img_show = cv2.cvtColor(cv2.flip(img_save, 1), cv2.COLOR_BGR2RGB)
            img_show = QImage(img_show, img_save.shape[1], img_save.shape[0], QImage.Format_RGB888)
            img_show = QPixmap(img_show).scaled(img_save.shape[1], img_save.shape[0])
        else:
            img_show = None

        return img_save, img_show

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()


class VideoWriter:
    def __init__(self, path, form=None, fps=None, size=None, cap: CameraReader = None):
        self.path = path
        self.form = form
        if cap:
            self.fps = cap.fps
            self.size = (cap.width, cap.height)
        else:
            self.fps = fps
            self.size = size

        self.videoForm = None
        if form == "mp4":
            self.videoForm = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        elif form == "avi":
            self.videoForm = cv2.VideoWriter_fourcc('m', 'j', 'p', 'g')
        else:
            tool.Tools.logFormat(tool.Tools.WARN, f'{form} 暂未开发')
            self.videoForm = form
        self.videoWriter = cv2.VideoWriter(self.path, self.videoForm, self.fps, self.size)

    def saveFigByImg(self, img):
        _img = cv2.resize(img, self.size)
        self.videoWriter.write(_img)

    def saveFigByReadCam(self, cap: CameraReader):
        # 暂时用不上，先写个接口
        ...

    def save(self):
        self.videoWriter.release()
