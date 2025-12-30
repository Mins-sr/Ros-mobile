#!/usr/bin/env python3
"""
ROS2 パブリッシャーノード
定期的にメッセージを送信します
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
from datetime import datetime


class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.publisher_ = self.create_publisher(String, 'chat_topic', 10)
        self.timer = self.create_timer(2.0, self.timer_callback)
        self.counter = 0
        self.get_logger().info('パブリッシャーノードを起動しました')

    def timer_callback(self):
        msg = String()
        data = {
            'counter': self.counter,
            'message': f'Hello from Publisher #{self.counter}',
            'timestamp': datetime.now().isoformat()
        }
        msg.data = json.dumps(data, ensure_ascii=False)
        self.publisher_.publish(msg)
        self.get_logger().info(f'送信: {data["message"]}')
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
