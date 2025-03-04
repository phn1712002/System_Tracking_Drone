from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QPixmap
from ui import Ui_MainWindow
from video import (VideoThread, QImage)
from infor import TextThread  
import roslibpy

class UI_Main(Ui_MainWindow):
    
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        
        # Start
        self.MainWindow = MainWindow
        self.btn_reset_all.setDisabled(True)
        self.btn_reset_vx.setDisabled(True)
        self.btn_reset_wx.setDisabled(True)
        self.btn_reset_wz.setDisabled(True)
        self.btn_tracking.setDisabled(True)
        self.sb_id_tracking.setDisabled(True)
        self.sli_vx.setDisabled(True)
        self.sli_wx.setDisabled(True)
        self.sli_wz.setDisabled(True)

        # ROS Noetic
        self.ros_client = None
        self.ros_param = None
        self.timeout_connect_ros = 1
        
        # btn_connect
        self.btn_connect.setStyleSheet("background-color: red;")
        self.count_clicked_btn_connect = 0
        
        # btn_tracking
        self.btn_tracking.setStyleSheet("background-color: green;")
        self.count_clicked_btn_tracking = 0
        self.value_un_tracking = -1
        
        # label_video
        self.thread_update_video = None
       
        # label_count_detect
        self.thread_update_label_count_detect = None
        
        # sli
        self.sli_vx_topic = None
        self.sli_vx_value_last = None
        
        self.sli_wx_topic = None
        self.sli_wx_value_last = None
        
        self.sli_wz_topic = None
        self.sli_wz_value_last = None
        
        # param
        self.ros_param = None
            
    def processSignalAndSlot(self):
        
        self.btn_tracking.clicked.connect(self.process_btn_tracking_clicked)
        
        self.btn_connect.clicked.connect(self.process_btn_connect_clicked)
        
        self.btn_reset_all.clicked.connect(lambda x: self.process_btn_reset_clicked(self.btn_reset_vx, 'all'))
        self.btn_reset_vx.clicked.connect(lambda x: self.process_btn_reset_clicked(self.btn_reset_vx, 'vx'))
        self.btn_reset_wx.clicked.connect(lambda x: self.process_btn_reset_clicked(self.btn_reset_wx, 'wx'))
        self.btn_reset_wz.clicked.connect(lambda x: self.process_btn_reset_clicked(self.btn_reset_wz, 'wz'))
        
        self.sli_vx.valueChanged[int].connect(lambda value: self.process_sli_value_changed(value, 'vx'))
        self.sli_wx.valueChanged[int].connect(lambda value: self.process_sli_value_changed(value, 'wx'))
        self.sli_wz.valueChanged[int].connect(lambda value: self.process_sli_value_changed(value, 'wz'))

    @Slot(str)
    def update_label_count_detect(self, txt):
        self.label_count_detect.setText(txt)
        
    @Slot(QImage)
    def update_image(self, image):
       self.label_video.setPixmap(QPixmap.fromImage(image))
    
    def process_btn_tracking_clicked(self):
        self.btn_tracking.setDisabled(True) 
        
        def set_disabled(self, status):
            self.btn_reset_all.setDisabled(status)
            self.btn_reset_vx.setDisabled(status)
            self.btn_reset_wx.setDisabled(status)
            self.btn_reset_wz.setDisabled(status)
            self.sb_id_tracking.setDisabled(status)
            self.sli_vx.setDisabled(status)
            self.sli_wx.setDisabled(status)
            self.sli_wz.setDisabled(status)
        
        self.count_clicked_btn_tracking += 1
        if self.count_clicked_btn_tracking % 2:
            
            set_disabled(self, True)
            self.btn_tracking.setText("Bỏ theo dõi")
            self.btn_tracking.setStyleSheet("background-color: red;")

            id_tracking_object = self.sb_id_tracking.value()
            self.ros_client.set_param("id_tracking_object", id_tracking_object)
        else: 
            set_disabled(self, False)
            self.btn_tracking.setText("Theo dõi")
            self.btn_tracking.setStyleSheet("background-color: green;")
            self.ros_client.set_param("id_tracking_object", self.value_un_tracking)
            
        return self.btn_tracking.setDisabled(False)
    
    def process_error_connect(self, ip):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Lỗi")
        msg.setText(f"Không tìm thấy hệ thống trên {ip} này.")
        msg.setInformativeText("Vui lòng thay đổi host/port khác !")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
        
    def process_btn_connect_clicked(self):
        self.btn_connect.setDisabled(True)
        
        def set_sli_value(sli, min, max, current):
            sli.setMaximum(max)
            sli.setMinimum(min)
            sli.setValue(current)
        
        def set_disabled(self, status):
            self.btn_reset_all.setDisabled(status)
            self.btn_reset_vx.setDisabled(status)
            self.btn_reset_wx.setDisabled(status)
            self.btn_reset_wz.setDisabled(status)
            self.btn_tracking.setDisabled(status)
            self.sb_id_tracking.setDisabled(status)
            self.sli_vx.setDisabled(status)
            self.sli_wx.setDisabled(status)
            self.sli_wz.setDisabled(status)
            self.edit_ip.setDisabled(not status)
        
        self.count_clicked_btn_connect += 1 
        if self.count_clicked_btn_connect % 2:
            host_port = self.edit_ip.text()
            
            try:
                host, port = host_port.split(":")
                self.ros_client = roslibpy.Ros(host, int(port))
                self.ros_client.run(self.timeout_connect_ros)
            except:
                pass
            
            if(self.ros_client.is_connected):
                set_disabled(self, False)
                self.btn_connect.setStyleSheet("background-color: green;")
                self.btn_connect.setText("Ngắt kết nối")
                
                
                
                # Video setup
                self.thread_update_video = VideoThread(self.ros_client, '/image_compressed')
                self.thread_update_video.start()
                self.thread_update_video.change_pixmap_signal.connect(self.update_image)
                
                # Count detect 
                self.thread_update_label_count_detect = TextThread(self.ros_client, '/count_detect', 'std_msgs/Int32')
                self.thread_update_label_count_detect.start()
                self.thread_update_label_count_detect.change_value_signal.connect(self.update_label_count_detect)
                
                # Slider setup
                self.sli_vx_topic = roslibpy.Topic(self.ros_client, '/sli_vx', 'std_msgs/Int32')
                set_sli_value(self.sli_vx, 
                              int(self.ros_client.get_param('/bound_min_vx')), 
                              int(self.ros_client.get_param('/bound_max_vx')), 
                              0)
                self.sli_vx_value_last = 0
                
                self.sli_wx_topic = roslibpy.Topic(self.ros_client, '/sli_wx', 'std_msgs/Int32')
                set_sli_value(self.sli_wx, 
                              int(self.ros_client.get_param('/bound_min_wx')), 
                              int(self.ros_client.get_param('/bound_max_wx')), 
                              0)
                self.sli_wx_value_last = 0
                
                self.sli_wz_topic = roslibpy.Topic(self.ros_client, '/sli_wz', 'std_msgs/Int32')
                set_sli_value(self.sli_wz, 
                              int(self.ros_client.get_param('/bound_min_wz')), 
                              int(self.ros_client.get_param('/bound_max_wz')), 
                              0)
                self.sli_vx_value_last = 0
                
            else:
                self.count_clicked_btn_connect -= 1
                self.process_error_connect(host_port)
  
        else:
            if self.ros_client.is_connected: 
                self.ros_client.close(self.timeout_connect_ros)
                self.thread_update_video.stop()
                self.thread_update_label_count_detect.stop()
                
            set_disabled(self, True)
            self.btn_connect.setStyleSheet("background-color: red;")
            self.btn_connect.setText("Kết nối")
 
        return self.btn_connect.setDisabled(False)
    
    def process_btn_reset_clicked(self, btn, mode='all'):
        btn.setDisabled(True)
        if mode == 'vx':
            pass
        elif mode == 'wx':
            pass
        elif mode == 'wz':
            pass
        elif mode == 'all':
            pass
        return btn.setDisabled(False)

    def process_sli_value_changed(self, value, mode='vx'):
        if self.ros_client.is_connected:
            if mode == 'vx':
                if self.sli_vx_value_last is not None:
                    self.sli_vx_topic.publish(roslibpy.Message({'data': value - self.sli_vx_value_last})) 
                    self.sli_vx_value_last = value
            elif mode == 'wx':
                if self.sli_wx_value_last is not None:
                    self.sli_wx_topic.publish(roslibpy.Message({'data': value - self.sli_wx_value_last}))
                    self.sli_wx_value_last = value 
            elif mode == 'wz':
                if self.sli_wz_value_last is not None:
                    self.sli_wz_topic.publish(roslibpy.Message({'data': value - self.sli_wz_value_last}))
                    self.sli_wz_value_last = value 