#!/bin/bash

PORT=${1:-8080}
BASE_URL="http://localhost:$PORT"

echo "Testing ML Service API on port $PORT"
echo "=========================================="

echo ""
echo "1. Testing /health endpoint:"
curl -s $BASE_URL/health | python3 -m json.tool

echo ""
echo "2. Testing root endpoint:"
curl -s $BASE_URL/ | python3 -m json.tool

echo ""
echo "3. Testing /predict endpoint with sample data:"
curl -s -X POST $BASE_URL/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}' | python3 -m json.tool

echo ""
echo "4. Testing /predict with different sample:"
curl -s -X POST $BASE_URL/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [6.7, 3.1, 4.7, 1.5]}' | python3 -m json.tool

echo ""
echo "=========================================="
echo "Testing complete"
