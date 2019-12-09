from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os, random, datetime
app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, 'database.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    email = db.Column(db.String(100), primary_key=True, nullable=False, unique=False)
    name = db.Column(db.String(40), unique=True, nullable=False)
    program = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(100), nullable=True)

class Teacher(db.Model):
    email = db.Column(db.String(100), primary_key=True, nullable=False, unique=False)
    name = db.Column(db.String(40), unique=True, nullable=False)
    program = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(100), nullable=True)

db.create_all()
db.session.commit()


@app.route('/admin-login', methods=['POST', 'GET'])
def admin_login():
    if request.method == 'POST':
        name = request.form['name']
        students = Student.query.all()
        teachers = Teacher.query.all()
        password = request.form['pwd']
        if name == "saylani" and password == "saylani":
            return render_template('dashboard-admin.html', name=name, teachers=teachers, students=students)
        else:
            return render_template('admin-login.html')
    return render_template('index.html')


@app.route('/add-member', methods=['POST', 'GET'])
def add_member():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = random.randint(10000111, 23456789)
        program = request.form['programm']
        typ = request.form['type']
        date = datetime.datetime.now()
        if typ == "teacher":
            valid = Teacher.query.filter_by(email=email).first()
            if valid:
                students = Student.query.all()
                teachers = Teacher.query.all()
                return render_template('dashboard-admin.html', students=students, teachers=teachers)
            else:
                teacher = Teacher()
                teacher.email = email
                teacher.name = name
                teacher.program = program
                teacher.password = password
                teacher.date = date
                db.session.add(teacher)
                db.session.commit()
                students = Student.query.all()
                teachers = Teacher.query.all()
                return render_template('dashboard-admin.html', students=students, teachers=teachers)
        elif typ == "student":
            valid = Student.query.filter_by(email=email).first()
            if valid:
                students = Student.query.all()
                teachers = Teacher.query.all()
                return render_template('dashboard-admin.html', students=students, teachers=teachers)
            else:
                student = Student()
                student.email = email
                student.password = password
                student.date = date
                student.name = name
                student.program = program
                db.session.add(student)
                db.session.commit()
                students = Student.query.all()
                teachers = Teacher.query.all()
                return render_template('dashboard-admin.html', students=students, teachers=teachers)
        else:
            return render_template('dashboard-admin.html')
    return render_template('admin-login.html')


@app.route('/remove-member', methods=['POST', 'GET'])
def remove_member():
    if request.method == 'POST':
        email = request.form['email']
        typ = request.form['type']
        if typ == "teacher":
            valid = Teacher.query.filter_by(email=email).first()
            if valid:
                db.session.delete(valid)
                db.session.commit()
                students = Student.query.all()
                teachers = Teacher.query.all()
                return render_template('dashboard-admin.html', students=students, teachers=teachers)
            else:
                students = Student.query.all()
                teachers = Teacher.query.all()
                return render_template('dashboard-admin.html', students=students, teachers=teachers)
        elif typ == "student":
            valid = Student.query.filter_by(email=email).first()
            if valid:
                db.session.delete(valid)
                db.session.commit()
                students = Student.query.all()
                teachers = Teacher.query.all()

                return render_template('dashboard-admin.html', students=students, teachers=teachers)
            else:
                students = Student.query.all()
                teachers = Teacher.query.all()

                return render_template('dashboard-admin.html', students=students, teachers=teachers)
        return render_template('dashboard-admin.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    return render_template('index.html')


@app.route('/update-member', methods=['POST', 'GET'])
def to_update():
    if request.method == 'POST':
        email = request.form['old-mail']
        member = request.form['type']
        new_email = request.form['new-email']
        new_name = request.form['new-name']
        new_password = request.form['new-password']
        if member == "teacher":
            valid = Teacher.query.filter_by(email=email).first()
            if valid:
                valid.email = new_email
                valid.name = new_name
                valid.password = new_password
                db.session.add(valid)
                db.session.commit()
                students = Student.query.all()
                teachers = Teacher.query.all()

                return render_template('dashboard-admin.html', students=students, teachers=teachers)
            if not valid:
                students = Student.query.all()
                teachers = Teacher.query.all()
                return render_template('dashboard-admin.html', students=students, teachers=teachers)
        if member == "student":
            valid = Student.query.filter_by(email=email).first()
            if valid:
                valid.email = new_email
                valid.name = new_name
                valid.password = new_password
                db.session.add(valid)
                db.session.commit()
                students = Student.query.all()
                teachers = Teacher.query.all()
                return render_template('dashboard-admin.html', students=students, teachers=teachers)
            if not valid:
                students = Student.query.all()
                teachers = Teacher.query.all()

                return render_template('dashboard-admin.html', students=students, teachers=teachers)

    students = Student.query.all()
    teachers = Teacher.query.all()
    return render_template('dashboard-admin.html', students=students, teachers=teachers)


@app.route('/member-login', methods=['POST', 'GET'])
def member_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        member = request.form['type']
        if member == "teacher":
            valid = Teacher.query.filter_by(email=email, password=password).first()
            if valid:
                name = valid.name
                password = valid.password
                join_date = valid.date
                email = valid.email
                program = valid.program
                date = datetime.datetime.now()
                return render_template('use-page.html', name=name, password=password, join_date=join_date,
                                       program=program, date=date, email=email)
            if not valid:
                msg = "Invalid information"
                return render_template('user-login.html' , msg=msg)
        if member == "student":
            valid = Student.query.filter_by(email=email,password=password).first()
            if valid:
                name = valid.name
                password = valid.password
                join_date = valid.date
                program = valid.program
                email = valid.email
                date = datetime.datetime.now()
                return render_template('use-page.html',email=email, name=name, password=password, join_date=join_date,
                                       program=program, date=date)
            if not valid:
                msg = "invlid information"
                return render_template('user-login.html',msg=msg)
    return render_template('user-login.html')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin-login.html')

@app.route('/user')
def user():
    return render_template('user-login.html')

if __name__ == '__main__':
    app.run(debug=True)