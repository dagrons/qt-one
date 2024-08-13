import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QListWidget, QStackedWidget, QStyle, QLabel
)

from func.page.file_processor import FileProcessorWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Sidebar Toggle with Icon Example")
        self.setGeometry(100, 100, 800, 600)

        # 创建主窗口的主部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 创建主布局
        self.main_layout = QHBoxLayout(main_widget)

        apps = {
            "进度条": FileProcessorWidget(),
            "Page2": QLabel("page2"),
            "Page3": QLabel("page3")
        }

        # 创建Sidebar（使用QListWidget作为选项）
        self.sidebar = QListWidget()

        # 创建StackedWidget，用于右侧显示页面内容
        self.pages = QStackedWidget()

        # 配置SideBar和Pages
        for k, v in apps.items():
            self.sidebar.addItem(k)
            self.pages.addWidget(v)
        self.sidebar.currentRowChanged.connect(self.display_page)

        # 创建一个用于隐藏Sidebar的图标按钮
        self.close_sidebar_btn = QPushButton()
        self.close_sidebar_btn.setIcon(self.style().standardIcon(getattr(QStyle, "SP_TitleBarCloseButton")))
        self.close_sidebar_btn.clicked.connect(self.toggle_sidebar)

        # 创建一个用于展开Sidebar的图标按钮（初始隐藏）
        self.open_sidebar_btn = QPushButton()
        self.open_sidebar_btn.setIcon(self.style().standardIcon(getattr(QStyle, "SP_ArrowRight")))  # 替换为你的展开图标路径
        self.open_sidebar_btn.clicked.connect(self.toggle_sidebar)
        self.open_sidebar_btn.hide()

        # 将关闭图标按钮放在Sidebar的右上角
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.addWidget(self.close_sidebar_btn, alignment=Qt.AlignRight)
        self.sidebar_layout.addWidget(self.sidebar)

        self.sidebar_container = QWidget()
        self.sidebar_container.setLayout(self.sidebar_layout)

        # 将Sidebar和StackedWidget添加到主布局
        self.main_layout.addWidget(self.sidebar_container)
        self.main_layout.addWidget(self.pages)

        # 将打开Sidebar的按钮放在主窗口的左上角
        self.main_layout.insertWidget(0, self.open_sidebar_btn, alignment=Qt.AlignTop)

    def display_page(self, index):
        # 根据Sidebar的选择显示对应页面
        self.pages.setCurrentIndex(index)

    def toggle_sidebar(self):
        # 切换Sidebar的显示和隐藏状态
        if self.sidebar_container.isVisible():
            self.sidebar_container.hide()
            self.open_sidebar_btn.show()
        else:
            self.sidebar_container.show()
            self.open_sidebar_btn.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
