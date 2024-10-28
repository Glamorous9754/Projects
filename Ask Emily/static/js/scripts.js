function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    if (!userInput.trim()) return;  // Avoid sending empty messages

    // Display the user message in the chat box
    displayMessage(`You: ${userInput}`, 'user');

    // Send the message to the backend
    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: userInput })
    })
    .then(response => response.json())
    .then(data => {
        displayMessage(`Ask Emily: ${data.response}`, 'bot');
    })
    .catch(error => console.error('Error:', error));

    // Clear the input field after sending
    document.getElementById('userInput').value = '';
}

function displayMessage(text, sender) {
    const chatBox = document.getElementById('chatBox');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.innerText = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the bottom
}
