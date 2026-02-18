import os
from unittest.mock import MagicMock, patch

os.environ.setdefault("OPENAI_API_KEY", "test-key")

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

# Disable rate limiting in tests
app.state.limiter._default_limits = []

MOCK_QUERY_RESULTS = {
    "ids": [["onboarding.md::chunk0", "onboarding.md::chunk1"]],
    "distances": [[0.2, 0.4]],
    "documents": [["First chunk text.", "Second chunk text."]],
    "metadatas": [[{"section": "Intro", "chunk_index": 0}, {"section": "Setup", "chunk_index": 1}]],
}


@pytest.fixture
def client():
    return TestClient(app)


# --- Health ---


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


# --- /api/docs ---


def test_list_docs(client):
    res = client.get("/api/docs")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(name.endswith(".md") for name in data)


def test_get_doc_valid(client):
    res = client.get("/api/docs/onboarding.md")
    assert res.status_code == 200
    data = res.json()
    assert data["filename"] == "onboarding.md"
    assert len(data["content"]) > 0


@pytest.mark.parametrize("filename", [
    "../secret.md",
    "../../etc/passwd",
    "docs/../../secret.md",
    "file\\path.md",
])
def test_get_doc_path_traversal(client, filename):
    res = client.get(f"/api/docs/{filename}")
    assert res.status_code == 404


def test_get_doc_not_found(client):
    res = client.get("/api/docs/nonexistent-file.md")
    assert res.status_code == 404


# --- /retrieve ---


@patch("backend.app.main.collection")
def test_retrieve(mock_col, client):
    mock_col.count.return_value = 5
    mock_col.query.return_value = MOCK_QUERY_RESULTS
    res = client.post("/retrieve", json={"query": "How do I onboard?"})
    assert res.status_code == 200
    data = res.json()
    assert len(data["results"]) == 2
    assert data["results"][0]["doc_id"] == "onboarding.md::chunk0"
    assert data["results"][0]["score"] == 0.8


@patch("backend.app.main.collection")
def test_retrieve_empty_collection(mock_col, client):
    mock_col.count.return_value = 0
    res = client.post("/retrieve", json={"query": "test"})
    assert res.status_code == 503


# --- /query ---


@patch("backend.app.main.openai_client")
@patch("backend.app.main.collection")
def test_query(mock_col, mock_openai, client):
    mock_col.count.return_value = 5
    mock_col.query.return_value = MOCK_QUERY_RESULTS
    choice = MagicMock()
    choice.message.content = "Mocked answer."
    mock_openai.chat.completions.create.return_value = MagicMock(choices=[choice])

    res = client.post("/query", json={"query": "How do I onboard?"})
    assert res.status_code == 200
    data = res.json()
    assert data["answer"] == "Mocked answer."
    assert "onboarding.md" in data["sources"]
    assert len(data["chunks"]) == 2


@patch("backend.app.main.collection")
def test_query_empty_collection(mock_col, client):
    mock_col.count.return_value = 0
    res = client.post("/query", json={"query": "test"})
    assert res.status_code == 503


@patch("backend.app.main.openai_client")
@patch("backend.app.main.collection")
def test_query_openai_failure(mock_col, mock_openai, client):
    mock_col.count.return_value = 5
    mock_col.query.return_value = MOCK_QUERY_RESULTS
    mock_openai.chat.completions.create.side_effect = Exception("API timeout")

    res = client.post("/query", json={"query": "test"})
    assert res.status_code == 503
    assert "LLM request failed" in res.json()["detail"]
