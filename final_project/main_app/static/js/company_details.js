const tab_buttons = document.querySelectorAll(".tab-btn");
const details = document.querySelectorAll(".details");
const section = document.querySelector(".center-section")

section.addEventListener("click", function (event) {
    const tab_id = event.target.dataset.id;
    if (tab_id) {
        tab_buttons.forEach(function (button) {
            button.classList.remove("active");
            event.target.classList.add("active");
        });
        details.forEach(function (detail) {
            detail.classList.remove("active");
        });
        const tab = document.getElementById(tab_id);
        tab.classList.add("active");
    }
});