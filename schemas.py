from datetime import date
from decimal import Decimal
from typing import List
from pydantic import BaseModel, EmailStr, Field

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
    # id: int
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