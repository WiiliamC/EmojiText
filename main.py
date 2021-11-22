from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

import src

UI_PATH = "ui.ui"


class Main(QWidget):

    def __init__(self):
        super(Main, self).__init__()
        # 加载UI
        self.main_win = uic.loadUi(UI_PATH)
        # 连接按钮
        self.main_win.runButton.clicked.connect(self._run)

    def _run(self):
        # 改变鼠标指针样式
        self.main_win.setCursor(QCursor(Qt.WaitCursor))
        # 处理
        processer = src.TextProcesser()
        self.emojis = processer.process(self.main_win.inputText.toPlainText())
        # 输出结果
        self.main_win.outputText.setPlainText(self.emojis)
        # 改变鼠标指针样式
        self.main_win.setCursor(QCursor(Qt.ArrowCursor))


if __name__ == '__main__':
    app = QApplication([])
    main = Main()
    main.main_win.show()
    app.exec_()
