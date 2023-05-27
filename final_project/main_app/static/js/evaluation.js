const tabButtons = document.querySelectorAll(".evaluation-box button")
const contentBoxes = document.querySelectorAll(".content")
const evaluationBox = document.querySelector(".evaluation-box")

evaluationBox.addEventListener("click", (event) => {
    const tab_id = event.target.dataset.id;
    if (tab_id) {
        tabButtons.forEach(function (button) {
            button.classList.remove("active");
            event.target.classList.add("active");
        });
        contentBoxes.forEach(function (content) {
            content.classList.remove("active");
        });
        const tab = document.getElementById(tab_id);
        tab.classList.add("active");
    }
});
