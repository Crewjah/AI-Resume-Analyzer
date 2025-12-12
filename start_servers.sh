#!/bin/bash
# Start both backend and frontend servers for AI Resume Analyzer

# Kill any existing servers
pkill -f "python.*backend/app.py" 2>/dev/null
pkill -f "python.*http.server.*8000" 2>/dev/null
sleep 1

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Start backend
echo "🚀 Starting backend on http://0.0.0.0:5000..."
python backend/app.py > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
sleep 2

# Check if backend started successfully
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Backend started successfully (PID: $BACKEND_PID)"
else
    echo "❌ Backend failed to start"
    cat /tmp/backend.log
    exit 1
fi

# Start frontend
echo "🚀 Starting frontend on http://0.0.0.0:8000..."
python -m http.server 8000 -d frontend > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
sleep 1

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  ✅ AI Resume Analyzer is now running                 ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📍 Backend API:  http://localhost:5000"
echo "📍 Frontend UI:  http://localhost:8000"
echo ""
echo "Backend PID:  $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "📊 Check logs:"
echo "   Backend:  tail -f /tmp/backend.log"
echo "   Frontend: tail -f /tmp/frontend.log"
echo ""
echo "🛑 To stop servers:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "   OR: pkill -f 'python.*app.py|http.server'"
echo ""
echo "🌐 Open browser: http://localhost:8000"
echo ""
