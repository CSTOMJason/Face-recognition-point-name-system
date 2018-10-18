    本人是一名学生请多多指教.谢谢！
人脸识别部分采用开源的框架额和训练好的人脸检测和人脸识别
与数据库mysql作为后端的数据的存放
mysql中很简单:数据库(face_recognition),三张表(studen_inf,course_inf,sql_face)
工具：opencv，dlib，face_recognition
     训练好的model：dlib_face_recognition_resnet_model_v1.dat
                haarcascade_frontalface_alt2.xml(人脸检测的模型)
                dlib_face_recognition_resnet_model_v1.dat(人脸识别模型采用残缺网络)
                shape_predictor_68_face_landmarks.dat
             
详细解析见每个.py的注释



Model的运行
from Model import Model
model=Model()

model.DECTING()#人脸识别将却请的人信息保存到mysql中


model.ADD_SQL()#添加新的人并把人脸的(128,)的特征编码保存到sql_face表中


注意：shape_predictor_68_face_landmarks.dat缺少这个自己可以在网上下载

model.DELETE()#删除学生的记录
真心的希望有大佬带带我！
