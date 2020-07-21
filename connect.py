import sqlite3
from flask import g

DATABASE = r"C:\Users\Asus\Desktop\DatabaseSystems\usda-sqlite-master\usda-sqlite-master\usda.sql3"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()