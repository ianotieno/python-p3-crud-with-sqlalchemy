#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Add autoincrement=True
    name = Column(String)
    email = Column(String)
    grade = Column(Integer)
    birthday = Column(DateTime)

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    session.add_all([albert_einstein, alan_turing])  # Use add_all instead of bulk_save_objects
    session.commit()

    print(f"New student ID is {albert_einstein.id}.")
    print(f"New student ID is {alan_turing.id}.")
all_students = session.query(Student).all()

for student in all_students:
    print(f"Student ID: {student.id}, Name: {student.name}, Email: {student.email} Grade:{student.grade},Birthday:{student.birthday}")

names = [name for name in session.query(Student.name)]

print(names)

students_by_name = [student for student in session.query(
            Student.name).order_by(
            Student.name)]

print(students_by_name)
query = session.query(Student).filter(Student.name.like('%Alan%'),
        Student.grade == 11)
for record in query:
    print(record.name)

for student in session.query(Student):
        student.grade += 1

session.commit()

print([(student.name,
        student.grade) for student in session.query(Student)])

session.query(Student).update({
        Student.grade: Student.grade + 3
    })

print([(
        student.name,
        student.grade
    ) for student in session.query(Student)])
