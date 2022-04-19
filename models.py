from sqlalchemy.orm import relationship

from app import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    courses = relationship("Course")


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    student = relationship("Student", back_populates="courses")
