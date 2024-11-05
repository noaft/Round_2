document.addEventListener("DOMContentLoaded", function() {
    const message = document.getElementsByClassName('input-field')[0]
    const chat_message = document.getElementsByClassName('chat-messages')[0]
    const userInput = document.getElementsByClassName('another-field')[0]
    const popup = document.getElementsByClassName('popup-container')[0]
    const plus_button = document.getElementsByClassName('plus-button')[0]
    const cancle = document.getElementById('cancel-button')
    const Submit = document.getElementById('submit-button')

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

    Submit.addEventListener("click", function() {
        // Collect input values
        const hours = document.getElementById('hours').value;
        const minutes = document.getElementById('minutes').value;
        const seconds = document.getElementById('seconds').value;

        // Combine the time values into a message
        const timeMessage = `Meeting Duration: ${hours}h ${minutes}m ${seconds}s`;
        
        // Create and append the new message element
        const allMessages = document.querySelectorAll('.chat-messages .message');
        let collectedText = '';

        // Concatenate all message text into one string
        allMessages.forEach(messageElement => {
            collectedText += messageElement.textContent + '\n';
        });

        // Display or process the collected text
        console.log("Collected Text:\n" + collectedText);
        console.log(collectedText, timeMessage)
        const data = { timeMessage: timeMessage, collectedText: collectedText };

        // Send the data to the FastAPI backend
        fetch("http://localhost:8000/submit-data/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log("Success:", data);
        })
        .catch((error) => {
            console.error("Error:", error);
        });

        // Hide the popup and clear input fields
        popup.style.display = "none";
        document.getElementById('hours').value = '';
        document.getElementById('minutes').value = '';
        document.getElementById('seconds').value = '';
    });

    plus_button.addEventListener("click", function(){
        popup.style.display = "flex"
    })

    cancle.addEventListener("click", function(){
        popup.style.display = "none"
    })

    userInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") { 
            const message_text = userInput.value
            // add new element
            const messageDiv = document.createElement("div");
            messageDiv.classList.add("message","received")
            messageDiv.textContent = message_text;
            chat_message.appendChild(messageDiv);

            userInput.value = '';
        }
    });
});
