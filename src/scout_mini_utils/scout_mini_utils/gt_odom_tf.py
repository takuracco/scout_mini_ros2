import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
import math

def quat_from_yaw(yaw: float):
    # z-w only
    return (0.0, 0.0, math.sin(yaw * 0.5), math.cos(yaw * 0.5))

class GtOdomToTf(Node):
    def __init__(self):
        super().__init__('gt_odom_tf')
        self.declare_parameter('in_odom_topic', '/ground_truth/odom')
        self.declare_parameter('out_parent_frame', 'odom')   # 出したい親
        self.declare_parameter('out_child_frame', 'base_link')

        self.in_topic = self.get_parameter('in_odom_topic').get_parameter_value().string_value
        self.out_parent = self.get_parameter('out_parent_frame').get_parameter_value().string_value
        self.out_child = self.get_parameter('out_child_frame').get_parameter_value().string_value

        self.br = TransformBroadcaster(self)
        self.sub = self.create_subscription(Odometry, self.in_topic, self.cb, 10)

        self.get_logger().info(
            f"Broadcast TF {self.out_parent} -> {self.out_child} from {self.in_topic}"
        )

    def cb(self, msg: Odometry):
        t = TransformStamped()
        t.header.stamp = msg.header.stamp
        t.header.frame_id = self.out_parent
        t.child_frame_id = self.out_child

        # ground_truth/odom は pose が world基準で入ってる想定
        t.transform.translation.x = msg.pose.pose.position.x
        t.transform.translation.y = msg.pose.pose.position.y
        t.transform.translation.z = msg.pose.pose.position.z
        t.transform.rotation = msg.pose.pose.orientation

        self.br.sendTransform(t)

def main():
    rclpy.init()
    node = GtOdomToTf()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
