import sqlite3
from typing import Optional

db = sqlite3.connect("./databases/users.sqlite")
cursor = db.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    age INTEGER NOT NULL,
    weight REAL NOT NULL,
    height REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS nutrients(
    id INTEGER PRIMARY KEY,
    proteins REAL,
    fats REAL,
    carbohydrates INTEGER
)""")

def add_user(id, age, weight, height) -> bool:
    cursor.execute("SELECT id FROM users WHERE id=?", (id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (id, age, weight, height) VALUES(?, ?, ?, ?)", (id, age, weight, height))
        db.commit()
        return True
    return False


def set_nutrients(id: float, proteins: float, fats: float, carbohydrates: float) -> bool:
    nutrients = cursor.execute("SELECT nutrients.* WHERE `id`=?", (id,)).fetchone()
    try:
        if nutrients is None:
            cursor.execute("INSERT INTO nutrients (id, proteins, fats, carbohydrates)", (id, proteins, fats, carbohydrates))
        else:
            cursor.execute("UPDATE nutrients SET (proteins, fats, carbohydrates), VALUES(?, ?, ?) WHERE id=?", (proteins, fats, carbohydrates, id))
    except sqlite3.Error as e:
        print(e)
        return False
    db.commit()
    return True


def set_field(id: int, field: int, value: int) -> bool:
    try:
        cursor.execute("UPDATE users SET ?=? WHERE id=?", (field, value, id))
    except sqlite3.Error as e:
        print(e)
        return False
    db.commit()
    return True


def get_field(field: int) -> Optional[int]:
    user = cursor.execute("SELECT age FROM users WHERE id=?", (field,)).fetchone()
    if user is None:
        return None
    return user[0]

