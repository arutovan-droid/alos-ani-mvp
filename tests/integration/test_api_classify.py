from fastapi.testclient import TestClient
from alos_core.customs.api import app

client = TestClient(app)


def test_classify_returns_hs_code():
    payload = {"text": "բլուտուզ խոսփաքեր"}
    resp = client.post("/classify", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["raw_input"] == payload["text"]
    assert data["hs_code"]  # непустой код
    assert "confidence" in data
    assert 0.0 <= data["confidence"] <= 1.0
