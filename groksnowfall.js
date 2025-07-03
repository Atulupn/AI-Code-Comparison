// Глобальная переменная для хранения идентификатора анимации
let animationId = null;

// Функция для запуска анимации падающих снежинок
function startSnowfall() {
  // Получение canvas и контекста
  const canvas = document.getElementById("snowCanvas");
  if (!canvas || !canvas.getContext) {
    console.error("Canvas с ID 'snowCanvas' не найден или не поддерживается.");
    return;
  }
  const ctx = canvas.getContext("2d");

  // Получение размеров canvas из его атрибутов
  const canvasWidth = canvas.width;
  const canvasHeight = canvas.height;

  // Массив для хранения объектов снежинок
  const snowflakes = [];
  const numSnowflakes = 10;

  // Инициализация снежинок с случайными координатами и скоростью
  for (let i = 0; i < numSnowflakes; i++) {
    snowflakes.push({
      x: Math.random() * canvasWidth, // Случайная X-координата
      y: Math.random() * canvasHeight, // Случайная начальная Y-координата
      speed: Math.random() * 2 + 1, // Скорость от 1 до 3
      radius: Math.random() * 3 + 2, // Радиус от 2 до 5
    });
  }

  // Функция анимации
  function animate() {
    // Очистка canvas перед новым кадром
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);

    // Установка стиля для всех снежинок (один раз)
    ctx.fillStyle = "white";
    ctx.beginPath(); // Начинаем путь для всех снежинок

    // Обновление и отрисовка снежинок
    for (let i = 0; i < snowflakes.length; i++) {
      const flake = snowflakes[i];

      // Отрисовка снежинки
      ctx.moveTo(flake.x, flake.y);
      ctx.arc(flake.x, flake.y, flake.radius, 0, Math.PI * 2);

      // Обновление позиции снежинки
      flake.y += flake.speed;

      // Проверка выхода за нижнюю границу canvas
      if (flake.y > canvasHeight) {
        flake.y = -flake.radius; // Перемещение наверх
        flake.x = Math.random() * canvasWidth; // Случайная X-координата
      }
    }

    // Завершение пути и заполнение всех снежинок
    ctx.fill();

    // Продолжение анимации
    animationId = requestAnimationFrame(animate);
  }

  // Запуск анимации
  animate();

  // Обработчик клика для увеличения скорости снежинок
  canvas.onclick = () => {
    for (let i = 0; i < snowflakes.length; i++) {
      // Увеличение скорости с ограничением (макс. 5)
      snowflakes[i].speed = Math.min(snowflakes[i].speed + 0.5, 5);
    }
  };

  // Возвращаем функцию для остановки анимации
  return () => {
    if (animationId) {
      cancelAnimationFrame(animationId);
      animationId = null;
      ctx.clearRect(0, 0, canvasWidth, canvasHeight); // Очистка canvas при остановке
    }
  };
}

// Функция для остановки анимации
let stopSnowfall = null;

// Запуск анимации при загрузке страницы
document.addEventListener("DOMContentLoaded", () => {
  stopSnowfall = startSnowfall();
});

// Пример остановки анимации (например, по клику на кнопку с id="stopButton")
document.getElementById("stopButton")?.addEventListener("click", () => {
  if (stopSnowfall) {
    stopSnowfall();
    stopSnowfall = null; // Сбрасываем для возможности повторного запуска
  }
});