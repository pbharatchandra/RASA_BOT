// --- CONFIGURATION ---
const RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook';
const SENDER_ID = 'user_' + Math.random().toString(36).substring(2, 9); // Unique ID for the session
const CHAT_WINDOW_ID = 'chat-window'; // Target the chat window div
let chatInitialized = false; // To track if the chat layout has been created

// --- DOM ELEMENT CREATION ---

function createChatLayout() {
    const chatWindow = document.getElementById(CHAT_WINDOW_ID);
    if (!chatWindow) return;

    // IMPORTANT: Add a dedicated CLOSE button inside the header
    chatWindow.innerHTML = `
        <div class="chat-header">
            NISTU Bot
            <button id="chat-close-btn" style="float: right; background: none; border: none; color: white; font-size: 1.2em; cursor: pointer; margin-right: 5px;">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="chat-messages" id="chat-messages"></div>
        <div class="chat-input-area">
            <input type="text" id="user-input" placeholder="Type a message..." autocomplete="off">
            <button id="send-btn"><i class="fas fa-paper-plane"></i></button>
        </div>
    `;

    // Attach event listeners
    document.getElementById('send-btn').addEventListener('click', handleUserInput);
    document.getElementById('user-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleUserInput();
        }
    });

    // NEW: Attach the close function to the 'X' button inside the chat window
    document.getElementById('chat-close-btn').addEventListener('click', closeChatWindow);
}

function scrollToBottom() {
    const messagesEl = document.getElementById('chat-messages');
    if (messagesEl) {
        messagesEl.scrollTop = messagesEl.scrollHeight;
    }
}

function renderMessage(message, isUser) {
    const messagesEl = document.getElementById('chat-messages');
    if (!messagesEl) return;
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = message;
    messagesEl.appendChild(messageDiv);
    scrollToBottom();
}

function renderBotResponse(response) {
    const messagesEl = document.getElementById('chat-messages');
    if (!messagesEl) return;
    const responseDiv = document.createElement('div');
    responseDiv.className = 'message bot-message';

    // 1. Text Message
    if (response.text) {
        responseDiv.innerHTML += `<p>${response.text}</p>`;
    }

    // 2. Buttons/Quick Replies
    if (response.buttons && response.buttons.length > 0) {
        const buttonsContainer = document.createElement('div');
        buttonsContainer.className = 'button-container';
        response.buttons.forEach(button => {
            const btn = document.createElement('button');
            btn.textContent = button.title;
            btn.className = 'quick-reply-btn';
            btn.addEventListener('click', () => {
                // Send the payload/title back to Rasa
                sendMessage(button.payload || button.title);
                // Disable all buttons in this response after one is clicked
                document.querySelectorAll('.quick-reply-btn').forEach(b => b.disabled = true);
            });
            buttonsContainer.appendChild(btn);
        });
        responseDiv.appendChild(buttonsContainer);
    }
    
    // Add more handlers here for image, attachment, custom, etc.
    // e.g., if (response.image) { responseDiv.innerHTML += `<img src="${response.image}" alt="Bot Image">`; }

    messagesEl.appendChild(responseDiv);
    scrollToBottom();
}

// --- API & COMMUNICATION ---

function showTypingIndicator() {
    const messagesEl = document.getElementById('chat-messages');
    if (!messagesEl) return;
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.id = 'typing-indicator';
    indicator.textContent = 'Assistant is typing...';
    messagesEl.appendChild(indicator);
    scrollToBottom();
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

async function sendMessage(message) {
    if (!message.trim()) return;

    // 1. Render user message immediately
    renderMessage(message, true);

    // Clear input
    const inputEl = document.getElementById('user-input');
    if (inputEl) inputEl.value = '';

    // 2. Show typing indicator
    showTypingIndicator();

    try {
        const response = await fetch(RASA_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                sender: SENDER_ID,
                message: message,
            }),
        });

        const data = await response.json();
        
        // 3. Remove typing indicator
        removeTypingIndicator();

        // 4. Render bot responses
        if (data && data.length > 0) {
            data.forEach(response => renderBotResponse(response));
        } else {
            renderMessage("Sorry, I didn't get a response from the bot.", false);
        }

    } catch (error) {
        console.error('Error connecting to Rasa:', error);
        removeTypingIndicator();
        renderMessage("Connection Error: Could not reach the Rasa server.", false);
    }
}

// --- MAIN HANDLER ---

function handleUserInput() {
    const inputEl = document.getElementById('user-input');
    const message = inputEl.value;
    sendMessage(message);
}

// --- WIDGET OPEN/CLOSE FUNCTIONS (NEW LOGIC) ---

function openChatWindow(chatWindow, chatToggleButton) {
    // 1. HIDE THE MESSAGE ICON
    chatToggleButton.style.display = 'none';

    // 2. SHOW the chat window
    chatWindow.style.display = 'flex'; // Make it visible for animation
    setTimeout(() => { // Allow reflow before adding 'open' class for transition
        chatWindow.classList.remove('hidden');
        chatWindow.classList.add('open');
    }, 10);

    // 3. Initialize chat layout and send /greet only once
    if (!chatInitialized) {
        createChatLayout();
        // sendMessage('/greet'); // Send a welcome message
        chatInitialized = true;
    }

    // 4. Focus on input after opening
    setTimeout(() => {
        const userInput = document.getElementById('user-input');
        if (userInput) userInput.focus();
    }, 300); // Give time for animation
}

function closeChatWindow() {
    const chatWindow = document.getElementById(CHAT_WINDOW_ID);
    const chatToggleButton = document.getElementById('chat-toggle-button');

    // 1. HIDE the chat window
    if (chatWindow && chatToggleButton) {
        chatWindow.classList.remove('open');
        // Use a timeout to fully hide it after transition
        setTimeout(() => {
            chatWindow.classList.add('hidden');
            chatWindow.style.display = 'none'; // Completely hide after animation

            // 2. SHOW THE MESSAGE ICON
            chatToggleButton.style.display = 'flex'; // Or 'block', depending on your CSS display property for the button
        }, 300); // Should match CSS transition duration
    }
}


// --- INITIALIZATION ---

document.addEventListener('DOMContentLoaded', () => {
    const chatToggleButton = document.getElementById('chat-toggle-button');
    const chatWindow = document.getElementById(CHAT_WINDOW_ID);

    if (chatToggleButton && chatWindow) {
        // Ensure the window is initially hidden
        chatWindow.style.display = 'none'; 
        chatWindow.classList.add('hidden');

        chatToggleButton.addEventListener('click', () => {
            // Only open if currently hidden
            if (chatWindow.classList.contains('hidden')) {
                openChatWindow(chatWindow, chatToggleButton);
            }
        });
        
        // Note: The close button event is attached inside createChatLayout()
    }
});