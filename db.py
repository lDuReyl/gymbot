import sqlite3
from typing import Any, Tuple

db = sqlite3.connect("./databases/db.sqlite")
cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS nutrients")
cursor.executescript("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    age INTEGER NOT NULL,
    sex INTEGER,
    weight REAL NOT NULL,
    height REAL NOT NULL,
    activity REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS nutrients(
    id INTEGER PRIMARY KEY,
    proteins REAL,
    fats REAL,
    carbohydrates REAL,
    daily_calories REAL
)""")

def add_user(id: int, age: int, sex: int, weight: float, height: float, activity: float=1.375) -> bool:
    cursor.execute("SELECT id FROM users WHERE id=?", (id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `users` (`id`, `age`, `sex`, `weight`, `height`, `activity`) VALUES(?, ?, ?, ?, ?, ?)", (id, age, sex, weight, height, activity))
        db.commit()
        return True
    cursor.execute("UPDATE `users` SET `age`=?, `sex`=?, `weight`=?, `height`=? WHERE `id`=?", (age, sex, weight, height, id))
    db.commit()
    return False


def get_user(id: int) -> Tuple[int, int, float, float, float]:
    return cursor.execute("SELECT `age`, `sex`, `weight`, `height`, `activity` FROM `users` WHERE `id`=?", (id,)).fetchone()


def set_nutrients(id: int, proteins: float, fats: float, carbohydrates: float) -> None:
    nutrients = cursor.execute("SELECT * FROM `nutrients` WHERE `id`=?", (id,)).fetchone()
    if nutrients is None:
        cursor.execute("INSERT INTO `nutrients` (`id`, `proteins`, `fats`, `carbohydrates`)", (id, proteins, fats, carbohydrates))
    else:
        cursor.execute("UPDATE `nutrients` SET `proteins`=?, `fats`=?, `carbohydrates`=? WHERE `id`=?", (proteins, fats, carbohydrates, id))
    db.commit()


    #def set_nutrients_by_norm(id: int):
    #proteins = 
    #fats = 
    #carbohydrates = 
    #cursor.execute("UPDATE `nutrients` SET `proteins`=?, `fats`=?, `carbohydrates`=? ", (proteins, fats, carbohydrates))

def set_field(id: int, field: str, value: Any) -> bool:
    try:
        cursor.execute("UPDATE `users` SET ?=? WHERE `id`=?", (field, value, id))
    except sqlite3.Error as e:
        print(e)
        return False
    db.commit()
    return True


def get_field(id: int, field: str) -> int:
    user = cursor.execute("SELECT ? FROM `users` WHERE `id`=?", (field, id)).fetchone()
    if user is None:
        return 0
    return user[0]


def get_users_id() -> list[int]:
    return cursor.execute("SELECT `id` FROM `users`").fetchall()


def set_daily_calories(id: int) -> None:
    age, sex, weight, height, activity = get_user(id)
    daily_calories: float
    if sex:
        daily_calories = (10 * weight + 6.25 * height - 5 * age + 5) * activity
    else:
        daily_calories = (10 * weight + 6.25 * height - 5 * age - 161) * activity
    set_field(id, "dayly_calories", daily_calories)



def get_nutrients(id: int) -> Tuple[float, float, float]:
    nutrients = cursor.execute("SELECT `proteins`, `fats`, `carbohydrates` FROM `nutrients` WHERE `id`=?", (id,)).fetchone()
    return nutrients


def subtract_nutrients(id: int, proteins: float, fats: float, carbohydrates: float) -> None:
    old_nutrients = tuple(map(float, get_nutrients(id)))
    new_proteins = old_nutrients[0] - proteins if old_nutrients[0] > proteins else 0 
    new_fats = old_nutrients[1] - fats if old_nutrients[1] > proteins else 0 
    new_carbohydrates = old_nutrients[2] - carbohydrates if old_nutrients[2] > proteins else 0 
    set_nutrients(id, new_proteins, new_fats, new_carbohydrates)

