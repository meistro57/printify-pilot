#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Install Python dependencies
if [ -f "$DIR/requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r "$DIR/requirements.txt"
fi

# Install Node dependencies
if [ -d "$DIR/webpack-app" ]; then
    echo "Installing Node dependencies..."
    (cd "$DIR/webpack-app" && npm install)
fi

# Start Flask backend
echo "Starting Flask backend..."
python "$DIR/app.py" &
FLASK_PID=$!

trap 'kill $FLASK_PID' EXIT

# Start React frontend
cd "$DIR/webpack-app"
echo "Starting React dev server..."
npm start
