from functools import wraps

import connexion
from flask import request, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def student_add(student_body):
    new_student = Student(name=student_body['name'])
    db.session.add(new_student)
    db.session.commit()


def student_find(student_id):
    found_person = db.session.query(Student).filter_by(id=student_id).first()
    if found_person:
        return found_person
    else:
        return {'error': '{} not found'.format(student_id)}, 404


def course_add(course_body):
    return "test"
    # student = student_find(course_body['student_id'])
    # new_course = Course(name=course_body['name'])
    # student.courses.append(new_course)
    # db.session.add(student)
    # db.session.add(new_course)
    # db.session.commit()


connexion_app = connexion.App(__name__, specification_dir="./")
app = connexion_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/courses'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
connexion_app.add_api("api.yml")

from models import Student, Course

if __name__ == '__main__':
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)
