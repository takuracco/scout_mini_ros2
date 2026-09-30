#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from rclpy.parameter import Parameter
from sensor_msgs.msg import PointCloud2

class LidarStampFix(Node):
    def __init__(self):
        super().__init__('lidar_stamp_fix')
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])

        qos = QoSProfile(depth=5)
        qos.reliability = ReliabilityPolicy.RELIABLE  # Gazebo側がRELIABLEなので合わせる

        self.pub = self.create_publisher(PointCloud2, '/lidar/points_now', qos)
        self.sub = self.create_subscription(PointCloud2, '/lidar/points', self.cb, qos)

        self.get_logger().info('Republish /lidar/points -> /lidar/points_now with stamp=now()')

    def cb(self, msg: PointCloud2):
        out = msg  # そのまま転送（中身はいじらない）
        out.header.stamp = self.get_clock().now().to_msg()  # /clock基準（use_sim_time）
        self.pub.publish(out)

def main():
    rclpy.init()
    node = LidarStampFix()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
