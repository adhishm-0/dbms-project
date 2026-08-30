#!/usr/bin/env bash
# Single command to run both backend and frontend for development (POSIX bash)
# Usage: ./run.sh
set -e
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

# Start backend in a virtualenv
cd "$ROOT_DIR/app/backend"
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
# run uvicorn in background
nohup uvicorn main:app --reload --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
cd "$ROOT_DIR"

# Start frontend
cd "$ROOT_DIR/app/frontend"
if [ ! -d "node_modules" ]; then
  npm install
fi
# start vite (dev server)
npm run dev &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID (http://localhost:8000)"
echo "Frontend PID: $FRONTEND_PID (usually http://localhost:5173)"
echo "Open http://localhost:5173 to view the site."

echo "To stop: kill $BACKEND_PID $FRONTEND_PID"

# wait for child processes
wait
