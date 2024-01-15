#!/usr/bin/python3
"""usr module."""
from models.base_model import BaseModel


class User(BaseModel):
    """user class definition."""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
