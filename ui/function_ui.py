from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QPixmap
from ui import Ui_MainWindow
from video import (VideoThread, QImage)
from infor import (TextThread, Angle_Motor_Thread)
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
        self.btn_vx_bw.setDisabled(True)
        self.btn_vx_fw.setDisabled(True)
        self.sli_wx.setDisabled(True)
        self.sli_wz.setDisabled(True)
        self.rotation_vx.setDisabled(True)

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
        
        self.thread_update_angle_motor_detect = None
        self.control_detect = False
        
        # sli
        self.reset_clicked = False
        self.sli_vx_topic = None
        self.reset_vx_topic = None
        
        self.sli_wx_topic = None
        self.angle_reset_link_2 = None
        self.reset_wx_topic = None
        
        self.sli_wz_topic = None
        self.angle_reset_link_1 = None
        self.reset_wz_topic = None
        
        # param
        self.ros_param = None
            
    def processSignalAndSlot(self):
        
        self.btn_tracking.clicked.connect(self.process_btn_tracking_clicked)
        
        self.btn_connect.clicked.connect(self.process_btn_connect_clicked)
        
        self.btn_reset_all.clicked.connect(lambda : self.process_btn_reset_clicked('all'))
        self.btn_reset_vx.clicked.connect(lambda : self.process_btn_reset_clicked('vx'))
        self.btn_reset_wx.clicked.connect(lambda : self.process_btn_reset_clicked('wx'))
        self.btn_reset_wz.clicked.connect(lambda : self.process_btn_reset_clicked('wz'))
        
        self.btn_vx_fw.clicked.connect(lambda : self.process_btn_vx_clicked('fw'))
        self.btn_vx_bw.clicked.connect(lambda : self.process_btn_vx_clicked('bw'))
        
        self.sli_wx.valueChanged[int].connect(lambda value: self.process_sli_value_changed(value, 'wx'))
        self.sli_wz.valueChanged[int].connect(lambda value: self.process_sli_value_changed(value, 'wz'))
    
    @Slot(list)
    def update_angle_motor_detect(self, list_value):
        if self.control_detect:
            angle_link_1_current, angle_link_2_current = list_value[0], list_value[1]
            self.sli_wx.setValue(angle_link_2_current)
            self.sli_wz.setValue(angle_link_1_current)
    
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
            self.btn_vx_bw.setDisabled(status)
            self.btn_vx_fw.setDisabled(status)
            self.sli_wx.setDisabled(status)
            self.sli_wz.setDisabled(status)
            self.rotation_vx.setDisabled(status)
        
        self.count_clicked_btn_tracking += 1
        if self.count_clicked_btn_tracking % 2:
            
            set_disabled(self, True)
            self.btn_tracking.setText("Bỏ theo dõi")
            self.btn_tracking.setStyleSheet("background-color: red;")

            id_tracking_object = self.sb_id_tracking.value()
            self.ros_client.set_param("id_tracking_object", id_tracking_object)
            self.control_detect = True
        else: 
            set_disabled(self, False)
            self.btn_tracking.setText("Theo dõi")
            self.btn_tracking.setStyleSheet("background-color: green;")
            self.ros_client.set_param("id_tracking_object", self.value_un_tracking)
            self.control_detect = False
            
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
            self.btn_vx_bw.setDisabled(status)
            self.btn_vx_fw.setDisabled(status)
            self.sli_wx.setDisabled(status)
            self.sli_wz.setDisabled(status)
            self.rotation_vx.setDisabled(status)
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
                
                # 
                self.thread_update_angle_motor_detect = Angle_Motor_Thread(self.ros_client, '/value_motor_current')
                self.thread_update_angle_motor_detect.start()
                self.thread_update_angle_motor_detect.change_value_signal.connect(self.update_angle_motor_detect)
                # Slider setup
                self.sli_vx_topic = roslibpy.Topic(self.ros_client, '/sli_vx', 'std_msgs/Int32')
                
                self.sli_wx_topic = roslibpy.Topic(self.ros_client, '/sli_wx', 'std_msgs/Int32')
                self.angle_reset_link_2 = int(self.ros_client.get_param('/angle_reset_link_2'))
                set_sli_value(self.sli_wx, 0, 180, self.angle_reset_link_2)
                
                
                self.sli_wz_topic = roslibpy.Topic(self.ros_client, '/sli_wz', 'std_msgs/Int32')
                self.angle_reset_link_1 = int(self.ros_client.get_param('/angle_reset_link_1'))
                set_sli_value(self.sli_wz, 0, 180, self.angle_reset_link_1)
                
                
                # Btn reset topic 
                self.reset_vx_topic = roslibpy.Topic(self.ros_client, '/reset_vx', 'std_msgs/Bool')
                self.reset_wx_topic = roslibpy.Topic(self.ros_client, '/reset_wx', 'std_msgs/Bool')
                self.reset_wz_topic = roslibpy.Topic(self.ros_client, '/reset_wz', 'std_msgs/Bool')
                
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
    
    def process_btn_reset_clicked(self, mode='all'):
        self.reset_clicked = True
        topic_send_reset_clicked = roslibpy.Message({'data': True})
        if mode == 'vx':
            self.reset_vx_topic.publish(topic_send_reset_clicked)
            
        elif mode == 'wx':
            self.sli_wx.setValue(self.angle_reset_link_2)
            self.reset_wx_topic.publish(topic_send_reset_clicked)
            
        elif mode == 'wz':
            self.sli_wz.setValue(self.angle_reset_link_1)
            self.reset_wz_topic.publish(topic_send_reset_clicked)
            
        elif mode == 'all': 
            self.reset_vx_topic.publish(topic_send_reset_clicked)
            self.reset_wz_topic.publish(topic_send_reset_clicked)
            self.reset_wx_topic.publish(topic_send_reset_clicked)
            
            self.sli_wx.setValue(self.angle_reset_link_2)
            self.sli_wz.setValue(self.angle_reset_link_1)
        self.reset_clicked = False


    def process_sli_value_changed(self, value, mode='wx'):
        if self.ros_client.is_connected and self.reset_clicked == False and self.control_detect == False:
            if mode == 'wx':
                self.sli_wx_topic.publish(roslibpy.Message({'data': value}))
            elif mode == 'wz':
                self.sli_wz_topic.publish(roslibpy.Message({'data': value}))
    
    def process_btn_vx_clicked(self, mode='bw'):    
        if self.ros_client.is_connected:
            if mode == 'bw':
                self.sli_vx_topic.publish(roslibpy.Message({'data': -self.rotation_vx.value()}))
            elif mode == 'fw':
                self.sli_vx_topic.publish(roslibpy.Message({'data': self.rotation_vx.value()}))