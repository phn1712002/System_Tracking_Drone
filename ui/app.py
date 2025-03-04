from PySide6.QtWidgets import QApplication, QMainWindow
from function_ui import UI_Main

app = QApplication([])
qMainWindow = QMainWindow()
ui_main = UI_Main()
ui_main.setupUi(qMainWindow)
ui_main.processSignalAndSlot()
qMainWindow.show()
app.exec()