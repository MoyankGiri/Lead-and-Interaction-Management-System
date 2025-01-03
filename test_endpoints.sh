#!/bin/bash

# Base URL of the API
BASE_URL="http://localhost:8000"

# Credentials for testing
USERNAME="testuser"
PASSWORD="testpassword"

echo "=== Testing FastAPI Endpoints ==="

# 1. Register a new user
echo "Registering a new user..."
curl -X POST "$BASE_URL/auth/register" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}"
echo -e "\n"

# 2. Login to get the JWT token
echo "Logging in..."
TOKEN=$(curl -s -X POST "$BASE_URL/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=$USERNAME&password=$PASSWORD" | jq -r '.access_token')

if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
    echo "Login failed! Exiting..."
    exit 1
fi
echo "JWT Token obtained: $TOKEN"
echo -e "\n"

# 3. Test the protected endpoints
echo "Testing /leads endpoint..."
curl -X GET "$BASE_URL/leads/?skip=0&limit=100" \
    -H "Authorization: Bearer $TOKEN"
echo -e "\n"

# Create a Lead
echo "Creating a new lead..."
curl -X POST "$BASE_URL/leads" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "restaurant_name": "Test Restaurant12",
        "address": "13 Test St, Test City",
        "status": "Active",
        "call_frequency": 5,
        "last_call_date": "2024-12-31"
    }'
echo -e "\n"

echo "Testing /leads endpoint..."
curl -X GET "$BASE_URL/leads/?skip=0&limit=100" \
    -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "Testing /leads/due_today endpoint..."
curl -X GET "$BASE_URL/leads/due_today" \
    -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "Testing /pocs endpoint (GET POCs for a lead)..."
curl -X GET "$BASE_URL/pocs/1" \
    -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "Testing /interactions endpoint (GET interactions for a lead)..."
curl -X GET "$BASE_URL/interactions/1" \
    -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "Testing /performance/well_performing endpoint..."
curl -X GET "$BASE_URL/performance/well_performing" \
    -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "Testing /performance/underperforming endpoint..."
curl -X GET "$BASE_URL/performance/underperforming" \
    -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "=== Testing Completed ==="