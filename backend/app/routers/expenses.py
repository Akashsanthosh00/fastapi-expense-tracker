from fastapi import APIRouter, Query, Depends
from backend.app.schemas.expense import (
    ExpenseCreate,
    Expense,
    ExpenseUpdate,
    ExpensePagination,
    SortField,
    SortOrder
)
from backend.app.services.expense_service import (
    get_expenses,
    create_expense, 
    delete_expense, 
    update_expense, 
    update_partial_expense)
from backend.app.database.database import get_db
from backend.app.core.security import verify_token
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

# ============================================================
# GET ALL EXPENSES
# Supports:
# 1. Filtering
# 2. Sorting
# 3. Pagination
# ============================= ===============================

@router.get("/expenses", response_model=ExpensePagination)
def get_expenses_endpoint(
    #JWT verification
    current_user = Depends(verify_token),

    # -------------------------
    # Filtering parameters
    # -------------------------
    category: List[str] | None = Query(default=None),
    date : List[str] | None = Query(default=None),
    title : List[str] | None = Query(default=None),
    amount: List[float] | None = Query(default=None),

    # -------------------------
    # Pagination parameters
    # -------------------------
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10 ,ge=1),

    # -------------------------
    # Sorting parameters
    # -------------------------
    # If the user doesn't provide sort_by,
    # expenses will be sorted by ID.
    sort_by: SortField = SortField.id,

    # If the user doesn't provide order,
    # ascending order will be used.
    order: SortOrder = SortOrder.asc,

    # Database session
    db: Session = Depends(get_db)
):
    

    user_id = int(current_user["sub"])
    
    return get_expenses(
        db = db,
        user_id = user_id,
        category = category,
        date = date,
        title = title,
        amount = amount,
        page = page,
        limit = limit,
        sort_by = sort_by,
        order = order
    )

# ============================================================
# POST / ADD EXPENSE
# ===========================================================
@router.post("/expenses", response_model=Expense, status_code=201)
def add_expense(
    expense: ExpenseCreate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    # Get the logged-in user's ID from the JWT payload.
    # This ensures the expense is associated with the correct user.
    user_id = int(current_user["sub"])

    # The router handles HTTP-related responsibilities such as:
    # - receiving the request
    # - validating input through Pydantic
    # - getting the authenticated user
    # - getting the database session
    #
    # The actual expense creation logic is handled by the service layer.
    return create_expense(
        db=db,
        expense=expense,
        user_id=user_id
    )

# ============================================================
# DELETE EXPENSE BY ID
# ============================================================
@router.delete("/expenses")
def delete_by_id(expense_id: int,
                 current_user: dict = Depends(verify_token),
                 db: Session = Depends(get_db)):
    
    # Get the logged-in user's ID from the JWT payload.
    user_id = int(current_user["sub"])

    return delete_expense(
        db = db,
        expense_id = expense_id,
        user_id = user_id
    )


# ============================================================
# PUT / COMPLETE UPDATE
# ============================================================
@router.put("/expenses", response_model=Expense)
def update_expense_endpoint(expense_id: int, 
                   expense: ExpenseCreate,
                   current_user: dict = Depends(verify_token),
                   db: Session = Depends(get_db)
                   ):
    
    # Get the logged-in user's ID from the JWT payload.
    user_id = int(current_user["sub"])

    return update_expense(
        db = db,
        expense_id = expense_id,
        user_id = user_id,
        expense = expense
    )
    

# ============================================================
# PATCH / PARTIAL UPDATE
# ============================================================
@router.patch("/expenses", response_model=Expense)
def update_partial_expense_endpoint(expense_id: int, 
                           expense: ExpenseUpdate,
                           current_user: dict = Depends(verify_token),
                           db: Session = Depends(get_db)):

    # Get the userid
    user_id = int(current_user["sub"])

    return update_partial_expense(
        db = db,
        expense_id = expense_id,
        expense = expense,
        user_id = user_id
    )