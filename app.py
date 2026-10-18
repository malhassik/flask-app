from flask import Flask, request, render_template
import json
from datetime import datetime

# Создаем приложение
app = Flask(__name__)


# Декоратор @app.route говорит: "Когда кто-то зайдет на главную страницу (/), выполни эту функцию"
@app.route("/")
def home():
    return render_template("index.html", company_name="Логистрим")


@app.route("/admin")
def admin():
    try:
        with open("orders.json", encoding="utf-8") as file:
            orders = json.load(file)
    except FileNotFoundError:
        orders = []

    return render_template("admin.html", orders=orders)


@app.route("/submit", methods=["POST"])
def submit():
    # 1. Получаем данные из формы
    client_name = request.form.get("client_name")
    from_city = request.form.get("from_city")
    to_city = request.form.get("to_city")

    # 2. Формируем словарь с заявкой
    new_order = {
        "client_name": client_name,
        "from_city": from_city,
        "to_city": to_city,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # 3. Читаем старые заявки из файла (если файла нет — создаем пустой список)
    try:
        with open("orders.json", "r", encoding="utf-8") as file:
            orders = json.load(file)

    except FileNotFoundError:
        orders = []

    # 4. Добавляем новую заявку и сохраняем обратно
    orders.append(new_order)

    with open("orders.json", "w", encoding="utf-8") as file:
        json.dump(orders, file, ensure_ascii=False, indent=2)

    print(f"Заявка сохранена! Всего заявок: {len(orders)}")

    # 5. Возвращаем красивую страницу
    return render_template("success.html", name=client_name)


if __name__ == "__main__":
    app.run(debug=True)
