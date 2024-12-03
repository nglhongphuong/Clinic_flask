from clinic import app, db, dao
from clinic.dao import hash_password
from clinic.models import User, UserRole
import hashlib # ma bam mk

def add_user(name, username, password, **kwargs):
    password = dao.hash_password(password)
    user = User(name=name.strip(), username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'),
                gender= kwargs.get('gender'),
                dob=kwargs.get('dob'),
                address=kwargs.get('address'),
                phone=kwargs.get('phone'))

    db.session.add(user)
    db.session.commit()

def check_login(username, password, role=UserRole.PATIENT):
   #truy vấn 1 đối tượng user trong User qua id
    user = User.query.filter_by(username=username.strip()).first()
    if user and dao.auth_password(password,user.password):
        return user

    return None

def get_user_by_id(user_id):
    return User.query.get(user_id)


