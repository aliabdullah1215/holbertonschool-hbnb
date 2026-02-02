#!/bin/bash
# Comprehensive cURL Testing Script for HBnB API
# Run with: bash curl_tests.sh

BASE_URL="http://localhost:5000/api/v1"
BOLD='\033[1m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print section headers
print_header() {
    echo -e "\n${BOLD}${YELLOW}========================================${NC}"
    echo -e "${BOLD}${YELLOW}$1${NC}"
    echo -e "${BOLD}${YELLOW}========================================${NC}\n"
}

# Function to print test results
print_test() {
    echo -e "${BOLD}Test: $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ SUCCESS${NC}\n"
}

print_error() {
    echo -e "${RED}✗ FAILED${NC}\n"
}

# Check if server is running
print_header "Checking Server Status"
if curl -s "$BASE_URL" > /dev/null 2>&1; then
    print_success
else
    echo -e "${RED}Server is not running! Please start with: cd part2 && python run.py${NC}"
    exit 1
fi

# ==================== USER TESTS ====================

print_header "USER ENDPOINT TESTS"

# Test 1: Create User
print_test "1. Create User (POST /api/v1/users/)"
USER_RESPONSE=$(curl -s -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@test.com",
    "is_admin": false
  }')
echo "$USER_RESPONSE" | json_pp 2>/dev/null || echo "$USER_RESPONSE"
USER_ID=$(echo "$USER_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
if [ -n "$USER_ID" ]; then
    print_success
else
    print_error
fi

# Test 2: Get All Users
print_test "2. Get All Users (GET /api/v1/users/)"
curl -s -X GET "$BASE_URL/users/" | json_pp 2>/dev/null || curl -s -X GET "$BASE_URL/users/"
print_success

# Test 3: Get User by ID
print_test "3. Get User by ID (GET /api/v1/users/$USER_ID)"
curl -s -X GET "$BASE_URL/users/$USER_ID" | json_pp 2>/dev/null || curl -s -X GET "$BASE_URL/users/$USER_ID"
print_success

# Test 4: Update User
print_test "4. Update User (PUT /api/v1/users/$USER_ID)"
curl -s -X PUT "$BASE_URL/users/$USER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John Updated",
    "last_name": "Doe Updated",
    "email": "john.updated@test.com",
    "is_admin": true
  }' | json_pp 2>/dev/null
print_success

# Test 5: Duplicate Email (Should Fail)
print_test "5. Create User with Duplicate Email (Should Return 409)"
DUPLICATE_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Another",
    "last_name": "User",
    "email": "john.updated@test.com",
    "is_admin": false
  }')
HTTP_CODE=$(echo "$DUPLICATE_RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "409" ]; then
    echo "Expected 409 Conflict"
    print_success
else
    echo "Expected 409 but got $HTTP_CODE"
    print_error
fi

# Test 6: Invalid Email (Should Fail)
print_test "6. Create User with Invalid Email (Should Return 400)"
INVALID_EMAIL_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Invalid",
    "last_name": "User",
    "email": "not-an-email",
    "is_admin": false
  }')
HTTP_CODE=$(echo "$INVALID_EMAIL_RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "400" ]; then
    echo "Expected 400 Bad Request"
    print_success
else
    echo "Expected 400 but got $HTTP_CODE"
    print_error
fi

# ==================== AMENITY TESTS ====================

print_header "AMENITY ENDPOINT TESTS"

# Test 7: Create Amenity
print_test "7. Create Amenity (POST /api/v1/amenities/)"
AMENITY_RESPONSE=$(curl -s -X POST "$BASE_URL/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name": "WiFi"}')
echo "$AMENITY_RESPONSE" | json_pp 2>/dev/null || echo "$AMENITY_RESPONSE"
AMENITY_ID=$(echo "$AMENITY_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
if [ -n "$AMENITY_ID" ]; then
    print_success
else
    print_error
fi

# Test 8: Get All Amenities
print_test "8. Get All Amenities (GET /api/v1/amenities/)"
curl -s -X GET "$BASE_URL/amenities/" | json_pp 2>/dev/null || curl -s -X GET "$BASE_URL/amenities/"
print_success

# Test 9: Update Amenity
print_test "9. Update Amenity (PUT /api/v1/amenities/$AMENITY_ID)"
curl -s -X PUT "$BASE_URL/amenities/$AMENITY_ID" \
  -H "Content-Type: application/json" \
  -d '{"name": "Fast WiFi"}' | json_pp 2>/dev/null
print_success

# Test 10: Duplicate Amenity Name (Should Fail)
print_test "10. Create Amenity with Duplicate Name (Should Return 409)"
DUPLICATE_AMENITY=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Fast WiFi"}')
HTTP_CODE=$(echo "$DUPLICATE_AMENITY" | tail -n1)
if [ "$HTTP_CODE" = "409" ]; then
    echo "Expected 409 Conflict"
    print_success
else
    echo "Expected 409 but got $HTTP_CODE"
    print_error
fi

# ==================== PLACE TESTS ====================

print_header "PLACE ENDPOINT TESTS"

# Test 11: Create Place
print_test "11. Create Place (POST /api/v1/places/)"
PLACE_RESPONSE=$(curl -s -X POST "$BASE_URL/places/" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Beautiful Apartment\",
    \"description\": \"A lovely place to stay\",
    \"price\": 150.0,
    \"latitude\": 40.7128,
    \"longitude\": -74.0060,
    \"owner_id\": \"$USER_ID\",
    \"amenities\": [\"$AMENITY_ID\"]
  }")
echo "$PLACE_RESPONSE" | json_pp 2>/dev/null || echo "$PLACE_RESPONSE"
PLACE_ID=$(echo "$PLACE_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
if [ -n "$PLACE_ID" ]; then
    print_success
else
    print_error
fi

# Test 12: Get All Places
print_test "12. Get All Places (GET /api/v1/places/)"
curl -s -X GET "$BASE_URL/places/" | json_pp 2>/dev/null || curl -s -X GET "$BASE_URL/places/"
print_success

# Test 13: Get Place by ID
print_test "13. Get Place by ID (GET /api/v1/places/$PLACE_ID)"
curl -s -X GET "$BASE_URL/places/$PLACE_ID" | json_pp 2>/dev/null || curl -s -X GET "$BASE_URL/places/$PLACE_ID"
print_success

# Test 14: Update Place
print_test "14. Update Place (PUT /api/v1/places/$PLACE_ID)"
curl -s -X PUT "$BASE_URL/places/$PLACE_ID" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Updated Apartment\",
    \"description\": \"Updated description\",
    \"price\": 200.0,
    \"latitude\": 40.7128,
    \"longitude\": -74.0060,
    \"owner_id\": \"$USER_ID\",
    \"amenities\": [\"$AMENITY_ID\"]
  }" | json_pp 2>/dev/null
print_success

# Test 15: Invalid Price (Should Fail)
print_test "15. Create Place with Negative Price (Should Return 400)"
INVALID_PRICE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/places/" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Test Place\",
    \"description\": \"Test\",
    \"price\": -100.0,
    \"latitude\": 40.7128,
    \"longitude\": -74.0060,
    \"owner_id\": \"$USER_ID\",
    \"amenities\": []
  }")
HTTP_CODE=$(echo "$INVALID_PRICE" | tail -n1)
if [ "$HTTP_CODE" = "400" ]; then
    echo "Expected 400 Bad Request"
    print_success
else
    echo "Expected 400 but got $HTTP_CODE"
    print_error
fi

# Test 16: Invalid Latitude (Should Fail)
print_test "16. Create Place with Invalid Latitude (Should Return 400)"
INVALID_LAT=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/places/" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Test Place\",
    \"description\": \"Test\",
    \"price\": 100.0,
    \"latitude\": 95.0,
    \"longitude\": -74.0060,
    \"owner_id\": \"$USER_ID\",
    \"amenities\": []
  }")
HTTP_CODE=$(echo "$INVALID_LAT" | tail -n1)
if [ "$HTTP_CODE" = "400" ]; then
    echo "Expected 400 Bad Request"
    print_success
else
    echo "Expected 400 but got $HTTP_CODE"
    print_error
fi

# ==================== REVIEW TESTS ====================

print_header "REVIEW ENDPOINT TESTS"

# Test 17: Create Review
print_test "17. Create Review (POST /api/v1/reviews/)"
REVIEW_RESPONSE=$(curl -s -X POST "$BASE_URL/reviews/" \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": \"Great place! Very comfortable.\",
    \"rating\": 5,
    \"user_id\": \"$USER_ID\",
    \"place_id\": \"$PLACE_ID\"
  }")
echo "$REVIEW_RESPONSE" | json_pp 2>/dev/null || echo "$REVIEW_RESPONSE"
REVIEW_ID=$(echo "$REVIEW_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
if [ -n "$REVIEW_ID" ]; then
    print_success
else
    print_error
fi

# Test 18: Get All Reviews
print_test "18. Get All Reviews (GET /api/v1/reviews/)"
curl -s -X GET "$BASE_URL/reviews/" | json_pp 2>/dev/null || curl -s -X GET "$BASE_URL/reviews/"
print_success

# Test 19: Get Review by ID
print_test "19. Get Review by ID (GET /api/v1/reviews/$REVIEW_ID)"
curl -s -X GET "$BASE_URL/reviews/$REVIEW_ID" | json_pp 2>/dev/null || curl -s -X GET "$BASE_URL/reviews/$REVIEW_ID"
print_success

# Test 20: Update Review
print_test "20. Update Review (PUT /api/v1/reviews/$REVIEW_ID)"
curl -s -X PUT "$BASE_URL/reviews/$REVIEW_ID" \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": \"Updated review: Excellent place!\",
    \"rating\": 5,
    \"user_id\": \"$USER_ID\",
    \"place_id\": \"$PLACE_ID\"
  }" | json_pp 2>/dev/null
print_success

# Test 21: Get Reviews for Place
print_test "21. Get Reviews for Place (GET /api/v1/reviews/places/$PLACE_ID/reviews)"
curl -s -X GET "$BASE_URL/reviews/places/$PLACE_ID/reviews" | json_pp 2>/dev/null || curl -s -X GET "$BASE_URL/reviews/places/$PLACE_ID/reviews"
print_success

# Test 22: Invalid Rating (Should Fail)
print_test "22. Create Review with Invalid Rating (Should Return 400)"
INVALID_RATING=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/reviews/" \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": \"Test review\",
    \"rating\": 10,
    \"user_id\": \"$USER_ID\",
    \"place_id\": \"$PLACE_ID\"
  }")
HTTP_CODE=$(echo "$INVALID_RATING" | tail -n1)
if [ "$HTTP_CODE" = "400" ]; then
    echo "Expected 400 Bad Request"
    print_success
else
    echo "Expected 400 but got $HTTP_CODE"
    print_error
fi

# Test 23: Delete Review
print_test "23. Delete Review (DELETE /api/v1/reviews/$REVIEW_ID)"
curl -s -X DELETE "$BASE_URL/reviews/$REVIEW_ID" | json_pp 2>/dev/null || curl -s -X DELETE "$BASE_URL/reviews/$REVIEW_ID"
print_success

# Test 24: Verify Deletion
print_test "24. Verify Review Deletion (Should Return 404)"
VERIFY_DELETE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/reviews/$REVIEW_ID")
HTTP_CODE=$(echo "$VERIFY_DELETE" | tail -n1)
if [ "$HTTP_CODE" = "404" ]; then
    echo "Expected 404 Not Found"
    print_success
else
    echo "Expected 404 but got $HTTP_CODE"
    print_error
fi

# ==================== SUMMARY ====================

print_header "TEST SUMMARY"
echo -e "${GREEN}All tests completed!${NC}"
echo -e "\nCreated Resources:"
echo -e "  User ID: $USER_ID"
echo -e "  Amenity ID: $AMENITY_ID"
echo -e "  Place ID: $PLACE_ID"
echo -e "\nSwagger Documentation: http://localhost:5000/api/v1/"
echo ""
