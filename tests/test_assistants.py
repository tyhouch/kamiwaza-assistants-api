# tests/test_assistants.py
import pytest
from unittest.mock import patch

def test_create_assistant(client):
    """Test creating a new assistant."""
    assistant_data = {
        "model": "gpt-4",
        "name": "Test Assistant",
        "instructions": "Test instructions",
        "tools": []
    }
    
    response = client.post("/v1/assistants", json=assistant_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["object"] == "assistant"
    assert data["name"] == assistant_data["name"]
    assert data["model"] == assistant_data["model"]
    assert data["instructions"] == assistant_data["instructions"]
    assert "id" in data
    assert "created_at" in data

def test_get_assistant(client, created_assistant):
    """Test retrieving an assistant."""
    response = client.get(f"/v1/assistants/{created_assistant['id']}")
    assert response.status_code == 200
    
    data = response.json()
    assert data == created_assistant

def test_list_assistants(client, created_assistant):
    """Test listing assistants with pagination."""
    # Create a second assistant
    second_assistant = {
        "model": "gpt-4",
        "name": "Second Assistant",
        "instructions": "More instructions",
        "tools": []
    }
    client.post("/v1/assistants", json=second_assistant)
    
    # Test default pagination
    response = client.get("/v1/assistants")
    assert response.status_code == 200
    
    data = response.json()
    assert data["object"] == "list"
    assert len(data["data"]) == 2
    assert "first_id" in data
    assert "last_id" in data
    assert "has_more" in data

def test_update_assistant(client, created_assistant):
    """Test updating an assistant."""
    update_data = {
        "name": "Updated Assistant",
        "instructions": "Updated instructions"
    }
    
    response = client.post(
        f"/v1/assistants/{created_assistant['id']}", 
        json=update_data
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["instructions"] == update_data["instructions"]
    assert data["id"] == created_assistant["id"]

def test_delete_assistant(client, created_assistant):
    """Test deleting an assistant."""
    response = client.delete(f"/v1/assistants/{created_assistant['id']}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == created_assistant["id"]
    assert data["object"] == "assistant.deleted"
    assert data["deleted"] is True

    # Verify assistant is deleted
    get_response = client.get(f"/v1/assistants/{created_assistant['id']}")
    assert get_response.status_code == 404

def test_invalid_assistant_id(client):
    """Test handling invalid assistant IDs."""
    invalid_id = "invalid_id"
    response = client.get(f"/v1/assistants/{invalid_id}")
    assert response.status_code == 400
    assert "error" in response.json()

def test_assistant_not_found(client):
    """Test handling non-existent assistant ID."""
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/v1/assistants/{non_existent_id}")
    assert response.status_code == 404
    assert "error" in response.json()

def test_invalid_create_data(client):
    """Test creating assistant with invalid data."""
    invalid_data = {
        "name": "Test Assistant",
        # Missing required 'model' field
    }
    
    response = client.post("/v1/assistants", json=invalid_data)
    assert response.status_code == 400
    assert "error" in response.json()