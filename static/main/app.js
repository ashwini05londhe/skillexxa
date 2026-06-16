// app.js
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

async function searchInstructors(url) {
    const q = document.getElementById('searchInput').value;
    const resp = await fetch(`${url}?q=${encodeURIComponent(q)}`);
    const json = await resp.json();
    const out = document.getElementById('searchResults');
    if (json.results.length === 0) {
        out.innerHTML = '<p class="text-muted">No instructors found</p>';
        return;
    }
    out.innerHTML = json.results.map(r => `
        <div class="card mb-2">
            <div class="card-body">
                <div class="d-flex align-items-center">
                    <img src="${r.photo_url || '/static/main/images/default-profile.png'}" alt="${r.name}" class="rounded-circle me-3" width="64" height="64">
                    <div>
                        <strong>${r.name || r.username}</strong><br>
                        <small class="text-muted">${r.domain}</small>
                    </div>
                    <div class="ms-auto">
                        <a class="btn btn-primary" href="/instructor/${r.id}/">View profile</a>
                        <a class="btn btn-secondary" href="/chat/${r.id}/">Chat</a>
                        <a class="btn btn-success" href="/video-call/${r.id}/">Video Call</a>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

function toggleEditProfile() {
    const form = document.getElementById('editProfileForm');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function togglePortfolioUpload() {
    const form = document.getElementById('portfolioUploadForm');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

async function uploadPortfolio(e) {
    e.preventDefault();
    const f = this.querySelector('input[type=file]').files[0];
    if (!f) {
        alert('Pick a file');
        return;
    }
    const fd = new FormData();
    fd.append('image', f);

    const csrfToken = getCookie('csrftoken');
    const resp = await fetch("/api/upload-portfolio/", {
        method: 'POST',
        body: fd,
        headers: { 'X-CSRFToken': csrfToken }
    });
    const json = await resp.json();
    if (json.ok) {
        alert('Portfolio item uploaded successfully!');
        location.reload();
    } else {
        alert('Upload failed. Please try again.');
    }
}

// Chatbot functionality
console.log('Initializing chatbot...');

const chatbotToggle = document.getElementById('chatbot-toggle');
const chatbotWindow = document.getElementById('chatbot-window');
const chatbotClose = document.getElementById('chatbot-close');
const chatbotInput = document.getElementById('chatbot-input');
const chatbotSend = document.getElementById('chatbot-send');
const chatbotMessages = document.getElementById('chatbot-messages');

console.log('Chatbot elements:', { chatbotToggle, chatbotWindow, chatbotClose, chatbotInput, chatbotSend, chatbotMessages });

if (!chatbotToggle || !chatbotWindow || !chatbotClose || !chatbotInput || !chatbotSend || !chatbotMessages) {
    console.error('Some chatbot elements not found!');
} else {
    console.log('All chatbot elements found successfully');

    // Toggle chatbot window
    chatbotToggle.addEventListener('click', function() {
        console.log('Chatbot toggle clicked');
        chatbotWindow.style.display = chatbotWindow.style.display === 'none' || chatbotWindow.style.display === '' ? 'flex' : 'none';
        console.log('Chatbot window display set to:', chatbotWindow.style.display);
    });

    // Close chatbot window
    chatbotClose.addEventListener('click', function() {
        console.log('Chatbot close clicked');
        chatbotWindow.style.display = 'none';
    });

    // Send message
    async function sendMessage() {
        const message = chatbotInput.value.trim();
        if (!message) return;

        console.log('Sending message:', message);

        // Add user message to chat
        addMessage(message, 'user');
        chatbotInput.value = '';

        // Send to API
        try {
            const csrfToken = getCookie('csrftoken');
            console.log('CSRF token:', csrfToken);
            const resp = await fetch('/api/chatbot/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ message: message })
            });
            console.log('API response status:', resp.status);
            const data = await resp.json();
            console.log('API response data:', data);
            addMessage(data.response, 'bot');
        } catch (error) {
            console.error('Error sending message:', error);
            addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        }
    }

    // Add message to chat
    function addMessage(text, type) {
        console.log('Adding message:', text, type);
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = text;
        chatbotMessages.appendChild(messageDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Send on button click
    chatbotSend.addEventListener('click', function() {
        console.log('Send button clicked');
        sendMessage();
    });

    // Send on Enter key
    chatbotInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            console.log('Enter key pressed');
            sendMessage();
        }
    });
}
