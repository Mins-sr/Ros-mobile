"""
AIエージェント - 自然言語をROS2コマンドに変換
"""
from openai import AsyncOpenAI
import json
from typing import Optional


class AIAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = AsyncOpenAI(api_key=api_key) if api_key else None

        self.system_prompt = """あなたはROS2の専門家です。
ユーザーの自然言語の指示を、適切なROS2コマンドに変換してください。

利用可能なコマンド:
- start_publisher: パブリッシャーノードを起動
- start_subscriber: サブスクライバーノードを起動
- stop_publisher: パブリッシャーノードを停止
- stop_subscriber: サブスクライバーノードを停止
- check_status: ノードの状態を確認
- list_topics: トピック一覧を表示
- echo_topic <topic_name>: トピックのメッセージを表示

ユーザーの指示から最適なコマンドを1つ選び、JSON形式で返してください。
形式: {"command": "コマンド名", "args": [引数のリスト]}

例:
入力: "パブリッシャーを起動して"
出力: {"command": "start_publisher", "args": []}

入力: "通信状態を確認"
出力: {"command": "check_status", "args": []}

入力: "chat_topicの内容を見せて"
出力: {"command": "echo_topic", "args": ["chat_topic"]}
"""

    def is_configured(self) -> bool:
        """API キーが設定されているか確認"""
        return self.client is not None

    async def interpret_command(self, user_message: str) -> str:
        """
        ユーザーのメッセージをROS2コマンドに変換
        """
        if not self.is_configured():
            # AIが使えない場合は簡易的なルールベース
            return self._fallback_interpret(user_message)

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=200
            )

            content = response.choices[0].message.content

            # JSONパース
            try:
                result = json.loads(content)
                command = result.get("command", "")
                args = result.get("args", [])

                # コマンド文字列生成
                if args:
                    return f"{command} {' '.join(args)}"
                return command
            except json.JSONDecodeError:
                # JSONでない場合はそのまま返す
                return content.strip()

        except Exception as e:
            print(f"AI interpretation error: {e}")
            return self._fallback_interpret(user_message)

    def _fallback_interpret(self, user_message: str) -> str:
        """
        フォールバック: ルールベースでコマンド解釈
        """
        msg = user_message.lower()

        if "パブリッシャ" in msg and ("起動" in msg or "開始" in msg or "スタート" in msg):
            return "start_publisher"
        elif "サブスクライバ" in msg and ("起動" in msg or "開始" in msg or "スタート" in msg):
            return "start_subscriber"
        elif "パブリッシャ" in msg and ("停止" in msg or "終了" in msg):
            return "stop_publisher"
        elif "サブスクライバ" in msg and ("停止" in msg or "終了" in msg):
            return "stop_subscriber"
        elif "状態" in msg or "ステータス" in msg or "確認" in msg:
            return "check_status"
        elif "トピック" in msg and "一覧" in msg:
            return "list_topics"
        elif "echo" in msg or "表示" in msg or "見せて" in msg:
            return "echo_topic chat_topic"
        else:
            return "check_status"
