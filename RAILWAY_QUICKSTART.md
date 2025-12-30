# Railway.app 3分デプロイ - 今すぐ始めるガイド

## 🚀 Railway.appの特徴

- ✅ **8GB RAM**（無料枠でも使える！）
- ✅ **常時起動**（自動スリープなし）
- ✅ **$5分/月の無料クレジット**
- ✅ **超高速セットアップ**（3分）

## ⚡ 今すぐ始める（3ステップ）

### ステップ1: Railway.appアカウント作成（1分）

1. **ブラウザで開く:**
   ```
   https://railway.app
   ```

2. **"Start a New Project"** をクリック

3. **GitHubでサインアップ**
   - "Login with GitHub" を選択
   - リポジトリへのアクセスを許可

4. ✅ ログイン完了！

---

### ステップ2: プロジェクトをデプロイ（1分）

1. **"New Project"** ボタンをクリック

2. **"Deploy from GitHub repo"** を選択

3. **リポジトリを選択**
   ```
   Mins-sr/Ros-mobile
   ```
   または自分のフォーク

4. **自動検出される**
   - Dockerfileが自動検出
   - `Dockerfile.rosbridge` を使用

5. **"Deploy Now"** をクリック

   デプロイ開始！進行状況が表示されます。

---

### ステップ3: 公開設定（1分）

#### 3-1. デプロイ完了を待つ（30秒）

ログに以下が表示されればOK:
```
✅ Build successful
✅ Deployment live
```

#### 3-2. ドメインを生成

1. **プロジェクトページ** → **Settings** タブ

2. **Networking** セクション

3. **"Generate Domain"** をクリック

   公開URLが発行されます:
   ```
   your-app-name.up.railway.app
   ```

4. **WebSocket URL**:
   ```
   wss://your-app-name.up.railway.app:9090
   ```

---

## 🎉 完成！GitHub Pagesから接続

### 接続テスト

1. **GitHub Pagesを開く:**
   ```
   https://mins-sr.github.io/Ros-mobile/rosbridge.html
   ```

2. **接続URLを入力:**
   ```
   wss://your-app-name.up.railway.app:9090
   ```

3. **「接続」ボタンをクリック**

4. ✅ **「接続中」と表示されれば成功！**

---

## 📊 使用量を確認

### ダッシュボードで監視

1. **プロジェクトページ** → **"Usage"** タブ

2. **確認できること:**
   - 今月の使用量
   - 残りクレジット（$5から）
   - 予測コスト

### 無料枠の計算

```
使用量 = 実行時間 × $0.000463/分

例: 常時稼働（30日）
= 30日 × 24時間 × 60分 × $0.000463
= 約$20/月

→ 無料枠$5を超えると課金開始
```

### 💡 コスト削減のコツ

**使わない時は停止:**
```bash
# Railway CLI（後述）
railway down

# または Web UI
Settings → Service → Pause
```

**必要な時だけ起動:**
- 開発中だけ起動
- デモ時だけ起動
- $5枠を有効活用

---

## 🔧 Railway CLI（オプション）

### インストール

```bash
# Node.js必要
npm install -g @railway/cli

# ログイン
railway login
```

### 便利なコマンド

```bash
# プロジェクトにリンク
cd Ros-mobile
railway link

# ログ確認
railway logs

# 環境変数設定
railway variables set ROS_DOMAIN_ID=0

# サービス停止
railway down

# サービス再開
railway up
```

---

## 🎮 動作確認

### Publisher/Subscriberテスト

1. **GitHub Pages** でPublisher起動

2. **Railway のログを確認:**
   ```bash
   railway logs --follow
   ```

   以下が表示されればOK:
   ```
   [INFO] [rosbridge_websocket]: Publishing to /chatter
   ```

3. **Subscriberも起動**

   メッセージの送受信を確認

---

## 🔍 トラブルシューティング

### ポート9090にアクセスできない

**原因:** ポートが公開されていない

**解決策:**
```
Settings → Networking
→ Public Networking を有効化
```

### デプロイが失敗する

**ログで確認:**
```bash
railway logs
```

**よくあるエラー:**
- Dockerビルドエラー → Dockerfile確認
- メモリ不足 → 設定確認

### WebSocketが切断される

**原因:** 無料枠使い切り

**確認:**
```
Usage タブ → 残りクレジット確認
```

---

## 📈 有料プランへ（必要に応じて）

### いつ必要？

- $5/月を超える使用量が必要
- 複数のプロジェクト運用
- チーム開発

### プラン

| プラン | 月額 | クレジット | 特徴 |
|-------|------|-----------|------|
| Developer | $0 | $5分 | 個人用 |
| Pro | $20 | $20分含む | 本格開発 |
| Team | $20/人 | チーム共有 | 共同開発 |

---

## 🎯 Railway.appのメリット

### ✅ 他サービスとの比較

| 項目 | Railway | Render | Oracle |
|------|---------|--------|--------|
| RAM | 8GB | 512MB | 24GB |
| スリープ | なし | あり | なし |
| セットアップ | 3分 | 5分 | 60分 |
| 推奨用途 | 開発 | デモ | 本番 |

### Railway が最適な場合

- ✅ 高スペックが必要
- ✅ 常時稼働させたい
- ✅ 簡単にセットアップしたい
- ✅ $5/月の予算がある

---

## 🔄 継続的デプロイ（自動）

### GitHub連携済み

Railway は自動デプロイが有効:

```bash
# ローカルで変更
git commit -m "Update config"
git push

# → Railwayが自動で再デプロイ！
```

### 特定のブランチのみデプロイ

```
Settings → Triggers
→ Branch: main（または任意）
```

---

## 📚 次のステップ

### カスタムドメイン設定

```
Settings → Domains
→ Custom Domain を追加
→ DNS設定: CNAME レコード
```

### 監視・アラート

```
Settings → Integrations
→ Slack連携
→ エラー時に通知
```

### データベース追加

```
New → Database → PostgreSQL
→ 自動で環境変数追加
```

---

## ✅ 完了チェックリスト

- [ ] Railway.appアカウント作成
- [ ] GitHubリポジトリ連携
- [ ] プロジェクトデプロイ成功
- [ ] 公開ドメイン生成
- [ ] GitHub Pagesから接続成功
- [ ] Publisher/Subscriber動作確認
- [ ] 使用量確認方法を理解
- [ ] Railway CLIインストール（オプション）

---

## 🎊 完成！

おめでとうございます！

**デプロイURL:**
```
wss://your-app-name.up.railway.app:9090
```

**GitHub Pages:**
```
https://mins-sr.github.io/Ros-mobile/rosbridge.html
```

これで8GB RAMの高スペック環境で常時稼働する
ROS2システムが完成しました！🚀

---

## 💬 サポート

問題があれば:
- Railway ドキュメント: https://docs.railway.app
- プロジェクトREADME: `DEPLOY_RAILWAY.md`
- コミュニティ: https://discord.gg/railway
