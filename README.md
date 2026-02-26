[index.html](https://github.com/user-attachments/files/25584418/index.html)
<!DOCTYPE html>
<html>
<head>
    <title>Моя первая страница</title>

    <style>
        body {
            margin: 0;
            background: linear-gradient(135deg, #667eea, #764ba2);
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .card {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
            width: 400px;
        }

        h1 {
            margin-bottom: 10px;
        }

        p {
            color: gray;
        }

        button {
            margin-top: 20px;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            background: #667eea;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover {
            background: #5a67d8;
        }
        input {
    width: 80%;
    padding: 10px;
    margin-top: 15px;
    border-radius: 8px;
    border: 1px solid #ccc;
    font-size: 16px;
}
    </style>
</head>

<body>

    <div class="card">
        <img src="https://picsum.photos/200" alt="Картинка">
        <h1>Привет, мир! 🚀</h1>
        <p>Это уже красивая версия моей первой страницы</p>
        <input type="text" id="nameInput" placeholder="Введи своё имя">
        <button onclick="showMessage()">Нажми меня</button>
    </div>

<script>
    function sayHello() {
        // Берем значение из поля именно в момент нажатия кнопки
        const nameInput = document.getElementById('nameInput'); 
        const name = nameInput.value.trim(); // trim() убирает лишние пробелы

        if (name === "") {
            alert("Пожалуйста, введи свое имя! 😊");
        } else {
            alert("Привет, " + name + "! Ты самая лучшая! 🚀❤️");
        }
    }
</script>

</body>
</html>
