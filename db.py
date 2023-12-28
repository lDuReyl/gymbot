import sqlite3
from typing import Optional, Tuple

db = sqlite3.connect("./databases/users.sqlite")
cursor = db.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    age INTEGER NOT NULL,
    sex INTEGER,
    weight REAL NOT NULL,
    height REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS nutrients(
    id INTEGER PRIMARY KEY,
    proteins REAL,
    fats REAL,
    carbohydrates INTEGER
)""")

def add_user(id: int, age: int, sex: int, weight: float, height: float) -> bool:
    cursor.execute("SELECT id FROM users WHERE id=?", (id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `users` (`id`, `age`, `sex`, `weight`, `height`) VALUES(?, ?, ?, ?, ?)", (id, age, sex, weight, height))
        db.commit()
        return True
    cursor.execute("UPDATE `users` SET `age`=?, `sex`=?, `weight`=?, `height`=? WHERE `nutrients.id`=?", (age, sex, weight, height, id))
    db.commit()
    return False


def set_nutrients(id: int, proteins: float, fats: float, carbohydrates: float) -> None:
    nutrients = cursor.execute("SELECT `nutrients`.* WHERE `id`=?", (id,)).fetchone()
    if nutrients is None:
        cursor.execute("INSERT INTO `nutrients` (`id`, `proteins`, `fats`, `carbohydrates`)", (id, proteins, fats, carbohydrates))
    else:
        cursor.execute("UPDATE `nutrients` SET `proteins`=?, `fats`=?, `carbohydrates`=? WHERE `id`=?", (proteins, fats, carbohydrates, id))
    db.commit()


def set_field(id: int, field: int|float, value: int) -> bool:
    try:
        cursor.execute("UPDATE `users` SET ?=? WHERE `id`=?", (field, value, id))
    except sqlite3.Error as e:
        print(e)
        return False
    db.commit()
    return True


def get_field(id: int, field: int) -> Optional[int]:
    user = cursor.execute("SELECT ? FROM `users` WHERE `id`=?", (field, id)).fetchone()
    if user is None:
        return None
    return user[0]


def get_nutrients(id: int) -> Tuple[float, float, float]:
    nutrients = cursor.execute("SELECT `proteins`, `fats`, `carbohydrates` FROM `nutrients` WHERE `id`=?", (id,)).fetchone()
    if nutrients is None:
        return (0.0, 0.0, 0.0)
    print(nutrients, "NUTRIENTS\n\n\n\n\n")
    return nutrients


def subtract_nutrients(id: int, proteins: float, fats: float, carbohydrates: float) -> None:
    old_nutrients = tuple(map(float, get_nutrients(id)))
    print(old_nutrients, "OLD NUTRIENTS\n\n\n\n\n")
    new_proteins = old_nutrients[0] - proteins if old_nutrients[0] > proteins else 0 
    new_fats = old_nutrients[1] - fats if old_nutrients[1] > proteins else 0 
    new_carbohydrates = old_nutrients[2] - carbohydrates if old_nutrients[2] > proteins else 0 
    set_nutrients(id, new_proteins, new_fats, new_carbohydrates)

