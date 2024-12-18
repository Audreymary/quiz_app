# models.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    
    # Define a relationship with the Option model
    options = relationship("Option", back_populates="question")
    
    def __repr__(self):
        return f"<Question(id={self.id}, text={self.text})>"

class Option(Base):
    __tablename__ = 'options'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    
    # Define a relationship with the Question model
    question = relationship("Question", back_populates="options")
    
    def __repr__(self):
        return f"<Option(id={self.id}, text={self.text})>"

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    option_id = Column(Integer, ForeignKey('options.id'), nullable=False)
    
    # Define a relationship with the Option model
    option = relationship("Option")
    
    def __repr__(self):
        return f"<Answer(id={self.id}, option_id={self.option_id})>"

# Database Setup
def create_session():
    engine = create_engine('sqlite:///quiz.db', echo=True)  # SQLite database
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
