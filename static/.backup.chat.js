function appendMessage(message, fromUser) {
    const chatBox = document.getElementById('chatBox');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + (fromUser ? 'from-user' : 'from-chatbot');
    messageDiv.innerHTML = `<p>${message}</p>`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
}

let sendingMessage = false; // Variable to track if a message is being sent

function sendMessage() {
    // If a message is already being sent, don't send another

    const userInput = document.getElementById('userInput').value;
    if (userInput.trim() === '') return;

    // Disable input field and "Send" button while sending the message
    const userInputField = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    userInputField.disabled = true;
    sendButton.disabled = true;

    appendMessage(userInput, true);

    // Make an AJAX request to the backend to get chatbot response
    fetch('/get_chat_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    })
        .then(response => response.json())
        .then(data => {
            const chatbotResponse = data.message;
            appendMessage(chatbotResponse, false);

            // Enable input field and "Send" button after the chatbot responds
            userInputField.disabled = false;
            sendButton.disabled = false;
            sendingMessage = false;
        })
        .catch(error => console.error('Error:', error));

    sendingMessage = true; // Set the sendingMessage flag to true to prevent multiple messages being sent
    // Clear user input field
    userInputField.value = '';
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}