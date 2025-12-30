# 無料枠クラウドサービス比較 - ROS2 + rosbridge対応

GitHub Pagesのフロントエンドと組み合わせて、ROS2環境を無料でホストできるクラウドサービスの比較

## 🏆 推奨順ランキング

### 1. Render.com ⭐⭐⭐⭐⭐（最推奨）

**無料枠:**
- 750時間/月（約31日分）
- 512MB RAM
- 0.1 CPU
- 自動スリープ（15分アイドルで停止）

**メリット:**
- ✅ Dockerサポート（ROS2イメージそのまま使える）
- ✅ WebSocket対応
- ✅ 自動SSL証明書（wss://）
- ✅ GitHub連携で自動デプロイ
- ✅ セットアップが簡単

**デメリット:**
- ⚠️ アイドルでスリープ（初回アクセス時30秒程度起動待ち）
- ⚠️ RAMが少なめ（ROS2は動くが重いノードは厳しい）

**セットアップ:**
```yaml
# render.rosbridge.yaml（既に用意済み）
services:
  - type: web
    name: ros2-rosbridge
    env: docker
    dockerfilePath: ./Dockerfile.rosbridge
```

**URL例:**
```
wss://your-app.onrender.com:9090
```

**コスト:**
- 無料: $0/月
- 有料プラン: $7/月〜（常時起動、より高スペック）

---

### 2. Railway.app ⭐⭐⭐⭐⭐

**無料枠:**
- $5分の使用量/月（約500時間）
- 8GB RAM（無料枠でも！）
- 8 vCPU
- 自動スリープなし

**メリット:**
- ✅ 無料枠でも高スペック
- ✅ Dockerサポート完璧
- ✅ 自動スリープなし（常時起動可）
- ✅ WebSocket完全対応
- ✅ GitHub連携

**デメリット:**
- ⚠️ 使用量課金（$5超えると課金開始）
- ⚠️ 2024年から無料枠が縮小傾向

**セットアップ:**
```bash
# Railway CLIで簡単デプロイ
railway init
railway up
```

**URL例:**
```
wss://your-app.railway.app:9090
```

**コスト:**
- 無料: $5分/月
- 超過分: 従量課金

---

### 3. Fly.io ⭐⭐⭐⭐

**無料枠:**
- 3つの共有CPU VM（256MB RAM）
- 3GB永続ストレージ
- 160GB転送量/月

**メリット:**
- ✅ Dockerサポート
- ✅ 世界中にエッジロケーション
- ✅ 永続ストレージあり
- ✅ 自動スリープなし

**デメリット:**
- ⚠️ RAMが少ない（256MB）
- ⚠️ CLIツールの習得が必要
- ⚠️ ROS2は動くが重い処理は厳しい

**セットアップ:**
```bash
# Fly.io CLI
fly launch
fly deploy
```

**URL例:**
```
wss://your-app.fly.dev:9090
```

**コスト:**
- 無料: 基本無料
- 有料: $1.94/月〜

---

### 4. Oracle Cloud Always Free ⭐⭐⭐⭐⭐（最強スペック）

**無料枠（永久）:**
- 2つのVM（AMD、各1GB RAM）
- または 4つのARM VM（各24GB RAM!）
- 200GB ストレージ
- 10TB転送量/月

**メリット:**
- ✅ **永久無料**（期限なし）
- ✅ ARM VMは24GB RAM（最強）
- ✅ 完全なVM（ROS2フル機能使える）
- ✅ 固定IPアドレス
- ✅ 自由度が高い

**デメリット:**
- ⚠️ 初期セットアップが複雑
- ⚠️ VMの管理が必要（Docker, nginx等）
- ⚠️ アカウント作成時にクレカ必須
- ⚠️ リージョンによっては混雑で作成できない

**セットアップ:**
```bash
# SSH接続後
sudo apt update
sudo apt install docker.io
docker-compose -f docker-compose.rosbridge.yml up -d

# nginxでリバースプロキシ設定
# SSL証明書（Let's Encrypt）設定
```

**URL例:**
```
wss://your-domain.com:9090
```

**コスト:**
- 永久無料: $0/月

---

### 5. AWS EC2 Free Tier ⭐⭐⭐⭐

**無料枠（12ヶ月間）:**
- t2.micro（1GB RAM）
- 30GB ストレージ
- 750時間/月（1インスタンス常時起動可）

**メリット:**
- ✅ AWSの信頼性
- ✅ 12ヶ月間完全無料
- ✅ フルVM（完全な自由度）
- ✅ 固定IP（Elastic IP）

**デメリット:**
- ⚠️ 12ヶ月後は有料（約$10/月）
- ⚠️ セットアップが複雑
- ⚠️ セキュリティ設定が必要

**セットアップ:**
```bash
# EC2インスタンス作成
# Ubuntu 22.04選択
# セキュリティグループで9090ポート開放

ssh ubuntu@your-ec2-ip
# ROS2 + rosbridgeインストール
```

**URL例:**
```
wss://ec2-xxx.compute.amazonaws.com:9090
```

**コスト:**
- 12ヶ月: 無料
- 13ヶ月目以降: $8-15/月

---

### 6. Google Cloud Run ⭐⭐⭐

**無料枠:**
- 2M リクエスト/月
- 360,000 GB-秒
- 180,000 vCPU-秒

**メリット:**
- ✅ Dockerサポート
- ✅ 自動スケール
- ✅ 従量課金（使わなければ無料）

**デメリット:**
- ⚠️ WebSocketサポートが複雑
- ⚠️ コールドスタートあり
- ⚠️ 長時間接続に向かない

**向き不向き:**
- ❌ rosbridgeには不向き（WebSocket常時接続が必要）
- ✅ REST APIバックエンドには向いている

---

### 7. Koyeb ⭐⭐⭐⭐

**無料枠:**
- 1つの無料インスタンス
- 512MB RAM
- 自動スリープなし

**メリット:**
- ✅ Dockerサポート
- ✅ 自動スリープなし
- ✅ セットアップ簡単
- ✅ WebSocket対応

**デメリット:**
- ⚠️ 新しいサービス（安定性未知数）
- ⚠️ ドキュメントが少ない

**URL例:**
```
wss://your-app.koyeb.app:9090
```

---

### 8. Replit ⭐⭐⭐

**無料枠:**
- 常時起動（Hacker プランで）
- ブラウザIDE統合

**メリット:**
- ✅ ブラウザで開発可能
- ✅ セットアップ不要

**デメリット:**
- ⚠️ ROS2の動作は保証されない
- ⚠️ リソースが限られる
- ⚠️ 本番環境には不向き

---

## 📊 比較表

| サービス | RAM | 常時起動 | Docker | 無料期間 | 難易度 | ROS2適性 |
|---------|-----|---------|--------|---------|--------|----------|
| **Render** | 512MB | ❌ | ✅ | 無期限 | ⭐ | ⭐⭐⭐⭐ |
| **Railway** | 8GB | ✅ | ✅ | 無期限 | ⭐ | ⭐⭐⭐⭐⭐ |
| **Fly.io** | 256MB | ✅ | ✅ | 無期限 | ⭐⭐ | ⭐⭐⭐ |
| **Oracle** | 24GB | ✅ | ✅ | **永久** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **AWS EC2** | 1GB | ✅ | ✅ | 12ヶ月 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Koyeb** | 512MB | ✅ | ✅ | 無期限 | ⭐ | ⭐⭐⭐⭐ |

## 🎯 用途別おすすめ

### 初心者・デモ用
**→ Render.com**
- 最も簡単
- すぐに始められる
- GitHub連携で自動デプロイ

### 本格開発・常時稼働
**→ Railway.app**
- 高スペック
- 常時起動
- $5枠内なら完全無料

### 最強スペック・永久無料
**→ Oracle Cloud Always Free**
- ARM VM 24GB RAM（驚異的）
- 永久無料
- セットアップは大変だが最強

### 12ヶ月間の実験
**→ AWS EC2 Free Tier**
- 信頼性高い
- 1年間じっくり試せる
- 本番環境への移行が容易

## 🚀 実装例（Render.com）

### 1. リポジトリ準備（完了済み）
`render.rosbridge.yaml` が既にあります

### 2. Render.comでデプロイ

1. https://render.com でサインアップ
2. "New" → "Blueprint"
3. GitHubリポジトリを接続
4. `render.rosbridge.yaml` が自動検出
5. "Apply" をクリック

### 3. GitHub Pagesから接続

```
接続URL: wss://your-app.onrender.com:9090
```

## 💡 コスト最適化のコツ

### 複数サービス併用
```
GitHub Pages (フロントエンド) - 無料
+ Render.com (rosbridge) - 無料
= 完全無料システム！
```

### スリープ対策（Render.com）
```bash
# 定期的にpingして起動状態維持（オプション）
# GitHub Actionsで5分ごとにアクセス
```

### 段階的移行
```
1. 最初: Render.com（無料・簡単）
2. 成長したら: Railway.app（高スペック）
3. 本番運用: Oracle Cloud（永久無料・最強）
```

## ⚠️ 注意点

### 無料枠の制限
- 多くのサービスは15分アイドルでスリープ
- ROS2は起動に時間がかかる（初回30秒程度）
- 本番運用には有料プランを推奨

### セキュリティ
- 無料枠でもSSL証明書を必ず使用
- 認証を追加推奨
- ファイアウォール設定を確認

## 📚 次のステップ

1. **まず試す**: Render.com（最も簡単）
2. **気に入ったら**: Railway.app（高スペック）
3. **本気なら**: Oracle Cloud（永久無料・最強）

各サービスの詳細セットアップは `DEPLOYMENT.md` を参照してください。
