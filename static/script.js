// Находим форму и блок для сообщений
const form = document.getElementById("order-form");
const messageBox = document.getElementById("message-box");

// Ловим событие "submit" (отправка формы)
form.addEventListener("submit", async function (event) {
    // 1. Отменяем стандартное поведение браузера (перезагрузку страницы)
    event.preventDefault();

    // 2. Собираем данные из формы
    const formData = new FormData(form);

    try {
        // 3. Отправляем данные на сервер через fetch (это как requests в Python)
        const response = await fetch("/submit", {
            method: "POST",
            body: formData
        });

        // 4. Ждем ответ от сервера в формате JSON
        const data = await response.json();

        // 5. Показываем сообщение пользователю
        if (data.status === "success") {
            messageBox.innerText = data.message;
            messageBox.style.color = "#2ecc71"; // Зеленый
            form.reset(); // Очищаем форму
        }

    } catch (error) {
        messageBox.innerText = "Ошибка сети. Попробуйте позже.";
        messageBox.style.color = "#ff4444"; // Красный
    }
});