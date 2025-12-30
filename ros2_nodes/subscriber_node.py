#!/usr/bin/env python3
"""
ROS2 サブスクライバーノード
パブリッシャーからのメッセージを受信します
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json


class SubscriberNode(Node):
    def __init__(self):
        super().__init__('subscriber_node')
        self.subscription = self.create_subscription(
            String,
            'chat_topic',
            self.listener_callback,
            10
        )
        self.message_count = 0
        self.get_logger().info('サブスクライバーノードを起動しました')

    def listener_callback(self, msg):
        try:
            data = json.loads(msg.data)
            self.message_count += 1
            self.get_logger().info(
                f'受信 #{self.message_count}: {data["message"]} '
                f'(counter: {data["counter"]})'
            )
        except json.JSONDecodeError:
            self.get_logger().warn(f'JSON解析エラー: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = SubscriberNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
