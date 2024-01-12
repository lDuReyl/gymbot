import sqlite3
from typing import Any, Tuple

db = sqlite3.connect("./databases/db.sqlite", check_same_thread=False)
cursor = db.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    sex INTEGER NOT NULL,
    weight REAL NOT NULL,
    goal INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS nutrients(
    id INTEGER PRIMARY KEY,
    proteins REAL,
    fats REAL,
    carbohydrates REAL
)""")


def add_user(id: int, sex: int, weight: float, goal: int) -> bool:
    cursor.execute("SELECT `id` FROM `users` WHERE `id`=?", (id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `users` (`id`, `sex`, `weight`, `goal`) VALUES(?, ?, ?, ?)", (id, sex, weight, goal))
        cursor.execute("INSERT INTO `nutrients` (`id`) VALUES(?)", (id,))
        db.commit()
        return True
    cursor.execute("UPDATE `users` SET `sex`=?, `goal`=?, `weight`=? WHERE `id`=?", (sex, goal, weight, id))
    db.commit()
    return False


def get_user(id: int) -> Tuple[int, float, int]: 
    """Returns tuple: [sex, weight, goal]"""
    return cursor.execute("SELECT `sex`, `weight`, `goal` FROM `users` WHERE `id`=?", (id,)).fetchone()


def set_nutrients(id: int, proteins: float, fats: float, carbohydrates: float) -> None:
    """Set user pfh"""
    nutrients = cursor.execute("SELECT * FROM `nutrients` WHERE `id`=?", (id,)).fetchone()
    if nutrients is None:
        cursor.execute("INSERT INTO `nutrients` (`id`, `proteins`, `fats`, `carbohydrates`)", (id, proteins, fats, carbohydrates))
    else:
        cursor.execute("UPDATE `nutrients` SET `proteins`=?, `fats`=?, `carbohydrates`=? WHERE `id`=?", (proteins, fats, carbohydrates, id))
    db.commit()
 

def get_nutrients(id: int) -> Tuple[float, float, float]:
    nutrients = tuple(map(float, cursor.execute("SELECT `proteins`, `fats`, `carbohydrates` FROM `nutrients` WHERE `id`=?", (id,)).fetchone()))
    return nutrients 


def subtract_nutrients(id: int, proteins: float, fats: float, carbohydrates: float) -> None:
    old_nutrients = get_nutrients(id)
    new_proteins = round(old_nutrients[0] - proteins if old_nutrients[0] > proteins else 0, 2)
    new_fats = round(old_nutrients[1] - fats if old_nutrients[1] > fats else 0, 2)
    new_carbohydrates = round(old_nutrients[2] - carbohydrates if old_nutrients[2] > carbohydrates else 0, 2)
    set_nutrients(id, new_proteins, new_fats, new_carbohydrates)


def set_nutrients_by_user_id(id: int) -> None:
    user_data = get_user(id)
    sex = user_data[0]
    weight = user_data[1]
    if sex == 1:
        proteins = 3 * weight
        fats =  1.7 * weight
        carbohydrates =  4 * weight
    else:
        proteins = 2.3 * weight
        fats =  1.4 * weight
        carbohydrates = 3 * weight
    set_nutrients(id, proteins, fats, carbohydrates)


def set_user_field(id: int, field: str, value: Any) -> bool:
    try:
        cursor.execute(f"UPDATE `users` SET {field}=? WHERE `id`=?", (value, id))
    except sqlite3.Error as e:
        print(f"sqlite error in set_user_field", e)
        return False
    db.commit()
    return True


def get_users_id() -> list[Tuple[tuple, ...]]:
    return cursor.execute("SELECT `id` FROM `users`").fetchall()


