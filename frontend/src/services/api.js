const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";


async function handleResponse(response) {
  if (!response.ok) {
    let message = "The API request failed.";

    try {
      const data = await response.json();

      if (data.detail) {
        message = data.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(message);
  }

  return response.json();
}


export async function getHealth() {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/health`
  );

  return handleResponse(response);
}


export async function sendChatMessage(
  message,
  conversation = []
) {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/chat`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        message,
        conversation,
      }),
    }
  );

  return handleResponse(response);
}