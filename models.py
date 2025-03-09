from datetime import date
from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from config import get_settings

# SQLAlchemy setup
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
        """Calculate retirement date based on configured retirement age."""
        settings = get_settings()
        return date(
            self.date_of_birth.year + settings.RETIREMENT_AGE,
            self.date_of_birth.month,
            self.date_of_birth.day
        ) 