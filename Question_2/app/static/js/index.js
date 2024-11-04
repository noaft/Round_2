document.addEventListener("DOMContentLoaded", function() {
    const message = document.getElementsByClassName('input-field')[0]
    const chat_message = document.getElementsByClassName('message_text')[0]
    message.addEventListener("keydown", function(event) {
        if (event.key === "Enter") { 
            const message_text = message.value
            // add new element
            const messageDiv = document.createElement("div");
            messageDiv.classList.add("message","sent")
            messageDiv.textContent = message_text;
            chat_message.appendChild(messageDiv);

            message.value = '';
        }
    });
});
