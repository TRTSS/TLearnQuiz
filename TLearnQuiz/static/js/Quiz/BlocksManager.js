function GetBlock (id) {
    let allBlocks = document.querySelectorAll("#quiz-block");

    allBlocks.forEach(item => {
        item.style.display = "none";
    })

    document.querySelector(`#${id}`).style.display = "block";
}