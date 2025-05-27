import requests
import json

def test_api():
    base_url = "http://localhost:5000"
    
    # Test health endpoint
    print("\nTesting health endpoint...")
    health_response = requests.get(f"{base_url}/api/health")
    print(f"Health check response: {json.dumps(health_response.json(), indent=2)}")
    
    # Test ask endpoint
    print("\nTesting ask endpoint...")
    test_message = "ኢትዮጵያ"  # Test with Amharic query
    response = requests.post(
        f"{base_url}/api/ask",
        json={"message": test_message}
    )
    
    if response.status_code == 200:
        print("\nSuccessful response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"\nError response (status code: {response.status_code}):")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_api() 