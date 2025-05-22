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

  // Lấy giá trị lĩnh vực nghề nghiệp từ select
  const careerValue = careerSelect.value;

  appendMessage("user", userMessage);
  input.value = "";
  toggleSendButton(true);

  if (startSection) startSection.style.display = "none";

  // Truyền careerValue vào hàm gửi
  const aiReply = await sendMessageToDify(userMessage, careerValue);
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

const careerSelect = document.getElementById("career-select");

careerValue = careerSelect.value;

let conversationId = ""; // Biến toàn cục lưu conversation_id


async function sendMessageToDify(messageText, careerValue ) {
  try {
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messageText,
        conversationId,
        inputs: { "abc": careerValue }  
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    if (data.conversation_id) {
      conversationId = data.conversation_id;
    }
    return data.answer || data.choices?.[0]?.message?.content || "Không có phản hồi từ AI.";
  } catch (error) {
    console.error("Lỗi gửi tin nhắn đến service:", error);
    return "Đã xảy ra lỗi khi kết nối với service.";
  }
}