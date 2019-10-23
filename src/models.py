from sqlalchemy import Table, Column, Integer, String, ForeignKey Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


student_subject = Table('student_subject', Base.metadata,
                        Column('student_id', Integer, ForeignKey('student.id')),
                        Column('subject_id', Integer, ForeignKey('subject.id')),
                        )




class TimeSlot(Base):
    __tablename__ = 'time_slot'

    id = Column(Integer, primary_key=True)
    day = Column(Enum(["MONDAY", "TUESDAY", "WEDNESDAY",
                        "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]))
    number = Column(Integer)
    subjects = relationship("Subject",
                            secondary=subject_time_slot,
                            back_populates="time_slots")


class Subject(Base):
    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    time_slots = relationship("TimeSlot",
                              secondary=subject_time_slot,
                              back_populates="subjects")
                              
    students = relationship("Student",
                            secondary=student_subject,
                            back_populates="subjects")


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    subjects = relationship("Subject",
                            secondary=student_subject,
                            back_populates="students")
