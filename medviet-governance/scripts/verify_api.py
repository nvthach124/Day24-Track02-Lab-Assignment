import requests
import json
import time

BASE_URL = "http://localhost:8000"

TOKENS = {
    "admin": "token-alice",
    "ml_engineer": "token-bob",
    "data_analyst": "token-carol",
    "intern": "token-dave"
}

def test_endpoint(name, method, path, role=None, expected_status=200):
    url = f"{BASE_URL}{path}"
    headers = {}
    if role:
        headers["Authorization"] = f"Bearer {TOKENS[role]}"
    
    print(f"Testing {name} as {role or 'anonymous'}...")
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    
    print(f"  Status: {response.status_code}")
    if response.status_code == expected_status:
        print(f"  ✅ SUCCESS")
    else:
        print(f"  ❌ FAILED (Expected {expected_status}, got {response.status_code})")
        print(f"  Response: {response.text}")
    print("-" * 40)

if __name__ == "__main__":
    # 1. Test Health
    test_endpoint("Health Check", "GET", "/health")

    # 2. Test Raw Data (Admin only)
    test_endpoint("Raw Data", "GET", "/api/patients/raw", role="admin", expected_status=200)
    test_endpoint("Raw Data", "GET", "/api/patients/raw", role="ml_engineer", expected_status=403)

    # 3. Test Anonymized Data (Admin & ML Engineer)
    test_endpoint("Anonymized Data", "GET", "/api/patients/anonymized", role="ml_engineer", expected_status=200)
    test_endpoint("Anonymized Data", "GET", "/api/patients/anonymized", role="data_analyst", expected_status=403)

    # 4. Test Aggregated Metrics (Admin, ML Engineer, Data Analyst)
    test_endpoint("Aggregated Metrics", "GET", "/api/metrics/aggregated", role="data_analyst", expected_status=200)
    test_endpoint("Aggregated Metrics", "GET", "/api/metrics/aggregated", role="intern", expected_status=403)

    # 5. Test Delete (Admin only)
    test_endpoint("Delete Patient", "DELETE", "/api/patients/123", role="admin", expected_status=200)
    test_endpoint("Delete Patient", "DELETE", "/api/patients/123", role="ml_engineer", expected_status=403)
