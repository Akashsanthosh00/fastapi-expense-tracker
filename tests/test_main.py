from fastapi.testclient import TestClient
from main import app
from conftest import TestingSessionLocal
from user_models import User
from security import hash_password

client = TestClient(app)


def test_app_starts():
    response = client.get("/docs")

    assert response.status_code == 200


def test_get_expenses_without_authentication():
    response = client.get("/expenses")

    assert response.status_code == 401


def test_login():
    db = TestingSessionLocal()

    user = User(
        username="login_test_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/login",
        data={
            "username": "login_test_user",
            "password": "Test@123"
        }
    )

    db.close()

    assert response.status_code == 200

def test_get_expenses_with_authentication():
    db = TestingSessionLocal()

    user = User(
        username="expenseuser",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/login",
        data={
            "username": "expenseuser",
            "password": "Test@123"
        }
    )

    access_token = response.json()["access_token"]

    response = client.get(
        "/expenses",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    db.close()

    assert response.status_code == 200

def test_create_and_get_expense():
    db = TestingSessionLocal()

    user = User(
        username="expense_create_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "expense_create_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    expense_response = client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250.0,
            "category": "Food",
            "date": "2026-08-18"
        },
        headers=headers
    )

    assert expense_response.status_code == 201

    get_response = client.get(
        "/expenses",
        headers=headers
    )

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Lunch"

def test_update_expense():

    db = TestingSessionLocal()

    user = User(
        username="expense_update_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "expense_update_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    expense_response = client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250.0,
            "category": "Food",
            "date": "2026-08-18"
        },
        headers=headers
    )

    assert expense_response.status_code == 201

    expense_id = expense_response.json()["id"]

    update_response = client.put(
        f"/expenses?expense_id={expense_id}",
        json={
            "title": "Dinner",
            "amount": 500.0,
            "category": "Food",
            "date": "2026-08-18"
        },
        headers=headers
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["title"] == "Dinner"
    assert data["amount"] == 500.0
    assert data["category"] == "Food"

def test_delete_expense():

    db = TestingSessionLocal()

    user = User(
        username="expense_delete_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "expense_delete_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    expense_response = client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250.0,
            "category": "Food",
            "date": "2026-08-18"
        },
        headers=headers
    )

    assert expense_response.status_code == 201

    expense_id = expense_response.json()["id"]

    delete_response = client.delete(
        f"/expenses?expense_id={expense_id}",
        headers=headers
    )

    assert delete_response.status_code == 200

    data = delete_response.json()

    assert data["message"] == "Expense deleted successfully"

def test_patch_expense():

    db = TestingSessionLocal()

    user = User(
        username="expense_patch_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "expense_patch_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    expense_response = client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250.0,
            "category": "Food",
            "date": "2026-08-18"
        },
        headers=headers
    )

    assert expense_response.status_code == 201

    expense_id = expense_response.json()["id"]

    patch_response = client.patch(
        f"/expenses?expense_id={expense_id}",
        json={
            "amount": 500.0
        },
        headers=headers
    )

    assert patch_response.status_code == 200

    data = patch_response.json()

    assert data["amount"] == 500.0
    assert data["title"] == "Lunch"
    assert data["category"] == "Food"

# Delete a non-existent expense
def test_delete_nonexistent_expense():

    db = TestingSessionLocal()

    user = User(
        username="expense_delete_invalid_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "expense_delete_invalid_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    delete_response = client.delete(
        "/expenses?expense_id=99999",
        headers=headers
    )

    assert delete_response.status_code == 404

    data = delete_response.json()

    assert data["detail"] == "Expense not found"

#  PUT with a non-existent expense ID.
def test_update_nonexistent_expense():

    db = TestingSessionLocal()

    user = User(
        username="expense_update_invalid_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "expense_update_invalid_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    update_response = client.put(
        "/expenses?expense_id=99999",
        json={
            "title": "Dinner",
            "amount": 500.0,
            "category": "Food",
            "date": "2026-08-18"
        },
        headers=headers
    )

    assert update_response.status_code == 404

    data = update_response.json()

    assert data["detail"] == "Expense not found"

# PATCH non-existent expense test

def test_patch_nonexistent_expense():

    db = TestingSessionLocal()

    user = User(
        username="expense_patch_invalid_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "expense_patch_invalid_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    patch_response = client.patch(
        "/expenses?expense_id=99999",
        json={
            "amount": 500.0
        },
        headers=headers
    )

    assert patch_response.status_code == 404

    data = patch_response.json()

    assert data["detail"] == "Expense not found!"
