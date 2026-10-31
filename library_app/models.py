"""Core domain models for the library management system."""
from dataclasses import dataclass
from datetime import date


@dataclass
class Book:
    id: int
    title: str
    author: str
    category: str
    total_copies: int
    available_copies: int


@dataclass
class Member:
    id: int
    name: str
    email: str
    phone: str = ""


@dataclass
class Transaction:
    id: int
    book_id: int
    member_id: int
    issue_date: date
    due_date: date
    return_date: date | None
    fine: float
