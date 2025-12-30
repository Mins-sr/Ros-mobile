# ROS2 AI Web Agent

ROS2開発をWebアプリから操作できるAIエージェントシステム

## 🚀 クイックスタート - GitHub Pagesでデモを試す

**すぐに試せるライブデモ:**
👉 **[https://mins-sr.github.io/Ros-mobile/](https://mins-sr.github.io/Ros-mobile/)**

ブラウザ内でROS2のパブリッシャー/サブスクライバー通信をシミュレートできます。

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

## デプロイオプション

### オプション1: GitHub Pages（最も簡単）
- ✅ すぐに試せる
- ✅ 無料
- ⚠️ ブラウザ内シミュレーション（実際のROS2は動かない）

### オプション2: ローカル環境（実際のROS2）
- ✅ 実際のROS2が動作
- ⚠️ ROS2環境が必要

### オプション3: クラウドデプロイ（本番運用）
- ✅ 実際のROS2が動作
- ✅ インターネットからアクセス可能
- 詳細: [DEPLOYMENT.md](./DEPLOYMENT.md)

## セットアップ

### 必要要件

- Docker & Docker Compose（推奨）
- または ROS2 Humble + Python 3.10+ + Node.js 20+
- OpenAI API Key（オプション）

### ローカルで起動（Docker）

1. 環境変数設定（オプション）
```bash
cp .env.example .env
# .envファイルにOPENAI_API_KEYを設定（なくても動作します）
```

2. Dockerコンテナ起動
```bash
docker-compose up -d
```

3. アクセス
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

### クイックセットアップスクリプト

```bash
./setup.sh
```

詳細な起動方法は [QUICKSTART.md](./QUICKSTART.md) を参照

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

## プロジェクト構成

```
Ros-mobile/
├── frontend/              # React + TypeScript フロントエンド
│   ├── src/
│   │   ├── App.tsx           # フルスタック版
│   │   └── App.standalone.tsx # GitHub Pages版（スタンドアロン）
│   └── package.json
├── backend/               # FastAPI バックエンド
│   ├── main.py              # APIサーバー
│   ├── ai_agent.py          # AIエージェント
│   └── ros2_controller.py   # ROS2制御
├── ros2_nodes/            # ROS2ノード
│   ├── publisher_node.py    # パブリッシャー
│   └── subscriber_node.py   # サブスクライバー
├── .github/workflows/     # GitHub Actionsデプロイ設定
├── docker-compose.yml     # Docker構成
└── README.md
```

## デプロイ

詳細なデプロイ方法は [DEPLOYMENT.md](./DEPLOYMENT.md) を参照してください。

## ライセンス

MIT
