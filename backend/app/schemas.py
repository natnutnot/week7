from datetime import datetime

from pydantic import BaseModel, Field


# --- Category Schemas ---
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- Note Schemas ---
class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    category_id: int | None = None


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    category_id: int | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotePatch(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = Field(None, min_length=1)
    category_id: int | None = None


# --- Action Item Schemas (Tetap sama dari Task 1) ---
class ActionItemCreate(BaseModel):
    description: str = Field(..., min_length=3)


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActionItemPatch(BaseModel):
    description: str | None = Field(None, min_length=3)
    completed: bool | None = None
