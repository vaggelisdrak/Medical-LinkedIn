from . import db
from . import app
from itsdangerous import Serializer, SignatureExpired
#from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime,timedelta
#from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer



class Users_database(db.Model, UserMixin): 
    __tablename__ = 'Users_database'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True ,nullable=False)
    email = db.Column(db.String(200), unique=True ,nullable=False)
    password_hash = db.Column(db.String(400), nullable=False)
    workfield = db.Column(db.String(200), nullable=False)

    #password encyption
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    #token creation for password reseting
    def get_token(self):
        #serial = Serializer('hard-to-guess-key',expires_in = expires_sec) #app.secret_key
        expiry_time = datetime.utcnow() + timedelta(minutes=3)
        file = open('datetime.txt', 'w')
        file.write(str(expiry_time)+'\n')
        file.close()
        
        serial = Serializer(app.secret_key)
        #return serial.dumps({'user_id':self.id}).decode('utf-8')
        #return serial.dumps({'user_id':self.id}).encode('utf-8').decode('utf-8')
        print('serializer',serial.dumps({'user_id':self.id}))
        return serial.dumps({'user_id':self.id})
    
    @staticmethod
    def verify_token(token):
        serial = Serializer(app.secret_key)

        user_id = serial.loads(token)['user_id']
        print('user id is',user_id)

        try:
            file = open('datetime.txt', 'r')
            if datetime.utcnow() > datetime.strptime(file.read()[:-8], '%Y-%m-%d %H:%M:%S'):
                raise SignatureExpired('Token has expired', 'exp')
        except:
            return None
        
        return Users_database.query.get(user_id)

    def __init__(self, username, email, password_hash, workfield):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.workfield = workfield

class JOB_ADS_database(db.Model):
    __tablename__ = 'JOB_ADS_database'
    __searchable__ =['org_name','reg_staff','location','contract_length','salary','salary_per','specialty','staff_type','position','job_desc']
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20) ,nullable=False)
    last_name = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(200),nullable=False)
    phone_number = db.Column(db.String(200),nullable=False)
    org_name = db.Column(db.String(200) ,nullable=False)
    org_postcode = db.Column(db.String(200),nullable=False)
    position = db.Column(db.String(200),nullable=False)
    reg_staff = db.Column(db.String(200))
    staff_type = db.Column(db.String(200))
    location = db.Column(db.String(200))
    staff_num = db.Column(db.Integer)
    specialty = db.Column(db.String(200))
    contract_length = db.Column(db.String(200))
    salary = db.Column(db.Integer)
    salary_per = db.Column(db.String(200))
    job_desc = db.Column(db.String(200))
    date_posted = db.Column(db.String(50) ,nullable=True)
    filename = db.Column(db.String(50),nullable=True)
    data = db.Column(db.LargeBinary,nullable=True)
    visibility = db.Column(db.Integer,nullable=True)
    requests = db.relationship("REQUESTS_database", backref="JOB_ADS_database",cascade="all, delete")
    

    def __init__(self, first_name, last_name, email, phone_number, org_name, org_postcode, position, reg_staff, staff_type, 
    location,staff_num,specialty,contract_length,salary,salary_per,job_desc,date_posted,filename,data,visibility):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.org_name = org_name
        self.org_postcode = org_postcode
        self.position = position
        self.reg_staff = reg_staff
        self.staff_type = staff_type
        self.location = location
        self.staff_num = staff_num
        self.specialty = specialty
        self.contract_length = contract_length
        self.salary = salary
        self.salary_per = salary_per
        self.job_desc = job_desc
        self.date_posted = date_posted
        self.filename = filename
        self.data = data
        self.visibility = visibility

    def convert_to_monthly_salary(self):
        if self.salary_per == "Annum":
            salary_per_month = float(self.salary/12)
        if self.salary_per == "Day":
            salary_per_month = float(self.salary*22)
        if self.salary_per == "Hour":
            salary_per_month = float(self.salary*8*22)
        if self.salary_per == "Month":
            salary_per_month = float(self.salary)
        if self.salary_per == "Week":
            salary_per_month = float(self.salary*3)

        self.salary = salary_per_month
        return self.salary

class REQUESTS_database(db.Model):
    __tablename__ = 'REQUESTS_database'
    #__searchable__ =['org_name','reg_staff','location','contract_length','salary','salary_per','specialty','staff_type','position','job_desc']
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20) ,nullable=False)
    last_name = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(200),nullable=False)
    phone_number = db.Column(db.String(200),nullable=False)
    job_id = db.Column(db.Integer,db.ForeignKey("JOB_ADS_database.id"), nullable=False)
    filename = db.Column(db.String(50),nullable=True)
    data = db.Column(db.LargeBinary,nullable=True)
    #parent_id = db.Column(db.Integer, db.ForeignKey("JOBS_ADS_database.id"), nullable=False)
    

    def __init__(self, first_name, last_name, email, phone_number,job_id,filename,data):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.job_id = job_id
        self.filename = filename
        self.data = data
