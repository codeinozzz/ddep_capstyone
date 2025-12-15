const API_URL = 'http://localhost:8000';

let sessionId = null;

const elements = {
    sessionIdDisplay: document.getElementById('session-id'),
    newSessionBtn: document.getElementById('new-session-btn'),
    chatMessages: document.getElementById('chat-messages'),
    messageInput: document.getElementById('message-input'),
    sendBtn: document.getElementById('send-btn'),
    styleSelect: document.getElementById('style-select'),
    modeSelect: document.getElementById('mode-select'),
    stepsInput: document.getElementById('steps-input'),
    guidanceInput: document.getElementById('guidance-input')
};

async function createSession() {
    try {
        const response = await fetch(`${API_URL}/api/sessions`, {
            method: 'POST'
        });
        const data = await response.json();
        sessionId = data.session_id;
        elements.sessionIdDisplay.textContent = `Session: ${sessionId.substring(0, 8)}`;
        elements.chatMessages.innerHTML = '';
        addSystemMessage('Nueva sesion iniciada');
    } catch (error) {
        console.error('Error creating session:', error);
        addSystemMessage('Error al crear sesion');
    }
}

async function sendMessage() {
    const message = elements.messageInput.value.trim();
    if (!message) return;

    if (!sessionId) {
        await createSession();
    }

    addMessage('user', message);
    elements.messageInput.value = '';

    const loadingDiv = addLoadingMessage();

    try {
        const config = {
            style: elements.styleSelect.value,
            default_mode: elements.modeSelect.value,
            max_steps: parseInt(elements.stepsInput.value),
            guidance_scale: parseFloat(elements.guidanceInput.value)
        };

        const response = await fetch(`${API_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                message: message,
                config: config
            })
        });

        const data = await response.json();
        loadingDiv.remove();

        addAssistantResponse(data);

    } catch (error) {
        console.error('Error sending message:', error);
        loadingDiv.remove();
        addSystemMessage('Error al enviar mensaje');
    }
}

function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;

    const timestampDiv = document.createElement('div');
    timestampDiv.className = 'message-timestamp';
    timestampDiv.textContent = new Date().toLocaleTimeString();

    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timestampDiv);

    elements.chatMessages.appendChild(messageDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

function addAssistantResponse(data) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';

    if (data.text_content) {
        const specDiv = document.createElement('div');
        specDiv.className = 'message-spec';
        specDiv.textContent = data.text_content;
        messageDiv.appendChild(specDiv);
    }

    if (data.image_url) {
        const imageDiv = document.createElement('div');
        imageDiv.className = 'message-image';
        const img = document.createElement('img');
        img.src = `${API_URL}${data.image_url}`;
        img.alt = 'Generated render';
        imageDiv.appendChild(img);
        messageDiv.appendChild(imageDiv);
    }

    const timestampDiv = document.createElement('div');
    timestampDiv.className = 'message-timestamp';
    timestampDiv.textContent = new Date().toLocaleTimeString();
    messageDiv.appendChild(timestampDiv);

    elements.chatMessages.appendChild(messageDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

function addLoadingMessage() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant';
    loadingDiv.innerHTML = '<div class="loading">Generando respuesta</div>';
    elements.chatMessages.appendChild(loadingDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
    return loadingDiv;
}

function addSystemMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = message;
    messageDiv.appendChild(contentDiv);
    elements.chatMessages.appendChild(messageDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

elements.sendBtn.addEventListener('click', sendMessage);
elements.messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

elements.newSessionBtn.addEventListener('click', createSession);

createSession();
