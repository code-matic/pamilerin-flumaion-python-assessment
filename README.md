# Employee Retirement Calculator

A simple FastAPI application that calculates employee retirement information and total salary liability.

## Features

- Calculate retirement dates for employees
- Determine employees retiring by next calculation date (June or December)
- Calculate total salary liability for retiring employees
- Simple SQLite database for storing employee information
- Dockerized deployment
- Test data seeding for development

## Running with Docker

1. Build and start the application:
```bash
docker-compose up --build
```

2. In a separate terminal, seed the test data:
```bash
docker-compose run seed
```

The application will be available at http://localhost:8000

### Test Data

The seeder creates 5 sample employees with different retirement scenarios:
- John Doe: Retiring in June
- Jane Smith: Retiring in December
- Robert Johnson: Retiring next year
- Maria Garcia: Already at retirement age
- William Brown: Retiring in December

Total salary liability for December retirements: $161,000.00 (Jane Smith + William Brown)

## Running Locally

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Seed the database (optional):
```bash
python seed_data.py
```

4. Run the application:
```bash
python main.py
```

The application will be available at http://localhost:8000

## API Endpoints

### Create Employee
```http
POST /employees/
```
Request body:
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "date_of_birth": "1956-03-15",
    "hire_date": "1990-01-01",
    "salary": "75000.00"
}
```

### Calculate Retirement
```http
GET /retirement-calculation/?calculation_date=2024-03-09
```
Optional query parameter:
- `calculation_date`: Date to calculate retirements from (defaults to current date)

## Documentation

API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment

The application is deployed on Google Cloud Run:
- Base URL: https://flumaion-assessment-749119130796.us-central1.run.app
- Swagger UI: https://flumaion-assessment-749119130796.us-central1.run.app/docs
- ReDoc: https://flumaion-assessment-749119130796.us-central1.run.app/redoc
- Health Check: https://flumaion-assessment-749119130796.us-central1.run.app/health

### Testing the Deployed API

1. Health Check:
```bash
curl https://flumaion-assessment-749119130796.us-central1.run.app/health
```

2. Create an Employee:
```bash
curl -X POST https://flumaion-assessment-749119130796.us-central1.run.app/employees/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "date_of_birth": "1960-01-01",
    "hire_date": "2000-01-01",
    "salary": 75000.00
  }'
```

3. Calculate Retirement:
```bash
curl "https://flumaion-assessment-749119130796.us-central1.run.app/retirement-calculation/?calculation_date=2024-03-10"
```

## Development with Docker

The application uses Docker volumes to enable hot-reloading in development. Any changes made to the local files will be reflected immediately in the running container.

To view logs:
```bash
docker-compose logs -f api
```

To stop the application:
```bash
docker-compose down
```

### Testing with Sample Data

The seed data includes employees with various retirement scenarios to test different cases:

1. Test June retirement calculation:
```bash
curl "http://localhost:8000/retirement-calculation/?calculation_date=2024-05-01"
```

2. Test December retirement calculation:
```bash
curl "http://localhost:8000/retirement-calculation/?calculation_date=2024-11-01"
```

Expected results:
- June calculation will include John Doe
- December calculation will include Jane Smith and William Brown
- All calculations will include Maria Garcia (already at retirement age)