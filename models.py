from datetime import date
from decimal import Decimal
from typing import List
from sqlalchemy import Column, Integer, String, Date, Numeric, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, EmailStr, Field

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./retirement.db"
Base = declarative_base()

class Employee(Base):
    """Employee model for storing employee information."""
    
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    hire_date = Column(Date, nullable=False)
    salary = Column(Numeric(10, 2), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    @property
    def age(self) -> int:
        """Calculate current age of employee."""
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    @property
    def retirement_date(self) -> date:
        """Calculate retirement date (when employee turns 67)."""
        return date(
            self.date_of_birth.year + 67,
            self.date_of_birth.month,
            self.date_of_birth.day
        )

# Pydantic models
class EmployeeBase(BaseModel):
    """Base schema for Employee data."""
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    date_of_birth: date
    hire_date: date
    salary: Decimal = Field(..., ge=0)

class EmployeeCreate(EmployeeBase):
    """Schema for creating a new employee."""
    pass

class EmployeeResponse(EmployeeBase):
    """Schema for employee response."""
    id: int
    age: int
    retirement_date: date

    class Config:
        from_attributes = True

class RetirementSummary(BaseModel):
    """Schema for retirement summary response."""
    retiring_employees: List[EmployeeResponse]
    total_salary_liability: Decimal
    calculation_date: date
    next_calculation_date: date 