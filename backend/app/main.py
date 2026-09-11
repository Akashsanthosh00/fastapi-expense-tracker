from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from backend.app.core.exceptions import ExpenseNotFoundException
from backend.app.routers.expenses import router as expenses_router
from backend.app.core.logging_config import setup_logging
from backend.app.routers.users import router as users_router
import logging

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Expense tracker API",
    description="A REST API for managing personal expenses",
    version="1.0.0"
)

app.include_router(expenses_router)
app.include_router(users_router)

@app.exception_handler(ExpenseNotFoundException)
def expense_not_found_handler(
    request: Request,
    exc: ExpenseNotFoundException
):

    #Log unexpected application errors
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=404,
        content={"detail": "Expense not found"}
    )

@app.exception_handler(Exception)
def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )