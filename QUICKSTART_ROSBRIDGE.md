# 5分でできる！GitHub Pages + ROS2 クイックスタート

GitHub Pagesから実際のROS2を制御する最速セットアップガイド

## ⚡ 最速セットアップ（5分）

### ステップ1: GitHub Pagesにアクセス（1分）

ブラウザで開く:
```
https://mins-sr.github.io/Ros-mobile/rosbridge.html
```

### ステップ2: ROS2 + rosbridgeを起動（3分）

**Dockerを使う場合（最も簡単）:**

```bash
# 1. リポジトリをクローン
git clone https://github.com/Mins-sr/Ros-mobile.git
cd Ros-mobile

# 2. rosbridgeサーバーを起動
docker-compose -f docker-compose.rosbridge.yml up

# これだけ！ws://localhost:9090 で待機開始
```

**ROS2が既にインストール済みの場合:**

```bash
# 1. rosbridgeパッケージをインストール
sudo apt install ros-humble-rosbridge-suite

# 2. 起動
source /opt/ros/humble/setup.bash
ros2 launch rosbridge_server rosbridge_websocket_launch.xml
```

### ステップ3: 接続（1分）

1. GitHub Pagesに戻る
2. 接続URL欄に入力: `ws://localhost:9090`
3. 「接続」ボタンをクリック
4. ✅ 「接続中」と表示されればOK！

### ステップ4: 動作確認

1. **Publisherを起動**
   - "Publisher Node" の「起動」ボタンをクリック
   - ログに緑色でメッセージが表示される

2. **Subscriberを起動**
   - "Subscriber Node" の「起動」ボタンをクリック
   - 受信メッセージが表示される

3. **ROS2コマンドで確認**
```bash
# 別ターミナルで
ros2 topic list
# /chatter が表示される

ros2 topic echo /chatter
# GitHub Pagesからのメッセージが表示される！
```

## 🎉 完成！

おめでとうございます！GitHub Pagesから実際のROS2を制御できました。

## 📊 動作確認チェックリスト

- [ ] GitHub Pagesに接続できた
- [ ] rosbridgeサーバーが起動している
- [ ] WebSocket接続が成功（緑色の「接続中」表示）
- [ ] Publisherからメッセージを送信できた
- [ ] Subscriberでメッセージを受信できた
- [ ] `ros2 topic echo /chatter` でメッセージを確認できた

## 🔧 トラブルシューティング

### 「接続エラー」と表示される

**原因**: rosbridgeサーバーが起動していない

**解決策**:
```bash
# サーバーが起動しているか確認
docker ps
# または
ps aux | grep rosbridge
```

### メッセージが表示されない

**原因**: トピック名が違う可能性

**解決策**:
```bash
# トピック一覧を確認
ros2 topic list

# トピックの詳細確認
ros2 topic info /chatter
```

### ポート9090が使用中

**原因**: 他のプログラムがポート9090を使用

**解決策**:
```bash
# 別のポートで起動
ros2 launch rosbridge_server rosbridge_websocket_launch.xml port:=9091

# GitHub Pagesの接続URLも変更
# ws://localhost:9091
```

## 🚀 次のステップ

### 1. カスタムトピックを追加

rosbridge.htmlを編集して独自のトピックを追加できます。

### 2. ロボットシミュレータと連携

```bash
# Gazeboシミュレータ起動
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# GitHub Pagesから制御可能に！
```

### 3. クラウドデプロイ

ローカルPCだけでなく、クラウドサーバーにデプロイすれば、
どこからでもROS2を制御できます。

詳細: [ROSBRIDGE_SETUP.md](./ROSBRIDGE_SETUP.md)

## 💡 使用例

### ロボットを動かす

```javascript
// rosbridge.html内のJavaScriptを編集
const cmdVel = new ROSLIB.Topic({
  ros: ros,
  name: '/cmd_vel',
  messageType: 'geometry_msgs/Twist'
});

const twist = new ROSLIB.Message({
  linear: { x: 0.5, y: 0, z: 0 },
  angular: { x: 0, y: 0, z: 0.5 }
});

cmdVel.publish(twist);
// ロボットが前進＋回転！
```

### センサーデータを可視化

```javascript
// レーザースキャンデータを購読
const laserScan = new ROSLIB.Topic({
  ros: ros,
  name: '/scan',
  messageType: 'sensor_msgs/LaserScan'
});

laserScan.subscribe((message) => {
  console.log('距離データ:', message.ranges);
  // グラフ描画等
});
```

## 📚 参考資料

- [完全セットアップガイド](./ROSBRIDGE_SETUP.md)
- [roslibjs ドキュメント](https://robotwebtools.github.io/roslibjs/)
- [rosbridge プロトコル](https://github.com/RobotWebTools/rosbridge_suite/blob/ros2/ROSBRIDGE_PROTOCOL.md)

## ❓ よくある質問

**Q: GitHub Pagesは無料ですか？**
A: はい、完全無料です。

**Q: インターネット経由で制御できますか？**
A: はい。rosbridgeサーバーを公開サーバーにデプロイすればOKです。

**Q: セキュリティは大丈夫？**
A: 本番環境では必ずSSL (wss://) と認証を設定してください。

**Q: スマホから操作できますか？**
A: はい、スマホのブラウザからも操作可能です。

**Q: 複数人で同時に操作できますか？**
A: はい、複数のブラウザから同じrosbridgeサーバーに接続できます。

---

🎊 Happy ROS2 Hacking!
