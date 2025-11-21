from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test listing rules
def test_list_rules():
    resp = client.get("/api/rules")

    assert resp.status_code == 200
    assert "rules" in resp.json()
    assert isinstance(resp.json()["rules"], list)
