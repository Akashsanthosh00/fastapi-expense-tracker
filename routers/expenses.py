from fastapi import APIRouter, HTTPException, Query, Depends
from schemas import (
    ExpenseCreate, Expense, ExpenseUpdate, ExpensePagination, SortField, SortOrder
    )
from database import get_db
from expense_models import Expense as ExpenseModel
from sqlalchemy.orm import Session
from security import verify_token
from typing import List

router = APIRouter()

# ============================================================
# GET ALL EXPENSES
# Supports:
# 1. Filtering
# 2. Sorting
# 3. Pagination
# ============================================================

@router.get("/expenses", response_model=ExpensePagination)
def get_expenses(
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
    user_id = current_user["sub"]
    
    # Start a query for the Expense table
    query = db.query(ExpenseModel).filter(
        ExpenseModel.user_id == user_id
    )

    # ========================================================
    # 1. FILTERING
    # ========================================================
    if category:
        query = query.filter(ExpenseModel.category.in_(category))

    if date:
        query = query.filter(ExpenseModel.date.in_(date))

    if title:
        query = query.filter(ExpenseModel.title.in_(title))

    if amount:
        query = query.filter(ExpenseModel.amount.in_(amount))

    # ========================================================
    # 2. SORTING
    # ========================================================

    # Convert the user's sort_by choice
    # into the corresponding SQLAlchemy column.
    if sort_by == SortField.id:
        sort_column = ExpenseModel.id
    elif sort_by == SortField.amount:
        sort_column = ExpenseModel.amount
    elif sort_by == SortField.date:
        sort_column = ExpenseModel.date

    if order == SortOrder.asc:
        order_by = sort_column.asc()
    else:
        order_by = sort_column.desc()

    # Apply the sorting instruction to the query
    query = query.order_by(order_by)

    # ========================================================
    # 3. COUNT TOTAL RESULTS
    # ========================================================

    # Count how many expenses match the filters.
    # This is the total number of matching records,
    # not the number returned on the current page.
    total = query.count()

    # ========================================================
    # 4. PAGINATION
    # ========================================================
    offset = (page-1) * limit

    # Skip the required number of records
    # and retrieve only 'limit' records.
    result = query.offset(offset).limit(limit).all()

    # ========================================================
    # 5. RESPONSE
    # ========================================================
    return {
        "items": result,
        "page": page,
        "limit": limit,
        "total": total
    }

# ============================================================
# GET EXPENSE BY ID
# ============================================================
@router.get("/expenses/{expense_id}", response_model=Expense)
def get_expenses_by_id(expense_id: int, db: Session=Depends(get_db)):
    # Create a query for the Expense table
    query = db.query(ExpenseModel)

    result = query.filter(ExpenseModel.id == expense_id).first()
    if result:
        return result

    raise HTTPException(status_code=404, detail="Expense not found")

# ============================================================
# POST / ADD EXPENSE
# ===========================================================
@router.post("/expenses",response_model=Expense,status_code=201)
def add_expense(expense: ExpenseCreate, user_id: int, db: Session = Depends(get_db)):

    # Create a new ExpenseModel object
    # using the data received from the request.
    new_expense = ExpenseModel(
        title=expense.title,
        amount=expense.amount,
        category=expense.category,
        date=expense.date,
        user_id=user_id
    )

    # Add the new expense to the database session
    db.add(new_expense)

    # Permanently save the changes
    db.commit()

    db.refresh(new_expense)

    # Return the newly created expense
    return new_expense

# ============================================================
# DELETE EXPENSE BY ID
# ============================================================
@router.delete("/expenses/{expense_id}")
def delete_by_id(expense_id: int, db: Session = Depends(get_db)):
    # Create a query for the Expense table
    query = db.query(ExpenseModel)

    result = query.filter(ExpenseModel.id == expense_id).first()

    if result:
        db.delete(result)
        db.commit()
        return {"message": "Expense deleted successfully"}

    raise HTTPException(status_code=404, detail="Expense not found")


# ============================================================
# PUT / COMPLETE UPDATE
# ============================================================
@router.put("/expenses/{expense_id}", response_model=Expense)
def update_expense(expense_id: int, 
                   expense: ExpenseCreate, 
                   db: Session = Depends(get_db)
                   ):
    # Create a query for the Expense table
    query = db.query(ExpenseModel)

    result = query.filter(ExpenseModel.id == expense_id).first()

    if result:
        # Convert the Pydantic model into a dictionary
        updated_data = expense.model_dump()

        # Update every field received
        for key, value in updated_data.items():
            setattr(result, key, value)

        db.commit()

        return result

    raise HTTPException(status_code=404, detail="Id not found")

# ============================================================
# PATCH / PARTIAL UPDATE
# ============================================================
@router.patch("/expenses/{expense_id}", response_model=Expense)
def update_partial_expense(expense_id: int, 
                           expense: ExpenseUpdate,
                           db: Session = Depends(get_db)):
    
    # Create a query for the Expense table
    query = db.query(ExpenseModel)

    result = query.filter(ExpenseModel.id == expense_id).first()

    if result:
        # Convert only the fields actually provided
        # by the user into a dictionary.
        updated_data = expense.model_dump(exclude_unset=True)

        for key, value in updated_data.items():
            setattr(result, key, value)

        db.commit()
        return result

    raise HTTPException(status_code=404, detail="Id not found!")