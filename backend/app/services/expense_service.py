from sqlalchemy.orm import Session
from backend.app.database.models.expense import Expense as ExpenseModel
from backend.app.core.exceptions import ExpenseNotFoundException
from backend.app.schemas.expense import ExpenseCreate, ExpenseUpdate, SortField, SortOrder
from typing import List
import time


def get_expenses(
        db: Session,
        user_id: int,
        category: List[str] | None,
        date: List[str] | None,
        title: List[str] | None,
        amount: List[float] | None,
        page: int,
        limit: int,
        sort_by: SortField,
        order: SortOrder
):
    start = time.perf_counter()

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

    # ========================================================
    # 3. COUNT TOTAL RESULTS
    # ========================================================

    # Count how many expenses match the filters.
    # This is the total number of matching records,
    # not the number returned on the current page.
    total = query.count()

    # Apply the sorting instruction to the query
    query = query.order_by(order_by)

    # ========================================================
    # 4. PAGINATION
    # ========================================================
    offset = (page-1) * limit

    # Skip the required number of records
    # and retrieve only 'limit' records.
    result = query.offset(offset).limit(limit).all()

    db_time = (time.perf_counter() - start) * 1000
    print(f"DB operation time: {db_time:.2f} ms")

    # ========================================================
    # 5. RESPONSE
    # ========================================================
    return {
        "items": result,
        "page": page,
        "limit": limit,
        "total": total
    }


def create_expense(
    db: Session,
    expense: ExpenseCreate,
    user_id: int
):
    # Create a new ExpenseModel object using the
    # validated expense data received from the router.
    # The user_id links the expense to the logged-in user.
    new_expense = ExpenseModel(
        title=expense.title,
        amount=expense.amount,
        category=expense.category,
        date=expense.date,
        user_id=user_id
    )

    # Add the new expense to the current database session.
    db.add(new_expense)

    # Commit the transaction so the expense is permanently
    # saved in the PostgreSQL database.
    db.commit()

    # Refresh the object so SQLAlchemy loads the latest
    # database-generated values, such as the generated ID.
    db.refresh(new_expense)

    # Return the newly created expense to the router.
    return new_expense


def delete_expense(
        db: Session, 
        expense_id: int,
        user_id: int
):
    result = db.query(ExpenseModel).filter(
        ExpenseModel.user_id == user_id,
        ExpenseModel.id == expense_id
    ).first()

    if result:
        db.delete(result)
        db.commit()
        return {"message": "Expense deleted successfully"}

    raise ExpenseNotFoundException()


def update_expense(
        db: Session,
        expense_id: int,
        user_id: int,
        expense: ExpenseCreate
):
    # Find the expense with the given ID that belongs to the logged-in user
    result = db.query(ExpenseModel).filter(
        ExpenseModel.user_id == user_id,
        ExpenseModel.id == expense_id
    ).first()

    if result:

        # Convert the Pydantic model into a dictionary
        updated_data = expense.model_dump()

        # Update every field received
        for key, value in updated_data.items():
            setattr(result, key, value)

        db.commit()

        return result

    raise ExpenseNotFoundException()


def update_partial_expense(
        db: Session,
        expense_id: int,
        expense: ExpenseUpdate,
        user_id: int
):
        
    # Find the specific expense with the given ID that belongs to the logged-in user
    result = db.query(ExpenseModel).filter(
        ExpenseModel.user_id == user_id,
        ExpenseModel.id == expense_id
        ).first()

    if result:
        # Convert only the fields actually provided
        # by the user into a dictionary.
        updated_data = expense.model_dump(exclude_unset=True)

        for key, value in updated_data.items():
            setattr(result, key, value)

        db.commit()
        return result
    
    raise ExpenseNotFoundException()