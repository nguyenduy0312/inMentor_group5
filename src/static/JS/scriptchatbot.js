const apiKey = "app-b78TsFpOzdbiHxEg5rK5TwSy";
const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const sendButton = document.getElementById("send-button");
const startSection = document.getElementById("chat-start");

form.addEventListener("submit", async function (e) {
  e.preventDefault();
  const userMessage = input.value.trim();
  if (!userMessage) return;

  appendMessage("user", userMessage);
  input.value = "";
  toggleSendButton(true);

  if (startSection) startSection.style.display = "none";

  const aiReply = await sendMessageToDify(userMessage);
  typeText("ai", aiReply, () => toggleSendButton(false));
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

function toggleSendButton(disabled) {
  sendButton.disabled = disabled;
  sendButton.textContent = disabled ? "Đang gửi..." : "Gửi";
}

async function sendMessageToDify(messageText) {
  try {
    const response = await fetch("https://api.dify.ai/v1/chat-messages", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: messageText,
        inputs: { "abc": "backend java" }
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.answer || data.choices?.[0]?.message?.content || "Không có phản hồi từ AI.";
  } catch (error) {
    console.error("Lỗi gửi tin nhắn đến Dify:", error);
    return "Đã xảy ra lỗi khi kết nối với AI.";
  }
}
