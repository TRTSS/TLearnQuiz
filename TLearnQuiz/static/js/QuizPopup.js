POPUP_MODAL = document.querySelector('#quiz-popup');
let LEVEL_UP_SOUND = new Audio('/static/audio/LevelUpSound.wav');

async function ShowLevelData(offset, scores) {
    POPUP_MODAL.innerHTML = "Получаем данные...";
    POPUP_MODAL.style.display = "block";

    let resp = await fetch(`/api/get_user_level_data?offset=${offset}`);
    let res = await resp.json();
    POPUP_MODAL.innerHTML = `
                                <p><b>Получено ${scores} ед. опыта</b></p>
                                <p>Уровень ${res.level}: <br><span id="currentXpBarLabel">${res.xp}</span> / ${res.xpNeed}</p>
                                <div class="xpbar-back">
                                    <div class="xpbar" id="modal-xp" style=""></div>
                                </div>
                            `;

    let bar = document.querySelector("#modal-xp");
    bar.style.width = String(100 / res.xpNeed * res.xp) + "%";
    let currentXpBarLabel = document.querySelector('#currentXpBarLabel');

    let addIter = 0;
    setTimeout(() => {
        let addingScoresInterval = setInterval(() => {
            addIter += 1;
            let pr = 100 / res.xpNeed * (res.xp + offset / 2000 * 10 * addIter);
            let w = String(pr) + "%";
            currentXpBarLabel.innerHTML = String(Math.round(res.xp + offset / 2000 * 10 * addIter));
            bar.style.width = w;
            if (pr >= 100) {
                clearInterval(addingScoresInterval);
                LEVEL_UP_SOUND.currentTime = 0;
                LEVEL_UP_SOUND.play();
                ShowLevelData(Math.round(offset - offset / 2000 * 10 * addIter), scores);
            }
        }, 10);
        setTimeout(() => {
            clearInterval(addingScoresInterval);
        }, 2000);
    }, 1000);
}