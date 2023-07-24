function appendMessage(message, fromUser) {
    const chatBox = document.getElementById('chatBox');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + (fromUser ? 'from-user' : 'from-chatbot');
    messageDiv.innerHTML = `<p>${message}</p>`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
}

let sendingMessage = false; 

function sendMessage() {
    if (sendingMessage) return; 

    const userInput = document.getElementById('userInput').value;

    if (userInput.trim() === '') return;

    appendMessage(userInput, true);

    sendingMessage = true; 

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
        })
        .catch(error => console.error('Error:', error));

    // Clear user input field
    document.getElementById('userInput').value = '';
    sendingMessage = false; 
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}