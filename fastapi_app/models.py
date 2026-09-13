from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "core_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True)
    password = Column(String(128))
    role = Column(String(10))

    projects = relationship("Project", back_populates="student")
    feedback_given = relationship("Feedback", back_populates="teacher")


class Project(Base):
    __tablename__ = "core_project"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    project_link = Column(String(200))
    student_id = Column(Integer, ForeignKey("core_user.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    student = relationship("User", back_populates="projects")
    feedback_list = relationship("Feedback", back_populates="project")


class Feedback(Base):
    __tablename__ = "core_feedback"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("core_project.id"))
    teacher_id = Column(Integer, ForeignKey("core_user.id"))
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime)

    project = relationship("Project", back_populates="feedback_list")
    teacher = relationship("User", back_populates="feedback_given")