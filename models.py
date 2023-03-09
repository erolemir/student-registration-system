from database import Base
from sqlalchemy import Column,String,Integer,Text


"""
class student:
    name:str
    age:int
    reg_no:text

"""

class Student(Base):
    __tablename__="students"
    id=Column(Integer(),primary_key=True) #Coulmn sutün özelliğini belirtmemize yarar.
    name=Column(String())
    age=Column(Integer())
    registration_no=Column(Text())

    def __repr__(self):
        return f"<student{self.name}>"