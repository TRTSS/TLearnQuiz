POPUP_MODAL = document.querySelector('#quiz-popup');

async function ShowLevelData() {
    POPUP_MODAL.innerHTML = "Получаем данные...";
    POPUP_MODAL.style.display = "block";
    let resp = await fetch('/api/get_user_level_data');
    let res = await resp.json();
    let newXp = 44;
    POPUP_MODAL.innerHTML = `
                                <p><b>Получено ${newXp} ед. опыта</b></p>
                                <p>Уровень ${res.level}</p>
                                <div>
                                
                                </div>
                            `;
}