// script.js
document.getElementById("send-btn").addEventListener("click", function () {
    const userInput = document.getElementById("user-input").value.trim();
    const lang = document.getElementById("user-lang").value;
    if (userInput) {
        // Add user message
        addMessage(userInput, "user-message");

        // Send user input to backend
        fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: userInput,
                lang: lang
            })
        })
            .then(response => response.json())
            .then(data => {
                const botResponse = data.response;
                addMessage(botResponse, "bot-message");
            })
            .catch(error => {
                console.error("Error:", error);
                addMessage("Something went wrong. Please try again.", "bot-message");
            });

        // Clear input field
        document.getElementById("user-input").value = "";
    }
});

document.getElementById("user-input").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("send-btn").click();
    }
});

function addMessage(message, className) {
    const chatWindow = document.getElementById("chat-window");
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${className}`;
    messageDiv.textContent = message;
    chatWindow.appendChild(messageDiv);

    // Scroll to the bottom
    chatWindow.scrollTop = chatWindow.scrollHeight;
}