# デプロイメントガイド

ROS2 AI Web Agentを本番環境にデプロイする方法を説明します。

## オプション1: GitHub Pages（推奨・最も簡単）

**特徴**: ブラウザ内シミュレーション版、無料、簡単

### セットアップ手順

1. **GitHubリポジトリの設定**
   - GitHubリポジトリ → Settings → Pages
   - Source: "GitHub Actions" を選択

2. **デプロイ**
   ```bash
   git push origin main
   # または
   git push origin claude/ros2-ai-web-agent-XrnSq
   ```

3. **アクセス**
   - 数分後に `https://[username].github.io/Ros-mobile/` でアクセス可能

### 注意事項
- ブラウザ内でROS2をシミュレート（実際のROS2は動きません）
- バックエンドは不要
- パブリッシャー/サブスクライバーの通信デモが可能

---

## オプション2: フルスタック版（実際のROS2）

**特徴**: 実際のROS2が動作、バックエンド必要

### A. Render.com（無料枠あり）

#### Backend + ROS2のデプロイ

1. **render.yaml作成済み**（リポジトリに含まれています）

2. **Renderアカウント作成**
   - https://render.com でサインアップ

3. **新しいWebサービス作成**
   - "New" → "Blueprint"
   - GitHubリポジトリを接続
   - `render.yaml` が自動検出されます

4. **環境変数設定**
   ```
   OPENAI_API_KEY=your-key-here
   ROS_DOMAIN_ID=0
   ```

5. **デプロイ**
   - 自動でビルド・デプロイされます
   - URLが発行されます（例: `https://ros2-backend.onrender.com`）

#### Frontendのデプロイ

**方法1: GitHub Pages + Render Backend**
```bash
# frontend/vite.config.ts を編集
export default defineConfig({
  // ...
  define: {
    'import.meta.env.VITE_API_URL': JSON.stringify('https://your-backend.onrender.com')
  }
})
```

**方法2: Render Static Site**
- Renderで新しいStatic Siteを作成
- Build Command: `cd frontend && npm install && npm run build`
- Publish Directory: `frontend/dist`

### B. Railway.app

1. **Railwayアカウント作成**
   - https://railway.app

2. **新しいプロジェクト作成**
   - "New Project" → "Deploy from GitHub repo"

3. **Backend サービス**
   - Root Directory: `/backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Port: 8000

4. **Frontend サービス**
   - Root Directory: `/frontend`
   - Build Command: `npm install && npm run build`
   - Start Command: `npm run preview`
   - Port: 5173

### C. Docker Composeで自前サーバー

VPS（さくらのVPS、AWS EC2、GCPなど）にデプロイ:

```bash
# サーバーにSSH接続
ssh user@your-server.com

# リポジトリクローン
git clone https://github.com/[username]/Ros-mobile.git
cd Ros-mobile

# 環境変数設定
cp .env.example .env
nano .env  # API keyを設定

# 起動
docker-compose up -d

# Nginxリバースプロキシ設定（オプション）
# SSL証明書設定（Let's Encrypt推奨）
```

---

## オプション3: Vercel / Netlify（Frontend のみ）

### Vercel

1. **Vercelアカウント作成**
   - https://vercel.com

2. **プロジェクトインポート**
   - "New Project" → GitHubリポジトリ選択

3. **設定**
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **環境変数**
   ```
   VITE_API_URL=https://your-backend-url.com
   ```

### Netlify

1. **Netlifyアカウント作成**
   - https://netlify.com

2. **サイト作成**
   - "Add new site" → "Import an existing project"

3. **設定**
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/dist`

---

## デプロイ方法の比較

| 方法 | 難易度 | コスト | 実際のROS2 | 推奨度 |
|------|--------|--------|-----------|--------|
| GitHub Pages | ⭐ 簡単 | 無料 | ❌ | ⭐⭐⭐⭐⭐ デモ用 |
| Render | ⭐⭐ 中 | 無料枠あり | ✅ | ⭐⭐⭐⭐ 実運用 |
| Railway | ⭐⭐ 中 | $5/月〜 | ✅ | ⭐⭐⭐⭐ 実運用 |
| VPS + Docker | ⭐⭐⭐ 難 | $5〜20/月 | ✅ | ⭐⭐⭐ 上級者 |
| Vercel/Netlify | ⭐ 簡単 | 無料 | ❌ | ⭐⭐⭐ Frontend のみ |

---

## トラブルシューティング

### GitHub Pagesでページが表示されない

1. Settings → Pages で GitHub Actions が選択されているか確認
2. Actions タブでデプロイが成功しているか確認
3. ブラウザのキャッシュをクリア

### RenderでROS2が動かない

- ROS2のインストールに時間がかかるため、初回デプロイは15-20分かかります
- ログを確認: `ros2 node list` が動作するか確認

### CORS エラー

Backend (`backend/main.py`)のCORS設定を確認:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # 本番ドメインを追加
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 推奨デプロイフロー

### デモ・プレゼン用
```
GitHub Pages（ブラウザ内シミュレーション）
↓
すぐに動作確認可能
```

### 本格開発・実証実験用
```
Frontend: Vercel/Netlify
Backend + ROS2: Render/Railway
↓
実際のROS2が動作
```

### 本番運用
```
全て自前サーバー（VPS + Docker Compose）
↓
完全なコントロール
```
