function startSnowfall() {
  var canvas = document.getElementById("snowCanvas");
  var context = canvas.getContext("2d");
  var snowflakes = [];
  for (var i = 0; i < 10; i++) {
    snowflakes[i] = { x: Math.random() * 300, y: 0, speed: Math.random() };
  }
  setInterval(function() {
    context.fillStyle = "white";
    for (var i = 0; i < snowflakes.length; i++) {
      context.beginPath();
      context.arc(snowflakes[i].x, snowflakes[i].y, 5, 0, Math.PI * 2);
      context.fill();
      snowflakes[i].y = snowflakes[i].y + snowflakes[i].speed;
      if (snowflakes[i].y > 150) {
        snowflakes[i].y = 0;
      }
      context.fillStyle = "white";
      context.beginPath();
      context.arc(snowflakes[i].x, snowflakes[i].y, 5, 0, Math.PI * 2);
      context.fill();
    }
  }, 100);
  canvas.onclick = function() {
    for (var i = 0; i < snowflakes.length; i++) {
      snowflakes[i].speed = snowflakes[i].speed + 0.5;
    }
  };
}