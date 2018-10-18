#人脸分离保存（检测被检测的图片）
import os
import cv2
from PIL import Image,ImageDraw
from datetime import datetime
import time
import dlib
from skimage import io
#detectFaces()返回图像中所有人脸的矩形坐标（矩形左上、右下顶点）
#使用haar特征的级联分类器haarcascade_frontalface_default.xml，在haarcascades目录下还有其他的训练好的xml文件可供选择。
#注：haarcascades目录下训练好的分类器必须以灰度图作为输入。
dector=dlib.get_frontal_face_detector()
class DlibResnet_face_dectecting_Save_class():
    def __init__(self):
        pass
    def detectFaces(self,image_name):
        img = cv2.imread(image_name)
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")#opencv训练好的模型
        if img.ndim == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img #if语句：如果img维度为3，说明不是灰度图，先转化为灰度图gray，如果不为3，也就是2，原图就是灰度图
 
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)#1.3和5是特征的最小、最大检测窗口，它改变检测结果也会改变
        result = []
        for (x,y,width,height) in faces:
            result.append((x,y,x+width,y+height))
        return result
    #保存人脸图
    def saveFaces(self,image_name,str_lab):
        """将检测到的人脸保存到add_sql目录下"""
        #global index
        faces = self.detectFaces(image_name)
        if faces:
            #将人脸保存在save_dir目录下。
            #Image模块：Image.open获取图像句柄，crop剪切图像(剪切的区域就是detectFaces返回的坐标)，save保存。
            save_dir ="add_sql"
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            for (x1,y1,x2,y2) in faces:
                file_name = os.path.join(save_dir,str_lab+".jpg")
                Image.open(image_name).crop((x1,y1,x2,y2)).save(file_name)
                return True
 
#开发代码的测试
if __name__=="__main__":
	temp=DlibResnet_face_dectecting_Save_class()
	temp.detectFaces("1.jpg")#检测图片中的人脸
