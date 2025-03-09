from datetime import date
from decimal import Decimal
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base, Employee
from config import get_settings

settings = get_settings()

# Sample employee data with various retirement scenarios
SAMPLE_EMPLOYEES = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "date_of_birth": date(1957, 6, 15),  # Retiring in June
        "hire_date": date(1990, 1, 1),
        "salary": Decimal("75000.00")
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "date_of_birth": date(1957, 12, 10),  # Retiring in December
        "hire_date": date(1995, 3, 15),
        "salary": Decimal("82000.00")
    },
    {
        "first_name": "Robert",
        "last_name": "Johnson",
        "email": "robert.johnson@example.com",
        "date_of_birth": date(1958, 3, 20),  # Retiring next year
        "hire_date": date(1992, 7, 1),
        "salary": Decimal("95000.00")
    },
    {
        "first_name": "Maria",
        "last_name": "Garcia",
        "email": "maria.garcia@example.com",
        "date_of_birth": date(1956, 9, 5),  # Already retirement age
        "hire_date": date(1988, 11, 30),
        "salary": Decimal("88000.00")
    },
    {
        "first_name": "William",
        "last_name": "Brown",
        "email": "william.brown@example.com",
        "date_of_birth": date(1957, 11, 25),  # Retiring in December
        "hire_date": date(1991, 4, 15),
        "salary": Decimal("79000.00")
    }
]

async def init_db():
    """Initialize the database with tables."""
    engine = create_async_engine(settings.DATABASE_URL, echo=settings.ECHO_SQL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Clear existing tables
        await conn.run_sync(Base.metadata.create_all)  # Create tables
    return engine

async def seed_employees(engine):
    """Seed the database with sample employees."""
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        for employee_data in SAMPLE_EMPLOYEES:
            employee = Employee(**employee_data)
            session.add(employee)
        await session.commit()

async def main():
    """Main function to run the seeding process."""
    engine = await init_db()
    await seed_employees(engine)
    print("Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(main()) 