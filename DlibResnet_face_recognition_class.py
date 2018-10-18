import cv2
import numpy as np
import os
import face_recognition
import dlib
import time
import pymysql
#数据库中的人信息相关到一个列表 
#name_sql=[]
#for line in os.listdir("facesql/"):
#    name_sql.append(line[:len(line)-4])


from pre_sql_face_encode_save_to_mysql_class import Encoding_mysql
temp=Encoding_mysql()
#从数据库中加载目标人脸的特征编码
sql_face_encode=temp.load_face_encoding_from_sql()
connection=pymysql.connect(host="localhost",user="root",password="root")


class DlibResnet_face_recognition_class():
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()# 1.加载正脸检测器
        # 2.加载人脸关键点检测器
        self.sp= dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        # 3. 加载人脸识别模型
        self.facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
        # 候选人脸描述子list
        self.descriptors = []
    def face_encod(self,img):#人脸特征的编码函数
        """ 将人脸进行特征编码为(128,)的形状 """
        dets=self.detector(img,1)#人脸的检测区域大小
        print("dets is",dets)
        #人脸的特征编码采用resnet（残缺网络）训练好的模型
        for k,d in enumerate(dets):
            shape=self.sp(img,d)
            face_encod=np.array(self.facerec.compute_face_descriptor(img,shape))#人脸的特征编码残缺网络模型
            return face_encod
        return np.array([1,2,3])
    #人脸的特征的匹配
    def match(self,sql_face_encode,face_real_encode,index=-1):
        """ 将检测的人脸图片与sql中导入的人脸图片的特征编码进行匹配 
        返回一个bool值和对应匹配的索引值"""
        for i in range(len(sql_face_encode)):
            match=face_recognition.compare_faces([sql_face_encode[i]],face_real_encode,tolerance=0.5)
            if match[0]==True:
                index=i
                return (match[0],index)
        return (False,index)
    def get_sql_stu_id_and_name(self):
        connection=pymysql.connect(host="localhost",user="root",password="root")
        with connection.cursor() as cursor:
            cursor.execute("use face_recognition")
            cursor.execute("select Stu_id,name from student_inf")
            res=cursor.fetchall()
            total_name_sql=[]
            for line in res:
                total_name_sql.append(line[0]+'-'+line[1])
        return total_name_sql
    #获取人脸检测的结果,得到没有来得人
    def get_result_face_recognition(self):
        """ get the redisual people's face in sql
        return a tuple which is combained number_id and name 
        """
        name_total=[]
        global sql_face_encode
        #global name_sql
        path="face_net_picture/"
        temp_name_sql=self.get_sql_stu_id_and_name()
        for per_pic in os.listdir(path):
            img=cv2.imread(path+per_pic)
            face_real_encode=self.face_encod(img)
            res,index=self.match(sql_face_encode,face_real_encode)
            print("res{},idex{}".format(res,index))
            if res:
                name_total.append(temp_name_sql[index])
        #print( name_total)数据库中的人的学号+姓名
        #res,index=match(sql_face_encode,face_real_encode)
        #if res:
        #   print("the name is ",name_sql[index])
        #temp_name_sql=self.get_sql_stu_id_and_name()
        #print(temp_name_sql)
        #print("++++++++++++++++++++++++++++++++++++++++++++++++")
        #print(name_total)
        name_total=list(set(name_total))
        
        #print("+++++++++++++++++++++++++++++++++++++++++++")
        for person in name_total:
            temp_name_sql.remove(person)
        print(temp_name_sql)
        input()
        return temp_name_sql#返回数据库中剩余的人的学号+姓名
        
    
    
    #获取当前的日期和缺席学生的学号
    def get_datetime_absence_id_stu(self):
        """ 获取当前的星期日"""
        #test
        #cur_dat="mo"
        cur_dat=time.strftime("%a")[:2].lower()
        if cur_dat in ["sa","su"]:
            print("双休日没课!")
        else:
            #日期对应的一个字典
            dic_date={"mo":0,"tu":1,"we":2,"th":3,"fr":4}
            dat_idx=dic_date[cur_dat]
            stu_ids=[]
            temp_name_sql=self.get_result_face_recognition()
            print("SSSSSSSSSSSSSSSS",temp_name_sql)
            for per_absence in temp_name_sql:
                stu_ids.append(per_absence[0:11])
            return cur_dat,dat_idx,stu_ids#返回日期对应的字典数和缺席学生的学号
        
    #对迟到的人的次数记录到数据库中的course_inf
    def times_course_inf_per_student(self):
        """ 对迟到的人记录到数据库中的course_inf表
        并且求出每个人总共的迟到次数"""
        #对迟到的人记录次数到数据库
        global connection
        with connection.cursor() as cursor:
            cursor.execute("use face_recognition")
            cur_dat,dat_idx,stu_ids=self.get_datetime_absence_id_stu()
            print(stu_ids)  
            print("_______________________________")        
            for stu_id in stu_ids:
                cursor.execute("select mo_absence,tu_absence,we_absence,th_absence,fr_absence from course_inf where id_stu='%s'"%(stu_id))
                res=cursor.fetchall()
                print(res)
                print("_____________________")
                temp=int(res[0][dat_idx])#缺课次数加1
                #print(temp)
                temp+=1
                com_dat=cur_dat+"_absence"
                cursor.execute("update course_inf set %s=%d where id_stu='%s'"%(com_dat,temp,stu_id))
            connection.commit()
    
    #查询缺课人的相关信息
    def absence_people_inf(self):
        """ scan the ansenec_people_inf from course_inf
        return a tuple"""
        global connection
        with connection.cursor() as cursor:
            cursor.execute("use face_recognition")
            cursor.execute("select Stu_id,name,mo_absence,tu_absence,we_absence,th_absence,fr_absence from student_inf inner join course_inf on student_inf.Stu_id=course_inf.id_stu")
            res_people_inf=cursor.fetchall()
            return res_people_inf

#开发的测试代码			
if __name__=="__main__":
	#创建人脸检测的对象
	face_re=DlibResnet_face_recognition_class()
	#获取没有正常到达的学生的学号+姓名
	res=face_re.get_result_face_recognition()
	print("没有正常倒带的学生的学号+信息是 ",res)
	print("__________________________________________________")
	#获取时间，时间的字典数和缺席学生的学号
	r,a,b=face_re.get_datetime_absence_id_stu()
	print(r,a,b)
	print("___________________________________________________")
	#将缺席学生的信息插入到数据库course_inf表中
	face_re.times_course_inf_per_student()
	#获取course_inf表中的信息
	#print(face_re.absence_people_inf())
	for line in face_re.absence_people_inf():
		print(line)

	