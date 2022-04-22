from sqlalchemy.orm import relationship

from app import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    courses = relationship("Course", cascade='all, delete, delete-orphan')

    def json(self):
        return {'id': self.id, 'name': self.name, 'surname': self.surname, 'courses': [x.json() for x in self.courses]}


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    grade = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id", ondelete="CASCADE"))
    student = relationship("Student", back_populates="courses")

    def json(self):
        return {'id': self.id, 'name': self.name, 'grade': self.grade}
