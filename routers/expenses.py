from fastapi import APIRouter, HTTPException, Query, Depends
from schemas import ExpenseCreate, Expense, ExpenseUpdate
from database import  get_db
from database_models import Expense as ExpenseModel
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.get("/expenses", response_model=List[Expense])
def get_expenses(
    category: List[str] | None = Query(default=None),
    date : List[str] | None = Query(default=None),
    title : List[str] | None = Query(default=None),
    amount: List[float] | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(ExpenseModel)

    if category:
        query = query.filter(ExpenseModel.category.in_(category))

    if date:
        query = query.filter(ExpenseModel.date.in_(date))

    if title:
        query = query.filter(ExpenseModel.title.in_(title))

    if amount:
        query = query.filter(ExpenseModel.amount.in_(amount))

    result = query.all()

    return result

@router.get("/expenses/{expense_id}", response_model=Expense)
def get_expenses_by_id(expense_id: int, db: Session=Depends(get_db)):
    query = db.query(ExpenseModel)

    result = query.filter(ExpenseModel.id == expense_id).first()
    if result:
        return result

    raise HTTPException(status_code=404, detail="Expense not found")

@router.post("/expenses", response_model=Expense, status_code=201)
def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):

    new_expense = ExpenseModel(
                          title = expense.title,
                          amount = expense.amount,
                          category = expense.category,
                          date = expense.date,
                          password = expense.password
                        )

    db.add(new_expense)

    db.flush()

    approval_code = "EXP" + str(new_expense.id)
    new_expense.approval_code = approval_code

    db.commit()

    return new_expense

@router.delete("/expenses/{expense_id}")
def delete_by_id(expense_id: int, db: Session = Depends(get_db)):
    query = db.query(ExpenseModel)

    result = query.filter(ExpenseModel.id == expense_id).first()

    if result:
        db.delete(result)
        db.commit()
        return {"message": "Expense deleted successfully"}

    raise HTTPException(status_code=404, detail="Expense not found")

@router.put("/expenses/{expense_id}", response_model=Expense)
def update_expense(expense_id: int, 
                   expense: ExpenseCreate, 
                   db: Session = Depends(get_db)
                   ):
    query = db.query(ExpenseModel)

    result = query.filter(ExpenseModel.id == expense_id).first()

    if result:
        updated_data = expense.model_dump()

        for key, value in updated_data.items():
            setattr(result, key, value)

        db.commit()

        return result

    raise HTTPException(status_code=404, detail="Id not found")

@router.patch("/expenses/{expense_id}", response_model=Expense)
def update_partial_expense(expense_id: int, 
                           expense: ExpenseUpdate,
                           db: Session = Depends(get_db)):
    query = db.query(ExpenseModel)
    result = query.filter(ExpenseModel.id == expense_id).first()
    if result:
        updated_data = expense.model_dump(exclude_unset=True)

        for key, value in updated_data.items():
            setattr(result, key, value)

        db.commit()
        return result

    raise HTTPException(status_code=404, detail="Id not found!")