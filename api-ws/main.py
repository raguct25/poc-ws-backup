# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # @app.websocket("/ws/chat")
# # async def websocket_endpoint(websocket: WebSocket):
# #     await websocket.accept()
# #     try:
# #         while True:
# #             # Receive from React
# #             data = await websocket.receive_text()
# #             print("From React:", data)

# #             # Send response to React
# #             response = f"Server received: {data}"
# #             await websocket.send_text(response)

# #     except WebSocketDisconnect:
# #         print("Client disconnected")


# # from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# # app = FastAPI()

# @app.websocket("/ws/chat")
# async def chat_socket(websocket: WebSocket):
#     await websocket.accept()

#     try:
#         while True:
#             # Receive message from React
#             msg = await websocket.receive_text()
#             print("Received from React:", msg)

#             # Reply BACK to React
#             reply = f"Python says: I received -> {msg}"
#             # await websocket.send_text(reply)
#             await websocket.send_text("PYTHON RESPONSE")

#     except WebSocketDisconnect:
#         print("React disconnected")



import asyncio
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()

# Background task: send terminal input to React
async def terminal_input_sender(websocket: WebSocket):
    loop = asyncio.get_event_loop()
    while True:
        # Read input from terminal (non-blocking)
        msg = await loop.run_in_executor(None, sys.stdin.readline)
        msg = msg.strip()

        if msg:
            await websocket.send_text(f"Terminal: {msg}")

@app.websocket("/ws/chat")
async def chat_socket(websocket: WebSocket):
    await websocket.accept()

    # Start reading terminal input
    asyncio.create_task(terminal_input_sender(websocket))

    try:
        while True:
            # Read message from React
            msg = await websocket.receive_text()
            print("React:", msg)

            # Reply to React
            await websocket.send_text(f"Python received: {msg}")

    except WebSocketDisconnect:
        print("React disconnected")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
