const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const sendButton = document.getElementById("send-button");
const startSection = document.getElementById("chat-start");

form.addEventListener("submit", function (e) {
  e.preventDefault();
  const userMessage = input.value.trim();
  if (!userMessage) return;

  appendMessage("user", userMessage);
  input.value = "";
  sendButton.disabled = true;
  sendButton.textContent = "Đang gửi...";

  // Ẩn phần "bắt đầu" sau khi gửi tin nhắn đầu tiên
  if (startSection) startSection.style.display = "none";

  // Giả lập phản hồi AI
  setTimeout(() => {
    const aiReply = "Tôi đã tiếp nhận và xử lý yêu cầu của bạn.";
    typeText("ai", aiReply, () => {
      sendButton.disabled = false;
      sendButton.textContent = "Gửi";
    });
  }, 800);
});

function appendMessage(sender, text) {
  const messageEl = document.createElement("div");
  messageEl.className = `message ${sender}`;
  messageEl.textContent = text;
  chatBox.appendChild(messageEl);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function typeText(sender, text, callback) {
  const messageEl = document.createElement("div");
  messageEl.className = `message ${sender}`;
  chatBox.appendChild(messageEl);

  let i = 0;
  const speed = 25;
  function typing() {
    if (i < text.length) {
      messageEl.textContent += text.charAt(i);
      i++;
      chatBox.scrollTop = chatBox.scrollHeight;
      setTimeout(typing, speed);
    } else {
      if (callback) callback();
    }
  }
  typing();
}
