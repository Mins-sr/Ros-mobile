# Render.com 5分デプロイガイド

ROS2 + rosbridgeをRender.comに無料デプロイする最速ガイド

## ⚡ 5分セットアップ

### 必要なもの
- GitHubアカウント
- Render.comアカウント（無料）

---

## ステップ1: Render.comアカウント作成（1分）

1. https://render.com にアクセス
2. "Get Started" をクリック
3. GitHubアカウントで連携サインアップ

---

## ステップ2: Blueprint からデプロイ（2分）

1. **Renderダッシュボードで "New" → "Blueprint"**

2. **GitHubリポジトリを接続**
   - "Connect a repository" をクリック
   - `Mins-sr/Ros-mobile` を選択（またはフォークしたリポジトリ）

3. **Blueprintファイルが自動検出される**
   - `render.rosbridge.yaml` が表示される
   - サービス名: `ros2-rosbridge-server`

4. **"Apply" をクリック**
   - デプロイ開始！
   - 進行状況が表示される

---

## ステップ3: デプロイ完了を待つ（2分）

初回デプロイは2-3分かかります：

```
Building...  (30秒)
  ↓
Deploying... (60秒)
  ↓
Live!        ✅
```

ログで以下が表示されればOK:
```
==> Listening on ws://0.0.0.0:9090
```

---

## ステップ4: URLを取得（30秒）

1. デプロイ完了後、サービスページを開く
2. URLが表示される（例: `ros2-rosbridge-server.onrender.com`）
3. WebSocket URL:
   ```
   wss://ros2-rosbridge-server.onrender.com:9090
   ```

---

## ステップ5: GitHub Pagesから接続（30秒）

1. https://mins-sr.github.io/Ros-mobile/rosbridge.html にアクセス

2. 接続URL欄に入力:
   ```
   wss://あなたのアプリ名.onrender.com:9090
   ```

3. 「接続」をクリック

4. ✅ 「接続中」と表示されればOK！

---

## 🎉 完成！

おめでとうございます！完全無料でROS2をクラウドデプロイできました。

## 📊 デプロイ後の確認

### ROS2が動作しているか確認

Renderのログを見る:
1. サービスページ → "Logs" タブ
2. 以下のようなログが表示されればOK:

```
[INFO] [launch]: All log files can be found below /root/.ros/log/...
[INFO] [rosbridge_websocket]: Rosbridge WebSocket server started on port 9090
```

### WebSocketに接続できるか確認

ブラウザのDevTools（F12）で:
```javascript
const ws = new WebSocket('wss://your-app.onrender.com:9090');
ws.onopen = () => console.log('Connected!');
```

---

## ⚙️ 設定のカスタマイズ

### 環境変数の追加

1. サービスページ → "Environment" タブ
2. "Add Environment Variable" をクリック
3. 変数を追加:
   ```
   ROS_DOMAIN_ID=0
   ```

### デプロイブランチの変更

1. サービスページ → "Settings" タブ
2. "Branch" セクション
3. ブランチを選択（例: `main`）

### 自動デプロイの設定

デフォルトで自動デプロイが有効:
- GitHubにpush → 自動で再デプロイ

無効にする場合:
1. Settings → "Build & Deploy"
2. "Auto-Deploy" をOFFに

---

## 💰 無料枠の制限

### Renderの無料プラン
- **750時間/月**（約31日分）
- **512MB RAM**
- **0.1 CPU**
- **自動スリープ**: 15分アイドルで停止

### 自動スリープの影響
- 15分間アクセスがないと自動停止
- 次回アクセス時に再起動（30秒程度）
- GitHub Pagesから接続すると自動で起動

### スリープ対策（オプション）

定期的にpingして起動状態を維持:

```yaml
# .github/workflows/keep-alive.yml
name: Keep Render Alive
on:
  schedule:
    - cron: '*/14 * * * *'  # 14分ごと
jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Render
        run: curl https://your-app.onrender.com/health
```

**注意**: 無料枠は750時間/月なので、常時起動は推奨しません

---

## 🔒 セキュリティ設定

### SSL証明書（自動）

Renderは自動でSSL証明書を発行:
- `wss://` (WebSocket Secure) が使用可能
- 追加設定不要

### カスタムドメイン（オプション）

独自ドメインを使用する場合:

1. Settings → "Custom Domains"
2. "Add Custom Domain" をクリック
3. ドメインを入力（例: `ros2.yourdomain.com`）
4. DNS設定を行う:
   ```
   CNAME: ros2.yourdomain.com → your-app.onrender.com
   ```

### 認証の追加（推奨）

rosbridgeに認証を追加:

```bash
# Dockerfile.rosbridge を編集
# 認証レイヤーを追加
```

---

## 🐛 トラブルシューティング

### デプロイが失敗する

**症状**: "Build failed" エラー

**解決策**:
1. Logsタブでエラー内容を確認
2. Dockerfileの構文チェック
3. リポジトリの権限確認

### WebSocketに接続できない

**症状**: "Connection refused"

**解決策**:
1. サービスが起動しているか確認（Logsタブ）
2. URLが正しいか確認（`wss://`）
3. ポート番号が正しいか確認（`:9090`）
4. スリープから復帰待ち（30秒待つ）

### メモリ不足エラー

**症状**: "Out of memory"

**解決策**:
1. 無料プランは512MBまで
2. 重いROS2ノードは動作しない可能性
3. 有料プラン（$7/月〜）にアップグレード

---

## 📈 有料プランへのアップグレード

### いつアップグレードすべきか

以下の場合は有料プランを検討:
- 自動スリープを無効にしたい
- より多くのRAMが必要（2GB〜）
- 常時稼働が必要
- 複数のサービスを運用

### プラン比較

| プラン | 価格 | RAM | スリープ |
|-------|------|-----|---------|
| Free | $0 | 512MB | あり（15分） |
| Starter | $7/月 | 512MB | なし |
| Standard | $25/月 | 2GB | なし |
| Pro | $85/月 | 4GB | なし |

---

## 🔄 更新とメンテナンス

### コードの更新

```bash
# ローカルで変更
git add .
git commit -m "Update rosbridge config"
git push

# Renderが自動で再デプロイ（5分程度）
```

### ログの確認

```bash
# リアルタイムログ
Logs タブ → "Live Logs"

# 過去のログ
Logs タブ → "All Logs"
```

### サービスの再起動

手動で再起動する場合:
1. サービスページ右上
2. "Manual Deploy" → "Clear build cache & deploy"

---

## 🚀 次のステップ

### ROS2ノードの追加

カスタムノードを追加する場合:

```python
# ros2_nodes/custom_node.py
# 独自のノードを作成
```

```dockerfile
# Dockerfile.rosbridge に追加
COPY ros2_nodes/ /workspace/ros2_nodes/
```

### Gazeboシミュレータの追加

```dockerfile
# Dockerfile.rosbridge
RUN apt-get install -y ros-humble-gazebo-ros-pkgs
```

**注意**: 無料枠のRAMでは厳しい（有料プラン推奨）

### 監視とアラート

Renderの監視機能:
- サービスページ → "Metrics"
- CPU、メモリ使用率を確認
- アラート設定可能

---

## 📚 参考リンク

- [Render.com ドキュメント](https://render.com/docs)
- [rosbridge GitHub](https://github.com/RobotWebTools/rosbridge_suite)
- [プロジェクトREADME](./README.md)

---

## ✅ チェックリスト

デプロイ完了後の確認:

- [ ] Render.comにサインアップ完了
- [ ] Blueprintからデプロイ成功
- [ ] サービスが "Live" 状態
- [ ] WebSocket URL取得
- [ ] GitHub Pagesから接続成功
- [ ] Publisher/Subscriber動作確認
- [ ] ログでROS2起動確認

すべてチェックできたら完成です！🎉
