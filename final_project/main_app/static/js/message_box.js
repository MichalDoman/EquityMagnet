const header = document.querySelector("header")
const messageTriggers = document.querySelectorAll(".message-trigger")
let messageDiv = null

function showMessage(message) {
    if (messageDiv) {
        document.body.removeChild(messageDiv)
    }
    messageDiv = document.createElement("div");
    messageDiv.classList.add("message-div")
    messageDiv.innerHTML = message;

    messageDiv.style.transform = 'translateX(-100%)'
    setTimeout(() => {
        messageDiv.style.transform = 'translateX(-2%)';
    }, 1);

    setTimeout(() => {
        messageDiv.style.transform = 'translateX(-100%)';
    }, 3000);

    header.insertAdjacentElement('afterend', messageDiv);
}

messageTriggers.forEach(trigger => {
    trigger.addEventListener("click", () => {
        let messageType = trigger.getAttribute("data-message-type")
        let message = ""
        if (messageType === "favorites") {
            if (trigger.innerHTML === "bookmark_border") {
                message = "Company added to favorites successfully!"
            } else {
                message = "Company removed from favorites!"
            }
        }
        showMessage(message)
    })
})
