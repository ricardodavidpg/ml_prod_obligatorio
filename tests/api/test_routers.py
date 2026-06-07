


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_classification_endpoint(client):
    payload = {"texts": ["I love this class", "I hate this"]}
    response = client.post("/classification/texts", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["texts"]) == 2
    assert all(text["label"] for text in data["texts"])
    assert all(text["score"] for text in data["texts"])


def test_classification_empty_input(client):
    payload = {"texts": []}
    response = client.post("/classification/texts", json=payload)
    assert response.status_code == 200
    assert response.json()["texts"] == []


def test_classification_invalid_input(client):
    response = client.post("/classification/texts", json={"texts": "not a list"})
    assert response.status_code == 422


def test_classification_missing_field(client):
    response = client.post("/classification/texts", json={})
    assert response.status_code == 422