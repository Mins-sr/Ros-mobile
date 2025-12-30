# クイックスタートガイド

## 最小構成での起動方法

### 1. 環境変数の設定

```bash
cp .env.example .env
```

`.env`ファイルを編集して、OpenAI API Keyを設定してください（オプション）:
```
OPENAI_API_KEY=sk-your-key-here
ROS_DOMAIN_ID=0
```

**注意**: OpenAI API Keyがない場合でも動作します。その場合は簡易的なルールベースでコマンドが解釈されます。

### 2. Dockerで起動（推奨）

```bash
# コンテナをビルド・起動
docker-compose up -d

# ログ確認
docker-compose logs -f
```

### 3. ローカルで起動（ROS2がインストール済みの場合）

#### Terminal 1: Backend起動
```bash
cd backend
pip install -r requirements.txt
python main.py
```

#### Terminal 2: Frontend起動
```bash
cd frontend
npm install
npm run dev
```

#### Terminal 3 & 4: ROS2ノード起動
```bash
# パブリッシャー
source /opt/ros/humble/setup.bash
cd ros2_nodes
python3 publisher_node.py

# サブスクライバー（別ターミナル）
source /opt/ros/humble/setup.bash
cd ros2_nodes
python3 subscriber_node.py
```

## 使い方

1. ブラウザで http://localhost:5173 にアクセス

2. チャット欄に自然言語で指示を入力:

   - **"パブリッシャーを起動して"** → パブリッシャーノードが起動
   - **"サブスクライバーを開始"** → サブスクライバーノードが起動
   - **"通信状態を確認"** → ノード一覧を表示
   - **"トピック一覧を見せて"** → アクティブなトピックを表示
   - **"chat_topicの内容を見せて"** → トピックのメッセージをエコー

3. 画面右上でノードのステータスがリアルタイムに確認できます

## トラブルシューティング

### ノードが起動しない
- ROS2がインストールされているか確認
- `source /opt/ros/humble/setup.bash` が実行されているか確認

### WebSocketに接続できない
- バックエンドが起動しているか確認（http://localhost:8000/health）
- CORS設定を確認

### Dockerコンテナが起動しない
- Dockerデーモンが起動しているか確認
- ポート8000, 5173が使用されていないか確認

## ROS2コマンド手動実行

```bash
# ノード一覧
ros2 node list

# トピック一覧
ros2 topic list

# トピックの内容表示
ros2 topic echo /chat_topic

# トピックの情報
ros2 topic info /chat_topic
```

## 停止方法

### Docker
```bash
docker-compose down
```

### ローカル
各ターミナルで `Ctrl+C` を押す
