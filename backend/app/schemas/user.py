from pydantic import BaseModel, Field, field_validator, EmailStr

def password_validation(value):
    if not any(char.isupper() for char in value):
        raise ValueError("Password must contain at least one uppercase letter.")

    if not any(char.islower() for char in value):
        raise ValueError("Password must contain at least one lowercase letter.")

    if not any(char.isdigit() for char in value):
        raise ValueError("Password must contain at least one digit.")

    if any(char.isspace() for char in value):
        raise ValueError("Password must not contain spaces.")

    if not any(not char.isalnum() for char in value):
        raise ValueError("Password must contain at least one special character")

    return value


class UserCreate(BaseModel):
    username: str = Field(
        min_length=5,
        max_length=20,
        pattern=r"^[a-zA-Z0-9_]+$"
    )
    email: EmailStr = Field(max_length=254)
    password: str = Field(min_length=8, max_length=64)

    @field_validator("password")
    @classmethod
    def password_validate(cls, password):
        return password_validation(password)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str