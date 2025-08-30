#!/bin/bash
set -e  # Exit on any error

echo "Setting up Mini RAG Full-Stack Application..."
echo

echo "1. Setting up Backend..."
cd backend || { echo "Error: backend directory not found"; exit 1; }
python3 -m venv venv || { echo "Error: Failed to create virtual environment"; exit 1; }
source venv/bin/activate || { echo "Error: Failed to activate virtual environment"; exit 1; }
pip install -r requirements.txt || { echo "Error: Failed to install Python dependencies"; exit 1; }
echo "Backend setup complete!"
echo

echo "2. Setting up Frontend..."
cd ../frontend || { echo "Error: frontend directory not found"; exit 1; }
npm install || { echo "Error: Failed to install Node.js dependencies"; exit 1; }
echo "Frontend setup complete!"
echo

echo "3. Setup Instructions:"
echo "- Copy backend/.env.example to backend/.env and add your API keys"
echo "- Copy frontend/.env.example to frontend/.env (optional)"
echo "- Run 'cd backend && source venv/bin/activate && uvicorn app.main:app --reload' for backend"
echo "- Run 'cd frontend && npm start' for frontend"
echo
echo "Setup complete! Check README.md for detailed instructions."