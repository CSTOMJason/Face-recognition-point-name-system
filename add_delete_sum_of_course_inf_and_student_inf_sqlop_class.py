#1添加学生----》人脸到facesql文件夹
import os
import cv2
import shutil#图片的移动
import pymysql
from DlibResnet_face_recognition_class import DlibResnet_face_recognition_class#对add_sql中的图片进行特征编码检测
from DlibResnet_face_dectecting_Save_class import DlibResnet_face_dectecting_Save_class#对输入的图片进行人脸检测和保存到add_sql
class1=DlibResnet_face_recognition_class()
class2=DlibResnet_face_dectecting_Save_class()

class add_delete_sum_of_course_inf_and_student_inf_sqlop():
    """添加和删除人脸图片对应的数据库中的表信息的变化"""
    def __init__(self):
        print("请将添加的图片加入到raw_pic的文件夹中注意图片是（学号+姓名.jpg)!")
    def check_detect_encode(self):
        """检测raw_pic中的人脸是否满足能被检测和能被编码
        return 没有被检测or编码成功的人脸的信息"""
        bad_pics=[]
        #for line in os.listdir("raw_pic"):
         #   if not class2.saveFaces("raw_pic"+"/"+line,line[:len(line)-4]):#检测通过？
          #      bad_pics.append(line)#保存检测人脸没通过
        for line in os.listdir("add_sql"):
            t=class1.face_encod(cv2.imread("add_sql/"+line))
            if not t.shape==(128,) or t.shape==(3,):#编码通过？
                bad_pics.append(line)
        #删除raw_pic下的图片
        for line in os.listdir("raw_pic"):
            os.remove("raw_pic/"+line)
        return bad_pics
    #将add_sql文件夹中的图片移动到facesql中并且获取移动图片的学号+姓名
    def move_and_get_inf(self):
        """将add_sql中的干净的图片保存到facesql目录下"""
        stus_inf=[]
        if not os.listdir("facesql")==[]:
            for line in os.listdir("facesql"):
                os.remove("facesql/"+line)
        for line in os.listdir("add_sql"):
            shutil.move("add_sql/"+line,"facesql/")
            stus_inf.append(line[:len(line)-4])#保存添加的学生的信息
        return stus_inf
    #对数据库进行跟新
    def update_sql(self,stus_inf):
        """将加入的人的信息保存到数据库中的student_inf和course_inf表中"""
        connection=pymysql.connect(host="localhost",user="root",password="root")
        with connection.cursor() as cursor:
            cursor.execute("use face_recognition")
            for line in stus_inf:
                cursor.execute("insert into student_inf values('%s','%s')"%(line[:11],line[12:]))
                cursor.execute("insert into course_inf(id_stu) values('%s')"%(line[:11]))
            connection.commit()
    #对数据库中进行添加是后在add_sql下一步将要添加到facesql中的图片特征编码保存到数据库sql_face中
    def insert_encode_to_sql_face(self):
        """将要保存到facesql中的图片在add_sql中编码保存到数据库中的sql_face表
        这而的path用户输入默认是add_sql目录"""
        from pre_sql_face_encode_save_to_mysql_class import Encoding_mysql
        encode_ob=Encoding_mysql()
        path=input("请输入图片的路径!")
        encode_ob.save_encoding_face_to_mysql(path)
    #删除某些学生的记录sql_face->course_inf->student_inf->本地文件夹facesql
    def delete_some_stu_record(self,de_stu_id):
        """删除某些学生的记录de_stu_id是市删除的学生的学
        sql_face->course_inf->student_inf->本地文件夹facesql
        """
        connection=pymysql.connect(host="localhost",user="root",password="root")
        with connection.cursor() as cursor:
            cursor.execute("use face_recognition")
            for per in de_stu_id:
                cursor.execute("delete from sql_face where stu_id='%s'"%per)
                cursor.execute("delete from course_inf where id_stu='%s'"%per)
                cursor.execute("delete from student_inf where Stu_id='%s'"%per)
            connection.commit()
                
            
    
    
        
"""if __name__=="__main__":
    ob=add_delete_sum_of_course_inf_and_student_inf_sqlop()
    ob.check_detect_encode()#检测人脸和人脸特征编码检测并保存到add_sql文件夹（相当于一个cache）
    ob.insert_encode_to_sql_face()#对数据库中进行添加是后在add_sql下一步将要添加到facesql中的图片特征编码保存到数据库sql_face中
    stus_inf=ob.move_and_get_inf()#将cache(add_sql)中的人脸图片送入到facesql
    ob.update_sql(stus_inf)#分别向数据库中的student_inf和course_inf表中插入添加的记录
	a=["16310520306"]
ob.delete_some_stu_record(a)

"""

