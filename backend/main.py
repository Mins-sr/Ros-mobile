#!/usr/bin/env python3
"""
FastAPI Backend with AI Agent
AIエージェントがユーザーの自然言語をROS2コマンドに変換
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
from typing import Dict, List
import os
from datetime import datetime

from ai_agent import AIAgent
from ros2_controller import ROS2Controller

app = FastAPI(title="ROS2 AI Web Agent API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# グローバルインスタンス
ai_agent = AIAgent(api_key=os.getenv("OPENAI_API_KEY", ""))
ros2_controller = ROS2Controller()

# WebSocket接続管理
active_connections: List[WebSocket] = []


class CommandRequest(BaseModel):
    message: str


class CommandResponse(BaseModel):
    success: bool
    message: str
    command: str = ""
    output: str = ""


@app.on_event("startup")
async def startup_event():
    print("🚀 ROS2 AI Web Agent Backend Started")
    print(f"📡 API Server: http://localhost:8000")
    print(f"📚 Docs: http://localhost:8000/docs")


@app.get("/")
async def root():
    return {
        "service": "ROS2 AI Web Agent",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ros2": ros2_controller.check_status(),
        "ai_agent": ai_agent.is_configured()
    }


@app.post("/command", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    """
    自然言語コマンドをAIエージェントで解釈してROS2コマンドを実行
    """
    try:
        # AIエージェントでコマンド解釈
        ros2_command = await ai_agent.interpret_command(request.message)

        # ROS2コマンド実行
        output = await ros2_controller.execute_command(ros2_command)

        return CommandResponse(
            success=True,
            message=f"実行完了: {request.message}",
            command=ros2_command,
            output=output
        )
    except Exception as e:
        return CommandResponse(
            success=False,
            message=f"エラー: {str(e)}",
            command="",
            output=""
        )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocketエンドポイント - リアルタイム通信
    """
    await websocket.accept()
    active_connections.append(websocket)

    try:
        # 接続通知
        await websocket.send_json({
            "type": "connection",
            "message": "WebSocket接続が確立されました",
            "timestamp": datetime.now().isoformat()
        })

        # メッセージ受信ループ
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # AIエージェントで解釈
            command = await ai_agent.interpret_command(message_data["message"])

            # コマンド送信
            await websocket.send_json({
                "type": "command_interpreted",
                "original": message_data["message"],
                "command": command,
                "timestamp": datetime.now().isoformat()
            })

            # ROS2コマンド実行
            output = await ros2_controller.execute_command(command)

            # 結果送信
            await websocket.send_json({
                "type": "command_result",
                "command": command,
                "output": output,
                "timestamp": datetime.now().isoformat()
            })

    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)


@app.get("/nodes/status")
async def get_nodes_status():
    """
    ROS2ノードの状態取得
    """
    return await ros2_controller.get_nodes_status()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
