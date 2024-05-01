// Get chatbot elements
const chatbot = document.getElementById("chatbot");
const conversation = document.getElementById("conversation");
const inputForm = document.getElementById("input-form");
const inputField = document.getElementById("input-field");
reset();

// Add event listener to input form
inputForm.addEventListener("submit", async function (event) {
  // Prevent form submission
  event.preventDefault();

  // Get user input
  const input = inputField.value;

  // Clear input field
  inputField.value = "";
  const currentTime = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  // Add user input to conversation
  let message = document.createElement("div");
  message.classList.add("chatbot-message", "user-message");
  message.innerHTML = `<p class="chatbot-text" sentTime="${currentTime}">${input}</p>`;
  conversation.appendChild(message);
  message.scrollIntoView({ behavior: "smooth" });

  // Generate chatbot response
  const response = await generateResponse(input);

  // Add chatbot response to conversation
  message = document.createElement("div");
  message.classList.add("chatbot-message", "chatbot");
  message.innerHTML = `<p class="chatbot-text" sentTime="${currentTime}">${response}</p>`;
  conversation.appendChild(message);
  message.scrollIntoView({ behavior: "smooth" });
});

//Reset Function for page refresh
async function reset() {
  await fetch("http://127.0.0.1:5000/reset", { method: "POST" });
}

// Generate chatbot response function
async function generateResponse(input) {
  // Get chatbot response
  const response = await fetch("http://127.0.0.1:5000/send_message", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input }),
  });
  const data = await response.json();

  const botResponse = data["bot_response"];

  // Return chatbot response
  return botResponse;
}
