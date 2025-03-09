from datetime import date
from decimal import Decimal
from typing import List, Optional
from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from models import Base, Employee
from schemas import EmployeeCreate, EmployeeResponse, RetirementSummary
from config import get_settings

settings = get_settings()

# Database setup
engine = create_async_engine(settings.DATABASE_URL, echo=settings.ECHO_SQL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# FastAPI app
app = FastAPI(title=settings.APP_NAME)

# Database dependency
async def get_db():
    async with async_session() as session:
        yield session

# Initialize database
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def get_next_calculation_date(current_date: date) -> date:
    """Get the next calculation date (June or December)."""
    year = current_date.year
    calc_months = settings.calculation_months
    
    # Find the next calculation month
    for month in calc_months:
        if current_date.month < month:
            return date(year, month, 1)
    
    # If no remaining months this year, use first month of next year
    return date(year + 1, calc_months[0], 1)

@app.post("/employees/", response_model=EmployeeResponse)
async def create_employee(employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    """Create a new employee."""
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    await db.commit()
    await db.refresh(db_employee)
    return db_employee

@app.get("/retirement-calculation/", response_model=RetirementSummary)
async def calculate_retirement(
    calculation_date: Optional[date] = Query(
        None,
        description="Date to calculate retirements from (defaults to current date)"
    ),
    db: AsyncSession = Depends(get_db)
) -> RetirementSummary:
    """
    Calculate retirement information for employees.
    Returns list of retiring employees and total salary liability.
    Calculations are done for the next calculation date (June or December).
    """
    current_date = calculation_date or date.today()
    next_calc_date = get_next_calculation_date(current_date)
    
    # Query employees who will be at retirement age by the next calculation date
    retirement_cutoff_date = date(
        next_calc_date.year - settings.RETIREMENT_AGE,
        next_calc_date.month,
        next_calc_date.day
    )
    
    query = select(Employee).where(Employee.date_of_birth <= retirement_cutoff_date)
    result = await db.execute(query)
    retiring_employees = result.scalars().all()
    
    # Calculate total salary liability
    total_liability = sum((employee.salary for employee in retiring_employees), Decimal(0))
    
    return RetirementSummary(
        retiring_employees=retiring_employees,
        total_salary_liability=total_liability,
        calculation_date=current_date,
        next_calculation_date=next_calc_date
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.APP_HOST,
        port=settings.APP_PORT
    )
