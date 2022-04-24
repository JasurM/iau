from models import *
from flask import send_from_directory
import random
import jwt

@app.route("/login", methods=['POST'])
def login_a():
    pin_code = request.form.get('pin')
    password = request.form.get('password')

    user = User.query.filter(User.pin==pin_code).first()
    if user:
        ch = user.check_password(password)
        if ch:
            token = jwt.encode({
                'public_id': user.id,
                'exp' : datetime.now() ++ timedelta(days = 100)
            }, SECRET_KEY,algorithm="HS256")
            print(token)
            db.session.commit()
            return jsonify({
                'token': token,
                'msg': "ok"
            }), 200
        return jsonify({
            'msg': "Password incorrect"
        }), 401
    print('CHORT')
    return jsonify({
        'msg': "User not found"
    }), 404

@app.route('/admission', methods=['GET', 'POST'])
@app.route('/admission/step/<int:step>', methods=['GET', 'POST'])
@token_required
def admission(c, step=0):
    user = User.query.filter_by(id=c.id).first()
    adm = Admission.query.filter_by(user_id=user.id).first()
    if not adm:
        adm = Admission()
        adm.user_id = user.id
    data = adm.format()

    if request.method == 'POST':
        if step == 1:
            adm.title = request.form.get("title")
            adm.firstname = request.form.get("firstname")
            adm.surname = request.form.get("surname")
            adm.middlename = request.form.get('middlename')
            dob_date = request.form.get('DoB')
            if not dob_date:
                dob_date = None
            else:
                adm.DoB = datetime.strptime(dob_date, '%Y-%m-%d')
            adm.gender = request.form.get('gender')
            adm.CoB = request.form.get('CoB')
            adm.nationality = request.form.get('nationality')
            adm.perma_residence = request.form.get("perma_residence")
            adm.curr_residence = request.form.get("curr_residence")
            adm.disability = request.form.get("disability")
        elif step == 2:
            adm.term = request.form.get("term")
            adm.type = request.form.get("type")
            adm.programme = request.form.get("programme")
        elif step == 3:
            adm.passport = request.form.get("passport")
            expiry_date = request.form.get("expiry_date")
            if not expiry_date:
                expiry_date = None
            else:
                adm.expiry_date = request.form.get("expiry_date")
            adm.issue_country = request.form.get("issue_country")
            passport_file = request.files.get("passport_copy")
            if passport_file:
                filename = Hash_User_File(secure_filename(passport_file.filename), c.id)
                filepath = "uploads/files/passport/" + filename
                passport_file.save(filepath)
                adm.passport_copy = filepath
        elif step == 4:
            adm.corr_address_1 = request.form.get("corr_address_1")
            adm.corr_address_2 = request.form.get("corr_address_2")
            adm.corr_city = request.form.get("corr_city")
            adm.corr_county = request.form.get("corr_county")
            adm.corr_zip = request.form.get("corr_zip")
            adm.corr_country = request.form.get("corr_country")
            if request.form.get("perma_corr").lower() == 'false':
                adm.perma_corr = False
            else:
                adm.perma_corr = True
            adm.perma_address_1 = request.form.get("perma_address_1")
            adm.perma_address_2 = request.form.get("perma_address_2")
            adm.perma_city = request.form.get("perma_city")
            adm.perma_county = request.form.get("perma_county")
            adm.perma_zip = request.form.get("perma_zip")
            adm.perma_country = request.form.get("perma_country")
            if request.form.get("perma_moved_from"):
                adm.perma_moved_from = request.form.get("perma_moved_from")
            if request.form.get("perma_moved_to"):
                adm.perma_moved_to = request.form.get("perma_moved_to")
            adm.contact_number = request.form.get("contact_number")
            adm.contact_number_other = request.form.get("contact_number_other")
            adm.email = request.form.get("email")
        elif step == 5:
            adm.school = request.form.get("school")
            adm.qualified_date = request.form.get("qualified_date")
            adm.qualified_type = request.form.get("qualified_type")
            adm.major = request.form.get("major")
            adm.major_type = request.form.get("major_type")
            if request.form.get("start_date"):
                adm.start_date = request.form.get("start_date")
            if request.form.get("completion_date"):
                adm.completion_date = request.form.get("completion_date")
            adm.transcript_grade = request.form.get("transcript_grade")
            if request.form.get("other_qualifications").lower() == 'false':
                adm.other_qualifications = False
            else:
                adm.other_qualifications = True

            transcript_file = request.files.get("transcript_copy")
            if transcript_file:
                filename = Hash_User_File(secure_filename(transcript_file.filename), c.id)
                filepath = "uploads/files/transcripts/" + filename
                transcript_file.save(filepath)
                adm.transcript_copy = filepath
            degree_cerf_file = request.files.get("degree_cerf_copy")
            if degree_cerf_file:
                filename = Hash_User_File(secure_filename(degree_cerf_file.filename), c.id)
                filepath = "uploads/files/degree_cerfs/" + filename
                degree_cerf_file.save(filepath)
                adm.degree_cerf_copy = filepath
        elif step == 6:
            if request.form.get("is_english_first_language") == 'false':
                adm.is_english_first_language = False
            else:
                adm.is_english_first_language = True
            if request.form.get("UK_qualification_equivalent") == 'false':
                adm.UK_qualification_equivalent = False
            else:
                adm.UK_qualification_equivalent = True
            adm.uqe_country = request.form.get("uqe_country")
            if request.form.get("ELT") == 'false':
                adm.ELT = False
            else:
                adm.ELT = True
            adm.ELT_type = request.form.get("ELT_type")
            if request.form.get("ELT_date"):
                adm.ELT_date = request.form.get("ELT_date")
            adm.overall_score = request.form.get("overall_score")
            adm.listening_score = request.form.get("listening_score")
            adm.reading_score = request.form.get("reading_score")
            adm.writing_score = request.form.get("writing_score")
            adm.speaking_score = request.form.get("speaking_score")
            adm.ELT_alternative = request.form.get("ELT_alternative")
            if request.form.get("alternative_date"):
                adm.alternative_date = request.form.get("alternative_date")
            if request.form.get("alternative_grade"):
                adm.alternative_grade = request.form.get("alternative_grade")
            adm.ELT_other = request.form.get("ELT_other")
        elif step == 7:
            personal_statement_file = request.files.get("personal_statement")
            if personal_statement_file:
                filename = Hash_User_File(secure_filename(personal_statement_file.filename), c.id)
                filepath = "uploads/files/" + filename
                personal_statement_file.save(filepath)
                adm.personal_statement = filepath
            research_proposal_file = request.files.get("research_proposal")
            if research_proposal_file:
                filename = Hash_User_File(secure_filename(research_proposal_file.filename), c.id)
                filepath = "uploads/files/" + filename
                research_proposal_file.save(filepath)
                adm.research_proposal = filepath
            cv_file = request.files.get("cv")
            if cv_file:
                filename = Hash_User_File(secure_filename(cv_file.filename), c.id)
                filepath = "uploads/files/" + filename
                cv_file.save(filepath)
                adm.cv = filepath
            pg_diploma_file = request.files.get("pg_diploma")
            if pg_diploma_file:
                filename = Hash_User_File(secure_filename(pg_diploma_file.filename), c.id)
                filepath = "uploads/files/" + filename
                pg_diploma_file.save(filepath)
                adm.pg_diploma = filepath
        elif step == 8:
            first_reference_file = request.files.get("first_reference")
            if first_reference_file:
                filename = Hash_User_File(secure_filename(first_reference_file.filename), c.id)
                filepath = "uploads/files/" + filename
                first_reference_file.save(filepath)
                adm.first_reference = filepath
            second_reference_file = request.files.get("second_reference")
            if second_reference_file:
                filename = Hash_User_File(secure_filename(second_reference_file.filename), c.id)
                
                filepath = "uploads/files/" + filename
                second_reference_file.save(filepath)
                adm.second_reference = filepath
        elif step == 9:
            if request.form.get("agree_terms") == 'true':
                adm.agree_terms = True
            else:
                adm.agree_terms = False
        elif step == 10:
            adm.submitted = True
            adm.status = 'pending'
            
        db.session.add(adm)
        db.session.commit()
    if request.method == 'GET':
        return jsonify(data)
    else:
        return jsonify({'msg': 'ok'})

@app.route('/title', methods=['GET'])
@token_required
def title(c):
    data = []
    titles = Title.query.all()
    for t in titles:
        data.append(t.format())
    return jsonify(data)

@app.route('/gender', methods=['GET'])
@token_required
def gender(c):
    data = []
    genders = Gender.query.all()
    for t in genders:
        data.append(t.format())
    return jsonify(data)

@app.route('/country', methods=['GET'])
@token_required
def country(c):
    data = []
    countries = Country.query.all()
    for t in countries:
        data.append(t.format())
    return jsonify(data)

@app.route('/disability', methods=['GET'])
@token_required
def disability(c):
    data = []
    disabilities = Disability.query.all()
    for t in disabilities:
        data.append(t.format())
    return jsonify(data)

@app.route('/add_term', methods=['GET'])
@token_required
def add_term(c):
    data = []
    add_terms = Add_Term.query.all()
    for t in add_terms:
        data.append(t.format())
    return jsonify(data)

@app.route('/app_type', methods=['GET'])
@token_required
def app_type(c):
    data = []
    app_types = App_Type.query.all()
    for t in app_types:
        data.append(t.format())
    return jsonify(data)

@app.route('/programme', methods=['GET'])
@token_required
def programme(c):
    data = []
    programmes = Programme.query.all()
    for t in programmes:
        data.append(t.format())
    return jsonify(data)

@app.route('/qualification', methods=['GET'])
@token_required
def qualification(c):
    data = []
    qualifications = Qualification.query.all()
    for t in qualifications:
        data.append(t.format())
    return jsonify(data)

@app.route('/major', methods=['GET'])
@token_required
def major(c):
    data = []
    majors = Major.query.all()
    for t in majors:
        data.append(t.format())
    return jsonify(data)

@app.route('/test', methods=['GET'])
@token_required
def test(c):
    data = []
    tests = Test.query.all()
    for t in tests:
        data.append(t.format())
    return jsonify(data)

@app.route('/other_test', methods=['GET'])
@token_required
def other_test(c):
    data = []
    other_tests = Other_Test.query.all()
    for t in other_tests:
        data.append(t.format())
    return jsonify(data)

@app.route('/logout')
@token_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('pages/index.html')

# @app.route('/uploads/<path:path>')
# def send_from_pth(path):
#     print(f'path is {path}')
#     if path.startswith("uploads"):
#         real_p = path.replace("\\", '/')
#         real_p = real_p.split("/")[1:]
#         real_p = '/'.join(real_p)
#     return send_from_directory('uploads', real_p)

@app.route("/registration",methods = ['POST'])
def registration():
    if request.method == 'POST':
        first_name = request.form.get("firstname")
        last_name = request.form.get("lastname")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")
        email_ = request.form.get("email")
        email_confirm = request.form.get("email_confirm")

        user = User.query.filter_by(firstname=first_name).first()
        user_u = User.query.filter_by(lastname=last_name).first()
        user_q = User.query.filter_by(email=email_).first()
        if user and user_u and user_q:
            return jsonify({'msg' : 'User with this firstname, lastname and email already exist'}),400
        elif password_confirm != password:
            return jsonify({'msg' : 'Password confirmation error'}),400
        elif email_confirm != email_:
            return jsonify({'msg' : 'Email confirmation error'}),400
        else:
            t_us = User(
                firstname = first_name,
                lastname = last_name,
                email = email_
            )
            t_us.set_password(password)
            while True:
                pin_code = ''
                for i in range(7):
                    pin_code = pin_code + str(random.randint(0, 9))
                if not User.query.filter_by(pin=pin_code).first():
                    t_us.pin = pin_code
                    text_body = 'Registration completed succesfully. Your PIN is: ' + pin_code
                    send_mail(t_us.email, text_body)
                    break
            db.session.add(t_us)
            db.session.commit()
            return jsonify({'msg' : 'ok'}),200
    else:
        return jsonify({"message":"Method not allowed"}),405

@app.route("/single_admission", methods=["GET"])
@token_required
def single_admission(c):
    id = request.args.get('id')
    u = User.query.get_or_404(id)
    data = {}
    if u.admissions:
        data['ads'] = u.admissions[0].format()
    else:
        data['ads'] = 'empty'
    return jsonify(data)

@app.route("/all_admissions", methods=["GET"])
@token_required
def all_admissions(c):
    data = {}
    data['all'] = [x.format() for x in User.query.all()]
    data["user_cols"] = [column.key for column in User.__table__.columns]
    
    return jsonify(data)

@app.route("/accept_admission", methods=["POST"])
@token_required
def accept_admission(c):
    ad_id = request.form.get("admission_id")
    adm = Admission.query.get(ad_id)
    adm.accepted = True
    adm.status = 'accepted'
    db.session.commit()
    return jsonify({"msg": "accepted"})


@app.route("/reject_admission", methods=["POST"])
@token_required
def reject_admission(c):
    ad_id = request.form.get("admission_id")
    adm = Admission.query.get(ad_id)
    adm.accepted = False
    adm.status = 'rejected'
    adm.reject_commentary = request.form.get("comment")
    db.session.commit()
    return jsonify({"msg": "rejected"})

@app.route("/review_admission", methods=["GET"])
@token_required
def review_admission(c):
    adm = Admission.query.filter_by(user_id=c.id).first()
    st = ''
    cc = ''
    if adm:
        print("CHORT")
        st = adm.status
        cc = adm.reject_commentary
    else:
        print("CHORTMAS")
        st = 'empty'
        cc = ''
    data = {
        "stst" : st,
        "comment" : cc
    }
    return jsonify(data)