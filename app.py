from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = "544"


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
            created_at TEXT NOT NULL,
            status TEXT DEFAULT 'Новая'
        )
    """)
    conn.commit()
    conn.close()


# Вызываем создание базы при старте программы
init_db()


@app.route("/")
def home():
    return render_template("index.html", company_name="Логистрим")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_password = request.form.get("password")
        real_password = os.getenv("ADMIN_PASSWORD")

        if user_password == real_password:
            # Пароль верный! Записываем в сессию отметку, что мы вошли
            session["is_admin"] = True
            return redirect(url_for("admin"))  # Перекидываем в админку
        else:
            return render_template("login.html", error="Неверный пароль")

    return render_template("login.html")


@app.route("/logout")
def logout():
    # Очищаем сессию (выходим)
    session.pop("is_admin", None)
    return redirect(url_for("home"))


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
    if not session.get("is_admin"):
        return redirect(url_for("login"))
    # Подключаемся к базе и берем все заявки (SELECT)
    conn = get_db_connection()
    orders = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    conn.close()

    return render_template("admin.html", orders=orders)


@app.route("/complete/<int:order_id>")
def complete_order(order_id):
    # Проверка, что мы авторизованы
    if not session.get("is_admin"):
        return redirect(url_for("login"))

    conn = get_db_connection()
    # SQL-запрос UPDATE: меняем статус у конкретной заявки (WHERE id = ?)
    conn.execute("UPDATE orders SET status = 'Выполнена' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin"))  # Возвращаемся обратно в админку


@app.route("/delete/<int:order_id>")
def delete_order_id(order_id):
    if not session.get("is_admin"):
        return redirect(url_for(login))

    conn = get_db_connection()
    conn.execute("DELETE FROM order WHERE id = ?", (order_id))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Render передает порт через переменную окружения PORT
    port = int(os.environ.get("PORT", 5000))
    # host="0.0.0.0" обязателен для работы внутри контейнеров хостинга
    app.run(host="0.0.0.0", port=port)
