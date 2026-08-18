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

# GET expenses without a token
def test_get_expenses_without_token():

    response = client.get("/expenses")

    assert response.status_code == 401


# POST /expenses without a token.
def test_create_expense_without_token():

    response = client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250.0,
            "category": "Food",
            "date": "2026-08-18"
        }
    )

    assert response.status_code == 401


# PUT without a token.
def test_update_expense_without_token():

    response = client.put(
        "/expenses?expense_id=1",
        json={
            "title": "Dinner",
            "amount": 500.0,
            "category": "Food",
            "date": "2026-08-18"
        }
    )

    assert response.status_code == 401


# Now PATCH without a token.
def test_patch_expense_without_token():

    response = client.patch(
        "/expenses?expense_id=1",
        json={
            "amount": 500.0
        }
    )

    assert response.status_code == 401

# Delete withouta token
def test_delete_expense_without_token():

    response = client.delete(
        "/expenses?expense_id=1"
    )

    assert response.status_code == 401

# authorization/user isolation
def test_user_cannot_delete_another_users_expense():

    db = TestingSessionLocal()

    user1 = User(
        username="expense_owner",
        password=hash_password("Test@123")
    )

    user2 = User(
        username="expense_other_user",
        password=hash_password("Test@123")
    )

    db.add_all([user1, user2])
    db.commit()

    # Login as User 1
    login_response = client.post(
        "/login",
        data={
            "username": "expense_owner",
            "password": "Test@123"
        }
    )

    token1 = login_response.json()["access_token"]

    headers1 = {
        "Authorization": f"Bearer {token1}"
    }

    # User 1 creates an expense
    expense_response = client.post(
        "/expenses",
        json={
            "title": "User 1 Lunch",
            "amount": 250.0,
            "category": "Food",
            "date": "2026-08-18"
        },
        headers=headers1
    )

    assert expense_response.status_code == 201

    expense_id = expense_response.json()["id"]

    # Login as User 2
    login_response = client.post(
        "/login",
        data={
            "username": "expense_other_user",
            "password": "Test@123"
        }
    )

    token2 = login_response.json()["access_token"]

    headers2 = {
        "Authorization": f"Bearer {token2}"
    }

    # User 2 tries to delete User 1's expense
    delete_response = client.delete(
        f"/expenses?expense_id={expense_id}",
        headers=headers2
    )

    assert delete_response.status_code == 404

    data = delete_response.json()

    assert data["detail"] == "Expense not found"

def test_user_cannot_update_another_users_expense():

    db = TestingSessionLocal()

    user1 = User(
        username="expense_put_owner",
        password=hash_password("Test@123")
    )

    user2 = User(
        username="expense_put_other_user",
        password=hash_password("Test@123")
    )

    db.add_all([user1, user2])
    db.commit()

    # Login as User 1
    login_response = client.post(
        "/login",
        data={
            "username": "expense_put_owner",
            "password": "Test@123"
        }
    )

    token1 = login_response.json()["access_token"]

    headers1 = {
        "Authorization": f"Bearer {token1}"
    }

    # User 1 creates an expense
    expense_response = client.post(
        "/expenses",
        json={
            "title": "User 1 Lunch",
            "amount": 250.0,
            "category": "Food",
            "date": "2026-08-18"
        },
        headers=headers1
    )

    assert expense_response.status_code == 201

    expense_id = expense_response.json()["id"]

    # Login as User 2
    login_response = client.post(
        "/login",
        data={
            "username": "expense_put_other_user",
            "password": "Test@123"
        }
    )

    token2 = login_response.json()["access_token"]

    headers2 = {
        "Authorization": f"Bearer {token2}"
    }

    # User 2 tries to update User 1's expense
    update_response = client.put(
        f"/expenses?expense_id={expense_id}",
        json={
            "title": "Hacked Expense",
            "amount": 9999.0,
            "category": "Shopping",
            "date": "2026-08-18"
        },
        headers=headers2
    )

    assert update_response.status_code == 404

    data = update_response.json()

    assert data["detail"] == "Expense not found"


def test_user_cannot_patch_another_users_expense():

    db = TestingSessionLocal()

    user1 = User(
        username="expense_patch_owner",
        password=hash_password("Test@123")
    )

    user2 = User(
        username="expense_patch_other_user",
        password=hash_password("Test@123")
    )

    db.add_all([user1, user2])
    db.commit()

    # Login as User 1
    login_response = client.post(
        "/login",
        data={
            "username": "expense_patch_owner",
            "password": "Test@123"
        }
    )

    token1 = login_response.json()["access_token"]

    headers1 = {
        "Authorization": f"Bearer {token1}"
    }

    # User 1 creates an expense
    expense_response = client.post(
        "/expenses",
        json={
            "title": "User 1 Lunch",
            "amount": 250.0,
            "category": "Food",
            "date": "2026-08-18"
        },
        headers=headers1
    )

    assert expense_response.status_code == 201

    expense_id = expense_response.json()["id"]

    # Login as User 2
    login_response = client.post(
        "/login",
        data={
            "username": "expense_patch_other_user",
            "password": "Test@123"
        }
    )

    token2 = login_response.json()["access_token"]

    headers2 = {
        "Authorization": f"Bearer {token2}"
    }

    # User 2 tries to modify User 1's expense
    patch_response = client.patch(
        f"/expenses?expense_id={expense_id}",
        json={
            "amount": 9999.0
        },
        headers=headers2
    )

    assert patch_response.status_code == 404

    data = patch_response.json()

    assert data["detail"] == "Expense not found!"


def test_user_cannot_see_another_users_expenses():

    db = TestingSessionLocal()

    user1 = User(
        username="expense_get_owner",
        password=hash_password("Test@123")
    )

    user2 = User(
        username="expense_get_other_user",
        password=hash_password("Test@123")
    )

    db.add_all([user1, user2])
    db.commit()

    # Login as User 1
    login_response = client.post(
        "/login",
        data={
            "username": "expense_get_owner",
            "password": "Test@123"
        }
    )

    token1 = login_response.json()["access_token"]

    headers1 = {
        "Authorization": f"Bearer {token1}"
    }

    # User 1 creates an expense
    expense_response = client.post(
        "/expenses",
        json={
            "title": "User 1 Lunch",
            "amount": 250.0,
            "category": "Food",
            "date": "2026-08-18"
        },
        headers=headers1
    )

    assert expense_response.status_code == 201

    # Login as User 2
    login_response = client.post(
        "/login",
        data={
            "username": "expense_get_other_user",
            "password": "Test@123"
        }
    )

    token2 = login_response.json()["access_token"]

    headers2 = {
        "Authorization": f"Bearer {token2}"
    }

    # User 2 gets their expenses
    get_response = client.get(
        "/expenses",
        headers=headers2
    )

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["total"] == 0
    assert len(data["items"]) == 0