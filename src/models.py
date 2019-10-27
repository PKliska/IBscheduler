import enum
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


student_subject = Table('student_subject', Base.metadata,
                        Column('student_id', Integer, ForeignKey('student.id')),
                        Column('subject_id', Integer, ForeignKey('subject.id')),
                        )

class DayOfWeek(enum.IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class Place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))


class TimePlace(Base):
    __tablename__ = 'time_place'

    id = Column(Integer, primary_key=True)
    day = Column(Enum(DayOfWeek))
    slot = Column(Integer)

    subject_id = Column(Integer, ForeignKey('subject.id'))

    place_id = Column(Integer, ForeignKey('place.id'))
    place = relationship("Place", backref='time_places')


class Subject(Base):
    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    abbreviation = Column(String(64))

    time_places = relationship("TimePlace",
                              backref='subject')

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
