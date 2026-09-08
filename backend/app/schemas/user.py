from pydantic import BaseModel, Field, field_validator

def password_validation(value):
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


class UserCreate(BaseModel):
    username: str = Field(min_length=5)
    password: str = Field(min_length=6, max_length=16)

    @field_validator("password")
    @classmethod
    def password_validate(cls, password):
        return password_validation(password)


class UserLogin(BaseModel):
    username: str
    password: str