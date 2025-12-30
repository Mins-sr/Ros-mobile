# Railway.app デプロイガイド

ROS2 + rosbridgeをRailway.appに無料デプロイ（高スペック）

## ⚡ 特徴

- 🚀 **8GB RAM**（無料枠でも！）
- 💰 **$5分の使用量/月**
- ⏰ **自動スリープなし**（常時起動可）
- 🐳 **Docker完全サポート**

---

## 📋 前提条件

- GitHubアカウント
- Railway.appアカウント（無料）
- クレジットカード（$5の無料枠使用後に必要）

---

## ステップ1: Railway.appアカウント作成（2分）

1. https://railway.app にアクセス
2. "Start a New Project" をクリック
3. GitHubアカウントで連携サインアップ
4. 無料プラン（Developer Plan）を選択
   - $5分のクレジット/月

---

## ステップ2: プロジェクト作成（3分）

### 方法A: GitHubから直接デプロイ（推奨）

1. **"New Project" をクリック**

2. **"Deploy from GitHub repo" を選択**

3. **リポジトリを選択**
   - `Mins-sr/Ros-mobile` を選択
   - または自分のフォークを選択

4. **サービス設定**
   - Root Directory: `/`
   - Dockerfile: `Dockerfile.rosbridge`

5. **環境変数を設定**
   - `ROS_DOMAIN_ID` = `0`

6. **"Deploy" をクリック**

### 方法B: Railway CLI（上級者向け）

```bash
# Railway CLIインストール
npm i -g @railway/cli

# ログイン
railway login

# プロジェクト初期化
cd Ros-mobile
railway init

# デプロイ
railway up

# 環境変数設定
railway variables set ROS_DOMAIN_ID=0
```

---

## ステップ3: ポート設定（1分）

1. **プロジェクトページを開く**

2. **Settings タブ**

3. **Networking セクション**
   - Public Networking を有効化
   - Port: `9090` を追加

4. **Generate Domain** をクリック
   - 公開URLが発行される
   - 例: `ros2-rosbridge.up.railway.app`

---

## ステップ4: デプロイ確認（2分）

### ログ確認

1. **Deployments タブ**
2. 最新のデプロイをクリック
3. ログで以下を確認:

```
[INFO] [rosbridge_websocket]: Rosbridge WebSocket server started on port 9090
```

### WebSocket URLを取得

```
wss://ros2-rosbridge.up.railway.app:9090
```

---

## ステップ5: GitHub Pagesから接続

1. https://mins-sr.github.io/Ros-mobile/rosbridge.html にアクセス

2. 接続URL:
   ```
   wss://your-app.up.railway.app:9090
   ```

3. 「接続」→ ✅ 成功！

---

## 💰 料金と使用量管理

### 無料枠の詳細

- **$5分のクレジット/月**
- 使用量計算:
  - 実行時間: $0.000463/分
  - メモリ: 追加料金なし（8GBまで無料）
  - ネットワーク: 100GB/月まで無料

### 使用量の確認

1. **プロジェクトページ → Usage タブ**
2. リアルタイムで確認可能:
   - 今月の使用量
   - 残りクレジット
   - 予測コスト

### 計算例

常時起動（30日）の場合:
```
30日 × 24時間 × 60分 = 43,200分
43,200分 × $0.000463 = 約$20/月

→ 無料枠$5超過するため、約$15/月の課金
```

**推奨**: 使わない時は一時停止

---

## ⚙️ カスタマイズ設定

### 環境変数の追加

```bash
# Railway CLI
railway variables set CUSTOM_VAR=value

# または Web UIで
Settings → Variables → Add Variable
```

### カスタムドメイン

1. Settings → Domains
2. "Custom Domain" を追加
3. DNS設定:
   ```
   CNAME: ros2.yourdomain.com → your-app.up.railway.app
   ```

### スケーリング設定

```bash
# リソース制限（オプション）
Settings → Resources
- vCPU: 最大8
- RAM: 最大8GB
```

---

## 🔄 CI/CD（自動デプロイ）

### 自動デプロイ設定

デフォルトで有効:
- GitHubにpush → 自動デプロイ
- 特定のブランチのみデプロイ可能

### ブランチ指定

```bash
# mainブランチのみデプロイ
Settings → Triggers → Branch
→ "main" を選択
```

### Webhook

外部からデプロイをトリガー:
```bash
Settings → Webhooks
→ Webhook URL取得

# curlでトリガー
curl -X POST https://railway.app/webhook/...
```

---

## 📊 監視とアラート

### メトリクス確認

1. **Metrics タブ**
   - CPU使用率
   - メモリ使用率
   - ネットワーク帯域

2. **リアルタイムログ**
   - Deployments → View Logs

### アラート設定

```bash
# Slackと連携
Settings → Integrations → Slack
```

---

## 🛑 コスト最適化

### 一時停止機能

使わない時は一時停止:
```bash
# Railway CLI
railway down

# または Web UI
Settings → Service → Pause
```

### スケジュール起動（GitHub Actions）

```yaml
# .github/workflows/railway-control.yml
name: Railway Control
on:
  schedule:
    - cron: '0 9 * * *'  # 毎日9時に起動
    - cron: '0 18 * * *' # 毎日18時に停止

jobs:
  start:
    runs-on: ubuntu-latest
    steps:
      - name: Start Railway Service
        run: |
          # Railway APIで起動
```

---

## 🐛 トラブルシューティング

### ポート9090にアクセスできない

**解決策**:
```bash
# Settings → Networking
# Public Networking を有効化
# Port 9090を追加
```

### メモリ不足

**症状**: "Out of Memory"

**解決策**:
- 無料枠でも8GB使えるはず
- Settings → Resources で確認
- 重いノードを削減

### デプロイ失敗

**ログで確認**:
```bash
railway logs
```

**再デプロイ**:
```bash
railway up --detach
```

---

## 💎 有料プラン（Developer Pro）

### アップグレードすべき時

- $5を超える使用量が必要
- 複数プロジェクトを運用
- チームで開発

### 料金

- **Developer（無料）**: $5分/月
- **Pro（$20/月）**: $20分含む + 使用量課金
- **Team（$20/ユーザー/月）**: チーム機能

---

## 🚀 高度な設定

### Docker Composeサポート

Railway.appはDocker Composeもサポート:

```bash
# railway.toml
[deploy]
dockerCompose = true
```

### プライベートネットワーク

複数サービス間で通信:
```bash
Settings → Networking → Private Networking
```

### データベース追加

```bash
# PostgreSQL追加
New → Database → PostgreSQL

# 環境変数に自動追加
DATABASE_URL
```

---

## 📚 参考リンク

- [Railway.app ドキュメント](https://docs.railway.app)
- [料金計算ツール](https://railway.app/pricing)
- [Railway CLI](https://docs.railway.app/develop/cli)

---

## ✅ デプロイチェックリスト

- [ ] Railway.appアカウント作成
- [ ] GitHubリポジトリ連携
- [ ] プロジェクト作成・デプロイ
- [ ] ポート9090公開設定
- [ ] 公開URL取得
- [ ] GitHub Pagesから接続確認
- [ ] 使用量モニタリング設定
- [ ] $5枠の残量確認

---

## 💡 Render vs Railway 比較

| 項目 | Render | Railway |
|------|--------|---------|
| RAM | 512MB | 8GB |
| スリープ | あり（15分） | なし |
| 無料枠 | 750時間/月 | $5分/月 |
| セットアップ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 推奨 | デモ用 | 開発・実験用 |

**結論**:
- デモ・プレゼン → Render
- 開発・常時稼働 → Railway

完了です！🎉
