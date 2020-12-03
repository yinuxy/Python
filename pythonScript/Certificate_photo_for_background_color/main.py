#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/8/21 12:22
# @Author : LYX-夜光

from PyQt5 import QtWidgets, QtGui
from PIL import Image, ImageQt
import math

class Photo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindow()

    def setWindow(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()  # 显示器屏幕
        self.winWidth, self.winHeight = screen.width() / 1.5, screen.height() / 1.5
        self.resize(self.winWidth, self.winHeight)  # 设置窗口大小
        self.setWindowTitle("处理证件照")

        buWidth, buHeight = self.winWidth / 13, self.winHeight / 13  # 按钮大小
        # 打开图片按钮
        button1 = QtWidgets.QPushButton("打开", self)
        button1.resize(buWidth, buHeight)
        button1.clicked.connect(self.getPhoto)
        # 保存图片按钮
        button2 = QtWidgets.QPushButton("保存", self)
        button2.resize(buWidth, buHeight)
        button2.move(buWidth, 0)
        button2.clicked.connect(self.setPhoto)
        # 参数文本框
        self.text1 = QtWidgets.QPlainTextEdit(self)
        self.text1.setPlaceholderText("像素宽度(默认319)")
        self.text1.resize(buWidth, buHeight)
        self.text1.move(buWidth * 2, 0)

        self.text2 = QtWidgets.QPlainTextEdit(self)
        self.text2.setPlaceholderText("像素高度(默认449)")
        self.text2.resize(buWidth, buHeight)
        self.text2.move(buWidth * 3, 0)

        self.text3 = QtWidgets.QPlainTextEdit(self)
        self.text3.setPlaceholderText("dpi(默认350)")
        self.text3.resize(buWidth, buHeight)
        self.text3.move(buWidth * 4, 0)
        # 裁剪按钮
        button3 = QtWidgets.QPushButton("裁剪预览", self)
        button3.resize(buWidth, buHeight)
        button3.move(buWidth * 5, 0)
        button3.clicked.connect(self.crop)
        # 中点x坐标
        self.text4 = QtWidgets.QPlainTextEdit(self)
        self.text4.setPlaceholderText("中心x坐标")
        self.text4.resize(buWidth, buHeight)
        self.text4.move(buWidth * 6, 0)

        self.text5 = QtWidgets.QPlainTextEdit(self)
        self.text5.setPlaceholderText("左下x坐标")
        self.text5.resize(buWidth, buHeight)
        self.text5.move(buWidth * 7, 0)

        self.text6 = QtWidgets.QPlainTextEdit(self)
        self.text6.setPlaceholderText("左下y坐标")
        self.text6.resize(buWidth, buHeight)
        self.text6.move(buWidth * 8, 0)
        # 修改底色
        button3 = QtWidgets.QPushButton("红色", self)
        button3.resize(buWidth, buHeight)
        button3.move(buWidth * 9, 0)
        button3.clicked.connect(lambda: self.editBackground((255, 0, 0)))

        button4 = QtWidgets.QPushButton("蓝色", self)
        button4.resize(buWidth, buHeight)
        button4.move(buWidth * 10, 0)
        button4.clicked.connect(lambda: self.editBackground((67, 142, 219)))

        button5 = QtWidgets.QPushButton("白色", self)
        button5.resize(buWidth, buHeight)
        button5.move(buWidth * 11, 0)
        button5.clicked.connect(lambda: self.editBackground((255, 255, 255)))
        # 使用说明
        button6 = QtWidgets.QPushButton("使用说明", self)
        button6.resize(buWidth, buHeight)
        button6.move(buWidth * 12, 0)
        button6.clicked.connect(self.description)

        # 子窗口大小
        self.swinWidth, self.swinHeight = self.winWidth / 2, self.winHeight - buHeight
        # 左侧子窗口原照片
        self.subwindow1 = QtWidgets.QPlainTextEdit(self)
        self.subwindow1.resize(self.swinWidth, self.swinHeight)
        self.subwindow1.move(0, buHeight)
        self.subwindow1.setPlaceholderText("原照片")
        # 右侧子窗口预览处理后的照片
        self.subwindow2 = QtWidgets.QPlainTextEdit(self)
        self.subwindow2.resize(self.swinWidth, self.swinHeight)
        self.subwindow2.move(self.swinWidth, buHeight)
        self.subwindow2.setPlaceholderText("处理后照片预览")

        self.label1 = QtWidgets.QLabel(self.subwindow1)  # 原照片
        self.label1.mousePressEvent = self.getPhotoPos
        self.label2 = QtWidgets.QLabel(self.subwindow2)  # 处理后照片预览

    # 获取图片的坐标
    def getPhotoPos(self, event):
        try:
            x_cen = float(self.text4.toPlainText().strip())
        except:
            x_cen = -1
        try:
            x_left = float(self.text5.toPlainText().strip())
        except:
            x_left = -1
        try:
            y_down = float(self.text6.toPlainText().strip())
        except:
            y_down = -1
        if x_cen < 0:
            self.text4.setPlainText(str(event.x()))
        else:
            if x_left < 0:
                self.text5.setPlainText(str(event.x()))
            if y_down < 0:
                self.text6.setPlainText(str(event.y()))

    # 打开图片
    def getPhoto(self):
        self.openFile = QtWidgets.QFileDialog.getOpenFileName()[0]  # 打开文件获取链接
        if not self.openFile:
            return
        pix = QtGui.QPixmap(self.openFile)
        self.oriPhoWidth, self.oriPhoHeight = pix.width(), pix.height()
        widPerHei = self.oriPhoWidth / self.oriPhoHeight  # 照片的宽高比
        margin = 10  # 与方框的最小间隔
        # 重设照片的宽和高
        self.phoWidth = self.swinWidth - margin
        self.phoHeight = self.phoWidth / widPerHei
        # 若照片高度超出显示宽，则再重新设置宽高
        if self.phoHeight > self.swinHeight - margin:
            self.phoHeight = self.swinHeight - margin
            self.phoWidth = self.phoHeight * widPerHei
        self.label1.move((self.swinWidth - self.phoWidth) / 2, (self.swinHeight - self.phoHeight) / 2)
        self.label1.setPixmap(QtGui.QPixmap())
        self.label1.setPixmap(pix)
        self.label1.resize(self.phoWidth, self.phoHeight)
        self.label1.setScaledContents(True)  # 图片自适应

        self.text4.setPlainText("")
        self.text5.setPlainText("")
        self.text6.setPlainText("")
    # 裁剪图片
    def crop(self):
        try:
            width = int(self.text1.toPlainText().strip())
            height = int(self.text2.toPlainText().strip())
        except:
            width, height = 319, 449
        try:
            x_cen = float(self.text4.toPlainText().strip())
            x_left = float(self.text5.toPlainText().strip())
            y_down = float(self.text6.toPlainText().strip())
        except:
            QtWidgets.QMessageBox.about(self, "操作错误", "请先填写相应的坐标！")
            return
        width_mul, height_mul = self.oriPhoWidth / self.phoWidth, self.oriPhoHeight / self.phoHeight
        x_cen, x_left, y_down = x_cen*width_mul, x_left*width_mul, y_down*height_mul
        self.img = Image.open(self.openFile)
        newW = (x_cen - x_left) * 2  # 裁剪图的宽
        newH = height / width * newW  # 裁剪图的高
        self.img = self.img.crop((x_left, y_down - newH, x_left + newW, y_down))  # 裁剪
        self.img = self.img.resize((width, height))  # 重设大小
        self.previewPhoto()

    # 预览图片
    def previewPhoto(self):
        pix = ImageQt.toqpixmap(self.img)
        self.label2.move((self.swinWidth - pix.width()) / 2, (self.swinHeight - pix.height()) / 2)
        self.label2.setPixmap(QtGui.QPixmap())
        self.label2.setPixmap(pix)
        self.label2.resize(pix.width(), pix.height())
        self.label2.setScaledContents(True)  # 图片自适应

    # 保存图片
    def setPhoto(self):
        self.saveFile = QtWidgets.QFileDialog.getSaveFileName()[0]
        if not self.saveFile:
            return
        try:
            dpi = float(self.text3.toPlainText().strip())
        except:
            dpi = 350
        self.img.save(self.saveFile, dpi=(dpi, dpi))
        self.img.close()

    # 换底色
    def editBackground(self, color):
        try:
            imgData = list(self.img.getdata())
            width, height = self.img.size
        except:
            QtWidgets.QMessageBox.about(self, "操作错误", "请先裁剪预览照片！")
            return
        newData = imgData.copy()
        newData[0] = newData[width-1] = color
        # 修改边缘像素点
        for x in range(1, int(width/2)+1):  # 图像的x坐标
            if self.colorEqual(imgData[x], imgData[0]):
                newData[x] = color
        for x in range(width-2, int(width/2), -1):
            if self.colorEqual(imgData[x], imgData[width-1]):
                newData[x] = color
        left_down, right_down = 0, 0
        for y in range(1, height):
            if self.colorEqual(imgData[y*width], imgData[0]):
                newData[y*width] = color
            else:
                left_down = y
                break
        for y in range(1, height):
            if self.colorEqual(imgData[(y+1)*width-1], imgData[width-1]):
                newData[(y+1)*width-1] = color
            else:
                right_down = y
                break
        # 修改非边缘像素点
        for y in range(1, left_down):
            for x in range(1, int(width/2)+1):
                if self.colorEqual(imgData[y*width+x], imgData[y*width]):
                    newData[y*width+x] = color
                else:
                    break
        for y in range(1, right_down):
            for x in range(width-2, int(width/2), -1):
                if self.colorEqual(imgData[y*width+x], imgData[(y+1)*width-1]):
                    newData[y*width+x] = color
                else:
                    break
        # 精修像素点
        k = 100
        for y in range(1, left_down):
            for x in range(1, int(width/2)+1):
                index = y * width + x
                if newData[index] != color and (newData[index-1] == color or
                    newData[index+1] == color or newData[index-width] == color or
                    newData[index+width] == color):
                    if self.colorEqual(imgData[index], imgData[0], k):
                        newData[index] = color
        for y in range(1, right_down):
            for x in range(width - 2, int(width / 2), -1):
                index = y * width + x
                if newData[index] != color and (newData[index-1] == color
                    or newData[index+1] == color or newData[index-width] == color or
                    newData[index+width] == color):
                    if self.colorEqual(imgData[index], imgData[width-1], k):
                        newData[index] = color

        self.img.putdata(newData)
        pix = ImageQt.toqpixmap(self.img)
        self.label2.move((self.swinWidth - pix.width()) / 2, (self.swinHeight - pix.height()) / 2)
        self.label2.setPixmap(QtGui.QPixmap())
        self.label2.setPixmap(pix)
        self.label2.resize(pix.width(), pix.height())
        self.label2.setScaledContents(True)  # 图片自适应

    def colorEqual(self, A, B, k=60):
        dist = math.sqrt(sum([(a - b) ** 2 for (a, b) in zip(A, B)]))
        return True if dist < k else False

    # 使用说明
    def description(self):
        QtWidgets.QMessageBox.about(self, "使用说明",
"""1. 点击“打开”按钮打开图片文件
2. 先点击照片中心（即眉心处）获取照片中心x坐标
3. 再点击照片左下角获取裁剪图的左下x和y坐标
4. 可点击“裁剪预览”按钮查看处理后的图片
5. 点击“保存”按钮保存图片""")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    photo = Photo()
    photo.show()
    app.exec_()