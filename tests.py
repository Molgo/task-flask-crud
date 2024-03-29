import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"
tasks = []

def test_create_task():
    new_task_data = {
        "title": "Flask",
        "description": "Documentação"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json
    tasks.append(response_json["id"])


def test_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200
    response_json = response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json

def test_get_task():
    if tasks:
        task_id = tasks[0]
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert task_id == response_json["id"]

def test_update_task():
    if tasks:
       task_id = tasks[0]
       update_data = {
           "title": "Novo título",
            "description": "Nova descrição",
            "completed": True 
       }
       response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data)
       assert response.status_code == 200
       response_json = response.json()
       assert "message" in response_json
       assert task_id == response_json["id"]

       response = requests.get(f"{BASE_URL}/tasks/{task_id}")
       response_json = response.json()
       assert update_data["title"] == response_json["title"]
       assert update_data["description"] == response_json["description"]
       assert update_data["completed"] == response_json["completed"]

def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200

        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 404
