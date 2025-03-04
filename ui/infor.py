from PySide6.QtCore import QThread, Signal, QMutex
import roslibpy

class TextThread(QThread):
    change_value_signal = Signal(str)

    def __init__(self, client, topic_name, message_type):
        super().__init__()
        self.client = client
        self.mutex = QMutex()
        self._run_flag = True

        self.images_raw_topic = roslibpy.Topic(client, topic_name, message_type)
        self.images_raw_topic.subscribe(self.receive_text)
        self.value_current = None
        self.value_last = None
        
    def receive_text(self, msg):
        self.value_current = msg['data']
        
    def run(self):
        while self.client.is_connected:
            if self.value_current != self.value_last:
                self.value_last = self.value_current
                self.change_value_signal.emit(str(self.value_current)) 
    
    def stop(self):
        self.mutex.lock()
        self._run_flag = False
        self.mutex.unlock()
        self.client.terminate()
        self.quit()
        self.wait()