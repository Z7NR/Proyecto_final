import sys
import os
import sqlite3

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from data_base import DBAdvanceManager
from functions.CRUD import CRUD_function

if __name__ == "__main__":
    db = DBAdvanceManager()
    db.create_user_tables()
    crud = CRUD_function()
    crud.create_user("Ermenejildo", "Perez", 24, "04244560182", "ermejol@email.com", "ermejol666", "Caracas", "Venezuela")
    crud.delete_user("4")
    print(crud.read_user())