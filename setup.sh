#!/bin/bash

# ROS2 AI Web Agent セットアップスクリプト

set -e

echo "🚀 ROS2 AI Web Agent セットアップ開始"

# 環境変数ファイルのチェック
if [ ! -f .env ]; then
    echo "📝 .envファイルを作成しています..."
    cp .env.example .env
    echo "⚠️  .envファイルにOPENAI_API_KEYを設定してください（オプション）"
fi

# Docker環境チェック
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "✅ Docker環境が検出されました"
    echo ""
    echo "🐳 Dockerで起動しますか？ (y/n)"
    read -r use_docker

    if [ "$use_docker" = "y" ]; then
        echo "📦 Dockerコンテナをビルド・起動しています..."
        docker-compose up -d
        echo ""
        echo "✅ セットアップ完了!"
        echo ""
        echo "📡 アクセス先:"
        echo "   - Frontend: http://localhost:5173"
        echo "   - Backend API: http://localhost:8000"
        echo "   - API Docs: http://localhost:8000/docs"
        echo ""
        echo "📝 ログ確認: docker-compose logs -f"
        exit 0
    fi
fi

# ローカルセットアップ
echo "💻 ローカル環境でセットアップします"

# ROS2チェック
if [ -z "$ROS_DISTRO" ]; then
    echo "⚠️  ROS2環境が検出されません"
    echo "ROS2 Humbleをインストールするか、以下のコマンドを実行してください:"
    echo "  source /opt/ros/humble/setup.bash"
    exit 1
fi

echo "✅ ROS2 $ROS_DISTRO が検出されました"

# Backend依存関係インストール
echo "📦 Backend依存関係をインストール中..."
cd backend
pip3 install -r requirements.txt
cd ..

# Frontend依存関係インストール
if command -v npm &> /dev/null; then
    echo "📦 Frontend依存関係をインストール中..."
    cd frontend
    npm install
    cd ..
else
    echo "⚠️  npmが見つかりません。Node.jsをインストールしてください"
    echo "フロントエンドのセットアップをスキップします"
fi

echo ""
echo "✅ セットアップ完了!"
echo ""
echo "🚀 起動方法:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend && python3 main.py"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend && npm run dev"
echo ""
echo "Terminal 3 - Publisher:"
echo "  cd ros2_nodes && python3 publisher_node.py"
echo ""
echo "Terminal 4 - Subscriber:"
echo "  cd ros2_nodes && python3 subscriber_node.py"
echo ""
echo "📖 詳細: QUICKSTART.md を参照してください"
