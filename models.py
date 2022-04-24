from imports import *
from functools import wraps
from config import SECRET_KEY
import jwt
import requests, json

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
mail = Mail(app)

def Get_Load(user_id):
    return User.query.get(user_id)

@login_manager.user_loader
def load_user(user_id):
    return Get_Load(user_id)

def Hash_User_File(filename, user_id):
    ext = filename.rsplit('.', 1)[1].lower()
    filename = filename.rsplit('.', 1)[0]
    filename = filename + "_" + str(datetime.now())
    return str(user_id) + "_" + sha256(filename.encode('utf-8')).hexdigest() + "." + ext

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({
                'message' : "Token is missing !!"
            }), 401
        try:
            print(token)
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            print(data)
            current_user = User.query\
                .filter_by(id=data['public_id'])\
                .first()
        except Exception as E:
            return jsonify({
                'message' : str(E)
            }), 401
        return  f(current_user, *args, **kwargs)
  
    return decorated

@app.after_request
def after_request(response):
    header = response.headers
    header.add('Access-Control-Allow-Origin', '*')
    header.add('Access-Control-Allow-Headers', '*')
    header.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

def send_mail(recipient, text_body):

    reqUrl = "https://internship.agro.uz/api/send_email"

    headersList = {
    "Accept": "*/*",
    "x-key": "333",
    "Content-Type": "application/json" 
    }

    payload = json.dumps(
    {
        "subject" : "Email verify",
        "recipients": [ recipient ],
        "text_body" : text_body
        
    })

    response = requests.request("POST", reqUrl, data=payload,  headers=headersList)

    print(response.text)

@app.route('/uploads/<path:path>')
def send_uploads(path):
    return send_from_directory('uploads', path, as_attachment=True)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    pin = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default='student')
    admissions = db.relationship('Admission', backref='user', lazy=True)
    
    def format(self):
        st = ''
        if self.admissions:
            st = self.admissions[0].status
        else:
            st = 'empty'
        return{
            "id" : self.id,
            "firstname" : self.firstname,
            "lastname" : self.lastname,
            "pin" : self.pin,
            "email" : self.email,
            "role" : self.role,
            "status" : st
        }

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<{self.firstname} ID: {self.id} >'
        
class Admission(db.Model):
    __tablename__ = 'admission'
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String, nullable=True)
    firstname = db.Column(db.String, nullable=True)
    surname = db.Column(db.String, nullable=True)
    middlename = db.Column(db.String, nullable=True)
    DoB = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String, nullable=True)
    CoB = db.Column(db.String, nullable=True)
    nationality = db.Column(db.String, nullable=True)
    perma_residence = db.Column(db.String, nullable=True)
    curr_residence = db.Column(db.String, nullable=True)
    disability = db.Column(db.String, nullable=True)
    #end of step 1
    term = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=True)
    programme = db.Column(db.String, nullable=True)
    #end of step 2
    passport = db.Column(db.String, nullable=True)
    expiry_date = db.Column(db.Date, nullable=True)
    issue_country = db.Column(db.String, nullable=True)
    passport_copy = db.Column(db.String, nullable=True)
    #end of step 3
    corr_address_1 = db.Column(db.String, nullable=True)
    corr_address_2 = db.Column(db.String, nullable=True)
    corr_city = db.Column(db.String, nullable=True)
    corr_county = db.Column(db.String, nullable=True)
    corr_zip = db.Column(db.String, nullable=True)
    corr_country = db.Column(db.String, nullable=True)
    perma_corr = db.Column(db.Boolean, nullable=True)
    perma_address_1 = db.Column(db.String, nullable=True)
    perma_address_2 = db.Column(db.String, nullable=True)
    perma_city = db.Column(db.String, nullable=True)
    perma_county = db.Column(db.String, nullable=True)
    perma_zip = db.Column(db.String, nullable=True)
    perma_country = db.Column(db.String, nullable=True)
    perma_moved_from = db.Column(db.Date, nullable=True)
    perma_moved_to = db.Column(db.Date, nullable=True)
    contact_number = db.Column(db.String, nullable=True)
    contact_number_other = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    #end of step 4
    school = db.Column(db.String, nullable=True)
    qualified_date = db.Column(db.String, nullable=True)
    qualified_type = db.Column(db.String, nullable=True)
    major = db.Column(db.String, nullable=True)
    major_type = db.Column(db.String, nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    completion_date = db.Column(db.Date, nullable=True)
    transcript_grade = db.Column(db.String, nullable=True)
    other_qualifications = db.Column(db.Boolean, nullable=True)
    transcript_copy = db.Column(db.String, nullable=True)
    degree_cerf_copy = db.Column(db.String, nullable=True)
    #end of step 5
    is_english_first_language = db.Column(db.Boolean, nullable=True)
    UK_qualification_equivalent = db.Column(db.Boolean, nullable=True)
    uqe_country = db.Column(db.String, nullable=True)
    ELT = db.Column(db.Boolean, nullable=True)
    ELT_type = db.Column(db.String, nullable=True)
    ELT_date = db.Column(db.Date, nullable=True)
    overall_score = db.Column(db.String, nullable=True)
    listening_score = db.Column(db.String, nullable=True)
    reading_score = db.Column(db.String, nullable=True)
    writing_score = db.Column(db.String, nullable=True)
    speaking_score = db.Column(db.String, nullable=True)
    ELT_alternative = db.Column(db.String, nullable=True)
    alternative_date = db.Column(db.Date, nullable=True)
    alternative_grade = db.Column(db.String, nullable=True)
    ELT_other = db.Column(db.String, nullable=True)
    #end of step 6
    personal_statement = db.Column(db.String, nullable=True)
    research_proposal = db.Column(db.String, nullable=True)
    cv = db.Column(db.String, nullable=True)
    pg_diploma = db.Column(db.String, nullable=True)
    #end of step 7
    first_reference = db.Column(db.String, nullable=True)
    second_reference = db.Column(db.String, nullable=True)
    #end of step 8
    agree_terms = db.Column(db.Boolean, nullable=True)
    #end of step 9
    last_step = db.Column(db.Integer, nullable=True)
    created_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    accepted = db.Column(db.Boolean)
    submitted = db.Column(db.Boolean)
    status = db.Column(db.String, default='filling')
    reject_commentary = db.Column(db.String, nullable=True)


    def __repr__(self):
        return f'<{self.title} {self.firstname} {self.surname} ID: {self.id} >'
    
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'firstname': self.firstname,
            'surname': self.surname,
            'middlename': self.middlename,
            'DoB': self.DoB,
            'gender': self.gender,
            'CoB': self.CoB,
            'nationality': self.nationality,
            'perma_residence': self.perma_residence,
            'curr_residence': self.curr_residence,
            'disability': self.disability,
            'term': self.term,
            'type': self.type,
            'programme': self.programme,
            'passport': self.passport,
            'expiry_date': self.expiry_date,
            'issue_country': self.issue_country,
            'passport_copy': self.passport_copy,
            'corr_address_1': self.corr_address_1,
            'corr_address_2': self.corr_address_2,
            'corr_city': self.corr_city,
            'corr_county': self.corr_county,
            'corr_zip': self.corr_zip,
            'corr_country': self.corr_country,
            'perma_corr': self.perma_corr,
            'perma_address_1': self.perma_address_1,
            'perma_address_2': self.perma_address_2,
            'perma_city': self.perma_city,
            'perma_county': self.perma_county,
            'perma_zip': self.perma_zip,
            'perma_country': self.perma_country,
            'perma_moved_from': self.perma_moved_from,
            'perma_moved_to': self.perma_moved_to,
            'contact_number': self.contact_number,
            'contact_number_other': self.contact_number_other,
            'email': self.email,
            'school': self.school,
            'qualified_date': self.qualified_date,
            'qualified_type': self.qualified_type,
            'major': self.major,
            'major_type': self.major_type,
            'start_date': self.start_date,
            'completion_date': self.completion_date,
            'transcript_grade': self.transcript_grade,
            'other_qualifications': self.other_qualifications,
            'transcript_copy': self.transcript_copy,
            'degree_cerf_copy': self.degree_cerf_copy,
            'is_english_first_language': self.is_english_first_language,
            'UK_qualification_equivalent': self.UK_qualification_equivalent,
            'uqe_country': self.uqe_country,
            'ELT': self.ELT,
            'ELT_type': self.ELT_type,
            'ELT_date': self.ELT_date,
            'overall_score': self.overall_score,
            'listening_score': self.listening_score,
            'reading_score': self.reading_score,
            'writing_score': self.writing_score,
            'speaking_score': self.speaking_score,
            'ELT_alternative': self.ELT_alternative,
            'alternative_date': self.alternative_date,
            'alternative_grade': self.alternative_grade,
            'ELT_other': self.ELT_other,
            'personal_statement': self.personal_statement,
            'research_proposal': self.research_proposal,
            'cv': self.cv,
            'pg_diploma': self.pg_diploma,
            'first_reference': self.first_reference,
            'second_reference': self.second_reference,
            'agree_terms': self.agree_terms,
            'accepted': self.accepted,
            'status': self.status,
            'submitted': self.submitted
            }

class Title(db.Model):
    __tablename__ = 'title'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)

    def format(self):
        return {
            "value" : self.id,
            "label" : self.name
        }
    
class Gender(db.Model):
    __tablename__ = 'gender'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    def format(self):
        return {
            "value" : self.id,
            "label" : self.name
        }
    
class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    def format(self):
        return {
            "value" : self.id,
            "label" : self.name
        }
    
class Disability(db.Model):
    __tablename__ = 'disability'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    def format(self):
        return {
            "value" : self.id,
            "label" : self.name
        }
    
class Add_Term(db.Model):
    __tablename__ = 'add_term'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    def format(self):
        return {
            "value" : self.id,
            "label" : self.name
        }
    
class App_Type(db.Model):
    __tablename__ = 'app_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    def format(self):
        return {
            "value" : self.id,
            "label" : self.name
        }
    
class Programme(db.Model):
    __tablename__ = 'programme'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    def format(self):
        return {
            "value" : self.id,
            "label" : self.name
        }
    
class Qualification(db.Model):
    __tablename__ = 'qualification'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    def format(self):
        return {
            "value" : self.id,
            "label" : self.name
        }
    
class Major(db.Model):
    __tablename__ = 'major'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    def format(self):
        return {
            "value" : self.id,
            "label" : self.name
        }
    
class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    def format(self):
        return {
            "value" : self.id,
            "label" : self.name
        }
    
class Other_Test(db.Model):
    __tablename__ = 'other_test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    def format(self):
        return {
            "value" : self.id,
            "label" : self.name
        }

admission_cols = [column.key for column in Admission.__table__.columns]

class OurView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return True
        return False
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))
admin = Admin(app, name='IAU', template_mode='bootstrap4')

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Admission, db.session))
admin.add_view(ModelView(Title, db.session))
admin.add_view(ModelView(Gender, db.session))
admin.add_view(ModelView(Country, db.session))
admin.add_view(ModelView(Disability, db.session))
admin.add_view(ModelView(Add_Term, db.session))
admin.add_view(ModelView(App_Type, db.session))
admin.add_view(ModelView(Programme, db.session))
admin.add_view(ModelView(Qualification, db.session))
admin.add_view(ModelView(Major, db.session))
admin.add_view(ModelView(Test, db.session))
admin.add_view(ModelView(Other_Test, db.session))
