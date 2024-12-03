from enum import Enum as UserEnum
from sqlalchemy import DateTime,Enum, Column,Integer,String,Float,Boolean,ForeignKey,Date
from sqlalchemy.orm import relationship
from clinic import app, db, dao
from datetime import datetime, date
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeSerializer as Serializer


class UserRole(UserEnum):
    ADMIN = 'admin'
    PATIENT = 'patient'
    NURSE = 'nurse'


class Gender(UserEnum):
    MALE = 'male'
    FEMALE = 'female'

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(70), nullable=False)
    avatar = Column(String(255))
    email = Column(String(50))
    user_role = Column(Enum(UserRole), default=UserRole.PATIENT)
    gender = Column(Enum(Gender))
    phone = Column(String(20), nullable=True)
    address = Column(String(255), default='HoChiMinh')
    dob = Column(Date, default=date.today)

    def get_token(self):
        serial=Serializer(app.secret_key)
        return serial.dumps({'user_id':self.id})

    @staticmethod
    def verify_token(token):
        serial = Serializer(app.secret_key)
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)



    def __str__(self):
        return self.name

class Admin(db.Model):
    id = Column(Integer, ForeignKey(User.id), primary_key=True)

class Patient(db.Model):
    id = Column(Integer, ForeignKey(User.id), primary_key=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tạo các bảng trong cơ sở dữ liệu
        db.session.commit()

        # Tạo tài khoản admin1
        admin1 = User(
            name='admin1',
            username='admin1',
            password=str(dao.hash_password("123")),  # Mật khẩu được băm
            avatar='https://res.cloudinary.com/dmz9kuzue/image/upload/v1732014605/samples/dessert-on-a-plate.jpg',
            email='admin1@example.com',
            user_role=UserRole.ADMIN,
            gender=Gender.FEMALE,
            phone='0708602388',
            dob=date(2004, 7, 23)
        )
        db.session.add(admin1)  # Lưu admin1 vào DB
        db.session.commit()

        # Liên kết admin1 với bảng Admin
        admin_entry = Admin(id=admin1.id)
        db.session.add(admin_entry)

        # Tạo tài khoản patient1
        patient1 = User(
            name='patient1',
            username='patient1',
            password=str(dao.hash_password("123")),  # Mật khẩu được băm
            avatar='https://res.cloudinary.com/dmz9kuzue/image/upload/v1732014605/samples/dessert-on-a-plate.jpg',
            email='patient1@example.com',
            user_role=UserRole.PATIENT,
            gender=Gender.MALE,
            phone = '0908703277',
            dob=date(2004, 7, 10)
        )
        db.session.add(patient1)  # Lưu patient1 vào DB
        db.session.commit()

        # Liên kết patient1 với bảng Patient
        patient_entry1 = Patient(id=patient1.id)
        db.session.add(patient_entry1)

        # Tạo tài khoản patient2
        patient2 = User(
            name='patient2',
            username='patient2',
            password=str(dao.hash_password("123")), # Mật khẩu được băm
            avatar='https://res.cloudinary.com/dmz9kuzue/image/upload/v1732014605/samples/dessert-on-a-plate.jpg',
            email='patient2@example.com',
            user_role=UserRole.PATIENT,
            gender=Gender.FEMALE,
            phone='0703792627',
            dob=date(2004, 3, 10)
        )
        db.session.add(patient2)  # Lưu patient2 vào DB
        db.session.commit()

        # Liên kết patient2 với bảng Patient
        patient_entry2 = Patient(id=patient2.id)
        db.session.add(patient_entry2)

        # Lưu các thay đổi vào cơ sở dữ liệu
        db.session.commit()

