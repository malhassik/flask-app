from flask import Flask, request, render_template

# Создаем приложение
app = Flask(__name__)


# Декоратор @app.route говорит: "Когда кто-то зайдет на главную страницу (/), выполни эту функцию"
@app.route("/")
def home():
    return render_template("index.html", company_name="Логистрим")


@app.route("/submit", methods=["POST"])
def submit():
    # Получаем данные из формы
    client_name = request.form.get("client_name")
    from_city = request.form.get("from_city")
    to_city = request.form.get("to_city")

    # Выводим в консоль терминала
    print(f"Новая заявка! Клиент: {client_name}. Маршрут: {from_city} -> {to_city}")

    return "<h2>Спасибо! Ваша заявка принята.</h2>"


if __name__ == "__main__":
    app.run(debug=True)
