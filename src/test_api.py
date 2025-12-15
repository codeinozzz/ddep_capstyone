import requests
import json

BASE_URL = "http://localhost:8000"


def test_health():
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")


def test_create_session():
    print("Testing create session...")
    response = requests.post(f"{BASE_URL}/api/sessions")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}\n")
    return data["session_id"]


def test_chat(session_id):
    print("Testing chat endpoint...")
    payload = {
        "session_id": session_id,
        "message": "genera especificacion para cocina minimalista mediana",
        "config": {"style": "minimalist", "default_mode": "spec", "max_steps": 30},
    }

    response = requests.post(f"{BASE_URL}/api/chat", json=payload)

    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response type: {data['response_type']}")
    if data.get("text_content"):
        print(f"Text preview: {data['text_content'][:200]}...\n")


def test_get_history(session_id):
    print("Testing get history...")
    response = requests.get(f"{BASE_URL}/api/history/{session_id}")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Message count: {data['message_count']}\n")


def test_update_config(session_id):
    print("Testing update config...")
    payload = {"style": "modern", "max_steps": 75}

    response = requests.patch(f"{BASE_URL}/api/config/{session_id}", json=payload)

    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Updated config: {data['config']}\n")


if __name__ == "__main__":
    print("=" * 50)
    print("API Test Suite")
    print("=" * 50 + "\n")

    try:
        test_health()
        session_id = test_create_session()
        test_chat(session_id)
        test_get_history(session_id)
        test_update_config(session_id)

        print("=" * 50)
        print("All tests completed")
        print("=" * 50)

    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the API is running on http://localhost:8000")
