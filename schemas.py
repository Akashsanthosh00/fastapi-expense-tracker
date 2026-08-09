from pydantic import BaseModel, Field, field_validator
from enum import Enum
import datetime

## The given are the validation functions to validate the input value

def password_validation(value): # to validate the password
    if not any(char.isupper() for char in value):
        raise ValueError("Password must contain at least one uppercase letter.")

    if not any(char.islower() for char in value):
        raise ValueError("Password must contain at least one lowercase letter.")

    if not any(char.isdigit() for char in value):
        raise ValueError("Password must contain at least one digit.")

    SPECIALS = "!@#$%^&*"

    if not any(char in SPECIALS for char in value):
        raise ValueError("Password must contain at least one special character")
    
    return value

def title_validation(value): # to validate the title
    if not any(char.isalpha() for char in value):
        raise ValueError(
            "title must contain at least one alphabetic character."
        )
    return value

def date_validation(value): # to validate the date
    if value > datetime.date.today():
        raise ValueError("The date cannot be in the future")
    return value

class Category(str, Enum):
    Food = "Food"
    Shopping = "Shopping"
    Entertainment = "Entertainment"
    Travel = "Travel"

 # this class is mainly for the patch endpoint, which means if the client
 # wants to update only some fields rather than every field
class ExpenseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3)
    amount: float | None = Field(default=None, gt=0)
    category: Category | None = None
    date: datetime.date | None = None
    password: str | None = Field(default= None, min_length=4, max_length=12)

    @field_validator("password")
    @classmethod
    def validate_p(cls, value):
        if value is None:
            return value
        return password_validation(value)

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

# this class is for validating the new data, especially used in post and
# put endpoint, whenever the client wants to update/create a new data
class ExpenseCreate(BaseModel):
    title: str = Field(min_length=3)
    amount: float = Field(gt=0)
    category: Category
    date: datetime.date
    password: str = Field(min_length=4, max_length=12)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        return password_validation(value)

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

class ExpenseDB(Expense):
    approval_code: str
    password: str