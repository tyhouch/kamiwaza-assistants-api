# tests/test_runs.py

import pytest
from uuid import uuid4

def create_test_thread(client):
    """Helper to create a new thread and return its ID."""
    res = client.post("/v1/threads", json={})
    assert res.status_code == 200
    return res.json()["id"]

def create_test_assistant(client):
    """Helper to create an assistant and return its data."""
    assistant_data = {
        "model": "gpt-4",
        "name": "Test Assistant for Runs",
        "instructions": "Some instructions"
    }
    response = client.post("/v1/assistants", json=assistant_data)
    assert response.status_code == 200
    return response.json()

def test_create_run(client):
    """Test creating a run with placeholder LLM response."""
    thread_id = create_test_thread(client)
    assistant_data = create_test_assistant(client)

    run_data = {
        "assistant_id": assistant_data["id"],
        "model": "gpt-4",  # optional override
        "instructions": "Override instructions"
    }
    res = client.post(f"/v1/threads/{thread_id}/runs", json=run_data)
    assert res.status_code == 200
    data = res.json()
    assert data["object"] == "thread.run"
    assert data["status"] == "completed"
    assert data["model"] == "gpt-4"
    assert data["instructions"] == "Override instructions"

    # Check the placeholder assistant message was created
    msg_list = client.get(f"/v1/threads/{thread_id}/messages").json()
    assert len(msg_list["data"]) == 1
    assert msg_list["data"][0]["role"] == "assistant"
    assert msg_list["data"][0]["content"][0]["text"]["value"] == "This is a placeholder response from the run."

def test_list_runs(client):
    """Test listing runs in a thread."""
    thread_id = create_test_thread(client)
    assistant_data = create_test_assistant(client)

    # Create two runs
    for i in range(2):
        run_data = {
            "assistant_id": assistant_data["id"],
            "model": "gpt-4"
        }
        client.post(f"/v1/threads/{thread_id}/runs", json=run_data)

    run_list = client.get(f"/v1/threads/{thread_id}/runs")
    assert run_list.status_code == 200
    data = run_list.json()
    assert data["object"] == "list"
    assert len(data["data"]) == 2

def test_get_run(client):
    """Test retrieving a single run."""
    thread_id = create_test_thread(client)
    asst_data = create_test_assistant(client)

    run_data = {
        "assistant_id": asst_data["id"]
    }
    run_res = client.post(f"/v1/threads/{thread_id}/runs", json=run_data)
    run_id = run_res.json()["id"]

    get_res = client.get(f"/v1/threads/{thread_id}/runs/{run_id}")
    assert get_res.status_code == 200
    data = get_res.json()
    assert data["id"] == run_id
    assert data["thread_id"] == thread_id

def test_update_run_metadata(client):
    """Test updating run metadata."""
    thread_id = create_test_thread(client)
    asst_data = create_test_assistant(client)

    # Create run
    run_data = {"assistant_id": asst_data["id"]}
    run_res = client.post(f"/v1/threads/{thread_id}/runs", json=run_data)
    run_id = run_res.json()["id"]

    # Update
    upd_res = client.post(
        f"/v1/threads/{thread_id}/runs/{run_id}",
        json={"test_meta": "run_update"}
    )
    assert upd_res.status_code == 200
    data = upd_res.json()
    assert data["metadata"]["test_meta"] == "run_update"

def test_run_not_found_in_thread(client):
    """Test retrieving a run with mismatched thread ID."""
    # Create two threads
    t1 = create_test_thread(client)
    t2 = create_test_thread(client)
    asst_data = create_test_assistant(client)

    # Create a run in t1
    run_data = {"assistant_id": asst_data["id"]}
    run_res = client.post(f"/v1/threads/{t1}/runs", json=run_data)
    run_id = run_res.json()["id"]

    # Attempt to fetch that run from t2
    get_res = client.get(f"/v1/threads/{t2}/runs/{run_id}")
    assert get_res.status_code == 404
    data = get_res.json()
    assert "error" in data
