import torch
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


self.imageSub = self.add_subscription(Image, "/camera/color/image_raw", self.image_callback, 10)
self.aiPub = self.add_publisher(Image, "/ai", 10)
self.bridge = CvBridge()


def image_callback(self, msg):
    self.image = self.bridge.imgmsg_to_cv2(msg)
self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', device=self.device)

self.results = self.model(self.image)
self.results.print()
self.results.show()

cv2.rectangle(self.image, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)

        # Draw label
label_size = cv2.getTextSize(label_with_score, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
label_x = int(xmin)
label_y = int(ymin) - label_size[1]
if label_y < 0:
    label_y = int(ymax) + label_size[1]
cv2.putText(image, label_with_score, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)