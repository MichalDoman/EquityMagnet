const header = document.querySelector("header")
const messageTriggers = document.querySelectorAll(".message-trigger")
let messageDiv = null

function showMessage(message) {
    if (messageDiv){
        document.body.removeChild(messageDiv)
    }
    messageDiv = document.createElement("div");
    messageDiv.classList.add("message-div")
    messageDiv.innerHTML = message;

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
