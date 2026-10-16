from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_checks_postgres_and_redis():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["postgres"] is True
    assert data["redis"] is True


def test_seeded_group_exists():
    response = client.get("/groups/1")

    assert response.status_code == 200
    data = response.json()
    assert data["group_id"] == 1
    assert len(data["members"]) >= 3


def test_unknown_group_returns_404():
    response = client.get("/groups/999999")

    assert response.status_code == 404


def test_bill_rejects_invalid_payer():
    response = client.post(
        "/groups/1/bills",
        json={
            "payer_id": 999999,
            "amount": 100,
            "note": "Invalid payer test",
        },
    )

    assert response.status_code == 400


def test_bill_rejects_shares_that_do_not_match_amount():
    response = client.post(
        "/groups/1/bills",
        json={
            "payer_id": 1,
            "amount": 100,
            "note": "Invalid shares test",
            "shares": {
                "1": 1000,
                "2": 1000,
                "3": 1000,
            },
        },
    )

    assert response.status_code == 400
