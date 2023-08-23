let conversationHistory = [];

function appendMessage(message, fromUser) {
    const chatBox = document.getElementById('chatBox');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + (fromUser ? 'from-user' : 'from-chatbot');
    messageDiv.innerHTML = `<p>${message}</p>`;

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom

    // Update conversation history
    conversationHistory.push(
        `${fromUser ? 'user' : 'assistant'}: ${message}`
    );
}

let sendingMessage = false;

function sendMessage() {
    if (sendingMessage) return;

    const userInput = document.getElementById('userInput').value;

    if (userInput.trim() === '') return;

    sendingMessage = true;

    // Disable the input field while waiting for the response
    document.getElementById('userInput').disabled = true;

    appendMessage(userInput, true);

    // Make an AJAX request to the backend to get chatbot response
    fetch('/get_chat_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            message: userInput, 
            conversationHistory: conversationHistory 
        }), // Include conversation history
    })
        .then(response => response.json())
        .then(data => {
            const chatbotResponse = data.message;
            appendMessage(chatbotResponse, false);

            // Enable the input field after the response is received
            document.getElementById('userInput').disabled = false;
            sendingMessage = false;

            // Focus on the input box after the response is posted
            document.getElementById('userInput').focus();
        })
        .catch(error => console.error('Error:', error));

    // Clear user input field
    document.getElementById('userInput').value = '';
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Example: Print the entire conversation history (if needed)
function printConversation() {
    conversationHistory.forEach(entry => {
        console.log(`From User: ${entry.fromUser}, Message: ${entry.message}`);
    });
}
