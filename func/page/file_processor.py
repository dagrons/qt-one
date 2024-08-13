import sys
from PyQt5.QtCore import pyqtSignal, QObject, QThread, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QVBoxLayout, QWidget, QPushButton


class FileProcessor(QObject):
    # 定义一个信号，用于通知进度更新
    progress_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def process_files(self):
        # 假设我们要处理100个文件
        for i in range(100):
            # 模拟一些处理工作
            QThread.sleep(1)
            # 发出进度信号，将当前进度发送出去
            self.progress_signal.emit(i + 1)


class FileProcessorWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.processor_thread = QThread()
        self.file_processor = FileProcessor()

        # 将FileProcessor移动到另一个线程中
        self.file_processor.moveToThread(self.processor_thread)

        # 连接信号和槽
        self.file_processor.progress_signal.connect(self.update_progress)
        self.processor_thread.started.connect(self.file_processor.process_files)

    def init_ui(self):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)

        self.start_button = QPushButton('Start Processing', self)
        self.start_button.clicked.connect(self.start_processing)

        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    @pyqtSlot(int)
    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def start_processing(self):
        # 启动线程，开始处理文件
        self.processor_thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileProcessorWidget()
    window.show()
    sys.exit(app.exec_())
