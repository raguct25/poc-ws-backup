import React, { useEffect, useState } from "react";

export default function Chat() {
  const [socket, setSocket] = useState(null);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/chat");

    ws.onopen = () => {
      console.log("Connected to WebSocket");
    };

    ws.onmessage = (event) => {
      console.log("From Python:", event.data);
      setMessages(prev => [...prev, event.data]); // show server messages
    };

    setSocket(ws);

    return () => ws.close();
  }, []);

  const sendMessage = () => {
    console.log("message", message);
        console.log("messages", messages);

    
    if (socket) {
      socket.send(message);       // send message to Python
      setMessage("");
    }
  };

  return (
    <div style={{ margin: "20px" }}>
      <h2>WebSocket Chat</h2>

      <div
        style={{
          height: "200px",
          border: "1px solid gray",
          overflowY: "auto",
          marginBottom: "10px",
          padding: "10px",
        }}
      >
        {messages.map((msg, index) => (
          <div key={index}>{msg}</div>
        ))}
      </div>

      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type something..."
      />

      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
