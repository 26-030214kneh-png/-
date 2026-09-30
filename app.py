  import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌깨기 게임",
    page_icon="🧱",
    layout="centered"
)

st.title("🧱 벽돌깨기 게임")
st.write("키보드 ← → 로 막대를 움직여 공이 떨어지지 않게 하세요!")

game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">

<style>
    body {
        margin: 0;
        padding: 0;
        background: #111827;
        display: flex;
        justify-content: center;
        align-items: center;
        font-family: Arial, sans-serif;
    }

    #gameContainer {
        text-align: center;
    }

    canvas {
        background: linear-gradient(#0f172a, #020617);
        border: 3px solid #38bdf8;
        border-radius: 10px;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.4);
    }

    #info {
        color: white;
        font-size: 18px;
        margin: 10px;
    }

    button {
        background: #38bdf8;
        color: #0f172a;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
    }

    button:hover {
        background: #7dd3fc;
    }
</style>
</head>

<body>

<div id="gameContainer">

    <div id="info">
        점수: <span id="score">0</span>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        목숨: <span id="lives">3</span>
    </div>

    <canvas id="gameCanvas" width="480" height="600"></canvas>

    <br><br>

    <button onclick="restartGame()">🔄 다시 시작</button>

</div>

<script>

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let score = 0;
let lives = 3;

let gameOver = false;
let gameWon = false;

// 공
let ball = {
    x: canvas.width / 2,
    y: canvas.height - 60,
    radius: 8,
    dx: 4,
    dy: -4
};

// 플레이어 막대
let paddle = {
    width: 90,
    height: 12,
    x: canvas.width / 2 - 45,
    y: canvas.height - 30,
    speed: 7
};

// 키 입력
let rightPressed = false;
let leftPressed = false;

// 벽돌
const brickRows = 6;
const brickColumns = 8;

const brickWidth = 50;
const brickHeight = 20;
const brickPadding = 8;

const brickOffsetTop = 50;
const brickOffsetLeft = 20;

let bricks = [];

function createBricks() {

    bricks = [];

    for (let r = 0; r < brickRows; r++) {

        bricks[r] = [];

        for (let c = 0; c < brickColumns; c++) {

            bricks[r][c] = {
                x: brickOffsetLeft +
                   c * (brickWidth + brickPadding),

                y: brickOffsetTop +
                   r * (brickHeight + brickPadding),

                alive: true,

                color: [
                    "#ef4444",
                    "#f97316",
                    "#eab308",
                    "#22c55e",
                    "#06b6d4",
                    "#8b5cf6"
                ][r]
            };
        }
    }
}

function drawBall() {

    ctx.beginPath();

    ctx.arc(
        ball.x,
        ball.y,
        ball.radius,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#ffffff";
    ctx.shadowColor = "#38bdf8";
    ctx.shadowBlur = 15;

    ctx.fill();

    ctx.shadowBlur = 0;

    ctx.closePath();
}

function drawPaddle() {

    ctx.beginPath();

    ctx.roundRect(
        paddle.x,
        paddle.y,
        paddle.width,
        paddle.height,
        6
    );

    ctx.fillStyle = "#38bdf8";
    ctx.fill();

    ctx.closePath();
}

function drawBricks() {

    for (let r = 0; r < brickRows; r++) {

        for (let c = 0; c < brickColumns; c++) {

            const brick = bricks[r][c];

            if (!brick.alive) continue;

            ctx.beginPath();

            ctx.roundRect(
                brick.x,
                brick.y,
                brickWidth,
                brickHeight,
                4
            );

            ctx.fillStyle = brick.color;
            ctx.fill();

            ctx.closePath();
        }
    }
}

function collisionDetection() {

    for (let r = 0; r < brickRows; r++) {

        for (let c = 0; c < brickColumns; c++) {

            const brick = bricks[r][c];

            if (!brick.alive) continue;

            if (
                ball.x > brick.x &&
                ball.x < brick.x + brickWidth &&
                ball.y > brick.y &&
                ball.y < brick.y + brickHeight
            ) {

                ball.dy = -ball.dy;

                brick.alive = false;

                score += 10;

                document.getElementById("score").textContent = score;

                checkWin();
            }
        }
    }
}

function checkWin() {

    let remaining = 0;

    for (let r = 0; r < brickRows; r++) {
        for (let c = 0; c < brickColumns; c++) {

            if (bricks[r][c].alive) {
                remaining++;
            }
        }
    }

    if (remaining === 0) {

        gameWon = true;
        gameOver = true;

        setTimeout(() => {
            alert("🎉 축하합니다! 모든 벽돌을 깼습니다!");
        }, 100);
    }
}

function resetBall() {

    ball.x = canvas.width / 2;
    ball.y = canvas.height - 60;

    ball.dx = 4 * (Math.random() > 0.5 ? 1 : -1);
    ball.dy = -4;
}

function update() {

    if (gameOver) return;

    // 벽 충돌
    if (
        ball.x + ball.radius > canvas.width ||
        ball.x - ball.radius < 0
    ) {
        ball.dx = -ball.dx;
    }

    if (ball.y - ball.radius < 0) {
        ball.dy = -ball.dy;
    }

    // 막대 충돌
    if (
        ball.y + ball.radius >= paddle.y &&
        ball.y - ball.radius <= paddle.y + paddle.height &&
        ball.x >= paddle.x &&
        ball.x <= paddle.x + paddle.width &&
        ball.dy > 0
    ) {

        ball.dy = -Math.abs(ball.dy);

        // 막대의 어느 위치에 맞았는지에 따라 방향 변경
        let hitPosition =
            (ball.x - paddle.x) / paddle.width;

        ball.dx =
            (hitPosition - 0.5) * 8;
    }

    // 바닥에 떨어짐
    if (ball.y + ball.radius > canvas.height) {

        lives--;

        document.getElementById("lives").textContent = lives;

        if (lives <= 0) {

            gameOver = true;

            setTimeout(() => {
                alert("💥 게임 오버! 점수: " + score);
            }, 100);

        } else {

            resetBall();
        }
    }

    // 막대 이동
    if (rightPressed) {

        paddle.x += paddle.speed;

        if (paddle.x + paddle.width > canvas.width) {
            paddle.x = canvas.width - paddle.width;
        }
    }

    if (leftPressed) {

        paddle.x -= paddle.speed;

        if (paddle.x < 0) {
            paddle.x = 0;
        }
    }

    ball.x += ball.dx;
    ball.y += ball.dy;

    collisionDetection();
}

function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    drawBricks();
    drawBall();
    drawPaddle();

    update();

    requestAnimationFrame(draw);
}

document.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "ArrowRight") {
            rightPressed = true;
        }

        if (event.key === "ArrowLeft") {
            leftPressed = true;
        }
    }
);

document.addEventListener(
    "keyup",
    function(event) {

        if (event.key === "ArrowRight") {
            rightPressed = false;
        }

        if (event.key === "ArrowLeft") {
            leftPressed = false;
        }
    }
);

function restartGame() {

    score = 0;
    lives = 3;

    gameOver = false;
    gameWon = false;

    document.getElementById("score").textContent = score;
    document.getElementById("lives").textContent = lives;

    paddle.x =
        canvas.width / 2 - paddle.width / 2;

    resetBall();
    createBricks();
}

// 게임 시작
createBricks();
draw();

</script>

</body>
</html>
"""

components.html(
    game_html,
    height=720,
    scrolling=False
)
