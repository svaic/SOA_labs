import connexion
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def get_students():
    students = db.session.query(Student).all()
    return [x.json() for x in students]


def student_add(student_body):
    new_student = Student(name=student_body['name'], surname=student_body['surname'])
    db.session.add(new_student)
    db.session.commit()
    return new_student.json()


def find_student(student_id):
    found_student = query_student(student_id)
    if found_student:
        return found_student.json()
    else:
        return {'error': '{} not found'.format(student_id)}, 404


def edit_student(student_id, student_body):
    student = query_student(student_id)
    if student:
        for property_name, value in student_body.items():
            setattr(student, property_name, value)
        db.session.add(student)
        db.session.commit()
        return student.json()
    else:
        return {'error': '{} not found'.format(student_id)}, 404


def delete_student(student_id):
    student = query_student(student_id)
    if student:
        response = student.json()
        Student.query.filter_by(id=student_id).delete()
        db.session.commit()
        return response
    else:
        return {'error': '{} not found'.format(student_id)}, 404


def get_courses():
    courses = db.session.query(Course).all()
    return [x.json() for x in courses]


def find_course(course_id):
    course = db.session.query(Course).filter_by(id=course_id).first()
    if course:
        return course.json()
    else:
        return {'error': '{} not found'.format(course_id)}, 404


def add_course(student_id, course_body):
    student = query_student(student_id)
    new_course = Course(name=course_body['name'], grade=course_body['grade'])
    student.courses.append(new_course)
    db.session.add(new_course)
    db.session.commit()
    return new_course.json()


def edit_course(course_id, course_body):
    course = query_course(course_id)
    if course:
        course = update_model(course, course_body)
        return course.json()
    else:
        return {'error': '{} not found'.format(course_id)}, 404


def delete_course(course_id):
    course = query_course(course_id)
    if course:
        response = course.json()
        Course.query.filter_by(id=course_id).delete()
        db.session.commit()
        return response
    else:
        return {'error': '{} not found'.format(course_id)}, 404


def query_student(student_id):
    return Student.query.filter_by(id=student_id).first()


def query_course(course_id):
    return Course.query.filter_by(id=course_id).first()


def update_model(model, upodate_params):
    for property, value in upodate_params.items():
        setattr(model, property, value)
    db.session.add(model)
    db.session.commit()
    return model


connexion_app = connexion.App(__name__, specification_dir="./")
app = connexion_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/courses'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
connexion_app.add_api("api.yml")

from models import Student, Course

if __name__ == '__main__':
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)
