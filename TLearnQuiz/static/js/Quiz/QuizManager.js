// TIMER STUFF
let timeForAnswer = 10;
let timeLeft = 10;
let timer = document.querySelector("#question-timer");

// SCORES STUFF
let scores = 0;
let scoresForQuestion;
let currentScoresReward;

let timerInterval;


// QUIZ QUESTIONS STUFF
let questionList = [];
let answers = [];
let corrects = [];
let currentQuestion = 0;
let playerAnswers = [];
let playerRes = 0;


function getCookie(name) {
    let cookie = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return cookie ? cookie[2] : null;
}

async function CheckAccess(quizId) {
    let data = new FormData();
    data.append("quizId", quizId);
    let resp = await fetch("/api/check_access_to_quiz", {
        method: "post",
        body: data,
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    });
    return await resp.json();
}

async function SendResults(quizId, scores) {
    let data = new FormData();
    data.append("quizId", quizId);
    data.append("scores", scores);
    let resp = await fetch("/api/send_quiz_result", {
        method: "post",
        body: data,
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    });

    return await resp.json();
}

async function GetQuizLeaders(quizId) {
    let data = new FormData();
    data.append("quizId", quizId);
    let resp = await fetch("{% url 'apiGetQuizLeaders' %}", {
        method: "post",
        body: data,
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    });
    return await resp.json();
}

async function ShowLeaderTable() {
    let board = await GetQuizLeaders();
    console.log(board);
    let boardTable = document.querySelector("#leader-board");

    let place = 1;

    console.log(board.data);

    for (var k in board.data) {
        boardTable.innerHTML += `<tr>
                                        <td>${place}</td>
                                        <td>${board.data[k].username}</td>
                                        <td>${board.data[k].scores}</td>
                                     </tr>`;
        place += 1
    }
}


async function SetCurrentQuestion() {

    document.querySelector('#quiz-loading-area').style.display = "block";
    document.querySelector("#quiz-area").style.display = "none";
    let timeAccess = await CheckAccess();
    document.querySelector('#quiz-loading-area').style.display = "none";
    if (timeAccess.ok) {
        document.querySelector("#quiz-area").style.display = "block";
        if (currentQuestion >= questionList.length) {
            clearInterval(timerInterval);
            for (let i = 0; i < playerAnswers.length; i++) {
                if (playerAnswers[i] === corrects[i]) {
                    playerRes += 1;
                }
            }

            quizEnd.play();
            console.log("RESULT: " + String(playerRes));
            document.querySelector("#quiz-result-area").innerHTML = `${playerRes} / ${corrects.length}`;
            document.querySelector("#quiz-scores-area").innerHTML = `Вы набрали ${scores} очков`;

            document.querySelector("#quiz-area").style.display = "none";
            document.querySelector("#quiz-end-area").style.display = "block";
            console.log(playerAnswers);

            let statusLabel = document.querySelector("#sending-res-status-area");
            statusLabel.innerHTML = "<span class='text-muted'>Отправляем данные... <i class='bx bx-loader-circle bx-spin' ></i></span>";

            let res = await SendResults(scores);
            if (res.ok) {
                statusLabel.innerHTML = "<span class='text-success'>Ваши результаты учтены <i class='bx bx-check' ></i></span>";
            } else {
                statusLabel.innerHTML = `<span class='text-danger'>Ваши результаты не учтены. Причина: ${res.verbose}</span>`;
            }
        } else {

            timeLeft = timeForAnswer;
            currentScoresReward = scoresForQuestion;
            timerInterval = setInterval(() => {
                timeLeft -= 10 / 1000
                timer.style.width = String(100 / timeForAnswer * timeLeft) + "%";
                if (currentScoresReward > Math.floor(scoresForQuestion / 2)) {
                    currentScoresReward = Math.floor(scoresForQuestion - (scoresForQuestion / 2 / timeForAnswer * (timeForAnswer - timeLeft)));
                }
                document.querySelector("#scores-reward").innerHTML = String(currentScoresReward);
                if (timeLeft <= 0) AcceptAnswer(null);
            }, 10);
            document.querySelector("#question-area").innerHTML = questionList[currentQuestion];

            document.querySelector("#question-counter-area").innerHTML = `Вопрос ${currentQuestion + 1} из ${corrects.length}`;

            document.querySelector("#question-answer-1").innerHTML = answers[currentQuestion * 4 + 0];
            document.querySelector("#question-answer-2").innerHTML = answers[currentQuestion * 4 + 1];
            document.querySelector("#question-answer-3").innerHTML = answers[currentQuestion * 4 + 2];
            document.querySelector("#question-answer-4").innerHTML = answers[currentQuestion * 4 + 3];

            document.querySelector("#question-answer-1").setAttribute("answer", answers[currentQuestion * 4 + 0]);
            document.querySelector("#question-answer-2").setAttribute("answer", answers[currentQuestion * 4 + 1]);
            document.querySelector("#question-answer-3").setAttribute("answer", answers[currentQuestion * 4 + 2]);
            document.querySelector("#question-answer-4").setAttribute("answer", answers[currentQuestion * 4 + 3]);
        }
    } else {
        document.querySelector("#quiz-not-begin-area").style.display = "block";
    }

}


async function StartQuiz() {
    document.querySelector("#welcome-area").style.display = "none";
    document.querySelector("#quiz-loading-area").style.display = "block";
    let res = await CheckAccess();
    document.querySelector("#quiz-loading-area").style.display = "none";
    if (res.ok) {
        document.querySelector("#quiz-area").style.display = "block";

        waitingMusic.pause();
        quizStarted.play();

        await SetCurrentQuestion();
    } else {
        document.querySelector("#quiz-not-begin-area").style.display = "block";
        document.querySelector("#welcome-area").style.display = "none";
    }

    scoresForQuestion = Math.floor(100 / corrects.length);
}