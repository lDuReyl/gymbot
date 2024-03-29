import sqlite3
from typing import Any, Tuple

db = sqlite3.connect("./databases/db.sqlite", check_same_thread=False)
cursor = db.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    age INTEGER NOT NULL,
    sex INTEGER NOT NULL,
    weight REAL NOT NULL,
    height REAL NOT NULL,
    goal INTEGER NOT NULL,
    activity REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS nutrients(
    id INTEGER PRIMARY KEY,
    proteins REAL,
    fats REAL,
    carbohydrates REAL,
    daily_calories REAL
)""")


def add_user(id: int, age: int, sex: int, weight: float, height: float, goal: int, activity: float) -> bool:
    cursor.execute("SELECT `id` FROM `users` WHERE `id`=?", (id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `users` (`id`, `age`, `sex`, `weight`, `height`, `goal`, `activity`) VALUES(?, ?, ?, ?, ?, ?,?)", (id, age, sex, weight, height, goal, activity))
        cursor.execute("INSERT INTO `nutrients` (`id`) VALUES(?)", (id,))
        db.commit()
        return True
    cursor.execute("UPDATE `users` SET `age`=?, `sex`=?, `weight`=?, `height`=?, `goal`=?, `activity`=? WHERE `id`=?", (age, sex, weight, height, goal, activity, id))
    db.commit()
    return False


def get_user(id: int) -> Tuple[int, int, float, float, int, float]:
    return cursor.execute("SELECT `age`, `sex`, `weight`, `height`, `goal`, `activity` FROM `users` WHERE `id`=?", (id,)).fetchone()


def set_nutrients(id: int, proteins: float, fats: float, carbohydrates: float) -> None:
    nutrients = cursor.execute("SELECT * FROM `nutrients` WHERE `id`=?", (id,)).fetchone()
    if nutrients is None:
        cursor.execute("INSERT INTO `nutrients` (`id`, `proteins`, `fats`, `carbohydrates`)", (id, proteins, fats, carbohydrates))
    else:
        cursor.execute("UPDATE `nutrients` SET `proteins`=?, `fats`=?, `carbohydrates`=? WHERE `id`=?", (proteins, fats, carbohydrates, id))
    db.commit()


def get_nutrients_coefficients(id: int) -> Tuple[float, float, float]:
    goal = cursor.execute("SELECT `goal` FROM `users` WHERE `id`=?", (id,)).fetchone()  # 1 - Поддерживать вес, 2 - худеть, 3 - набирать массу
    if goal == 1: return (0.3, 0.2, 0.5) # БЖУ
    if goal == 2: return (0.3, 0.3, 0.4)
    return (0.5, 0.2, 0.3)


def set_nutrients_by_norm(id: int):
    calories: float = cursor.execute("SELECT `daily_calories` FROM `nutrients` WHERE `id`=?", (id,)).fetchone()[0]
    proteins_coeff, fats_coeff, carbohydrates_coeff = get_nutrients_coefficients(id)
    proteins = round((calories * proteins_coeff) / 4, 2)
    fats = round((calories * fats_coeff) / 9, 2)
    carbohydrates = round((calories * carbohydrates_coeff) / 4, 2)
    set_nutrients(id, proteins, fats, carbohydrates)


def set_user_field(id: int, field: str, value: Any) -> bool:
    try:
        cursor.execute(f"UPDATE `users` SET {field}=? WHERE `id`=?", (value, id))
    except sqlite3.Error as e:
        print(f"sqlite error in set_user_field while processing\n UPDATE `users` SET {field}={value} WHERE id={id}:", e)
        return False
    db.commit()
    return True


def get_user_field(id: int, field: str) -> int:
    user = cursor.execute("SELECT ? FROM `users` WHERE `id`=?", (field, id)).fetchone()
    if user is None:
        return 0
    return user[0]


def get_users_id() -> list[int]:
    return cursor.execute("SELECT `id` FROM `users`").fetchall()


def set_daily_calories(id: int) -> None:
    user = get_user(id)
    age, sex, weight, height, activity = user[0], user[1], user[2], user[3], user[5]
    daily_calories: float
    if sex:
        daily_calories = (10 * weight + 6.25 * height - 5 * age + 5) * activity
    else:
        daily_calories = (10 * weight + 6.25 * height - 5 * age - 161) * activity
    daily_calories = round(daily_calories, 2)
    cursor.execute("UPDATE `nutrients` SET `daily_calories`=? WHERE `id`=?", (daily_calories, id))



def get_nutrients(id: int) -> Tuple[float, float, float]:
    nutrients = tuple(map(float, cursor.execute("SELECT `proteins`, `fats`, `carbohydrates` FROM `nutrients` WHERE `id`=?", (id,)).fetchone()))
    return nutrients


def subtract_nutrients(id: int, proteins: float, fats: float, carbohydrates: float) -> None:
    old_nutrients = get_nutrients(id)
    new_proteins = round(old_nutrients[0] - proteins if old_nutrients[0] > proteins else 0, 2)
    new_fats = round(old_nutrients[1] - fats if old_nutrients[1] > fats else 0, 2)
    new_carbohydrates = round(old_nutrients[2] - carbohydrates if old_nutrients[2] > carbohydrates else 0, 2)
    set_nutrients(id, new_proteins, new_fats, new_carbohydrates)


def set_cpfh(id : int):
    set_daily_calories(id)
    set_nutrients_by_norm(id)
