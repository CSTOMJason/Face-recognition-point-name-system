import os
import shutil
from face_normalization_64x64x3 import face_normalization#图片归一化为(64,64,64)
#进行人脸的检测
from DlibResnet_face_recognition_class import DlibResnet_face_recognition_class
from add_delete_sum_of_course_inf_and_student_inf_sqlop_class import add_delete_sum_of_course_inf_and_student_inf_sqlop

class Model():
    def __init__(self):
        pass
    def ADD_SQL(self):
        norm_ob=face_normalization()
        norm_ob.dection()
        for line in os.listdir("emb_img"):
            shutil.move("emb_img/"+line,"add_sql/")
            os.remove("test_img/"+line)
        check_ob=add_delete_sum_of_course_inf_and_student_inf_sqlop()
        bad_pic=check_ob.check_detect_encode()
        check_ob.insert_encode_to_sql_face()
        stus_inf=check_ob.move_and_get_inf()
        check_ob.update_sql(stus_inf)
        return bad_pic
    def DECTING(self):
        if os.listdir("raw_pic")==[]:
            print("请把要检测的图片放置到raw_piv文件夹中")
        else:
            norm_ob=face_normalization()
            for line in os.listdir("raw_pic"):
                shutil.move("raw_pic/"+line,"test_img/")
            norm_ob.dection()
            for line in os.listdir("emb_img"):
                shutil.move("emb_img/"+line,"face_net_picture/")
                os.remove("test_img/"+line)
            face_re=DlibResnet_face_recognition_class()#人脸检测
            res=face_re.get_result_face_recognition()
            print("__________________________________________________")
            #获取时间，时间的字典数和缺席学生的学号
            r,a,b=face_re.get_datetime_absence_id_stu()
            print(r,a,b)
            print("__________________________________________________")
            #将缺席学生的信息插入到数据库course_inf表中
            face_re.times_course_inf_per_student()
            #获取course_inf表中的信息
            #print(face_re.absence_people_inf())
            for line in face_re.absence_people_inf():
                print(line)
            #删除face_net_picture下的图片
            for line in os.listdir("face_net_picture"):
                os.remove("face_net_picture/"+line)
            
    def DELETE(self):
        de_list=[]
        ob_del=add_delete_sum_of_course_inf_and_student_inf_sqlop()
        number_stu=int(input("请输入删除学生的人数"))
        for i in range(number_stu):
            stu_id=input("请输入学生的11位学号！")
            de_list.append(stu_id)
        ob_del.delete_some_stu_record(de_list)
        
        
            
            
        

            
        
        