let membership = [];

document.addEventListener("DOMContentLoaded", () => {
    loadMembership();
    loadChatMessages();
    loadLogs();

    document.getElementById("chat-message").addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});

async function loadMembership() {
    const response = await fetch('/membership');
    const data = await response.json();
    membership = data.membership;
    updateMembership();
}

async function loadChatMessages() {
    const response = await fetch('/messages');
    const data = await response.json();
    const chatLog = document.getElementById("chat-log");
    chatLog.innerHTML = "";
    data.messages.forEach(msg => {
        const chatItem = document.createElement("div");
        chatItem.textContent = msg;
        chatLog.appendChild(chatItem);
    });
}

async function loadLogs() {
    const response = await fetch('/logs');
    const data = await response.json();
    const logsContainer = document.getElementById("logs");
    logsContainer.innerHTML = "";
    data.logs.forEach(log => {
        const logItem = document.createElement("li");
        logItem.textContent = log;
        logsContainer.appendChild(logItem);
    });
}

async function clearLogs() {
    await fetch('/clear-logs', { method: 'POST' });
    loadLogs();
}

async function clearChat() {
    await fetch('/clear-messages', { method: 'POST' });
    const chatLog = document.getElementById("chat-log");
    chatLog.innerHTML = "";
    logEvent("CHAT: Todas as mensagens foram excluídas.");
}

async function joinGroup() {
    const processId = document.getElementById("membership-id").value;
    const response = await fetch('/join', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ process_id: processId })
    });
    const data = await response.json();
    if (!data.error) {
        loadMembership();
        logEvent(`JOIN: ${data.message}`);
    } else {
        alert(data.error);
    }
}

async function leaveGroup() {
    const processId = document.getElementById("membership-id").value;
    const response = await fetch('/leave', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ process_id: processId })
    });
    const data = await response.json();
    logEvent(`LEAVE: ${data.message}`);
    loadMembership();
}

async function sendMessage() {
    const processId = document.getElementById("process-id").value;
    const message = document.getElementById("chat-message").value;

    if (!message.trim()) {
        alert("Mensagem não pode estar vazia.");
        return;
    }

    const response = await fetch('/send-message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ process_id: processId, message: message.trim() })
    });
    const data = await response.json();
    if (!data.error) {
        logEvent(`MSG: Processo ${processId} enviou mensagem "${data.message}" com sequência ${data.sequence}.`);
        document.getElementById("chat-message").value = "";
        animateMessage(processId, data.sequence);
        loadChatMessages();
    } else {
        alert(data.error);
    }
}

async function resetSequence() {
    const response = await fetch('/reset-sequence', { method: 'POST' });
    const data = await response.json();
    logEvent(data.message);
    alert(data.message); // Notifica o usuário
}

function updateMembership() {
    const membershipDisplay = document.getElementById("membership");
    membershipDisplay.innerHTML = membership.map(id => {
        return `<div class="process" id="process-${id}" onclick="selectProcess('${id}')">${id}</div>`;
    }).join('');
}

function selectProcess(processId) {
    const chatProcessField = document.getElementById("process-id");
    const messageField = document.getElementById("chat-message");

    chatProcessField.value = processId;
    messageField.focus();
}

function animateMessage(processId, seqNumber) {
    const sequencer = document.getElementById("sequencer");
    const process = document.getElementById(`process-${processId}`);
    const messageToSequencer = document.createElement("div");
    const messageFromSequencer = document.createElement("div");

    messageToSequencer.className = "message-to-sequencer";
    messageToSequencer.textContent = `Msg: ${seqNumber}`;
    document.body.appendChild(messageToSequencer);

    messageFromSequencer.className = "message-from-sequencer";
    messageFromSequencer.textContent = `Seq: ${seqNumber}`;
    document.body.appendChild(messageFromSequencer);

    const procRect = process.getBoundingClientRect();
    const seqRect = sequencer.getBoundingClientRect();

    const scrollX = window.scrollX;
    const scrollY = window.scrollY;

    messageToSequencer.style.left = `${procRect.left + procRect.width / 2 - 10 + scrollX}px`;
    messageToSequencer.style.top = `${procRect.top + procRect.height / 2 - 10 + scrollY}px`;

    messageFromSequencer.style.left = `${seqRect.left + seqRect.width / 2 - 10 + scrollX}px`;
    messageFromSequencer.style.top = `${seqRect.top + seqRect.height / 2 - 10 + scrollY}px`;

    messageToSequencer.animate([
        { left: `${procRect.left + procRect.width / 2 - 10 + scrollX}px`, top: `${procRect.top + procRect.height / 2 - 10 + scrollY}px` },
        { left: `${seqRect.left + seqRect.width / 2 - 10 + scrollX}px`, top: `${seqRect.top + seqRect.height / 2 - 10 + scrollY}px` }
    ], {
        duration: 1000,
        easing: 'ease-in-out'
    }).onfinish = () => {
        messageToSequencer.remove();
        messageFromSequencer.animate([
            { left: `${seqRect.left + seqRect.width / 2 - 10 + scrollX}px`, top: `${seqRect.top + seqRect.height / 2 - 10 + scrollY}px` },
            { left: `${procRect.left + procRect.width / 2 - 10 + scrollX}px`, top: `${procRect.top + procRect.height / 2 - 10 + scrollY}px` }
        ], {
            duration: 1000,
            easing: 'ease-in-out'
        }).onfinish = () => {
            messageFromSequencer.remove();
        };
    };
}

function logEvent(message) {
    const logsContainer = document.getElementById("logs");
    const logItem = document.createElement("li");
    logItem.textContent = message;
    logsContainer.appendChild(logItem);
    logsContainer.scrollTop = logsContainer.scrollHeight;
}