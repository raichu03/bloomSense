
document.getElementById('send-button').addEventListener('click', function() {
    getMessage();
});

document.getElementById('message').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        getMessage();
    }
});

function getMessage() {
    const message = document.getElementById('message').value;
    document.getElementById('message').value = '';

    if (message.trim() !== '') {
        const chatBox = document.getElementById('chat-box');
        const userTextDiv = document.createElement('div');
        userTextDiv.className = 'user-text';
        userTextDiv.textContent = message;
        chatBox.appendChild(userTextDiv);
    }

    askAgent(message);
}

function askAgent(message){
    console.log('Asking agent');
    fetch('/conversation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({message: message})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.response);
        addAgentResponse(data.response);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function addAgentResponse(message){
    const chatBox = document.getElementById('chat-box');
    const agentTextDiv = document.createElement('div');
    agentTextDiv.className = 'assistant-text';
    agentTextDiv.textContent = message;
    chatBox.appendChild(agentTextDiv);
}