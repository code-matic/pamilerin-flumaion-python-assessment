from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pydantic import Field, validator
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings.
    
    All settings can be overridden by environment variables.
    Example:
        APP_NAME="Custom Name" python main.py
    """
    
    # Application Settings
    APP_NAME: str = Field(
        default=os.getenv("APP_NAME", "Employee Retirement Calculator"),
        description="Name of the application"
    )
    APP_HOST: str = Field(
        default=os.getenv("APP_HOST", "0.0.0.0"),
        description="Host to run the application on"
    )
    APP_PORT: int = Field(
        default=int(os.getenv("APP_PORT", "8000")),
        description="Port to run the application on",
        gt=0,
        lt=65536
    )

    # Database Settings
    DATABASE_URL: str = Field(
        default=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./retirement.db")
    )
    ECHO_SQL: bool = Field(
        default=os.getenv("ECHO_SQL", "true").lower() == "true"
    )

    # Business Rules
    RETIREMENT_AGE: int = Field(
        default=int(os.getenv("RETIREMENT_AGE", "67")),
        description="Age at which employees retire",
        gt=0,
        lt=100
    )
    CALCULATION_MONTHS: str = Field(
        default=os.getenv("CALCULATION_MONTHS", "6,12"),
        description="Comma-separated list of months (1-12) when retirement calculations are run"
    )

    @validator("CALCULATION_MONTHS")
    def validate_calculation_months(cls, v: str) -> str:
        """Validate that calculation months are valid (1-12) and properly formatted."""
        try:
            months = [int(month.strip()) for month in v.split(",")]
            if not all(1 <= month <= 12 for month in months):
                raise ValueError("Months must be between 1 and 12")
            if len(months) != len(set(months)):
                raise ValueError("Duplicate months are not allowed")
            if not months:
                raise ValueError("At least one calculation month is required")
            # Sort and reconstruct the string to ensure consistent format
            return ",".join(str(month) for month in sorted(months))
        except ValueError as e:
            raise ValueError(f"Invalid CALCULATION_MONTHS format: {e}")

    @property
    def calculation_months(self) -> List[int]:
        """Get list of months when calculations should be run."""
        return [int(month) for month in self.CALCULATION_MONTHS.split(",")]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        # Add validation error messages to help users fix configuration issues
        validate_default=True,
        # Allow environment variables to override defaults
        env_prefix="",
        # Add extra documentation
        title="Employee Retirement Calculator Settings",
        description="Configuration settings for the Employee Retirement Calculator application"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings() 