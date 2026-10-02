import { useState } from "react";

import { sendChatMessage } from "../services/api";


function Chat() {
  const [message, setMessage] = useState("");
  const [conversation, setConversation] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");


  async function handleSubmit(event) {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage || isLoading) {
      return;
    }

    setError("");
    setIsLoading(true);

    try {
      const response = await sendChatMessage(
        trimmedMessage,
        conversation
      );

      setConversation((current) => [
        ...current,

        {
          role: "user",
          content: trimmedMessage,
        },

        {
          role: "assistant",
          content: response.answer,
        },
      ]);

      setMessage("");

    } catch (err) {
      setError(
        err.message ||
        "Unable to contact the AI service."
      );

    } finally {
      setIsLoading(false);
    }
  }


  return (
    <section className="chat-card">

      <div className="chat-header">
        <div>
          <h2>Ask CivicOps AI</h2>

          <p>
            Ask a general question about
            government services.
          </p>
        </div>
      </div>


      <div className="conversation">

        {conversation.length === 0 && (
          <div className="empty-chat">
            <p>
              Try asking:
            </p>

            <ul>
              <li>
                What services can CivicOps AI help with?
              </li>

              <li>
                Explain how a government service
                assistant should work.
              </li>

              <li>
                What information should I provide
                when requesting a service?
              </li>
            </ul>
          </div>
        )}


        {conversation.map((item, index) => (
          <div
            className={`message ${item.role}`}
            key={`${item.role}-${index}`}
          >
            <div className="message-role">
              {item.role === "user"
                ? "You"
                : "CivicOps AI"}
            </div>

            <div className="message-content">
              {item.content}
            </div>
          </div>
        ))}


        {isLoading && (
          <div className="message assistant">
            <div className="message-role">
              CivicOps AI
            </div>

            <div className="message-content">
              Thinking...
            </div>
          </div>
        )}

      </div>


      {error && (
        <div className="chat-error">
          {error}
        </div>
      )}


      <form
        className="chat-form"
        onSubmit={handleSubmit}
      >

        <textarea
          value={message}
          onChange={(event) =>
            setMessage(event.target.value)
          }
          placeholder="Ask CivicOps AI..."
          rows={3}
          disabled={isLoading}
        />

        <button
          type="submit"
          disabled={
            isLoading ||
            !message.trim()
          }
        >
          {isLoading
            ? "Thinking..."
            : "Send"}
        </button>

      </form>

    </section>
  );
}


export default Chat;