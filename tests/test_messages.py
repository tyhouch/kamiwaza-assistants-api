# tests/test_messages.py

import pytest
from uuid import uuid4

def create_test_thread(client):
    """Helper to create a new thread and return its ID."""
    res = client.post("/v1/threads", json={})
    assert res.status_code == 200
    return res.json()["id"]

def test_create_message(client):
    """Test creating a user message in a thread."""
    thread_id = create_test_thread(client)
    msg_data = {
        "role": "user",
        "content": "Hello, Messages!"
    }
    res = client.post(f"/v1/threads/{thread_id}/messages", json=msg_data)
    assert res.status_code == 200
    data = res.json()
    assert data["role"] == "user"
    assert data["content"][0]["text"]["value"] == "Hello, Messages!"
    assert data["thread_id"] == thread_id

def test_list_messages(client):
    """Test listing messages in a thread."""
    thread_id = create_test_thread(client)

    # Create two messages
    for i in range(2):
        res = client.post(
            f"/v1/threads/{thread_id}/messages",
            json={"role": "user", "content": f"Message {i}"}
        )
        assert res.status_code == 200

    # List
    list_res = client.get(f"/v1/threads/{thread_id}/messages")
    assert list_res.status_code == 200
    data = list_res.json()
    assert data["object"] == "list"
    assert len(data["data"]) == 2
    assert data["data"][0]["role"] == "user"
    assert data["data"][1]["content"][0]["text"]["value"].startswith("Message")

def test_get_message(client):
    """Test retrieving a single message."""
    thread_id = create_test_thread(client)
    msg_res = client.post(
        f"/v1/threads/{thread_id}/messages",
        json={"role": "assistant", "content": "A single message test"}
    )
    msg_id = msg_res.json()["id"]

    get_res = client.get(f"/v1/threads/{thread_id}/messages/{msg_id}")
    assert get_res.status_code == 200
    data = get_res.json()
    assert data["id"] == msg_id
    assert data["role"] == "assistant"
    assert data["content"][0]["text"]["value"] == "A single message test"

def test_update_message(client):
    """Test updating a message's metadata."""
    thread_id = create_test_thread(client)
    # Create message
    msg_res = client.post(
        f"/v1/threads/{thread_id}/messages",
        json={"role": "user", "content": "Update me!"}
    )
    msg_id = msg_res.json()["id"]

    # Update
    update_res = client.post(
        f"/v1/threads/{thread_id}/messages/{msg_id}",
        json={"metadata": {"modified": "true"}}
    )
    assert update_res.status_code == 200
    data = update_res.json()
    assert data["metadata"]["modified"] == "true"

def test_delete_message(client):
    """Test deleting a message."""
    thread_id = create_test_thread(client)
    # Create message
    msg_res = client.post(
        f"/v1/threads/{thread_id}/messages",
        json={"role": "assistant", "content": "Will be deleted"}
    )
    msg_id = msg_res.json()["id"]

    # Delete
    del_res = client.delete(f"/v1/threads/{thread_id}/messages/{msg_id}")
    assert del_res.status_code == 200
    del_data = del_res.json()
    assert del_data["deleted"] is True
    assert del_data["object"] == "thread.message.deleted"

    # Confirm it's gone
    get_res = client.get(f"/v1/threads/{thread_id}/messages/{msg_id}")
    assert get_res.status_code == 404

def test_message_not_found_in_thread(client):
    """Test retrieving a message that doesn't belong to the thread."""
    # Create two threads
    t1 = create_test_thread(client)
    t2 = create_test_thread(client)

    # Create a message in t1
    msg_res = client.post(
        f"/v1/threads/{t1}/messages",
        json={"role": "assistant", "content": "Cross-thread fetch?"}
    )
    msg_id = msg_res.json()["id"]

    # Attempt to fetch that message from t2
    get_res = client.get(f"/v1/threads/{t2}/messages/{msg_id}")
    assert get_res.status_code == 404
    data = get_res.json()
    assert "error" in data
