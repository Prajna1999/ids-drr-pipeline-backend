#!/bin/bash


# Create virtual environment
python3 -m venv ids-drr-backend
source ids-drr-backend/bin/activate

# Install required packages
pip install flask flask-restful pydantic requests aiohttp sqlalchemy psycopg2-binary pytest black isort mypy

# Create project structure
mkdir app tests

# Create main application file
cat > app/__init__.py <<EOL
from flask import Flask
from flask_restful import Api

def create_app():
    app = Flask(__name__)
    api = Api(app)
    
    # Add routes here
    
    return app
EOL

# Create configuration file
cat > app/config.py <<EOL
from pydantic import BaseSettings

class Settings(BaseSettings):
    API_URL: str
    API_KEY: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
EOL

# Create API client file
cat > app/api_client.py <<EOL
import aiohttp
from app.config import settings

async def fetch_disaster_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{settings.API_URL}", headers={"Authorization": f"Bearer {settings.API_KEY}"}) as response:
            return await response.json()
EOL

# Create models file
cat > app/models.py <<EOL
from pydantic import BaseModel
from datetime import datetime

class DisasterData(BaseModel):
    id: int
    event_type: str
    location: str
    timestamp: datetime
    severity: int
EOL

# Create main file
cat > main.py <<EOL
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
EOL

# Create test file
cat > tests/test_api.py <<EOL
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    response = client.get('/')
    assert response.status_code == 200
EOL

# Create requirements file
pip freeze > requirements.txt

# Create .env file (don't forget to fill in the actual values)
cat > .env <<EOL
API_URL=https://api.example.com/disaster_data
API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:password@localhost/dbname
EOL

# Create .gitignore file
cat > .gitignore <<EOL
venv/
__pycache__/
*.pyc
.env
EOL


git add .
git commit -m "Initial commit"

echo "Flask backend for $PROJECT_NAME has been set up successfully!"