from sqlalchemy import create_engine, Column, String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import date
import pymysql


Base = declarative_base()

# MySQL connection string (update with your credentials)
DATABASE_URI = 'mysql+pymysql://root:@localhost/note_manage'


engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Base Class for CRUD Operations
class BaseModel:
    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    @classmethod
    def get_all(cls):
        return session.query(cls).all()

    @classmethod
    def get_by_id(cls, record_id):
        return session.query(cls).filter_by(id=record_id).first()

# Entity: Student
class Student(Base, BaseModel):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    birthdate = Column(Date)
    email = Column(String(255))
    phone = Column(String(20))
    mclass_id = Column(Integer, ForeignKey('mclasses.id'))
    mclass = relationship('MClass', back_populates='students')
    notes = relationship('NoteGoupe', back_populates='student')

# Entity: MClass
class MClass(Base, BaseModel):
    __tablename__ = 'mclasses'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    year = Column(Integer)
    students = relationship('Student', back_populates='mclass')

# Entity: Group
class Group(Base, BaseModel):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    notes = relationship('NoteGoupe', back_populates='group')

# Entity: Evalution
class Evalution(Base, BaseModel):
    __tablename__ = 'evalutions'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    desc = Column(String(255))
    notes = relationship('NoteGoupe', back_populates='evalution')

# Entity: NoteGoupe
class NoteGoupe(Base, BaseModel):
    __tablename__ = 'notegoupes'
    id = Column(Integer, primary_key=True)
    note = Column(Float)
    student_id = Column(Integer, ForeignKey('students.id'))
    student = relationship('Student', back_populates='notes')
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship('Group', back_populates='notes')
    evalution_id = Column(Integer, ForeignKey('evalutions.id'))
    evalution = relationship('Evalution', back_populates='notes')

# Create all tables
Base.metadata.create_all(engine)

# # Example Usage
# if __name__ == "__main__":
#     # Adding an MClass
#     mclass = MClass(name="Physics 202", year=2024)
#     mclass.save()
#
#     # Adding a Student
#     student = Student(name="John Doe", birthdate=date(2000, 1, 1), email="john@example.com", phone="1234567890", mclass=mclass)
#     student.save()
#
#     # Retrieve and display Students
#     students = Student.get_all()
#     for s in students:
#         print(f"Student: {s.name}, Email: {s.email}")
