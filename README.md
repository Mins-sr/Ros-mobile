# ROS2 AI Web Agent

ROS2開発をWebアプリから操作できるAIエージェントシステム

## 概要

AIエージェントに自然言語で指示を出すと、ROS2コマンドとして実行してくれるWebアプリケーションです。

## 機能

- Webインターフェースからの操作
- AIエージェントによる自然言語コマンド解釈
- ROS2パブリッシャー/サブスクライバーノードの制御
- リアルタイム通信状態の監視

## システム構成

- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI + WebSocket
- **ROS2**: Humble (Python)
- **AI**: OpenAI API (GPT-4)

## セットアップ

### 必要要件

- Docker & Docker Compose
- OpenAI API Key

### 起動方法

1. 環境変数設定
```bash
cp .env.example .env
# .envファイルにOPENAI_API_KEYを設定
```

2. Dockerコンテナ起動
```bash
docker-compose up -d
```

3. アクセス
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

## 使い方

1. Webブラウザでフロントエンドにアクセス
2. チャット欄に自然言語で指示を入力
   - 例: "パブリッシャーを起動して"
   - 例: "サブスクライバーを開始"
   - 例: "通信状態を確認"
3. AIエージェントが解釈してROS2コマンドを実行

## 開発

### ローカル開発

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# Frontend
cd frontend
npm install
npm run dev

# ROS2 (別ターミナル)
source /opt/ros/humble/setup.bash
cd ros2_nodes
python publisher_node.py
python subscriber_node.py
```

## ライセンス

MIT
