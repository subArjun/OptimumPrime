# pylint: skip-file
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
import cv2
from cv_bridge import CvBridge
import tf2_ros
from tf2_geometry_msgs import TransformStamped
import numpy as np
import cv2
from pupil_apriltags import Detector
import transforms3d as tf_transformations

class AprilTagDetector(Node):
    def __init__(self):
        super().__init__('apriltag_detector')
        self.subscription = self.create_subscription(
            Image,
            '/camera/color/image_raw',
            self.image_callback,
            10)
        self.camera_info_subscription = self.create_subscription(
            CameraInfo,
            '/camera/color/camera_info',
            self.camera_info_callback,
            10)
        self.br = CvBridge()
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        self.detector = Detector(families='tag36h11',
                                 nthreads=4,
                                 quad_decimate=1.0,
                                 quad_sigma=0.0,
                                 refine_edges=1,
                                 decode_sharpening=0.25,
                                 debug=0)
        self.camera_matrix = None
        self.dist_coeffs = None

    def camera_info_callback(self, msg):
        if self.camera_matrix is None:
            self.camera_matrix = np.array(msg.k).reshape((3, 3))
        if self.dist_coeffs is None:
            self.dist_coeffs = np.array(msg.d)

    def image_callback(self, msg):
        if self.camera_matrix is None or self.dist_coeffs is None:
            self.get_logger().warn('No camera info received yet')
            return

        cv_image = self.br.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        tags = self.detector.detect(gray_image, estimate_tag_pose=True, camera_params=[self.camera_matrix[0][0], self.camera_matrix[1][1], self.camera_matrix[0][2], self.camera_matrix[1][2]], tag_size=0.05)

        for tag in tags:
            t = TransformStamped()
            t.header.stamp = self.get_clock().now().to_msg()
            t.header.frame_id = msg.header.frame_id
            t.child_frame_id = f'tag_{tag.tag_id}'
            t.transform.translation.x = float(tag.pose_t[0])
            t.transform.translation.y = float(tag.pose_t[1])
            t.transform.translation.z = float(tag.pose_t[2])
            # Assuming tag.pose_R is a rotation matrix, convert it to a quaternion
            # This part may require additional code for conversion
            quat = tf_transformations.quaternions.mat2quat(tag.pose_R)
            t.transform.rotation.x = float(quat[0])
            t.transform.rotation.y = float(quat[1])
            t.transform.rotation.z = float(quat[2])
            t.transform.rotation.w = float(quat[3])
            # t.transform.rotation = ...

            self.tf_broadcaster.sendTransform(t)

def main(args=None):
    rclpy.init(args=args)
    apriltag_detector = AprilTagDetector()
    rclpy.spin(apriltag_detector)
    apriltag_detector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

