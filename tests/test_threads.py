# tests/test_threads.py

import pytest
from uuid import uuid4

def test_create_thread(client):
    """Test creating a new thread with no initial messages."""
    response = client.post("/v1/threads", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["object"] == "thread"
    assert "id" in data
    assert "created_at" in data
    assert data["metadata"] == {}
    assert data["tool_resources"] is None

def test_create_thread_with_messages(client):
    """Test creating a new thread with initial messages."""
    thread_data = {
        "messages": [
            {"role": "user", "content": "Hello World"}
        ]
    }
    response = client.post("/v1/threads", json=thread_data)
    assert response.status_code == 200
    data = response.json()
    assert data["object"] == "thread"
    thread_id = data["id"]

    # Now list messages to confirm the initial message was created
    msg_res = client.get(f"/v1/threads/{thread_id}/messages")
    assert msg_res.status_code == 200
    msg_data = msg_res.json()
    assert len(msg_data["data"]) == 1
    assert msg_data["data"][0]["role"] == "user"
    assert msg_data["data"][0]["content"][0]["text"]["value"] == "Hello World"

def test_get_thread_not_found(client):
    """Test retrieving a non-existent thread."""
    fake_id = str(uuid4())
    response = client.get(f"/v1/threads/{fake_id}")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data

def test_update_thread(client):
    """Test updating a thread's metadata."""
    # Create a thread
    thread_res = client.post("/v1/threads", json={})
    thread_id = thread_res.json()["id"]

    # Update it
    update_data = {
        "metadata": {"updated": "true"},
        "tool_resources": {"file_search": {"vector_store_ids": ["vs_123"]}}
    }
    update_res = client.post(f"/v1/threads/{thread_id}", json=update_data)
    assert update_res.status_code == 200
    data = update_res.json()
    assert data["metadata"] == {"updated": "true"}
    assert data["tool_resources"] == {"file_search": {"vector_store_ids": ["vs_123"]}}

def test_delete_thread(client):
    """Test deleting a thread."""
    # Create a thread
    thread_res = client.post("/v1/threads", json={})
    thread_id = thread_res.json()["id"]

    # Delete it
    del_res = client.delete(f"/v1/threads/{thread_id}")
    assert del_res.status_code == 200
    del_data = del_res.json()
    assert del_data["object"] == "thread.deleted"
    assert del_data["deleted"] is True

    # Verify retrieving the thread returns 404
    get_res = client.get(f"/v1/threads/{thread_id}")
    assert get_res.status_code == 404
