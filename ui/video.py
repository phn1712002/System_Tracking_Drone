from PySide6.QtCore import QThread, Signal, QMutex
from PySide6.QtGui import QImage
import roslibpy
import base64
import cv2
import numpy as np

class VideoThread(QThread):
    change_pixmap_signal = Signal(QImage)

    def __init__(self, client, topic_name='/camera/image_compressed'):
        super().__init__()
        self.client = client
        self.topic_name = topic_name
        self.mutex = QMutex()
        self._run_flag = True

        self.images_raw_topic = roslibpy.Topic(client, topic_name, 'sensor_msgs/CompressedImage')
        self.images_raw_topic.subscribe(self.receive_image)
        self.image_current = None
        self.imgsz = None
        
    def receive_image(self, msg):
        base64_bytes = msg['data'].encode('ascii')
        image_bytes = base64.b64decode(base64_bytes)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        self.image_current = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
    def run(self):
        while self.client.is_connected:
            if self.image_current is not None:
                frame = cv2.cvtColor(self.image_current, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.change_pixmap_signal.emit(convert_to_Qt_format)
            
    def stop(self):
        self.mutex.lock()
        self._run_flag = False
        self.mutex.unlock()
        self.client.terminate()
        self.quit()
        self.wait()