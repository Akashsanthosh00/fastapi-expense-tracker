from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import List
import datetime


def title_validation(value):
    if not any(char.isalpha() for char in value):
        raise ValueError(
            "title must contain at least one alphabetic character."
        )
    return value


def date_validation(value):
    if value > datetime.date.today():
        raise ValueError("The date cannot be in the future")
    return value


class Category(str, Enum):
    Food = "Food"
    Shopping = "Shopping"
    Entertainment = "Entertainment"
    Travel = "Travel"


class ExpenseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3)
    amount: float | None = Field(default=None, gt=0)
    category: Category | None = None
    date: datetime.date | None = None

    @field_validator("title")
    @classmethod
    def validate_t(cls, value):
        if value is None:
            return value
        return title_validation(value)

    @field_validator("date")
    @classmethod
    def validate_d(cls, value):
        if value is None:
            return value
        return date_validation(value)


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=3)
    amount: float = Field(gt=0)
    category: Category
    date: datetime.date

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        return title_validation(value)

    @field_validator("date")
    @classmethod
    def validate_date(cls, value):
        return date_validation(value)


class Expense(BaseModel):
    id: int
    title: str
    amount: float
    category: Category
    date: datetime.date


class ExpensePagination(BaseModel):
    items: List[Expense]
    page: int
    limit: int
    total: int


class SortField(str, Enum):
    id = "id"
    amount = "amount"
    date = "date"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"