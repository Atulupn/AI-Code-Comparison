<!DOCTYPE html>
<html>
<head>
    <title>Анимация снегопада</title>
    <style>
        canvas {
            border: 1px solid black;
            background-color: #333;
        }
    </style>
</head>
<body>
    <canvas id="snowCanvas" width="400" height="300"></canvas>
    <div>
        <button id="stopBtn">Остановить анимацию</button>
        <button id="speedBtn">Увеличить скорость</button>
    </div>

    <script>
        // Глобальные переменные для управления анимацией
        let animationId = null;
        let isAnimating = false;

        function startSnowfall() {
            const canvas = document.getElementById("snowCanvas");
            
            // Проверка наличия canvas
            if (!canvas || !canvas.getContext) {
                console.error("Canvas не поддерживается или не найден");
                return;
            }
            
            const context = canvas.getContext("2d");
            const snowflakes = [];
            
            // Инициализация снежинок
            for (let i = 0; i < 50; i++) {
                snowflakes.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height * -1, // Начинаем выше canvas
                    speed: 1 + Math.random() * 2,
                    radius: 2 + Math.random() * 3
                });
            }
            
            // Остановка предыдущей анимации, если была
            if (animationId) {
                cancelAnimationFrame(animationId);
            }
            
            isAnimating = true;
            
            function animate() {
                // Очищаем canvas
                context.clearRect(0, 0, canvas.width, canvas.height);
                
                // Рисуем снежинки
                context.fillStyle = "white";
                for (const flake of snowflakes) {
                    context.beginPath();
                    context.arc(flake.x, flake.y, flake.radius, 0, Math.PI * 2);
                    context.fill();
                    
                    // Обновляем позицию
                    flake.y += flake.speed;
                    
                    // Если снежинка вышла за нижнюю границу
                    if (flake.y > canvas.height + flake.radius) {
                        flake.y = -flake.radius; // Возвращаем вверх
                        flake.x = Math.random() * canvas.width; // Новая случайная позиция по X
                    }
                }
                
                // Продолжаем анимацию, если не остановлена
                if (isAnimating) {
                    animationId = requestAnimationFrame(animate);
                }
            }
            
            // Запускаем анимацию
            animate();
        }
        
        // Обработчики кнопок
        document.getElementById('stopBtn').addEventListener('click', function() {
            isAnimating = !isAnimating;
            this.textContent = isAnimating ? 'Остановить анимацию' : 'Продолжить анимацию';
            
            if (isAnimating) {
                startSnowfall();
            }
        });
        
        document.getElementById('speedBtn').addEventListener('click', function() {
            const canvas = document.getElementById("snowCanvas");
            const context = canvas.getContext("2d");
            const snowflakes = [];
            
            // Увеличиваем скорость всех снежинок
            for (const flake of snowflakes) {
                flake.speed += 0.5;
            }
        });
        
        // Запускаем анимацию при загрузке страницы
        window.addEventListener('load', startSnowfall);
    </script>
</body>
</html>