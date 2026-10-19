from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)


# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect("logistrim.db")
    # Эта магия (row_factory) позволяет обращаться к колонкам базы по имени,
    # как к ключам словаря (например, order['client_name'])
    conn.row_factory = sqlite3.Row
    return conn


# Создаем таблицу при первом запуске (если её еще нет)
def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            from_city TEXT NOT NULL,
            to_city TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Вызываем создание базы при старте программы
init_db()


@app.route("/")
def home():
    return render_template("index.html", company_name="Логистрим")


@app.route("/submit", methods=["POST"])
def submit():
    client_name = request.form.get("client_name")
    from_city = request.form.get("from_city")
    to_city = request.form.get("to_city")
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Подключаемся к базе и сохраняем данные через SQL-запрос INSERT
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO orders (client_name, from_city, to_city, created_at) VALUES (?, ?, ?, ?)",
        (client_name, from_city, to_city, created_at),
    )
    conn.commit()
    conn.close()

    print(f"Заявка от {client_name} сохранена в базу данных!")

    return render_template("success.html", name=client_name)


@app.route("/admin")
def admin():
    # Подключаемся к базе и берем все заявки (SELECT)
    conn = get_db_connection()
    orders = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    conn.close()

    return render_template("admin.html", orders=orders)


if __name__ == "__main__":
    app.run(debug=True)
