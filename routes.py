from models import *
from flask import send_from_directory
import random

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
                'exp' : datetime.datetime.now() ++ timedelta(days = 100)
            }, SECRET_KEY,algorithm="HS256")
            print(token)
            db.session.commit()
            return jsonify({
                'token': token,
                'msg': "ok"
            }), 200
        return jsonify({
            'msg': "incorrect"
        }), 401
    print('CHORT')
    return jsonify({
        'msg': "not found"
    }), 404

@app.route('/admission', methods=['GET', 'POST'])
@app.route('/admission/step/<int:step>', methods=['GET', 'POST'])
@token_required
def admission(step=0):
    user = User.query.filter_by(id=current_user.id).first()
    adm = Admission.query.filter_by(user_id=user.id).first()
    if not adm:
        adm = Admission()
        adm.user_id = user.id
    data = adm.format()
    if step == 1:
        adm.last_step = 1
        data['title'] = adm.title
        data['firstname'] = adm.firstname
        data['surname'] = adm.surname
        data['middlename'] = adm.middlename
        data['DoB'] = adm.DoB
        data['CoB'] = adm.CoB
        data['nationality'] = adm.nationality
        data['perma_residence'] = adm.perma_residence
        data['curr_residence'] = adm.curr_residence
        data['disability'] = adm.disability
    elif step == 2:
        adm.last_step = 2
        data['term'] = adm.term
        data['type'] = adm.type
        data['programme'] = adm.programme
    elif step == 3:
        adm.last_step = 3
        data['passport'] = adm.passport
        data['expiry_date'] = adm.expiry_date
        data['issue_country'] = adm.issue_country
        data['passport_copy'] = adm.passport_copy
    elif step == 4:
        adm.last_step = 4
        data['corr_address_1'] = adm.corr_address_1
        data['corr_address_2'] = adm.corr_address_2
        data['corr_city'] = adm.corr_city
        data['corr_county'] = adm.corr_county
        data['corr_zip'] = adm.corr_zip
        data['corr_country'] = adm.corr_country
        data['perma_corr'] = adm.perma_corr
        if not data['perma_corr']:
            data['perma_address_1'] = adm.perma_address_1
            data['perma_address_2'] = adm.perma_address_2
            data['perma_city'] = adm.perma_city
            data['perma_county'] = adm.perma_county
            data['perma_zip'] = adm.perma_zip
            data['perma_country'] = adm.perma_country
            data['perma_moved_from'] = adm.perma_moved_from
            data['perma_moved_to'] = adm.perma_moved_to
        data['contact_number'] = adm.contact_number
        data['email'] = adm.email
    elif step == 5:
        adm.last_step = 5
        data['school'] = adm.school
        data['qualified_date'] = adm.qualified_date
        if data['qualified_date'] == 'Other':
            data['qualified_type'] = adm.qualified_type
        data['major'] = adm.major
        if data['major'] == 'Other':
            data['major_type'] = adm.major_type
        data['start_date'] = adm.start_date
        data['completion_date'] = adm.completion_date
        data['transcript_date'] = adm.transcript_date
        data['other_qualifications'] = adm.other_qualifications
        data['transcript_copy'] = adm.transcript_copy
        data['degree_cerf_copy'] = adm.degree_cerf_copy
    elif step == 6:
        adm.last_step = 6
        data['is_english_first_language'] = adm.is_english_first_language
        data['UK_qualification_equivalent'] = adm.UK_qualification_equivalent
        if data['UK_qualification_equivalent']:
            data['uqe_country'] = adm.uqe_country
        data['ELT'] = adm.ELT
        if data['ELT']:
            data['ELT_type'] = adm.ELT_type
        data['ELT_date'] = adm.ELT_date
        data['overall_score'] = adm.overall_score
        data['listening_score'] = adm.listening_score
        data['reading_score'] = adm.reading_score
        data['writing_score'] = adm.writing_score
        data['speaking_score'] = adm.speaking_score
        data['ELT_alternative'] = adm.ELT_alternative
        if data['ELT_alternative'] != 'No':
            data['alternative_date'] = adm.alternative_date
            data['alternative_grade'] = adm.alternative_grade
        data['ELT_other'] = adm.ELT_other
    elif step == 7:
        adm.last_step = 7
        data['personal_statement'] = adm.personal_statement
        data['research_proposal'] = adm.research_proposal
        data['pg_diploma'] = adm.pg_diploma
    elif step == 8:
        adm.last_step = 8
        data['first_reference'] = adm.first_reference
        data['second_reference'] = adm.second_reference
    elif step == 9:
        adm.last_step = 9
        data['agree_terms'] = adm.agree_terms
    elif step == 10:
        adm.last_step = 10
        data['admission_cols'] = [column.key for column in Admission.__table__.columns]
        data['ads'] = current_user.admissions[0]

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
            adm.issue_date = request.form.get("issue_date")
            passport_file = request.files.get("passport_copy")
            if passport_file:
                filename = Hash_User_File(secure_filename(passport_file.filename), current_user.id)
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
            if request.form.get("perma_corr").lower() == 'no':
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
            if request.form.get("transcript_date"):
                adm.transcript_date = request.form.get("transcript_date")
            if request.form.get("other_qualifications").lower() == 'no':
                adm.other_qualifications = False
            else:
                adm.other_qualifications = True

            transcript_file = request.files.get("transcript_copy")
            if transcript_file:
                filename = Hash_User_File(secure_filename(transcript_file.filename), current_user.id)
                filepath = "uploads/files/transcripts/" + filename
                transcript_file.save(filepath)
                adm.transcript_copy = filepath
            degree_cerf_file = request.files.get("degree_cerf_copy")
            if degree_cerf_file:
                filename = Hash_User_File(secure_filename(degree_cerf_file.filename), current_user.id)
                filepath = "uploads/files/degree_cerfs/" + filename
                degree_cerf_file.save(filepath)
                adm.degree_cerf_copy = filepath
        elif step == 6:
            if request.form.get("is_english_first_language") == 'no':
                adm.is_english_first_language = False
            else:
                adm.is_english_first_language = True
            if request.form.get("UK_qualification_equivalent") == 'no':
                adm.UK_qualification_equivalent = False
            else:
                adm.UK_qualification_equivalent = True
            adm.uqe_country = request.form.get("uqe_country")
            if request.form.get("ELT") == 'no':
                adm.ELT = False
            else:
                adm.ELT = True
            adm.ELT_type = request.form.get("ELT_type")
            if request.form.get("ELT_date"):
                adm.ELT_date = request.form.get("ELT_date")
            adm.overall_score = request.form.get("overall_score")
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
                filename = Hash_User_File(secure_filename(personal_statement_file.filename), current_user.id)
                filepath = "uploads/files/" + filename
                personal_statement_file.save(filepath)
                adm.personal_statement = filepath
            research_proposal_file = request.files.get("research_proposal")
            if research_proposal_file:
                filename = Hash_User_File(secure_filename(research_proposal_file.filename), current_user.id)
                filepath = "uploads/files/" + filename
                research_proposal_file.save(filepath)
                adm.research_proposal = filepath
            cv_file = request.files.get("cv")
            if cv_file:
                filename = Hash_User_File(secure_filename(cv_file.filename), current_user.id)
                filepath = "uploads/files/" + filename
                cv_file.save(filepath)
                adm.cv = filepath
            pg_diploma_file = request.files.get("pg_diploma")
            if pg_diploma_file:
                filename = Hash_User_File(secure_filename(pg_diploma_file.filename), current_user.id)
                filepath = "uploads/files/" + filename
                pg_diploma_file.save(filepath)
                adm.pg_diploma = filepath
        elif step == 8:
            first_reference_file = request.files.get("first_reference")
            if first_reference_file:
                filename = Hash_User_File(secure_filename(first_reference_file.filename), current_user.id)
                filepath = "uploads/files/" + filename
                first_reference_file.save(filepath)
                adm.first_reference = filepath
            second_reference_file = request.files.get("second_reference")
            if second_reference_file:
                filename = Hash_User_File(secure_filename(second_reference_file.filename), current_user.id)
                
                filepath = "uploads/files/" + filename
                second_reference_file.save(filepath)
                adm.second_reference = filepath
        elif step == 9:
            if request.form.get("agree_terms") == 'on':
                adm.agree_terms = True
            else:
                adm.agree_terms = False
            if not (adm.firstname and adm.surname and adm.DoB and adm.nationality):
                return redirect(url_for('admission', step=1))
            elif not (adm.passport and adm.expiry_date and adm.passport_copy):
                return redirect(url_for('admission', step=3))
            elif not (adm.contact_number and adm.email and adm.corr_address_1 and adm.corr_city and adm.corr_zip and ((adm.perma_corr) or (not adm.perma_corr and adm.perma_address_1 and adm.perma_city and adm.perma_zip and adm.perma_moved_from and adm.perma_moved_to))):
                return redirect(url_for('admission', step=4))
            elif not ((adm.school and adm.start_date and adm.completion_date and adm.transcript_date and adm.transcript_copy and adm.degree_cerf_copy) and ((adm.qualified_date == 'Other Qualification' and adm.qualified_type) or (adm.qualified_date != 'Other Qualification')) and ((adm.major == 'Other subject not listed here' and adm.major_type) or (adm.major != 'Other subject not listed here'))):
                return redirect(url_for('admission', step=5))
            elif not ((adm.ELT_date and adm.alternative_date and adm.alternative_grade)):
                return redirect(url_for('admission', step=6))
            elif not ((adm.personal_statement and adm.research_proposal)):
                return redirect(url_for('admission', step=7))
            elif not ((adm.first_reference and adm.second_reference)):
                return redirect(url_for('admission', step=8))
        elif step == 10:
            adm.submitted = True
            adm.status = 'pending'
            
        db.session.add(adm)
        db.session.commit()
        print(request.form.get('step'))
        if int(request.form.get('step')) == 10 and int(request.form.get('prev')) == 0:
            flash("Your admission submitted", "success")
            return redirect(url_for("index"))
        if int(request.form.get('prev')) == 0:
            return redirect(url_for('admission', step=int(request.form.get('step')) + 1))
        else:
            return redirect(url_for('admission', step=int(request.form.get('step')) - 1))
    return render_template('pages/admission.html', step=step, data=data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('pages/index.html')



@app.route('/uploads/<path:path>')
def send_from_pth(path):
    print(f'path is {path}')
    if path.startswith("uploads"):
        real_p = path.replace("\\", '/')
        real_p = real_p.split("/")[1:]
        real_p = '/'.join(real_p)
    return send_from_directory('uploads', real_p)

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
                email = email_,
            )
            t_us.set_password(password)
            while True:
                pin_code = ''
                for i in range(7):
                    pin_code = pin_code + str(random.randint(0, 9))
                if not User.query.filter_by(pin=pin_code).first():
                    t_us.pin = pin_code
                    break
            db.session.add(t_us)
            db.session.commit()
            return jsonify({'msg' : 'ok'}),200
    else:
        return jsonify({"message":"Method not allowed"}),405

@app.route("/single_admission/<int:id>")
@login_required
def single_admission(id):
    if current_user.role != 'admin':
        return redirect(url_for("index"))
    u = User.query.get_or_404(id)
    data = {}
    data['admission_cols'] = [column.key for column in Admission.__table__.columns]
    try:
        data['ads'] = u.admissions[0]
    except:
        flash("This user does not have admission yet", 'danger')
        return redirect(url_for("index"))
    return render_template("pages/single_admission.html", data=data)

@app.route("/all_admissions")
def all_admissions():
    data = {}
    data['all'] = User.query.all()
    data["user_cols"] = [column.key for column in User.__table__.columns]
    
    return render_template('pages/all_admissions.html', data=data)

@app.route("/accept_admission", methods=["POST"])
@login_required
def accept_admission():
    ad_id = request.form.get("admission_id")
    adm = Admission.query.get(ad_id)
    adm.accepted = True
    adm.status = 'accepted'
    db.session.commit()
    return redirect(url_for("all_admissions"))


@app.route("/reject_admission", methods=["POST"])
@login_required
def reject_admission():
    ad_id = request.form.get("admission_id")
    adm = Admission.query.get(ad_id)
    adm.accepted = False
    adm.status = 'rejected'
    db.session.commit()
    return redirect(url_for("all_admissions"))
