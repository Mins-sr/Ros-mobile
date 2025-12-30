# GitHub Pages + rosbridge で実際のROS2を動かす

このガイドでは、GitHub Pagesにホストされたフロントエンドから、実際のROS2環境を制御する方法を説明します。

## 🎯 アーキテクチャ

```
┌─────────────────────────────┐
│  GitHub Pages               │  ← 完全無料
│  (静的サイト)               │
│  - HTML + JavaScript        │
│  - roslibjs                 │
└──────────┬──────────────────┘
           │
           │ WebSocket (ws:// or wss://)
           │
           ↓
┌─────────────────────────────┐
│  ROS2 環境                  │  ← ローカルまたはクラウド
│  - rosbridge_server         │
│  - Publisher Node           │
│  - Subscriber Node          │
│  - その他のROS2ノード       │
└─────────────────────────────┘
```

## 📋 必要なもの

1. **GitHub Pages**: フロントエンド（無料）
2. **ROS2環境**: 以下のいずれか
   - ローカルPC（開発用）
   - クラウドサーバー（本番用）
   - Raspberry Pi（エッジデバイス）

## 🚀 セットアップ手順

### ステップ1: GitHub Pagesのデプロイ

既にデプロイ済みです：
- URL: `https://mins-sr.github.io/Ros-mobile/rosbridge.html`

### ステップ2: ROS2環境のセットアップ

#### オプションA: ローカル環境（推奨・開発用）

1. **rosbridgeのインストール**
```bash
# ROS2 Humbleの場合
sudo apt update
sudo apt install ros-humble-rosbridge-suite
```

2. **rosbridgeサーバーの起動**
```bash
source /opt/ros/humble/setup.bash
ros2 launch rosbridge_server rosbridge_websocket_launch.xml
```

デフォルトで `ws://localhost:9090` で起動します。

3. **GitHub Pagesにアクセス**
- ブラウザで `https://mins-sr.github.io/Ros-mobile/rosbridge.html` を開く
- 接続URL: `ws://localhost:9090`
- 「接続」ボタンをクリック

#### オプションB: Dockerで起動（最も簡単）

```bash
# リポジトリのクローン
git clone https://github.com/Mins-sr/Ros-mobile.git
cd Ros-mobile

# rosbridge + ROS2をDockerで起動
docker-compose -f docker-compose.rosbridge.yml up

# GitHub Pagesから接続
# URL: ws://localhost:9090
```

#### オプションC: クラウドサーバー（本番運用）

**Render.comを使用する場合:**

1. **render.rosbridge.yaml を使用**
```bash
# Render.comにログイン
# "New" → "Blueprint" を選択
# このリポジトリを接続
```

2. **環境変数設定**
- `ROS_DOMAIN_ID`: 0

3. **公開URL取得**
- Renderが `https://your-app.onrender.com` のようなURLを発行
- WebSocketは `wss://your-app.onrender.com:9090`

4. **GitHub Pagesから接続**
- 接続URL: `wss://your-app.onrender.com:9090`

**AWS EC2 / GCP / Azure を使用する場合:**

```bash
# サーバーにSSH接続
ssh user@your-server.com

# ROS2 + rosbridgeインストール
sudo apt update
sudo apt install ros-humble-rosbridge-suite

# rosbridgeサーバー起動（バックグラウンド）
source /opt/ros/humble/setup.bash
nohup ros2 launch rosbridge_server rosbridge_websocket_launch.xml &

# ファイアウォール設定（ポート9090を開放）
sudo ufw allow 9090/tcp

# SSL証明書設定（推奨）
# Let's Encrypt等でwss://接続を有効化
```

## 🎮 使い方

### 基本操作

1. **rosbridgeに接続**
   - GitHub Pages (`https://mins-sr.github.io/Ros-mobile/rosbridge.html`) にアクセス
   - 接続URLを入力（例: `ws://localhost:9090`）
   - 「接続」ボタンをクリック

2. **Publisherの起動**
   - "Publisher Node" セクションで「起動」ボタンをクリック
   - 2秒ごとに `/chatter` トピックにメッセージを送信

3. **Subscriberの起動**
   - "Subscriber Node" セクションで「起動」ボタンをクリック
   - `/chatter` トピックのメッセージを受信・表示

4. **ROS2側で確認**
```bash
# トピック一覧
ros2 topic list

# メッセージ確認
ros2 topic echo /chatter
```

### 独自のノードを追加

GitHub Pagesから任意のROS2ノードを制御できます：

```javascript
// カスタムトピックへのパブリッシュ
const customTopic = new ROSLIB.Topic({
  ros: ros,
  name: '/my_custom_topic',
  messageType: 'geometry_msgs/Twist'
});

const twistMsg = new ROSLIB.Message({
  linear: { x: 1.0, y: 0.0, z: 0.0 },
  angular: { x: 0.0, y: 0.0, z: 0.5 }
});

customTopic.publish(twistMsg);
```

## 🔒 セキュリティ考慮事項

### 本番環境での推奨事項

1. **SSL/TLS暗号化**
   - `wss://` (WebSocket Secure) を使用
   - Let's Encryptで無料SSL証明書を取得

2. **認証の追加**
   - rosbridgeに認証レイヤーを追加
   - Nginx等でBasic認証を設定

3. **ファイアウォール設定**
   - 必要なIPアドレスのみ許可
   - VPNの使用を検討

4. **CORS設定**
```xml
<!-- rosbridge_websocket_launch.xml -->
<arg name="authenticate" default="true"/>
<arg name="ssl" default="true"/>
```

## 📊 トラブルシューティング

### 接続できない

**症状**: "接続エラー" と表示される

**解決策**:
1. rosbridgeサーバーが起動しているか確認
```bash
ros2 node list | grep rosbridge
```

2. ポート9090が開いているか確認
```bash
netstat -an | grep 9090
```

3. ファイアウォール設定を確認

### メッセージが届かない

**症状**: Publisherは動いているが、Subscriberで受信できない

**解決策**:
1. トピック名が一致しているか確認
2. メッセージ型が正しいか確認
3. ROS2側でトピックを確認
```bash
ros2 topic echo /chatter
```

### Mixed Content エラー

**症状**: `https://` のGitHub Pagesから `ws://` に接続できない

**解決策**:
- rosbridgeサーバーをSSL対応させて `wss://` を使用
- または、ローカルテスト時は `http://` でアクセス

## 🎯 ユースケース

### 1. リモートロボット制御
```
GitHub Pages (UI) → rosbridge → ROS2 → ロボット制御
```

### 2. センサーデータ可視化
```
センサー → ROS2 → rosbridge → GitHub Pages (グラフ表示)
```

### 3. 複数ユーザーでのモニタリング
```
User1 (GitHub Pages) ↘
User2 (GitHub Pages) → rosbridge → ROS2システム
User3 (GitHub Pages) ↗
```

## 🔧 カスタマイズ

### ポート変更

```bash
# カスタムポートで起動
ros2 launch rosbridge_server rosbridge_websocket_launch.xml port:=8080
```

### SSL有効化

```bash
ros2 launch rosbridge_server rosbridge_websocket_launch.xml \
  port:=9090 \
  ssl:=true \
  certfile:=/path/to/cert.pem \
  keyfile:=/path/to/key.pem
```

## 📚 参考リンク

- [rosbridge_suite ドキュメント](https://github.com/RobotWebTools/rosbridge_suite)
- [roslibjs API](https://robotwebtools.github.io/roslibjs/current/)
- [ROS2 公式ドキュメント](https://docs.ros.org/en/humble/)

## 💡 次のステップ

1. カスタムメッセージ型の追加
2. ロボットシミュレータ（Gazebo）との連携
3. カメラ映像のストリーミング
4. 3D可視化（ros3djs）の追加
5. モバイルアプリ化（PWA）
