from database import Base
from sqlalchemy import Column, Integer, String, Float, Date

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    approval_code = Column(String, unique=True)
    password = Column(String, nullable=False)