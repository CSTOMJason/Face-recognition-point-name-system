import cv2
import numpy as np
import os
import face_recognition
import dlib
import time
import pymysql
"""实现将目标人脸的特征编码保存到数据库中--->encoding_face()将目标人脸进行编码-->save_encoding_face_to_mysql(encoding_face())
   实现将计算数据库中的人脸编码的总数---就是总的人数-->total_face_encode()
   实现将数据库中的编码的人脸导入到对应的程序中来-->load_face_encoding_from_sql()
   未实现的功能添加目标人脸和删除人脸对数据库中的操作
   
"""
def get_number_id(path):
	t=os.listdir(path)
	number_ids=[]
	for line in t:
		number_ids.append(line[:11])
	return number_ids
class Encoding_mysql():
    """实现将目标人脸的特征编码保存到数据库中--->encoding_face()将目标人脸进行编码-->save_encoding_face_to_mysql(encoding_face())
    实现将计算数据库中的人脸编码的总数---就是总的人数-->total_face_encode()
    实现将数据库中的编码的人脸导入到对应的程序中来-->load_face_encoding_from_sql()
    未实现的功能添加目标人脸和删除人脸对数据库中的操作
    """
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()# 1.加载正脸检测器
        #加载人脸关键点检测器
        self.sp = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        # 3. 加载人脸识别模型
        self.facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
        # 候选人脸描述子list
        self.descriptors = []
    def face_encod(self,img):#人脸特征的编码函数
        dets=self.detector(img,1)#人脸的检测区域大小
        #人脸的特征编码采用resnet（残缺网络）训练好的模型
        for k,d in enumerate(dets):
            shape=self.sp(img,d)
            face_encod=np.array(self.facerec.compute_face_descriptor(img,shape))#人脸的特征编码残缺网络模型
        return face_encod
    #将人脸进行编码
    def encoding_face(self,path):
        """encoding the face for feature's encoding whose shape is (128,)"""
        sql_face_encode=[]
        for per_img in os.listdir(path):
            img=cv2.imread(path+"/"+per_img)
            sql_face_encode.append(self.face_encod(img))
        #print("the sql people's number is ",len(sql_face_encode))
        return sql_face_encode

    #将编码存入到mysql数据库
    def save_encoding_face_to_mysql(self,path):
        """将指定目录下的人脸编码保存到数据库中的sql_face表中"""
        sql_face_encode=self.encoding_face(path)
        number_ids=get_number_id(path)
        cnt=0
        for sql_img in sql_face_encode:
            sql_img=sql_face_encode[cnt].tolist()
            sql_img_str=str(sql_img)
            number_id=number_ids[cnt]
			#number_id=number_ids[cnt]
            conection=pymysql.connect(host="localhost",user="root",password="root")
            with conection.cursor() as cursor:
                cursor.execute("use face_recognition")
                cursor.execute('insert into sql_face(img,stu_id) values("%s","%s")'%(sql_img_str,number_id))
                conection.commit()
            cnt+=1
    #计算mysql中编码的人的个数
    def total_face_encode(self):
        """计算mysql中编码的人的个数"""
        #查询sql中已有的人的总数
        conection=pymysql.connect(host="localhost",user="root",password="root")
        with conection.cursor() as cursor:
            cursor.execute("use face_recognition")
            cursor.execute("select count(*) from sql_face")
            total_num_people=cursor.fetchall()
        return int(total_num_people[0][0])

    #将mysql中的人脸编码导入到程序中
    def load_face_encoding_from_sql(self):
        """将mysql中的人脸编码导入到程序中"""
        #将mysql数据库中的人脸的编码导入到当前的程序
        conection=pymysql.connect(host="localhost",user="root",password="root")
        with conection.cursor() as cursor:
            cursor.execute("use face_recognition")
            cursor.execute("select img from sql_face")
            to_sql_face_encode=cursor.fetchall()
        #将查询出来的元组转换为np.array()的结构
        array_sql_face_encode=[]
        cnt=0
        for per_line in to_sql_face_encode:
            temp=np.array(eval(to_sql_face_encode[cnt][0]))
            array_sql_face_encode.append(temp)
            cnt+=1
        return array_sql_face_encode
#开发测试代码
if __name__=="__main__":
	from pre_sql_face_encode_save_to_mysql_class import Encoding_mysql
	encode_ob=Encoding_mysql()
	encode_ob.save_encoding_face_to_mysql("add_sql")#调用函数是指定文件中的图片编码保存到数据库中
	sql_face_encode=encode_ob.load_face_encoding_from_sql()#将数据库中的编码导入相应的程序中来
	total=encode_ob.total_num_people()#求出数据库编码的总数就是需要匹配人的总数
	
	
	
    