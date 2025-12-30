"""
ROS2 コントローラー - ROS2ノードの制御
"""
import asyncio
import subprocess
from typing import Dict, Optional
import os
import signal


class ROS2Controller:
    def __init__(self):
        self.processes: Dict[str, subprocess.Popen] = {}
        self.ros2_workspace = "/home/user/Ros-mobile/ros2_nodes"

    def check_status(self) -> str:
        """ROS2環境のステータス確認"""
        try:
            result = subprocess.run(
                ["ros2", "node", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return "available" if result.returncode == 0 else "unavailable"
        except Exception:
            return "unavailable"

    async def execute_command(self, command: str) -> str:
        """
        コマンドを実行
        """
        parts = command.strip().split()
        if not parts:
            return "空のコマンド"

        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        try:
            if cmd == "start_publisher":
                return await self._start_node("publisher")
            elif cmd == "start_subscriber":
                return await self._start_node("subscriber")
            elif cmd == "stop_publisher":
                return await self._stop_node("publisher")
            elif cmd == "stop_subscriber":
                return await self._stop_node("subscriber")
            elif cmd == "check_status":
                return await self._check_nodes_status()
            elif cmd == "list_topics":
                return await self._list_topics()
            elif cmd == "echo_topic":
                topic = args[0] if args else "chat_topic"
                return await self._echo_topic(topic)
            else:
                return f"未知のコマンド: {cmd}"
        except Exception as e:
            return f"エラー: {str(e)}"

    async def _start_node(self, node_type: str) -> str:
        """ノード起動"""
        key = f"{node_type}_node"

        if key in self.processes and self.processes[key].poll() is None:
            return f"{node_type}ノードは既に実行中です"

        script_name = f"{node_type}_node.py"
        script_path = os.path.join(self.ros2_workspace, script_name)

        if not os.path.exists(script_path):
            return f"スクリプトが見つかりません: {script_path}"

        try:
            # ROS2環境をソース
            env = os.environ.copy()
            if "ROS_DISTRO" not in env:
                # ROS2セットアップスクリプトを実行
                setup_cmd = "source /opt/ros/humble/setup.bash"
                env.update({"ROS_DISTRO": "humble"})

            process = subprocess.Popen(
                ["python3", script_path],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            self.processes[key] = process

            # 少し待ってから状態確認
            await asyncio.sleep(1)

            if process.poll() is not None:
                _, stderr = process.communicate()
                return f"{node_type}ノードの起動に失敗: {stderr.decode()}"

            return f"{node_type}ノードを起動しました (PID: {process.pid})"
        except Exception as e:
            return f"{node_type}ノード起動エラー: {str(e)}"

    async def _stop_node(self, node_type: str) -> str:
        """ノード停止"""
        key = f"{node_type}_node"

        if key not in self.processes:
            return f"{node_type}ノードは起動していません"

        process = self.processes[key]

        if process.poll() is not None:
            del self.processes[key]
            return f"{node_type}ノードは既に停止しています"

        try:
            process.send_signal(signal.SIGINT)
            await asyncio.sleep(1)

            if process.poll() is None:
                process.kill()

            del self.processes[key]
            return f"{node_type}ノードを停止しました"
        except Exception as e:
            return f"{node_type}ノード停止エラー: {str(e)}"

    async def _check_nodes_status(self) -> str:
        """ノード状態確認"""
        try:
            result = await asyncio.create_subprocess_exec(
                "ros2", "node", "list",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await result.communicate()

            if result.returncode == 0:
                nodes = stdout.decode().strip().split('\n')
                return f"実行中のノード:\n" + "\n".join(f"- {node}" for node in nodes if node)
            else:
                return f"ノード一覧取得エラー: {stderr.decode()}"
        except Exception as e:
            return f"ステータス確認エラー: {str(e)}"

    async def _list_topics(self) -> str:
        """トピック一覧"""
        try:
            result = await asyncio.create_subprocess_exec(
                "ros2", "topic", "list",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await result.communicate()

            if result.returncode == 0:
                topics = stdout.decode().strip().split('\n')
                return f"トピック一覧:\n" + "\n".join(f"- {topic}" for topic in topics if topic)
            else:
                return f"トピック一覧取得エラー: {stderr.decode()}"
        except Exception as e:
            return f"トピック一覧エラー: {str(e)}"

    async def _echo_topic(self, topic: str, duration: int = 3) -> str:
        """トピックのメッセージ表示"""
        try:
            result = await asyncio.create_subprocess_exec(
                "timeout", str(duration), "ros2", "topic", "echo", topic,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await result.communicate()

            output = stdout.decode().strip()
            return f"トピック '{topic}' の内容 ({duration}秒間):\n{output}" if output else f"トピック '{topic}' からメッセージを受信できませんでした"
        except Exception as e:
            return f"トピックecho エラー: {str(e)}"

    async def get_nodes_status(self) -> Dict:
        """ノード状態取得（API用）"""
        status = {}
        for key in ["publisher_node", "subscriber_node"]:
            if key in self.processes:
                process = self.processes[key]
                status[key] = {
                    "running": process.poll() is None,
                    "pid": process.pid if process.poll() is None else None
                }
            else:
                status[key] = {"running": False, "pid": None}
        return status
