<!-- AI Ring Expert Chatbot UI -->
<div id="chat-welcome-note" style="cursor: default;">
  How Can I Help You?
</div>

<div id="chatbot-icon" title="Ask Ring Expert">💬</div>

<!-- Modal Chatbot IFRAME -->
<div id="chatbot-modal">
  <iframe
    src="https://qnabot-1fyd.onrender.com"
    allow="camera; microphone"
    frameborder="0">
  </iframe>
</div>

<style>
  #chatbot-icon {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    background-color: #000;
    color: #fff;
    font-size: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
    cursor: pointer;
    z-index: 9999;
    animation: zoomIcon 2s infinite ease-in-out;
    transition: transform 0.2s ease-in-out;
  }

  @keyframes zoomIcon {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
  }

  #chatbot-icon:hover {
    transform: scale(1.15);
  }

  #chat-welcome-note {
    position: fixed;
    bottom: 90px;
    right: 26px;
    background: #000;
    color: #fff;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-family: 'Georgia', serif;
    font-weight: 400;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    z-index: 9999;
    max-width: 220px;
    white-space: nowrap;
    animation: fadeInOut 7s ease forwards;
  }

  @keyframes fadeInOut {
    0% { opacity: 0; transform: translateY(10px); }
    10%, 85% { opacity: 1; transform: translateY(0); }
    100% { opacity: 0; display: none; }
  }

  #chatbot-modal {
    display: none;
    position: fixed;
    bottom: 90px;
    right: 30px;
    width: 380px;
    height: 580px;
    background: white;
    border-radius: 14px;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.3);
    z-index: 10000;
    overflow: hidden;
  }

  #chatbot-modal iframe {
    width: 100%;
    height: 100%;
    border: none;
  }

  /* 🔍 MOBILE FULLSCREEN MODE */
  @media screen and (max-width: 480px) {
    #chatbot-modal {
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      width: 100vw;
      height: 100vh;
      border-radius: 0;
    }

    #chatbot-icon {
      width: 48px;
      height: 48px;
      font-size: 22px;
      bottom: 16px;
      right: 16px;
    }

    #chat-welcome-note {
      bottom: 70px;
      right: 16px;
      font-size: 12px;
      padding: 6px 12px;
      max-width: 180px;
    }
  }
</style>

<script>
  document.getElementById('chatbot-icon').addEventListener('click', function () {
    const modal = document.getElementById('chatbot-modal');
    modal.style.display = modal.style.display === 'block' ? 'none' : 'block';
  });

  window.addEventListener('click', function (e) {
    const modal = document.getElementById('chatbot-modal');
    const icon = document.getElementById('chatbot-icon');
    if (!modal.contains(e.target) && !icon.contains(e.target)) {
      modal.style.display = 'none';
    }
  });
</script>
