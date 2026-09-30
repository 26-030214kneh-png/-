import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌깨기 게임",
    page_icon="🧱",
    layout="centered",
)

st.title("🧱 벽돌깨기")
st.caption("← → 방향키 또는 마우스로 패들을 움직여 보세요!")

game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">

<style>
    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        padding: 0;
        background: #111827;
        font-family: Arial, sans-serif;
        color: white;
        text-align: center;
    }

    #game-wrapper {
        width: 100%;
        max-width: 720px;
        margin: auto;
    }

    #game {
        display: block;
        width: 100%;
        max-width: 700px;
        height: auto;
        margin: 10px auto;
        background: linear-gradient(
            180deg,
            #172554 0%,
            #0f172a 100%
        );
        border: 3px solid #38bdf8;
        border-radius: 10px;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.3);
    }

    #info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 700px;
        margin: 10px auto;
        padding: 10px 15px;
        background: #1e293b;
        border-radius: 8px;
        font-size: 18px;
    }

    #message {
        font-size: 24px;
        font-weight: bold;
        color: #facc15;
        min-height: 35px;
    }

    button {
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        background: #0ea5e9;
        color: white;
        font-size: 16px;
        cursor: pointer;
    }

    button:hover {
        background: #0284c7;
    }

    #mobile-controls {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 10px;
    }

    .control-button {
        width: 120px;
        height: 55px;
        font-size: 25px;
        user-select: none;
        -webkit-user-select: none;
        touch-action: none;
    }

    @media (max-width: 600px) {
        #info {
            font-size: 15px;
        }

        .control-button {
            width: 100px;
        }
    }
</style>
</head>

<body>

<div id="game-wrapper">

    <div id="info">
        <span>점수: <strong id="score">0</strong></span>
        <span>목숨: <strong id="lives">3</strong></span>
        <button onclick="restartGame()">다시 시작</button>
    </div>

    <canvas id="game" width="700" height="500"></canvas>

    <div id="message"></div>

    <div id="mobile-controls">
        <button
            class="control-button"
            id="leftButton"
        >◀</button>

        <button
            class="control-button"
            id="rightButton"
        >▶</button>
    </div>

</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const scoreElement = document.getElementById("score");
const livesElement = document.getElementById("lives");
const messageElement = document.getElementById("message");

const WIDTH = canvas.width;
const HEIGHT = canvas.height;

// -----------------------------
// 게임 설정
// -----------------------------

const paddle = {
    width: 110,
    height: 15,
    x: WIDTH / 2 - 55,
    y: HEIGHT - 35,
    speed: 8
};

const ball = {
    radius: 9,
    x: WIDTH / 2,
    y: HEIGHT - 55,
    dx: 4,
    dy: -4
};

const brickSettings = {
    rows: 5,
    columns: 9,
    width: 65,
    height: 22,
    padding: 8,
    offsetTop: 55,
    offsetLeft: 22
};

let bricks = [];
let score = 0;
let lives = 3;

let leftPressed = false;
let rightPressed = false;

let gameRunning = true;

// 벽돌 색상
const brickColors = [
    "#ef4444",
    "#f97316",
    "#eab308",
    "#22c55e",
    "#3b82f6"
];

// -----------------------------
// 벽돌 생성
// -----------------------------

function createBricks() {

    bricks = [];

    for (let row = 0; row < brickSettings.rows; row++) {

        for (let column = 0; column < brickSettings.columns; column++) {

            const x =
                brickSettings.offsetLeft +
                column *
                (brickSettings.width + brickSettings.padding);

            const y =
                brickSettings.offsetTop +
                row *
                (brickSettings.height + brickSettings.padding);

            bricks.push({
                x: x,
                y: y,
                width: brickSettings.width,
                height: brickSettings.height,
                visible: true,
                color: brickColors[row % brickColors.length]
            });
        }
    }
}

// -----------------------------
// 공 초기화
// -----------------------------

function resetBall() {

    ball.x = WIDTH / 2;
    ball.y = HEIGHT - 55;

    ball.dx = Math.random() > 0.5 ? 4 : -4;
    ball.dy = -4;
}

// -----------------------------
// 게임 초기화
// -----------------------------

function restartGame() {

    score = 0;
    lives = 3;

    scoreElement.textContent = score;
    livesElement.textContent = lives;

    paddle.x = WIDTH / 2 - paddle.width / 2;

    resetBall();
    createBricks();

    gameRunning = true;

    messageElement.textContent = "";
}

// -----------------------------
// 키보드 입력
// -----------------------------

document.addEventListener("keydown", function(event) {

    if (event.key === "ArrowLeft") {
        leftPressed = true;
        event.preventDefault();
    }

    if (event.key === "ArrowRight") {
        rightPressed = true;
        event.preventDefault();
    }

    if (event.key === " ") {

        if (!gameRunning) {
            restartGame();
        }

        event.preventDefault();
    }
});

document.addEventListener("keyup", function(event) {

    if (event.key === "ArrowLeft") {
        leftPressed = false;
    }

    if (event.key === "ArrowRight") {
        rightPressed = false;
    }
});

// -----------------------------
// 모바일 버튼
// -----------------------------

const leftButton = document.getElementById("leftButton");
const rightButton = document.getElementById("rightButton");

function startLeft(e) {
    e.preventDefault();
    leftPressed = true;
}

function stopLeft(e) {
    e.preventDefault();
    leftPressed = false;
}

function startRight(e) {
    e.preventDefault();
    rightPressed = true;
}

function stopRight(e) {
    e.preventDefault();
    rightPressed = false;
}

leftButton.addEventListener("pointerdown", startLeft);
leftButton.addEventListener("pointerup", stopLeft);
leftButton.addEventListener("pointerleave", stopLeft);
leftButton.addEventListener("pointercancel", stopLeft);

rightButton.addEventListener("pointerdown", startRight);
rightButton.addEventListener("pointerup", stopRight);
rightButton.addEventListener("pointerleave", stopRight);
rightButton.addEventListener("pointercancel", stopRight);

// -----------------------------
// 마우스로 패들 이동
// -----------------------------

canvas.addEventListener("mousemove", function(event) {

    const rect = canvas.getBoundingClientRect();

    const mouseX =
        (event.clientX - rect.left)
        * (canvas.width / rect.width);

    paddle.x = mouseX - paddle.width / 2;

    if (paddle.x < 0) {
        paddle.x = 0;
    }

    if (paddle.x + paddle.width > WIDTH) {
        paddle.x = WIDTH - paddle.width;
    }
});

// -----------------------------
// 그리기 함수
// -----------------------------

function drawPaddle() {

    ctx.fillStyle = "#38bdf8";

    ctx.beginPath();

    ctx.roundRect(
        paddle.x,
        paddle.y,
        paddle.width,
        paddle.height,
        7
    );

    ctx.fill();
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
    ctx.fill();

    ctx.closePath();
}

function drawBricks() {

    bricks.forEach(function(brick) {

        if (!brick.visible) {
            return;
        }

        ctx.fillStyle = brick.color;

        ctx.beginPath();

        ctx.roundRect(
            brick.x,
            brick.y,
            brick.width,
            brick.height,
            5
        );

        ctx.fill();

        // 벽돌 하이라이트
        ctx.fillStyle = "rgba(255,255,255,0.25)";

        ctx.fillRect(
            brick.x + 3,
            brick.y + 3,
            brick.width - 6,
            4
        );
    });
}

function draw() {

    ctx.clearRect(
        0,
        0,
        WIDTH,
        HEIGHT
    );

    drawBricks();
    drawPaddle();
    drawBall();
}

// -----------------------------
// 벽돌 충돌
// -----------------------------

function collisionDetection() {

    for (let i = 0; i < bricks.length; i++) {

        const brick = bricks[i];

        if (!brick.visible) {
            continue;
        }

        if (
            ball.x > brick.x &&
            ball.x < brick.x + brick.width &&
            ball.y - ball.radius < brick.y + brick.height &&
            ball.y + ball.radius > brick.y
        ) {

            ball.dy = -ball.dy;

            brick.visible = false;

            score += 10;

            scoreElement.textContent = score;

            // 모든 벽돌을 깼는지 확인
            const remaining = bricks.some(
                brick => brick.visible
            );

            if (!remaining) {
                gameWin();
            }

            break;
        }
    }
}

// -----------------------------
// 승리
// -----------------------------

function gameWin() {

    gameRunning = false;

    messageElement.textContent =
        "🎉 축하합니다! 모든 벽돌을 깼습니다!";

}

// -----------------------------
// 게임 오버
// -----------------------------

function gameOver() {

    gameRunning = false;

    messageElement.textContent =
        "💥 게임 오버! 스페이스바 또는 다시 시작 버튼을 누르세요.";
}

// -----------------------------
// 공 이동
// -----------------------------

function updateBall() {

    ball.x += ball.dx;
    ball.y += ball.dy;

    // 왼쪽 / 오른쪽 벽
    if (
        ball.x + ball.radius > WIDTH ||
        ball.x - ball.radius < 0
    ) {

        ball.dx = -ball.dx;
    }

    // 위쪽 벽
    if (
        ball.y - ball.radius < 0
    ) {

        ball.dy = -ball.dy;
    }

    // 패들과 충돌
    if (
        ball.y + ball.radius >= paddle.y &&
        ball.y - ball.radius <= paddle.y + paddle.height &&
        ball.x >= paddle.x &&
        ball.x <= paddle.x + paddle.width &&
        ball.dy > 0
    ) {

        // 패들 중앙에서 얼마나 떨어졌는지 계산
        const hitPosition =
            (ball.x - paddle.x)
            / paddle.width;

        const angle =
            (hitPosition - 0.5) * Math.PI * 0.8;

        const speed =
            Math.sqrt(
                ball.dx * ball.dx +
                ball.dy * ball.dy
            );

        ball.dx =
            Math.sin(angle) * speed;

        ball.dy =
            -Math.abs(
                Math.cos(angle) * speed
            );

        // 패들 안으로 파고드는 현상 방지
        ball.y =
            paddle.y - ball.radius;
    }

    // 바닥
    if (ball.y - ball.radius > HEIGHT) {

        lives--;

        livesElement.textContent = lives;

        if (lives <= 0) {

            gameOver();

        } else {

            resetBall();
        }
    }
}

// -----------------------------
// 패들 이동
// -----------------------------

function updatePaddle() {

    if (leftPressed) {
        paddle.x -= paddle.speed;
    }

    if (rightPressed) {
        paddle.x += paddle.speed;
    }

    if (paddle.x < 0) {
        paddle.x = 0;
    }

    if (paddle.x + paddle.width > WIDTH) {
        paddle.x = WIDTH - paddle.width;
    }
}

// -----------------------------
// 게임 루프
// -----------------------------

function gameLoop() {

    draw();

    if (gameRunning) {

        updatePaddle();
        updateBall();
        collisionDetection();
    }

    requestAnimationFrame(gameLoop);
}

// 게임 시작
restartGame();
gameLoop();

</script>

</body>
</html>
"""

components.html(
    game_html,
    height=650,
    scrolling=False
)
