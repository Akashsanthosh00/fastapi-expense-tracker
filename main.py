from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from database import engine, Base
from routers.expenses import router as expenses_router

app = FastAPI(
    title="Expense tracker API",
    description="A REST API for managing personal expenses",
    version = "1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(expenses_router)

@app.exception_handler(Exception)
def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500,
                        content={"detail": "Internal server error"})