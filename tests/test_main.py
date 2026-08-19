from fastapi.testclient import TestClient
from main import app
from conftest import TestingSessionLocal
from user_models import User
from security import hash_password, SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta, timezone
from expense_models import Expense as ExpenseModel
from datetime import datetime, timedelta, timezone, date
from jose import jwt

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

# valid login test
def test_login_success():

    db = TestingSessionLocal()

    user = User(
        username="login_success_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/login",
        data={
            "username": "login_success_user",
            "password": "Test@123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["access_token"] != ""

# wrong password
def test_login_wrong_password():

    db = TestingSessionLocal()

    user = User(
        username="login_wrong_password_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/login",
        data={
            "username": "login_wrong_password_user",
            "password": "Wrong@123"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid username or password"

# non-existant username
def test_login_nonexistent_user():

    response = client.post(
        "/login",
        data={
            "username": "user_does_not_exist",
            "password": "Test@123"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid username or password"

# missing login data
def test_login_missing_password():

    response = client.post(
        "/login",
        data={
            "username": "some_user"
        }
    )

    assert response.status_code == 422

# missing username
def test_login_missing_username():

    response = client.post(
        "/login",
        data={
            "password": "Test@123"
        }
    )

    assert response.status_code == 422

# invalid JWT token
def test_get_expenses_with_invalid_token():

    headers = {
        "Authorization": "Bearer invalid_token"
    }

    response = client.get(
        "/expenses",
        headers=headers
    )

    assert response.status_code == 401

# malformed JWT.
def test_get_expenses_with_malformed_token():

    headers = {
        "Authorization": "Bearer abc.def.ghi"
    }

    response = client.get(
        "/expenses",
        headers=headers
    )

    assert response.status_code == 401

# expired JWT
def test_get_expenses_with_expired_token():

    expired_token = jwt.encode(
        {
            "sub": "1",
            "username": "expired_user",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    headers = {
        "Authorization": f"Bearer {expired_token}"
    }

    response = client.get(
        "/expenses",
        headers=headers
    )

    assert response.status_code == 401


# POST expense with a negative amount
def test_create_expense_negative_amount():

    db = TestingSessionLocal()

    user = User(
        username="negative_amount_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "negative_amount_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": -250.0,
            "category": "Food",
            "date": "2026-08-18"
        },
        headers=headers
    )

    assert response.status_code == 422

# amount = 0
def test_create_expense_zero_amount():

    db = TestingSessionLocal()

    user = User(
        username="zero_amount_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "zero_amount_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 0,
            "category": "Food",
            "date": "2026-08-18"
        },
        headers=headers
    )

    assert response.status_code == 422

# invalid category.
def test_create_expense_invalid_category():

    db = TestingSessionLocal()

    user = User(
        username="invalid_category_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "invalid_category_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250.0,
            "category": "InvalidCategory",
            "date": "2026-08-18"
        },
        headers=headers
    )

    assert response.status_code == 422

# title validation test
def test_create_expense_without_title():

    db = TestingSessionLocal()

    user = User(
        username="missing_title_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "missing_title_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.post(
        "/expenses",
        json={
            "amount": 250.0,
            "category": "Food",
            "date": "2026-08-18"
        },
        headers=headers
    )

    assert response.status_code == 422


#invalid date
def test_create_expense_invalid_date():

    db = TestingSessionLocal()

    user = User(
        username="invalid_date_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "invalid_date_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250.0,
            "category": "Food",
            "date": "invalid-date"
        },
        headers=headers
    )

    assert response.status_code == 422

#Missing required fields
def test_create_expense_missing_required_fields():

    db = TestingSessionLocal()

    user = User(
        username="missing_fields_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "missing_fields_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.post(
        "/expenses",
        json={},
        headers=headers
    )

    assert response.status_code == 422

#Invalid expense_id
def test_update_expense_invalid_expense_id():

    db = TestingSessionLocal()

    user = User(
        username="invalid_expense_id_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "invalid_expense_id_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = client.put(
        "/expenses",
        params={
            "expense_id": "abc"
        },
        json={
            "title": "Updated Lunch",
            "amount": 300.0,
            "category": "Food",
            "date": "2026-08-19"
        },
        headers=headers
    )

    assert response.status_code == 422

#category filtering
def test_get_expenses_category_filter():

    db = TestingSessionLocal()

    user = User(
        username="category_filter_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    expense1 = ExpenseModel(
        title="Lunch",
        amount=250.0,
        category="Food",
        date=date(2026, 8, 18),
        user_id=user.id
    )

    expense2 = ExpenseModel(
        title="Movie",
        amount=500.0,
        category="Entertainment",
        date=date(2026, 8, 18),
        user_id=user.id
    )

    db.add_all([expense1, expense2])
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "category_filter_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/expenses",
        params={"category": "Food"},
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["total"] == 1
    assert len(result["items"]) == 1
    assert result["items"][0]["category"] == "Food"

#Title filtering
def test_get_expenses_title_filter():

    db = TestingSessionLocal()

    user = User(
        username="title_filter_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    expense1 = ExpenseModel(
        title="Lunch",
        amount=250.0,
        category="Food",
        date=date(2026, 8, 18),
        user_id=user.id
    )

    expense2 = ExpenseModel(
        title="Movie",
        amount=500.0,
        category="Entertainment",
        date=date(2026, 8, 18),
        user_id=user.id
    )

    db.add_all([expense1, expense2])
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "title_filter_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/expenses",
        params={"title": "Lunch"},
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["total"] == 1
    assert len(result["items"]) == 1
    assert result["items"][0]["title"] == "Lunch"

#date filtering
def test_get_expenses_date_filter():

    db = TestingSessionLocal()

    user = User(
        username="date_filter_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    expense1 = ExpenseModel(
        title="Lunch",
        amount=250.0,
        category="Food",
        date=date(2026, 8, 18),
        user_id=user.id
    )

    expense2 = ExpenseModel(
        title="Dinner",
        amount=400.0,
        category="Food",
        date=date(2026, 8, 19),
        user_id=user.id
    )

    db.add_all([expense1, expense2])
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "date_filter_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/expenses",
        params={"date": "2026-08-18"},
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["total"] == 1
    assert len(result["items"]) == 1
    assert result["items"][0]["date"] == "2026-08-18"

#Amount filtering
def test_get_expenses_amount_filter():

    db = TestingSessionLocal()

    user = User(
        username="amount_filter_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    expense1 = ExpenseModel(
        title="Lunch",
        amount=250.0,
        category="Food",
        date=date(2026, 8, 18),
        user_id=user.id
    )

    expense2 = ExpenseModel(
        title="Movie",
        amount=500.0,
        category="Entertainment",
        date=date(2026, 8, 18),
        user_id=user.id
    )

    db.add_all([expense1, expense2])
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "amount_filter_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/expenses",
        params={"amount": 500.0},
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["total"] == 1
    assert len(result["items"]) == 1
    assert result["items"][0]["amount"] == 500.0

#Pagination
def test_get_expenses_pagination():

    db = TestingSessionLocal()

    user = User(
        username="pagination_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    expenses = [
        ExpenseModel(
            title=f"Expense {i}",
            amount=100.0 + i,
            category="Food",
            date=date(2026, 8, 18),
            user_id=user.id
        )
        for i in range(1, 6)
    ]

    db.add_all(expenses)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "pagination_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/expenses",
        params={
            "page": 1,
            "limit": 2
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["page"] == 1
    assert result["limit"] == 2
    assert result["total"] == 5
    assert len(result["items"]) == 2

#Multiple expenses
def test_get_multiple_expenses():

    db = TestingSessionLocal()

    user = User(
        username="multiple_expenses_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    expenses = [
        ExpenseModel(
            title="Lunch",
            amount=250.0,
            category="Food",
            date=date(2026, 8, 18),
            user_id=user.id
        ),
        ExpenseModel(
            title="Movie",
            amount=500.0,
            category="Entertainment",
            date=date(2026, 8, 18),
            user_id=user.id
        ),
        ExpenseModel(
            title="Bus",
            amount=50.0,
            category="Travel",
            date=date(2026, 8, 18),
            user_id=user.id
        )
    ]

    db.add_all(expenses)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "multiple_expenses_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/expenses",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["total"] == 3
    assert len(result["items"]) == 3

#User with no expenses
def test_get_expenses_user_with_no_expenses():

    db = TestingSessionLocal()

    user = User(
        username="no_expenses_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "no_expenses_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/expenses",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["total"] == 0
    assert result["items"] == []

#sorting
def test_get_expenses_sorting():

    db = TestingSessionLocal()

    user = User(
        username="sorting_user",
        password=hash_password("Test@123")
    )

    db.add(user)
    db.commit()

    expense1 = ExpenseModel(
        title="Expensive",
        amount=500.0,
        category="Food",
        date=date(2026, 8, 18),
        user_id=user.id
    )

    expense2 = ExpenseModel(
        title="Cheap",
        amount=100.0,
        category="Food",
        date=date(2026, 8, 18),
        user_id=user.id
    )

    expense3 = ExpenseModel(
        title="Medium",
        amount=300.0,
        category="Food",
        date=date(2026, 8, 18),
        user_id=user.id
    )

    db.add_all([expense1, expense2, expense3])
    db.commit()

    login_response = client.post(
        "/login",
        data={
            "username": "sorting_user",
            "password": "Test@123"
        }
    )

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/expenses",
        params={
            "sort_by": "amount",
            "order": "asc"
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["total"] == 3
    assert len(result["items"]) == 3

    assert result["items"][0]["amount"] == 100.0
    assert result["items"][1]["amount"] == 300.0
    assert result["items"][2]["amount"] == 500.0