#!/bin/bash
# Script to run both frontend and backend

echo "🚀 Starting Speech-to-Text Application"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to cleanup on exit
cleanup() {
    echo -e "\n${RED}Stopping services...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup EXIT INT TERM

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${RED}Error: Virtual environment not activated!${NC}"
    echo "Please run: source ~/envs/text2speach/bin/activate"
    exit 1
fi

# Start backend
echo -e "\n${BLUE}Starting Backend Server...${NC}"
cd ../backend
./start_server.sh &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "Waiting for backend to initialize..."
sleep 5

# Check if backend is running
if ! curl -s http://localhost:6541/health > /dev/null; then
    echo -e "${RED}Backend failed to start!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Backend is running on http://localhost:6541${NC}"

# Install frontend dependencies if needed
if [ ! -d "../frontend/node_modules" ]; then
    echo -e "\n${BLUE}Installing frontend dependencies...${NC}"
    cd ../frontend
    npm install
    cd ..
fi

# Start frontend
echo -e "\n${BLUE}Starting Frontend...${NC}"
cd ../frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 3

echo -e "\n${GREEN}✨ Application is ready!${NC}"
echo -e "${GREEN}===================================${NC}"
echo -e "Frontend: ${BLUE}http://localhost:6542${NC}"
echo -e "Backend:  ${BLUE}http://localhost:6541${NC}"
echo -e "\n${GREEN}Press Ctrl+C to stop${NC}\n"

# Keep script running
wait